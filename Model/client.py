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

    def connect(self, addr: tuple, username, password):
        try:
            self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("Failed to create the socket")
            return False

        try:
            self.client_sock.connect(("127.0.0.1", 12345))
            msg = f'{username}'
            self.client_sock.send(msg.encode(ENCODING))
            success = self.client_sock.recv(1024).decode(ENCODING)
        except socket.error as e:
            print("Failed to connect to the server 1")
            return False


        # check credentials
        if success != 'OK':
            print("Failed to connect to the server 2")
            self.client_sock.close()
            return False
        self.username = username
        self.active = True
        return True

    def disconnect(self):
        self.client_sock.send('EXIT'.encode(ENCODING))
        self.client_sock.close()

    def send_message(self, message):
        self.client_sock.send(message.encode(ENCODING))

    def receive_message(self):
        if self.active:
            try:
                msg = self.client_sock.recv(1024).decode(ENCODING)
                return msg
            except socket.error as e:
                print("Failed to receive message")


