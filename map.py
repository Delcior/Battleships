import numpy as np
import random

class Map:
    def __init__(self):
        self.mapa = np.zeros((10, 10))
        self.pozycje = []
        self._notAvailable = set()
        self._boats = {1:4, 2:3, 3:2, 4:1}
        self._buildingMap = True
        self._directions = {'N':(-1,0), 'S':(1,0), 'E':(0,1), 'W':(0,-1)}

    def configuration(self):
        self._buildMap()
        print("===============Twoja mapa===============")
        print(self.mapa)
        return self.mapa
        
    def _buildMap(self):
        while self._buildingMap:
            self.printInfo()
            command = int(input("Wybierz opcję: "))

            if command == 0:
                self.generateMap()

            elif self._boats[command] == 0:
                print("Nie możesz już postawić tego statku")
                continue
            else:
                flag = self._placeBoat(command)
                if flag:
                    #zmniejszam ilosc stateczkow
                    self._boats[command] -= 1
            self._buildingMap = not sum(self._boats.values()) == 0

    def _placeBoat(self, length):
        start = input("Podaj koordynaty początkowe [0-9],[0-9]: ")
        start = start.split(',')
        start = (int(start[0]), int(start[1]))
        direction = input("Podaj kierunek [N, S, E, W]: ")

        pts = self._checkBoat(start, length, direction)

        if pts is None:
            return False

        for point in pts:
            self.mapa[point[0], point[1]] = 1
            self._notAvailable.add(point)

        return True

    def _checkBoat(self, start, len, direction):
        if not self._isGood(start):
            return None

        points = [start]
        for i in range(len-1):
            start = tuple(np.add(start, self._directions[direction]))
            print(start)
            if not self._isGood(start):
                return None
            points.append(start)
        print(points)
        return points


    def _checkPoints(self, a, b, length):
        return (a[0] == b[0] or a[1] == b[1]) and (abs(a[0]-b[0]) == length or abs(a[1]-b[1]) == length)

    def printInfo(self):
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
                      "[4] roztaw czteromasztowiec\n" \
                      "[0] Zaakceptuj (brak statków zostanie uzupełniony losowo)"
        print(self.mapa)
        print(msg_choice,end='')
        print(msg_options)

    def generateMap(self):
        for i in range(4, 0, -1):
            self._placeBoats(i)
        return self.mapa
        # print(self.mapa)
        # print(np.sum(self.mapa))

    def _placeBoats(self, length):
        while self._boats[length] > 0:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
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
