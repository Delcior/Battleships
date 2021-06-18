'''
Serwer TCP
'''
import asyncio
import random
from time import sleep
from utils import *

import numpy as np
from concurrent.futures import ThreadPoolExecutor
import pickle
# import rsa
import map
from threading import Thread
from game_server import *
from map import *
"""
kod\r\nwiadomosc\r\nklucz..\r\n\r\n


"211\r\nMessage=hello,give me your key.\r\nKey=key\r\nKey-len:2048\r\n\r\n"



"401\r\nx:3\r\ny:4\r\n\r\n"

"""


class HelloHandshake:
    def __init__(self):
        self.codes = {}
        self.finished = False

    def accept_201(self, data):
        """
        Funkcja przyjmuje wiadomość powitalną, zwraca ramkę z odpowiedzią
        (klucz publiczny serwera i długość tego klucza)
        """
        if data == "201\r\nHello":
            self.codes[201] = True
            message = "211\r\nMessage=Hello,give me your key.\r\n" \
                      "Key={key}\r\nKey-len=2048\r\n\r\n".format(
                key=ciphering.get_pubKey().decode())
            return message

    def accept_212(self, data):

        headers = HandshakeParser(data)
        # assert headers['key-len'] >= 2048

        if headers['code'] == 211 and self.codes[201]:
            #print(headers['key'])
            ciphering.set_pubKey2(headers['key'])
            self.finished = True
            return '210\r\nMessage=Od teraz wszystkie wiadomosci sa szyfrowane\r\n\r\n' \
                   '101\r\nInfo:Zbuduj mape\r\n\r\n'

        return "301\r\nERROR"
        # klient 211\r\nMessage=There is my key\r\nKey={key}\r\nKey-len=2048\r\n\r\n
    # def accept_202(self, data):


class BattleshipProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.encrypted = False
        self.transport = transport
        self.addr = transport.get_extra_info('peername')
        self._rest = b''
        self.name = None
        self.HelloHandshake = HelloHandshake()
        self.game_server = Game_server()
        print('Connection from {}'.format(self.addr))

    def data_received(self, data):
        if not self.HelloHandshake.finished:
            data = data.decode()
            if int(data[:3]) == 201:
                message = self.HelloHandshake.accept_201(data)
                self.transport.write(message.encode())
                print(message)
            elif int(data[:3]) == 211:
                message = self.HelloHandshake.accept_212(data)
                self.transport.write(message.encode())
                #self.encrypted = True
                print(message)
            return
        #tu decrypt
        print(data)
        data = ciphering.decrypt(data)
        asyncio.create_task(self.game_async(data))

    async def game_async(self, data):
        await loop.run_in_executor(thread_pool, self.game, data)

    def game(self, data):
        if int(data[:3].decode()) == 400:
            data = data[5:]
            client_map = pickle.loads(data)

            self.game_server.setMap("client", client_map)
            server_map = Map().generateMap()
            print(server_map)
            self.game_server.setMap("server", server_map)
            message = "401\r\nLet the game begin!\r\n\r\n"
            self.transport.write(ciphering.encrypt(message)+b'\r\n\r\n')

        elif int(data[:3].decode()) == 405:
            code, message = self.game_server.client_move(data.decode())
            self.transport.write(ciphering.encrypt(message)+b'\r\n\r\n')

            while code == 421 or code == 422 or code == 413:
                code, message, client_map = self.game_server.server_move()
                message = message.encode()
                client_map = pickle.dumps(client_map) + b"\r\n\r\n"
                self.transport.write(ciphering.encrypt(message)+b'\r\n\r\n')
                message = client_map
                self.transport.write(ciphering.encrypt(message)+b'\r\n\r\n')
                if code == 421 or code == 422:
                    sleep(5)

            if code == 431 or code == 432:
                message = "450\r\nIf u want to play again send your map\r\n\r\n"
                self.transport.write(ciphering.encrypt(message)+b'\r\n\r\n')

    def connection_lost(self, ex):
        print('Client {} disconnected'.format(self.addr))

    # async def async_fib(self, fib_num):
    #     task = await loop.run_in_executor(thread_pool, Fib, fib_num)
    #
    #     response = (str(task) + "\r\n").encode()
    #     self.transport.write(response)


ciphering = EncryptorDecryptor()
thread_pool = ThreadPoolExecutor()
loop = asyncio.get_event_loop()
coroutine = loop.create_server(BattleshipProtocol, host='localhost', port=1769)
server = loop.run_until_complete(coroutine)

loop.run_forever()


