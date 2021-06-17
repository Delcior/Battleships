'''
Klient TCP
'''
import socket
import numpy as np
import pickle
import random
CRLF = b"\r\n\r\n"

class Map:
    def __init__(self):
        self.mapa = np.zeros((10, 10))
        self.pozycje = []
        self._notAvailable = set()
        self._boats = {1:4, 2:3, 3:2, 4:1}

    def buildMap(self):

        pass

    def _printInfo(self):
        msg_choice = "Masz do wyboru:\n" \
              " czteromasztowców: {czt}\n" \
              " trójmasztowców: {czy}\n" \
              " dwumasztowców:{dwa}\n" \
              " jednomasztowców: {jed}".format(
            czt=self._boats[4],
            czy=self._boats[3],
            dwa=self._boats[2],
            jed=self._boats[1])

        msg_options = "\n ====Menu====\n" \
                      "[1] rozstaw jednomasztowiec\n" \
                      "[2] rozstaw dwumasztowiec\n" \
                      "[3] rozstaw trójmasztwoiec\n" \
                      "[4] roztaw czwórmasztwiec\n" \
                      "[enter] Zaakceptuj (brak statków zostanie uzupełniony losowo)"
        print(self.mapa)
        print(msg_choice)
        print(msg_options)
    def generateMap(self):
        for i in range(4, 0, -1):
            self._placeBoats(i)
            # print("======po ulozeniu %d" % (i,))
            # print(self.mapa)
            # print(np.sum(self.mapa))
            # print("===================")
        # self._placeBoats(4)
        # print("======po ulozeniu %d" % (4,))
        print(self.mapa)
        print(np.sum(self.mapa))
        # print("===================")

    def _placeBoats(self, length):
        while self._boats[length] > 0:
            x = random.randint(0, 10)
            y = random.randint(0, 10)
            coords = (x, y)#np.array([x, y])

            if self._isGood(coords):
                #0 - góra
                #1 - prawo itd..
                for i in range(4):
                    flag, points, map = self._chooseDirection(coords, i, length)
                    if flag:
                        self.mapa = map
                        self._excludePoints(points)
                        self._boats[length]-=1
                        break


    def _chooseDirection(self, point, direction, len):
        if not self._isGood(point):
            return False, None, None
        #TODO: USUN MAP_COPY :)
        map_copy = np.copy(self.mapa)
        points = {point}
        points = self._addNeighbours(point, points)
        map_copy[point[0], point[1]] = 1

        if direction == 0:
            for i in range(len-1):
                point = point[0], point[1]+1
                if not self._isGood(point):
                    return False, None, None
                points.add(point)
                map_copy[point[0], point[1]] = 1
                points = self._addNeighbours(point, points)
        elif direction == 1:
            for i in range(len-1):
                point = (point[0]+1, point[1])
                if not self._isGood(point):
                    return False, None, None
                points.add(point)
                map_copy[point[0], point[1]] = 1
                points = self._addNeighbours(point, points)
        elif direction == 2:
            for i in range(len-1):
                point = (point[0], point[1]-1)
                if not self._isGood(point):
                    return False, None, None
                points.add(point)
                map_copy[point[0], point[1]] = 1
                points = self._addNeighbours(point, points)
        elif direction == 3:
            for i in range(len-1):
                point = (point[0]-1, point[1])
                if not self._isGood(point):
                    return False, None, None
                points.add(point)
                map_copy[point[0], point[1]] = 1
                points = self._addNeighbours(point, points)

        return True, points, map_copy


    def _isGood(self, coords):
        return coords not in self._notAvailable and (0 <= coords[0] < 10 and 0 <=coords[1] < 10)


    def _addNeighbours(self, point, points):
        points.add((point[0]+1, point[1]))
        points.add((point[0]+1, point[1]+1))
        points.add((point[0]+1, point[1]-1))
        points.add((point[0]-1, point[1]))
        points.add((point[0]-1, point[1]+1))
        points.add((point[0]-1, point[1]-1))
        points.add((point[0], point[1]+1))
        points.add((point[0], point[1]-1))

        return points


    def _excludePoints(self, points):
        """
        :param points - tablica par (x,y):
        :return:
        """
        for point in points:
            if self._isGood(point):
                self._notAvailable.add(point)

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
klasa.generateMap()

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
