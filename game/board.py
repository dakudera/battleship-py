
import random
from . import Player, Referi, Ship

rows = 10
cols = 10
ships = [1, 1, 1, 1, 2, 2, 2, 3, 3]


class Board:

    def __init__(self, board, shooted_board):
        self.board = board
        self.shooted_board = shooted_board


class BorderPrinter():

    def __init__(self, board: Board, player_name: Player) -> None:
        self.board = board
        self.player_name = player_name

    def print(self):
        print(f"<----- BORDERS {self.player_name} ----->")

        print("PLAYER                   SHOOTED BORDER")
        for r in range(rows):
            line_player = ""
            line_pc = ""
            for c in range(cols):
                line_player += self.board.board[r][c].value+" "
                line_pc += self.board.shooted_board[r][c].value+" "
            print(line_player+"     "+line_pc)


class Cell():

    def __init__(self, value: str, is_shoted: bool, ship: Ship = None):
        self.value = value
        self.is_shoted = is_shoted
        self.ship = ship


class RandomSetBoat:
    def __init__(self, board, referi: Referi):
        self.board = board
        self.referi = referi

    def can_place_ship(self, ship_size, row, col, direction):
        size = len(self.board)

        if direction == 'horizontal':
            if col + ship_size > size:
                return False
            for i in range(ship_size):
                if self.board[row][col + i].value != '0':
                    return False
            for i in range(-1, ship_size + 1):
                if 0 <= row - 1 < size and 0 <= col + i < size and self.board[row - 1][col + i].value != '0':
                    return False
                if 0 <= row + 1 < size and 0 <= col + i < size and self.board[row + 1][col + i].value != '0':
                    return False
                if 0 <= col + i < size and self.board[row][col + i].value != '0':
                    return False
        else:  # vertical
            if row + ship_size > size:
                return False
            for i in range(ship_size):
                if self.board[row + i][col].value != '0':
                    return False
            for i in range(-1, ship_size + 1):
                if 0 <= col - 1 < size and 0 <= row + i < size and self.board[row + i][col - 1].value != '0':
                    return False
                if 0 <= col + 1 < size and 0 <= row + i < size and self.board[row + i][col + 1].value != '0':
                    return False
                if 0 <= row + i < size and self.board[row + i][col].value != '0':
                    return False

        return True

    def place_ship(self, ship_size):
        size = len(self.board)
        placed = False

        while not placed:
            row = random.randint(0, size - 1)
            col = random.randint(0, size - 1)
            direction = random.choice(['horizontal', 'vertical'])

            if self.can_place_ship(ship_size, row, col, direction):
                if direction == 'horizontal':
                    for i in range(ship_size):
                        self.board[row][col + i] = Cell(
                            value="1", is_shoted=False, ship=Ship(is_alive=True, size=i, referi=self.referi))
                else:
                    for i in range(ship_size):
                        self.board[row + i][col] = Cell(
                            value="1", is_shoted=False, ship=Ship(is_alive=True, size=i, referi=self.referi))
                placed = True

    def place_all_ships(self):
        for ship_size in ships:
            self.place_ship(ship_size)

        return self.board
