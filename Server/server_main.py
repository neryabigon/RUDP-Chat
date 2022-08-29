from server import Server

server = Server(('127.0.0.1', 12345))
server.listen_for_clients()