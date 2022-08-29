import os
import socket
import struct
import threading
import time
import logging

ENCODING = 'utf-8'
HOST = '127.0.0.1'  # here we need to put the server IP
II = '0.0.0.0'
PORT = 50004
# ports for files
SENDER_PORT = 50001
RECEIVE_PORT = 50002


# client object
class Client:
    def __init__(self):
        try:
            self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("Failed to create the socket")
            raise e
        self.username = ''

    def connect(self, addr: tuple, username, password):
        try:
            self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("Failed to create the socket")
            raise e

        try:
            self.client_sock.connect(addr)
            msg = f'{username}|{password}'
            self.client_sock.send(msg.encode(ENCODING))
            success = self.client_sock.recv(1024).decode(ENCODING)
        except socket.error as e:
            print("Failed to connect to the server")
            raise e

        # check credentials
        if success is not 'OK':
            print("Failed to connect to the server")
            self.client_sock.close()
            return False
        self.username = username
        return True

    def disconnect(self):
        self.client_sock.send('EXIT'.encode(ENCODING))
        self.client_sock.close()

    def send_message(self, message, send_to):
        msg = f'{self.username}|{send_to}|{message}'
        self.client_sock.send(msg.encode(ENCODING))

