'''
Klient TCP
'''
import socket
import numpy as np
import pickle
import random
from map import Map
CRLF = b"\r\n\r\n"


def rec(sock, crlf):
    data_rec = b''
    while not data_rec.endswith(crlf):
        data_rec += sock.recv(1)
    return data_rec[:-4].decode()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#algorytm musi sprawdzac dookoła wszystko
#powinien zaczynac w losowym punkcie i sie rozszerzac tam gdzie moze
# układa statki obok siebie
# point = (1,2)
# print(type(point))
# point = (point[0]+1, point[1])
# print(point)
klasa = Map()
klasa.configuration()
# try:
#     s.connect(('localhost', 1769))
#
#     a = [[4,2,3,4,2,1,3],[1,2,3,4,5,6,7,8]]
#
#     hello = "201\r\nHello"
#     klucz = "211\r\nMessage=My key\r\nKey=1231241\r\nKey-len=2048\r\n\r\n"
#     s.sendall(str(hello).encode())
#     message_rec = rec(s, CRLF)
#     print(message_rec)
#     s.sendall(klucz.encode())
#     msg2=rec(s, CRLF)
#     print(msg2)
#     msg3=rec(s, CRLF)
#     print(msg3)
#
#     board = Map()
#     #board._printInto()
#     mapa = pickle.dumps(board)
#
#     s.sendall(mapa)
#     s.close()
# except socket.error:
#     print ('Error')
# except KeyboardInterrupt:
#     s.close()
