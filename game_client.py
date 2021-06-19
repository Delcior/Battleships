import numpy as np
import pickle


class Game_client:
    def __init__(self, s, board, ciph):
        self._legend = {0:'\': woda',
                        1: 'S: statek',
                        2: '*: oddany strzał',
                        3: 'X: trafiony statek przeciwnika'}
        self._shooting_board = np.zeros((10, 10))
        self._board = board
        self._s = s
        self._ciph = ciph

    def startGame(self):
        while True:
            self._print_boards()
            coords = input("Podaj koordynaty do strzału [0-9],[0,9]")
            try:
                x, y = int(coords[0]), int(coords[2])
            except:
                print("Niepoprawny format koordynatów. Spróbuj ponownie")
                continue

            if self._shooting_board[x, y] == 2 or self._shooting_board[x, y] == 3:
                print("Już strzelałeś w to miejsce")
                continue
            else:
                self._shooting_board[x, y] = 2
            self._s.sendall(self._ciph.encrypt(("405\r\nx:{x}\r\ny:{y}\r\n\r\n".format(x=x, y=y))))

            msg = self._rec()
            print(msg[4:])
            code = int(msg[:3])
            if code == 411 or code == 412:
                self._shooting_board[x, y] = 3
                continue
            if code == 413:
                while code == 421 or code == 422 or code == 413:
                    msg = self._rec()
                    print(msg[4:])
                    code = int(msg[:3])
                    mapa_od_serwera = self._rec_map()
                    board = pickle.loads(mapa_od_serwera)
                    self._board = board
            if code == 350:
                continue
            if code == 431 or code == 432:
                msg = self._rec()
                print(msg[4:3])
                break

    def _rec_map(self):
        crlf = b"\r\n\r\n"
        data_rec = b''
        while not data_rec.endswith(crlf):
            data_rec += self._s.recv(1)
        return self._ciph.decrypt(data_rec[:-4])[:-4]

    def _rec(self):
        crlf = b"\r\n\r\n"
        data_rec = b''
        while not data_rec.endswith(crlf):
            data_rec += self._s.recv(1)
        return self._ciph.decrypt(data_rec[:-4])[:-4].decode()

    def _print_boards(self):
        print(" " * 10 + "Twoja mapa " + "<" + "=" * 29 + ">" + " Mapa strzałów")

        print("-", end="  ")
        for j in range(self._board.shape[1]):
            print(j, end="  ")
        print("#" * 8, end="  ")
        print("-", end="  ")
        for j in range(self._board.shape[1]):
            print(j, end="  ")

        print("LEGENDA:")
        for i in range(self._board.shape[0]):
            print(i, end="  ")
            for j in range(self._board.shape[1]):
                ch = ''
                if self._board[i, j] == 0:
                    ch = '\''
                elif self._board[i, j] == 1:
                    ch = 'S'
                elif self._board[i, j] == 2:
                    ch = '*'
                elif self._board[i, j] == 3:
                    ch = 'X'
                print(ch, end="  ")
            print("#" * 8, end="  ")
            print(i, end="  ")
            for j in range(self._shooting_board.shape[1]):
                ch = ''
                if self._shooting_board[i, j] == 0:
                    ch = '\''
                elif self._shooting_board[i, j] == 1:
                    ch = 'S'
                elif self._shooting_board[i, j] == 2:
                    ch = '*'
                elif self._shooting_board[i, j] == 3:
                    ch = 'X'
                print(ch, end="  ")

            msg = self._legend[i] if i < len(self._legend) else ""
            print(msg)
