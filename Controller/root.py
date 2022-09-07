import json
import threading

from kivy.clock import Clock
from kivy.factory import Factory  # NOQA: F401
from kivy.uix.screenmanager import ScreenManager
from kivymd.toast import toast
from kivy.animation import Animation
from kivy.properties import ListProperty
from plyer import filechooser

HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 1024


class Root(ScreenManager):
    """
    The Root (or Assembler) of the App.
    """

    def __init__(self, model, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.add_screens)
        """
        Adding the screens to the Root (ScreenManager).
        """
        self.model = model
        self.send_to = []

    def add_screens(self, interval):
        """
        Adding screens to the screenManager
        """
        with open("./View/screens.json") as f:
            # upload the screens from the screens json, into `screens`
            screens = json.load(f)

            for import_screen, screen_details in screens.items():
                exec(import_screen)  # executing imports
                screen_object = eval(
                    screen_details["factory"]
                )  # adding it to Factory
                screen_object.name = screen_details[
                    "screen_name"
                ]  # giving the name of the screen
                self.widget = self.add_widget(screen_object)

    # screens switching
    def goto_screen(self, go_to):
        self.current = go_to

    def login(self, username, password, email):
        if not username:
            toast("Please enter a username")
            return
        if not password:
            toast('Please enter a password')
            return
        self.model.username = username
        self.model.password = password
        self.model.email = email
        print(f'username: {username}, password: {password}, email: {email}')
        check = self.model.connect((HOST, PORT), self.model.username, self.model.password, self.model.email, True)
        if check:
            self.goto_screen('chat')
        else:
            toast('Login failed')
        if not check:
            toast('Invalid username or password or server is down')
            self.get_screen('home').ids.username.text = ''
            self.get_screen('home').ids.password.text = ''
            return
        print(f'{username} connected successfully!')
        toast(f'{username} connected successfully!')
        self.goto_screen('chat')
        Clock.schedule_interval(self.receive, 0.5)
        Clock.schedule_interval(self.update_users, 3)
        Clock.schedule_interval(self.update_files, 5)

    def signup(self, username, password, email):
        if not username:
            toast("Please enter a username")
            return
        if not password:
            toast('Please enter a password')
            return
        self.model.username = username
        self.model.password = password
        self.model.email = email
        print(f'username: {username}, password: {password}, email: {email}')
        check = self.model.connect((HOST, PORT), self.model.username, self.model.password, self.model.email, False)

        if not check:
            toast('Invalid username or password or server is down')
            self.get_screen('home').ids.username.text = ''
            self.get_screen('home').ids.password.text = ''
            return
        print(f'{username} connected successfully!')
        toast(f'{username} connected successfully!')
        self.goto_screen('chat')
        Clock.schedule_interval(self.receive, 0.5)
        Clock.schedule_interval(self.update_users, 3)
        Clock.schedule_interval(self.update_files, 5)

    # def start_rec(self, _):
    #     self.re_thread.start()

    def log_out(self):
        self.model.disconnect()
        print(f'{self.model.username} disconnected')
        toast(f'{self.model.username} disconnected')
        self.goto_screen('home')

    def send(self, text):
        if not text:
            toast("Please enter any text!")
            return

        print(self.send_to)
        self.model.send_message(text, self.send_to)
        self.get_screen('chat').chat_logs.append(
            {"text": text, "send_by_user": True, "pos_hint": {"right": 1}}
        )

        self.scroll_to_bottom()
        # clean text from textfield after sending
        self.get_screen('chat').ids.field.children[2].text = ""
        self.send_to.clear()

    def receive(self, dt):
        if self.model.received_messages:
            msg = self.model.received_messages.pop()
            self.get_screen('chat').chat_logs.append(
                {"text": msg, "send_by_user": False, "pos_hint": {"left": 1}}  # maybe will need to remove the pos_hint
            )
            self.scroll_to_bottom()

    def update_users(self, dt):
        self.model.get_users()
        if self.model.users:
            self.get_screen('chat').users.clear()
            for user in self.model.users:
                self.get_screen('chat').users.append(
                    {"text": user, "online": True}
                )

    def update_files(self, dt):
        if self.model.files:
            self.get_screen('chat').files.clear()
            for file in self.model.files:
                self.get_screen('chat').files.append(
                    {"text": file[0], "download": file[1]}
                )

    def scroll_to_bottom(self):
        rv = self.get_screen('chat').ids.chat_rv
        box = self.get_screen('chat').ids.box
        if rv.height < box.height:
            Animation.cancel_all(rv, "scroll_y")
            Animation(scroll_y=0, t="out_quad", d=0.5).start(rv)

    def update_send_to_list(self, name:str):
        self.send_to.append(name)

    def download(self, file_name):
        print(f'file name: {file_name}')

    """
    handling file choosing
    """
    # selection = ListProperty([])
    #
    # def choose(self):
    #     """
    #     Call plyer filechooser API to run a filechooser Activity.
    #     """
    #     filechooser.open_file(on_selection=self.handle_selection)
    #
    # def handle_selection(self, selection):
    #     """
    #     Callback function for handling the selection response from Activity.
    #     """
    #     self.selection = selection
    #     if len(selection) > 0:
    #         toast(str(selection[0]))
