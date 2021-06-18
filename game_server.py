import random

import numpy as np


class Game_server:
    def __init__(self):
        self._server_map = np.zeros((10, 10))
        self._server_boats_counter = 20
        self._client_map = np.zeros((10, 10))
        self._client_boats_counter = 20

    def setMap(self, owner, new_map):
        if owner == "server":
            self._server_map = new_map
        elif owner == "client":
            self._client_map = new_map

    def _parse_attack(self, message):
        x, y = 0, 0
        for i in range(len(message)):
            if message[i] == 'x':
                x = int(message[i + 2])
            elif message[i] == 'y':
                y = int(message[i + 2])
                return x, y

    def client_move(self, message):
        x, y = self._parse_attack(message)

        if self._server_map[x, y] == 1:
            self._server_boats_counter -= 1

            if self._server_boats_counter == 0:
                return 431, "431\r\nYou won this time\r\n\r\n"

            neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            self._server_map[x, y] = 2
            for el in neighbours:
                x_n, y_n = el
                if 0 <= x_n < 10 and 0 <= y_n < 10:
                    if self._server_map[x_n, y_n] == 1:
                        return 411, "411\r\nHit!\r\n\r\n"

            return 412, "412\r\nHit and sink!\r\n\r\n"
        return 413, "413\r\nMiss!\r\n\r\n"

    def server_move(self):

        x, y = random.randint(0, 9), random.randint(0, 9)
        print(x, y)
        while self._client_map[x, y] == 2:
            x, y = random.randint(0, 9), random.randint(0, 9)

        if self._client_map[x, y] == 1:
            self._client_boats_counter -= 1
            self._client_map[x, y] = 2
            if self._client_boats_counter == 0:
                return 432, "432\r\nI shoot {x},{y}. Of course I won!\r\n\r\n".format(x=x, y=y), self._client_map

            neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

            for el in neighbours:
                x_n, y_n = el
                if 0 <= x_n < 10 and 0 <= y_n < 10:
                    if self._client_map[x_n, y_n] == 1:
                        return 421, "421\r\nI shoot {x},{y} I hit!\r\n\r\n".format(x=x, y=y), self._client_map

            return 422, "422\r\nYour battleship sinks!\r\n\r\n", self._client_map
        elif self._client_map[x, y] == 0:
            self._client_map[x, y] = 2
        return 423, "423\r\nI missed!\r\n\r\n", self._client_map
