'''
Serwer TCP
'''
import asyncio
import random
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

"""
200: dals[pdsap[l\r\n


212

"211\r\nMessage=hello,give me your key.There is my key\r\nKey=key\r\nKey-len:2048\r\n\r\n"

"""
def Fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return Fib(n - 1) + Fib(n - 2)

class ProjectA:

    def __init__(self):
        self.codes = {}
        self.finished = False

    def accept_201(self, data):
        if data == "201: Hello\r\n\r\n":
            self.codes[201] = True
            # read key from file

            message = "211\r\nMessage=hello,give me your key.There is my key\r\nKey={key}\r\nKey-len=2048\r\n\r\n".format(
                key=""
            )
            # klient 211\r\nMessage=There is my key\r\nKey={key}\r\nKey-len=2048\r\n\r\n
    def accept_202(self, data):




class BattleshipProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.addr = transport.get_extra_info('peername')
        self._rest = b''
        self.name = None
        self.ProjectA = ProjectA()
        print('Connection from {}'.format(self.addr))

    def data_received(self, data):
        data = self._rest + data
        print(data)

        if not self.ProjectA.finished:
            data = data.decode()
            if int(data[:3]) == 201:
                message = self.ProjectA.accept_201(data)
                self.transport.write(message.encode())
            if int(data[:3]) == 202:
                if self.ProjectA.codes[201]:
                    self.ProjectA.accept_202(data)
                else:


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

    async def async_fib(self, fib_num):
        task = await loop.run_in_executor(thread_pool, Fib, fib_num)

        response = (str(task) + "\r\n").encode()
        self.transport.write(response)


thread_pool = ThreadPoolExecutor()
loop = asyncio.get_event_loop()
coroutine = loop.create_server(BattleshipProtocol, host='localhost', port=1769)
server = loop.run_until_complete(coroutine)

loop.run_forever()