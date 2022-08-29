from Model.client import Client
from threading import Thread
from Utility.utils import deconstruct_msg

MSG = 1
USERS = 2
DIRECT_MSG = 3

class ClientModel:

    def __init__(self):
        self.username = None
        self.password = None
        self.client = Client()
        self.receive_thread = Thread(target=self.receive_message, daemon=True)
        self.active = False
        self.recieved_messages = []
        self.users = []

    def connect(self, addr: tuple, username, password):
        if not self.client.connect(addr, username, password):
            return False
        return True

    def disconnect(self):
        self.client.disconnect()

    def send_message(self, message, send_to="all"):
        self.client.send_message(message, send_to)

    def receive_message(self):
        while self.active:
            try:
                msg = self.client.receive_message()
                deconstructed_msg = deconstruct_msg(msg)
            except Exception as e:
                print('Error receiving message: ')
                raise e
                self.active = False
                break

            if deconstructed_msg[0] == MSG:
                self.recieved_messages.append(msg)
            elif deconstructed_msg[0] == USERS:
                self.users.clear()
                self.users.extend(deconstructed_msg)

