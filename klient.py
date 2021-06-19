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
    # connect to server without ciphering
    s.connect(('localhost', 1770))

    # send hello message
    hello_message = "201\r\nHello\r\n\r\n"
    s.sendall(str(hello_message).encode())

    # get message from server about handshake
    handshake_rec = rec_(s, CRLF)

    code = int(handshake_rec[:3])
    if code != 211:
        print(handshake_rec[4:])
    else:
        # if got proper code, parse response
        headers = HandshakeParser(handshake_rec)

        # set server public key
        ciphering.set_pubKey2(headers['key'])

        # send my public key
        key = "212\r\nMessage=My key\r\nKey-len=2048\r\nKey={}\r\n\r\n".format(ciphering.get_pubKey().decode())

        s.sendall(key.encode())

        # get reposnonse about my ciphering key
        ciphering_msg = rec_(s, CRLF)
        code = int(ciphering_msg[:3])
        if code != 210:
            print(ciphering_msg[4:])
        else:
            # get information message about building map
            info_msg = rec_(s, CRLF)
            code = int(info_msg[:3])
            if code != 101:
                print(info_msg)
            else:
                Map = Map()
                board = Map.configuration()
                board_to_send = b"400\r\n" + pickle.dumps(board)
                encrypted_message = ciphering.encrypt(board_to_send)
                s.sendall(encrypted_message)

                begin_game_msg = rec(s, CRLF)
                code = int(begin_game_msg[:3])
                if code != 401:
                    print(begin_game_msg[4:])
                else:
                    print("\n" + begin_game_msg[4:])

                    # start game

                    game = Game_client(s, board, ciphering)
                    game.startGame()

    s.close()
except socket.error:
    print('Error')
except KeyboardInterrupt:
    s.close()
