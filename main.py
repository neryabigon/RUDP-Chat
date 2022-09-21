import os
import sys

root_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.join(root_dir, "libs", "applibs"))

import platform
from kivy.core.window import Window
from kivymd.app import MDApp
from Presenter.root import Root  # this is the presenter
from Model.clientmodel import ClientModel  # this is the model

# This is needed for supporting Windows 10 with OpenGL < v2.0
if platform.system() == "Windows":
    os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"


class ChatApp(MDApp):
    def __init__(self, **kwargs):
        super(ChatApp, self).__init__(**kwargs)
        Window.soft_input_mode = "below_target"
        self.title = "Chat App"
        self.model = ClientModel()

    def build(self):
        Window.bind(on_request_close=self.on_request_close)
        return Root(self.model)

    def on_request_close(self, *args):
        if self.model.active:
            self.model.disconnect()
            return False
        return False


if __name__ == '__main__':
    ChatApp().run()
