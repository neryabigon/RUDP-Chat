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

    def login(self, username, password):
        if not username:
            toast("Please enter a username")
            return
        if not password:
            toast('Please enter a password')
            return
        self.model.username = username
        self.model.password = password
        print(f'username: {username}: password: {password}')
        check = self.model.connect((HOST, PORT), self.model.username, self.model.password)
        if not check:
            toast('Invalid username or password or server is down')
            self.get_screen('home').ids.username.text = ''
            self.get_screen('home').ids.password.text = ''
            return
        print(f'{username} connected successfuly!')
        toast(f'{username} connected successfuly!')
        self.goto_screen('chat')
        Clock.schedule_interval(self.receive, 0.5)
        Clock.schedule_interval(self.update_users, 3)
        Clock.schedule_interval(self.update_files, 5)

    # def login(self, username, password):
    #     if not username:
    #         toast("Please enter a username")
    #         return
    #     if not password:
    #         toast('Please enter a password')
    #         return
    #     print(f'hey: {username}: passw: {password}')
    #     self.Rclient = basicClient.connect(username, password, False)
    #     if not self.Rclient:
    #         print(f'{username} was unable to connect')
    #         toast(f'{username} was unable to connect')
    #         return
    #     print(f'{username} connected successfuly!')
    #     toast(f'{username} connected successfuly!')
    #     self.goto_screen('chat')
    #     self.re_thread = threading.Thread(target=self.receive, daemon=True)
    #     self.re_thread.start()
    #     # Clock.schedule_interval(self.start_rec, 1)
    #
    # def signup(self, username, password):
    #     if not username:
    #         toast("Please enter a username")
    #         return
    #     if not password:
    #         toast('Please enter a password')
    #         return
    #     print(f'hey: {username}: passw: {password}')
    #     self.Rclient = basicClient.connect(username, password, True)
    #     if not self.Rclient:
    #         print(f'{username} was unable to connect')
    #         toast(f'{username} was unable to connect')
    #         return
    #     print(f'{username} connected successfuly!')
    #     toast(f'{username} connected successfuly!')
    #     self.goto_screen('chat')
    #
    # def start_rec(self, _):
    #     self.re_thread.start()
    #
    def log_out(self):
        self.model.disconnect()
        print(f'{self.model.username} disconnected')
        toast(f'{self.model.username} disconnected')
        self.goto_screen('home')

    def send(self, text):
        if not text:
            toast("Please enter any text!")
            return

        self.model.send_message(text)
        self.get_screen('chat').chat_logs.append(
            {"text": text, "send_by_user": True, "pos_hint": {"right": 1}}
        )

        self.get_screen('chat').files.append({"text": 'file', "download": False})
        self.get_screen('chat').files.append({"text": 'file', "download": False})
        self.get_screen('chat').files.append({"text": 'file', "download": True})
        self.get_screen('chat').files.append({"text": 'file', "download": False})

        # print(self.get_screen('chat').chat_logs)

        self.scroll_to_bottom()
        # clean text from textfield after sending
        self.get_screen('chat').ids.field.children[2].text = ""

    def scroll_to_bottom(self):
        rv = self.get_screen('chat').ids.chat_rv
        box = self.get_screen('chat').ids.box
        if rv.height < box.height:
            Animation.cancel_all(rv, "scroll_y")
            Animation(scroll_y=0, t="out_quad", d=0.5).start(rv)

    def receive(self, dt):
        if self.model.received_messages:
            msg = self.model.received_messages.pop()
            self.get_screen('chat').chat_logs.append(
                {"text": msg, "send_by_user": False, "pos_hint": {"left": 1}}  # maybe will need to remove the pos_hint
            )
            self.scroll_to_bottom()

    def update_users(self, dt):
        self.model.get_users()
        print(f'current users: {self.model.users}')
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

    def download(self, file_name):
        print(f'file name: {file_name}')

    # def receive(self):
    #     incom = self.Rclient.receive()
    #     if incom == '' or 'joined the chat':
    #         return
    #     if incom[:4] == '/msg':
    #         message = incom[5:]
    #         self.get_screen('chat').chat_logs.append(
    #             {
    #                 "text": message,
    #                 "send_by_user": False,
    #             }
    #         )
    #         self.scroll_to_bottom()
    #
    # def update_users(self):
    #     self.Rclient.write('/clientslist')
    #     all = self.Rclient.clients_list
    #     # if all == '':
    #     #     self.update_users()
    #     print(f'all: {all}')
    #     if all[:3] == '/cl':
    #         ls = all.split(' ')
    #         ls.remove('/cl')
    #         ls.remove('')
    #         self.get_screen('chat').users.clear()
    #         for user in ls:
    #             sp = user.split(',')
    #             if int(sp[1]) == 1:
    #                 on = True
    #             else:
    #                 on = False
    #             self.get_screen('chat').users.append(
    #                 {"text": sp[0], "online": on, }
    #             )

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
