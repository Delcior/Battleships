'''
Klient TCP
'''
import socket
import numpy as np
import pickle
import random

from game_client import *
from map import Map

CRLF = b"\r\n\r\n"


def rec(sock, crlf):
    data_rec = b''
    while not data_rec.endswith(crlf):
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
    klucz = "211\r\nMessage=My key\r\nKey=1231241\r\nKey-len=2048\r\n\r\n"
    s.sendall(str(hello).encode())
    message_rec = rec(s, CRLF)
    print(message_rec)
    s.sendall(klucz.encode())
    msg2 = rec(s, CRLF)
    print(msg2)
    msg3 = rec(s, CRLF)
    print(msg3)

    Map = Map()
    board = Map.configuration()
    board_to_send = b"400\r\n" + pickle.dumps(board)
    s.sendall(board_to_send)
    msg4 = rec(s, CRLF)
    print(msg4)

    # rozgrywka

    game = Game_client(s, board)
    game.startGame()

    s.close()
except socket.error:
    print('Error')
except KeyboardInterrupt:
    s.close()

"421\r\nI shoot {x},{y} I hit!\r\n\r\ndasdsadsadsadsadsadasdsadasdsa"
