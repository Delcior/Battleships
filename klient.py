'''
Klient TCP
'''
import socket
import numpy as np
import pickle
import random
from utils import *
from game_client import *
from map import Map

CRLF = b"\r\n\r\n"

ciphering = EncryptorDecryptor()
print("12341")

def rec(sock, crlf):
    data_rec = b''
    while not data_rec.endswith(crlf):
        #print("1 ", end="")
        data_rec += sock.recv(1)

    return ciphering.decrypt(data_rec[:-4])[:-4].decode()
    #return ciphering.decrypt(data_rec)[:-4].decode()


def rec_(sock, crlf):
    data_rec = b''
    while not data_rec.endswith(crlf):
        #`print("1 ", end="")
        data_rec += sock.recv(1)
    return data_rec[:-4].decode()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# algorytm musi sprawdzac dookoła wszystko
# powinien zaczynac w losowym punkcie i sie rozszerzac tam gdzie moze
# układa statki obok siebie
# point = (1,2)
# print(type(point))
# point = (point[0]+1, point[1])
# print(point)

try:


    s.connect(('localhost', 1769))

    hello = "201\r\nHello"
    klucz = "211\r\nMessage=My key\r\nKey={}\r\nKey-len=2048\r\n\r\n".format(ciphering.get_pubKey().decode())
    s.sendall(str(hello).encode())
    message_rec = rec_(s, CRLF)
    headers = HandshakeParser(message_rec)
    ciphering.set_pubKey2(headers['key'])

    s.sendall(klucz.encode())
    msg2 = rec_(s, CRLF)
    print("=-====", msg2)
    msg3 = rec_(s, CRLF)
    print("======", msg3)

    Map = Map()
    board = Map.configuration()
    board_to_send = b"400\r\n" + pickle.dumps(board)
    print("len ", len(board_to_send))
    aa = ciphering.encrypt(board_to_send)
    print(aa)
    s.sendall((aa))
    msg4 = rec(s, CRLF)
    print(msg4)

    # rozgrywka

    game = Game_client(s, board, ciphering)
    game.startGame()

    s.close()
except socket.error:
    print('Error')
except KeyboardInterrupt:
    s.close()

"421\r\nI shoot {x},{y} I hit!\r\n\r\ndasdsadsadsadsadsadasdsadasdsa"
