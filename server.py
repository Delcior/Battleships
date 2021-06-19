'''
Serwer TCP
'''
import asyncio
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import pickle
from utils import *
from game_server import *
from map import *


class HelloHandshake:
    def __init__(self):
        self.codes = {}
        self.finished = False

    def accept_201(self, data):
        """
        The function accepts a welcome message, returns a frame with the response
        (server public key and length of this key)
        """
        if data == "201\r\nHello\r\n\r\n":
            self.codes[201] = True
            message = "211\r\nMessage=Hello,give me your key.\r\n" \
                      "Key-len=2048\r\n" \
                      "Key={key}\r\n\r\n".format(
                key=ciphering.get_pubKey().decode())
            return message
        return "399:\r\nMessage not recognized. Try again\r\n\r\n"

    def accept_212(self, data):
        if "212\r\nMessage=My key\r\nKey-len=2048\r\nKey=" in data:
            headers = HandshakeParser(data)
            if headers['key'] == 'Bad key':
                return "397: Key format is not valid.\r\n\r\n"
            if headers['code'] == 212 and self.codes[201]:
                try:
                    ciphering.set_pubKey2(headers['key'])
                except:
                    return "396: Key is not valid. Try again\r\n\r\n"
                self.finished = True
                return '210\r\nMessage=All messages are now encrypted \r\n\r\n' \
                       '101\r\nInfo:Build a map\r\n\r\n'

        return "398:\r\nMessage type not recognized. Try again. Remember we accept only RSA keys with length " \
               "2048\r\n\r\n "


class BattleshipProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.addr = transport.get_extra_info('peername')
        self.HelloHandshake = HelloHandshake()
        self.game_server = Game_server()
        self.encrypted = False
        print('Connection from {}'.format(self.addr))

    def data_received(self, data):
        if not self.encrypted and data[:3].isdigit():
            if not self.HelloHandshake.finished:
                code = int(data[:3])
                data = data.decode()
                if code == 201:
                    message = self.HelloHandshake.accept_201(data)
                    self.transport.write(message.encode())
                elif code == 212:
                    message = self.HelloHandshake.accept_212(data)
                    self.transport.write(message.encode())
                else:
                    message = "371\r\n Message code is not valid.\r\n\r\n"
                    self.transport.write(message.encode())
                return

        data = ciphering.decrypt(data)
        if data[:3].isdigit():
            asyncio.create_task(self.game_async(data))
        else:
            message = "370\r\n Message without a code. Not valid.\r\n\r\n"
            if self.encrypted:
                self.transport.write(ciphering.encrypt(message) + b'\r\n\r\n')

    async def game_async(self, data):
        await loop.run_in_executor(thread_pool, self.game, data)

    def game(self, data):
        code = int(data[:3].decode())
        if code == 400:
            data = data[5:]
            client_map = pickle.loads(data)

            self.game_server.setMap("client", client_map)
            server_map = Map().generateMap()
            self.game_server.setMap("server", server_map)
            message = "401\r\nLet the game begin!\r\n\r\n"
            self.transport.write(ciphering.encrypt(message) + b'\r\n\r\n')

        elif code == 405:
            code, message = self.game_server.client_move(data.decode())
            self.transport.write(ciphering.encrypt(message) + b'\r\n\r\n')

            while code == 421 or code == 422 or code == 413:
                code, message, client_map = self.game_server.server_move()
                message = message.encode()
                client_map = pickle.dumps(client_map) + b"\r\n\r\n"
                self.transport.write(ciphering.encrypt(message) + b'\r\n\r\n')
                message = client_map
                self.transport.write(ciphering.encrypt(message) + b'\r\n\r\n')
                if code == 421 or code == 422:
                    sleep(2)
            if code == 431 or code == 432:
                self.transport.close()
        else:
            message = "371\r\n Message code is not valid.\r\n\r\n"
            self.transport.write(ciphering.encrypt(message) + b'\r\n\r\n')

    def connection_lost(self, ex):
        print('Client {} disconnected'.format(self.addr))


ciphering = EncryptorDecryptor()
thread_pool = ThreadPoolExecutor()
loop = asyncio.get_event_loop()
coroutine = loop.create_server(BattleshipProtocol, host='localhost', port=1770)
server = loop.run_until_complete(coroutine)

loop.run_forever()
