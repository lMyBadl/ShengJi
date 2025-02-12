from _thread import *
from socket import *
import pickle
from player import Player

server = "SERVER IP"
port = 5555

server_socket = socket.socket(AF_INET, SOCK_STREAM)
try:
    server_socket.bind((server, port))
except socket.error as e:
    str(e)

server_socket.listen()
print("Server started. Waiting for connections...")



while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection has been established | {addr}")