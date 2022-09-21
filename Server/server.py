import json
import os
import threading
from socket import socket, AF_INET, SOCK_STREAM, error, SO_REUSEADDR, SOL_SOCKET
from Utility import db_initialization
from Utility import db_interface

firebase = db_initialization.initialize_db()
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

# from Utilities import tcp_packets
ENCODING = 'utf-8'
SIGN = 0
LOGIN = 1
MSG = 2
USERS = 3
DIRECT_MSG = 4


class Server:

    def __init__(self, addr: tuple):
        self.addr = addr
        self.clients_addr = {}  # (name:addr)
        self.clients_token = {}  # (name:token)
        self.clients_sock = {}  # (socket:name)
        self.clients_threads = []

        self.on = True

        try:
            self.serverSock = socket(AF_INET, SOCK_STREAM)  # socket for Client to connect
            self.serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            self.serverSock.bind(self.addr)
        except error:
            print("ERROR with Server Socket creation or bind")
            exit(1)

    def listen_for_clients(self):
        self.serverSock.listen(5)
        print('Waitnig for clients to connect...')
        while self.on:
            client_sock = client_addr = None
            try:
                client_sock, client_addr = self.serverSock.accept()
            except error:
                pass
            print(f'{len(self.clients_sock) + 1} client connected: {client_addr[0]}')
            print(f'{client_addr} connected')

            thread = threading.Thread(target=self.handle_client, args=(client_sock, client_addr,))
            self.clients_threads.append(thread)
            thread.start()

    # Private Method
    def handle_client(self, client_sock, client_addr):
        client_credentials = client_sock.recv(1024).decode(ENCODING).split('|')
        log_or_sign = client_credentials[0]
        client_name = client_credentials[1]
        client_password = client_credentials[2]
        client_email = client_credentials[3]
        token_id = None
        if int(log_or_sign) == SIGN:
            try:
                token_id = db_interface.add_user(auth, db, client_name, client_password, client_email)
            except Exception as e:
                er_obj = json.loads(e.args[1])
                print(f'{client_name} was unable to sign up duo to: ' + er_obj['error']['message'])
                return
        elif int(log_or_sign) == LOGIN:
            try:
                token_id = db_interface.login_user(auth, db, client_name, client_password, client_email)
            except Exception as e:
                er_obj = json.loads(e.args[1])
                print(f'{client_name} was unable to login duo to: ' + er_obj['error']['message'])
                return
        elif token_id is None:
            self.remove_client(client_sock, None)
            return

        try:
            client_sock.send(f'OK|{token_id}'.encode(ENCODING))
        except error:
            self.remove_client(client_sock, token_id)
            return

        self.clients_sock[client_sock] = client_name
        self.clients_addr[client_name] = client_addr
        self.clients_token[client_name] = token_id
        print(f'***** {client_name} connected *****')

        # announce to all clients that a new client has connected
        # connected_msg = tcp_packets.msg_packet('server', 'broadcast', f'***** {client_name} connected *****')
        # self.broadcast(connected_msg, client_sock)

        while self.on:
            try:
                pkt = client_sock.recv(4096).decode()
                # print(pkt)
            except error:
                continue
            if pkt != 'EXIT':
                if pkt == '':
                    return
                self.handle_pkt(pkt, client_sock, token_id)
            else:
                self.remove_client(client_sock, token_id)
                break

    def remove_client(self, client_sock: socket, token_id: str):
        if token_id is not None:
            client_name = self.clients_sock[client_sock]
            print(f'***** {client_name} disconnected *****')
            del self.clients_sock[client_sock]
            del self.clients_addr[client_name]
            db_interface.logout_user(db, client_name, token_id)
        client_sock.close()

    def find_sock_by_name(self, name_to_search: str):
        for sock, name in self.clients_sock.items():
            if name == name_to_search:
                return sock

    def find_token_by_name(self, name_to_search: str):
        for name, token in self.clients_token.items():
            if name == name_to_search:
                return token

    def handle_pkt(self, pkt: str, client_sock: socket, token_id: str):
        layers = pkt.split('|')

        if layers[0] == '':
            return
        if int(layers[0]) == 0 or int(layers[0]) == 1:
            print(f'{layers[1]} connected')

        if int(layers[0]) == USERS:
            pkt = f'{USERS}|' + '|'.join(list(self.clients_addr.keys()))
            try:
                client_sock.send(pkt.encode(ENCODING))
            except error as err:
                raise err

        if int(layers[0]) == MSG:
            print(f'in the process of sending the pkt: {pkt}')

            if layers[2] != 'all':
                print(f'sending pkt to {layers[2]}')
                receiver_sock = self.find_sock_by_name(layers[2])
                try:
                    receiver_sock.send(pkt.encode(ENCODING))
                    db_interface.push_message(auth, token_id, db, layers[1], layers[3], layers[2])
                except error as err:
                    raise err
            else:
                print('broadcasting')
                self.broadcast(pkt, client_sock, token_id)
                db_interface.push_message(auth, token_id, db, layers[1], layers[3], layers[2])

    def broadcast(self, pkt, conn=None, token_id: str = None):
        clients_sock_copy = self.clients_sock.copy()
        for client in clients_sock_copy:
            if client == conn:
                continue
            print(f'trying to send to {self.clients_sock[client]}')
            try:
                client.send(pkt.encode(ENCODING))

            except error:
                self.remove_client(client, token_id)
