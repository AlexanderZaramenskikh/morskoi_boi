from random import randint

class Dot:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы делаете выстрел за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Клетка уже занята!"

class BoardWrongShipException(BoardException):
    pass


class Ship:
    def __init__(self, nose, length, vert_or_horis):
        self.nose = nose
        self.length = length
        self.vert_or_horis = vert_or_horis
        self.lives = length

    @property
    def dots(self):
        ship_cord = []
        for i in range(self.length):
            x = self.nose.x
            y = self.nose.y
            if self.vert_or_horis == 1:
                x += i
            elif self.vert_or_horis == 0:
                y += i
            ship_cord.append(Dot(x, y))
        return ship_cord

    def shooten(self, shot):
        return shot in self.dots

class Board:

    def __init__(self, hiden=False):
        self.hiden = hiden
        self.count = 0
        self.pole = [["□"] * 6 for _ in range(6)]
        self.busy = []
        self.ships = []


    def out(self, d):
        return not ((0 <= d.x < 6) and (0 <= d.y < 6))

    def contour(self,ship, verb = False):
        dots_near = [
                  (-1, -1), (-1, 0), (-1, 1),
                  (0, -1),   (0, 0),  (0, 1),
                  (1, -1),   (1, 0),  (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in dots_near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.pole[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
            for d in ship.dots:
                if self.out(d) or d in self.busy:
                    raise BoardWrongShipException()
            for d in ship.dots:
                self.pole[d.x][d.y] = "■"
                self.busy.append(d)

            self.ships.append(ship)
            self.contour(ship)


    def __str__(self):
        res = ""
        res += "   | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.pole):
            res += f"\n{i + 1}  | " + " | ".join(row) + " |"

        if self.hiden:
            res = res.replace('■', '□')
        return res


    def shot(self, d):
        if self.out(d):
            raise BoardOutException

        if d in self.busy:
            raise BoardUsedException

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.pole[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль подбит!")
                    return False
                else:
                    print("Корабль повреждён!")
                    return True

        self.pole[d.x][d.y] = "."
        print("Не попал!")
        return False

    def nachalo(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, 6), randint(0, 6)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.nachalo()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def __init__(self):
        self.size = 6
        pl = self.random_board()
        co = self.random_board()
        co.hiden = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def greet(self):
        print("-------------------")
        print(" Здравствуйте это  ")
        print("       игра        ")
        print("    морской бой    ")
        print("-------------------")
        print(" Правила ввода: x y")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Поле пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Поле компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Вы выиграли!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()




