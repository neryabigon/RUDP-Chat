from Model.client import Client
from threading import Thread
from Utility.utils import deconstruct_msg

MSG = 1
USERS = 2
DIRECT_MSG = 3
FILES = 4


class ClientModel:

    def __init__(self):
        self.username = None
        self.password = None
        self.client = Client()
        self.receive_thread = Thread(target=self.receive_message, daemon=True)
        self.active = False
        self.received_messages = []
        self.users = []
        self.files = []

    def connect(self, addr: tuple, username, password):
        if not self.client.connect(addr, username, password):
            return False
        self.username = username
        self.password = password
        self.active = True
        try:
            self.receive_thread.start()
        except RuntimeError as e:
            self.receive_thread = Thread(target=self.receive_message, daemon=True)
            self.receive_thread.start()
        return True

    def disconnect(self):
        self.active = False
        self.client.active = False
        self.client.disconnect()

    def send_message(self, message, send_to="all"):
        msg = f'{MSG}|{self.username}|{send_to}|{message}'
        self.client.send_message(msg)

    def receive_message(self):
        while self.active:
            try:
                msg = self.client.receive_message()
            except Exception as e:
                print('Error receiving message: ')
                print(e)
                self.active = False
                break

            if not msg:
                continue
            deconstructed_msg = msg.split('|')

            if int(deconstructed_msg[0]) == MSG:
                print('Received a message, appending it to received_messages')
                formated = self.format_msg(deconstructed_msg)
                self.received_messages.append(formated)
            elif int(deconstructed_msg[0]) == USERS:
                self.users.clear()
                self.users.extend(deconstructed_msg[1:])
            elif int(deconstructed_msg[0]) == FILES:
                self.files.append(deconstructed_msg[1])

    def format_msg(self, msg):
        return f'{msg[1]}: {msg[3]}'

    def get_users(self):
        if self.active:
            self.client.send_message(f'{USERS}|{self.username}')