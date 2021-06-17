'''
Serwer TCP
'''
import asyncio
import random
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import pickle
# import rsa
import map
from threading import Thread
from board import *
from map import *
"""
kod\r\nwiadomosc\r\nklucz..\r\n\r\n


"211\r\nMessage=hello,give me your key.There is my key\r\nKey=key\r\nKey-len:2048\r\n\r\n"



"401\r\nx:3\r\ny:4\r\n\r\n"

"""

def HandshakeParser(data):
    results = {}
    data = data.split('\r\n')
    try:

        code = int(data[0])
    except ValueError:
        return '302\r\nBAD CODE ERROR'

    results['code'] = code

    # TODO:co jesli jest blad
    if "Message=" == data[1][:8]:
        results['message'] = data[1][8:]
    if "Key=" == data[2][:4]:
        results['key'] = data[2][4:]
    if "Key-len=" == data[3][:8]:
        results['key-len'] = int(data[3][8:])

    return results


class HelloHandshake:
    def __init__(self):
        self.codes = {}
        self.finished = False
        self.clientPubKey = ""

    def accept_201(self, data):
        """
        Funkcja przyjmuje wiadomość powitalną, zwraca ramkę z odpowiedzią
        (klucz publiczny serwera i długość tego klucza)
        """
        if data == "201\r\nHello":
            self.codes[201] = True
            # read key from file
            # TODO: add trycatch
            publicKey = open("./publicKey.crt", "r")

            message = "211\r\nMessage=Hello,give me your key.\r\n" \
                      "Key={key}\r\nKey-len=2048\r\n\r\n".format(
                key=publicKey.read())
            return message

    def accept_212(self, data):

        headers = HandshakeParser(data)
        # assert headers['key-len'] >= 2048

        if headers['code'] == 211 and self.codes[201]:
            self.clientPubKey = headers['key']
            self.finished = True
            return '210\r\nMessage=Od teraz wszystkie wiadomosci sa szyfrowane\r\n\r\n' \
                   '101\r\nInfo:Zbuduj mape\r\n\r\n'

        return "301\r\nERROR"
        # klient 211\r\nMessage=There is my key\r\nKey={key}\r\nKey-len=2048\r\n\r\n
    # def accept_202(self, data):


class BattleshipProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.addr = transport.get_extra_info('peername')
        self._rest = b''
        self.name = None
        self.HelloHandshake = HelloHandshake()
        self.board = Board()
        print('Connection from {}'.format(self.addr))

    def data_received(self, data):
        data = self._rest + data

        if not self.HelloHandshake.finished:
            data = data.decode()
            if int(data[:3]) == 201:
                message = self.HelloHandshake.accept_201(data)
                self.transport.write(message.encode())
                print(message)
            elif int(data[:3]) == 211:
                message = self.HelloHandshake.accept_212(data)
                self.transport.write(message.encode())
                print(message)
            return
        if int(data[:3].decode()) == 400:
            data = data[5:]
            client_map = pickle.loads(data)

            self.board.setMap("client", client_map)
            server_map = Map().generateMap()
            self.board.setMap("server", server_map)
            message = "401\r\nLet the game begin!\r\n\r\n"
            self.transport.write(message.encode())

        elif int(data[:3].decode()) == 405:
            code, message = self.board.client_move(data.decode())
            print(code)
            print(message)
            self.transport.write(message.encode())

            while code == 421 or code == 422 or code == 413:
                code, message, client_map = self.board.server_move()
                message = message.encode()
                client_map = pickle.dumps(client_map) + b"\r\n\r\n"
                message += client_map
                self.transport.write(message)

            if code == 431 or code == 432:
                message = "450\r\nIf u want to play again send your map\r\n"
                self.transport.write(message.encode())


        # fib_num = int(data.decode())
        #
        # task = asyncio.create_task(self.async_fib(fib_num))

        ###  klient sie laczy
        ###  serwer odpowiada ze sie polaczyl
        ###  wymiana kluczami
        ###
        ###  serwer wysyla informacje o wyborze opcji
        ###  klient wysyla w odpowiedzi swoj wybor
        ###  wybor serwer:
        ###  serwer generuje swoja mape, a klient tworzy swoja mape
        ###  klient wysyla mape do serwera
        ###  serwer zwraca odpowiedz o poprawnosci
        ###  rozpoczyna sie gra

    def connection_lost(self, ex):
        print('Client {} disconnected'.format(self.addr))

    # async def async_fib(self, fib_num):
    #     task = await loop.run_in_executor(thread_pool, Fib, fib_num)
    #
    #     response = (str(task) + "\r\n").encode()
    #     self.transport.write(response)


thread_pool = ThreadPoolExecutor()
loop = asyncio.get_event_loop()
coroutine = loop.create_server(BattleshipProtocol, host='localhost', port=1769)
server = loop.run_until_complete(coroutine)

loop.run_forever()
