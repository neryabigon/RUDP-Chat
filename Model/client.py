import os
import socket
import struct
import threading
import time
import logging

ENCODING = 'utf-8'
HOST = '127.0.0.1'  # here we need to put the server IP
PORT = 12345


# client object
class Client:
    def __init__(self):
        try:
            self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("Failed to create the socket")
            raise e
        self.username = ''
        self.active = False
        self.token_id = ''
        self.password = ''
        self.email = ''

    def connect(self, addr: tuple, username, password, email, log_or_sign):
        try:
            self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("Failed to create the socket")
            return False

        try:
            self.client_sock.connect(("127.0.0.1", 12345))
            if log_or_sign:
                msg = f'1|{username}|{password}|{email}'
            else:
                msg = f'0|{username}|{password}|{email}'

            self.client_sock.send(msg.encode(ENCODING))
            success = self.client_sock.recv(1024).decode(ENCODING)
        except socket.error as e:
            print("Failed to connect to the server 1")
            return False

        # check credentials
        # print(f'<{success[:2]}>')
        # print(f'<{success}>')
        if success[:2] != 'OK':
            print("Failed to connect to the server 2")
            self.disconnect()
            return False
        self.username = username
        self.active = True
        self.token_id = success[3:]
        self.password = password
        self.email = email
        return True

    def disconnect(self):
        self.client_sock.send('EXIT'.encode(ENCODING))
        self.client_sock.close()

    def send_message(self, message: str, send_to=None):
        if send_to is None:
            self.client_sock.send(message.encode(ENCODING))
        else:
            splited = message.split('|')
            msg = f'{splited[0]}|{splited[1]}|'
            for client in send_to:
                msg += f'{client}|{splited[3]}'
                self.client_sock.send(msg.encode(ENCODING))

    def receive_message(self):
        if self.active:
            try:
                msg = self.client_sock.recv(1024).decode(ENCODING)
                return msg
            except socket.error as e:
                print("Failed to receive message")
