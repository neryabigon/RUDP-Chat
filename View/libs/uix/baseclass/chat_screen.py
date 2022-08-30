from Utility import utils
from kivy.properties import ListProperty, StringProperty
from kivymd.uix.screen import MDScreen
from Utility.observer import Observer

utils.load_kv("chat_screen.kv")


class ChatScreen(MDScreen, Observer):
    title = StringProperty()
    chat_logs = ListProperty()
    files = ListProperty()
    users = ListProperty()

    def model_is_changed(self):
        """
        The method is called when the model changes.
        Requests and displays the value of the sum.
        """
        pass