import numpy as np
import random


class Map:
    def __init__(self):
        self.mapa = np.zeros((10, 10), dtype=int)
        self.pozycje = []
        self._notAvailable = set()
        self._boats = {1: 4, 2: 3, 3: 2, 4: 1}
        self._buildingMap = True
        # self._directions = {'N':(-1,0), 'S':(1,0), 'E':(0,1), 'W':(0,-1)}
        self._directions = {'N': 3, 'S': 1, 'E': 0, 'W': 2}
        self._menu = {0: "[1] Put a Patrol Boat", 1: "[2] Put a Submarine",
                      2: "[3] Put a Cruiser", 3: "[4] Put a Battleship",
                      4: "[0] Accept (spacing randomly)"}

    def configuration(self):
        self._buildMap()
        return self.mapa

    def _buildMap(self):
        while self._buildingMap:
            self._print_map()
            command = input("Choose option: ")
            if command.isdigit():
                command = int(command)
                if command == 0:
                    self.generateMap()

                elif self._boats[command] == 0:
                    print("You cannot build this ship anymore")
                    continue
                else:
                    message = self._placeBoat(command)
                    if not message:
                        print("You can't put your ship there.")

                self._buildingMap = not sum(self._boats.values()) == 0
            else:
                print("Invalid option. Retry your selection.")

    def _placeBoat(self, length):
        start = input("Enter the initial coordinates  [0-9],[0-9]. Default 0,0: ")
        if len(start) == 3:
            start = start.split(',')
            if start[0].isdigit() and start[1].isdigit():
                start = (int(start[0]), int(start[1]))
        else:
            start = (0, 0)
        direction = input("Enter the direction [N, S, E, W]. If None by default N: ") if length > 1 else "N"
        if direction != 'N' or direction != 'S' or direction != 'E' or direction != 'W':
            direction = 'N'
        flag, points, map = self._chooseDirection(start, self._directions[direction], length)
        if flag:
            self.mapa = map
            self._excludePoints(points)
            self._boats[length] -= 1

        if points is None:
            return False

        return True

    def _checkBoat(self, start, len, direction):
        if not self._isGood(start):
            return None

        points = [start]
        for i in range(len - 1):
            start = tuple(np.add(start, self._directions[direction]))
            if not self._isGood(start):
                return None
            points.append(start)
        return points

    def _checkPoints(self, a, b, length):
        return (a[0] == b[0] or a[1] == b[1]) and (abs(a[0] - b[0]) == length or abs(a[1] - b[1]) == length)

    def _print_map(self):
        print("Your map")
        board = self.mapa
        print("-", end="  ")
        for j in range(board.shape[1]):
            print(j, end="  ")
        header = "<" + "-" * 13 + "MENU" + "-" * 13 + "> "
        print(header + "Ships:")
        for i in range(board.shape[0]):
            print(i, end="  ")
            for j in range(board.shape[1]):
                ch = ''
                if board[i, j] == 0:
                    ch = '\''
                elif board[i, j] == 1:
                    ch = 'S'
                print(ch, end="  ")

            menu = self._menu[i] + " " * (len(header) - len(self._menu[i])) if i < len(self._menu) else ""

            menu += "Left: {}".format(self._boats[i + 1]) if i < len(self._boats) else ""
            print(menu)

    def generateMap(self):
        for i in range(4, 0, -1):
            self._placeBoats(i)
        return self.mapa

    def _placeBoats(self, length):
        while self._boats[length] > 0:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            coords = (x, y)  # np.array([x, y])

            if self._isGood(coords):
                # 0 - up
                # 1 - right itd..
                for i in range(4):
                    flag, points, map = self._chooseDirection(coords, i, length)
                    if flag:
                        self.mapa = map
                        self._excludePoints(points)
                        self._boats[length] -= 1
                        break

    def _chooseDirection(self, point, direction, len):
        if not self._isGood(point):
            return False, None, None
        map_copy = np.copy(self.mapa)
        points = {point}
        points = self._addNeighbours(point, points)
        map_copy[point[0], point[1]] = 1

        if direction == 0:
            for i in range(len - 1):
                point = point[0], point[1] + 1
                if not self._isGood(point):
                    return False, None, None
                points.add(point)
                map_copy[point[0], point[1]] = 1
                points = self._addNeighbours(point, points)
        elif direction == 1:
            for i in range(len - 1):
                point = (point[0] + 1, point[1])
                if not self._isGood(point):
                    return False, None, None
                points.add(point)
                map_copy[point[0], point[1]] = 1
                points = self._addNeighbours(point, points)
        elif direction == 2:
            for i in range(len - 1):
                point = (point[0], point[1] - 1)
                if not self._isGood(point):
                    return False, None, None
                points.add(point)
                map_copy[point[0], point[1]] = 1
                points = self._addNeighbours(point, points)
        elif direction == 3:
            for i in range(len - 1):
                point = (point[0] - 1, point[1])
                if not self._isGood(point):
                    return False, None, None
                points.add(point)
                map_copy[point[0], point[1]] = 1
                points = self._addNeighbours(point, points)

        return True, points, map_copy

    def _isGood(self, coords):
        return coords not in self._notAvailable and (0 <= coords[0] < 10 and 0 <= coords[1] < 10)

    def _addNeighbours(self, point, points):
        points.add((point[0] + 1, point[1]))
        points.add((point[0] + 1, point[1] + 1))
        points.add((point[0] + 1, point[1] - 1))
        points.add((point[0] - 1, point[1]))
        points.add((point[0] - 1, point[1] + 1))
        points.add((point[0] - 1, point[1] - 1))
        points.add((point[0], point[1] + 1))
        points.add((point[0], point[1] - 1))

        return points

    def _excludePoints(self, points):
        """
        :param points - tablica par (x,y):
        :return:
        """
        for point in points:
            if self._isGood(point):
                self._notAvailable.add(point)
