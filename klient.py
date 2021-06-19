'''
Klient TCP
'''
import socket
from utils import *
from game_client import *
from map import Map

CRLF = b"\r\n\r\n"
ciphering = EncryptorDecryptor()


def rec(sock, crlf):
    data_rec = b''
    while not data_rec.endswith(crlf):
        data_rec += sock.recv(1)

    return ciphering.decrypt(data_rec[:-4])[:-4].decode()


def rec_(sock, crlf):
    data_rec = b''
    while not data_rec.endswith(crlf):
        data_rec += sock.recv(1)
    return data_rec[:-4].decode()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:


    s.connect(('localhost', 1770))

    hello = "201\r\nHello"
    klucz = "211\r\nMessage=My key\r\nKey={}\r\nKey-len=2048\r\n\r\n".format(ciphering.get_pubKey().decode())
    s.sendall(str(hello).encode())
    message_rec = rec_(s, CRLF)
    headers = HandshakeParser(message_rec)
    ciphering.set_pubKey2(headers['key'])

    s.sendall(klucz.encode())
    msg2 = rec_(s, CRLF)
    #print("=-====", msg2)
    msg3 = rec_(s, CRLF)
    #print("======", msg3)

    Map = Map()
    board = Map.configuration()
    board_to_send = b"400\r\n" + pickle.dumps(board)
    #print("len ", len(board_to_send))
    aa = ciphering.encrypt(board_to_send)
    #print(aa)
    s.sendall((aa))
    msg4 = rec(s, CRLF)
    print("\n"+msg4.split('\n')[1])

    # rozgrywka

    game = Game_client(s, board, ciphering)
    game.startGame()

    s.close()
except socket.error:
    print('Error')
except KeyboardInterrupt:
    s.close()

"421\r\nI shoot {x},{y} I hit!\r\n\r\ndasdsadsadsadsadsadasdsadasdsa"
