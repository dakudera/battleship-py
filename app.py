import random
from ships import Ship, Referi, Player

ships = [1, 1, 1, 1, 2, 2, 2, 3, 3]

rows = 10
cols = 10


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


class StartUpGameConfig:

    def __init__(self) -> None:
        self.sum_ships = sum(ships[s] for s in range(len(ships)-1))

        self.referi = Referi(player_ships=self.sum_ships,
                             pc_ships=self.sum_ships)
        self.player_border = self.default_init_borders()
        self.player_shooted_border = self.default_init_borders()

        self.pc_border = self.default_init_borders()
        self.pc_shooted_border = self.default_init_borders()
        self.set_ships()
        self.player: Board = Board(board=self.player_border,
                                   shooted_board=self.player_shooted_border)
        self.pc: Board = Board(board=self.pc_border,
                               shooted_board=self.pc_shooted_border)

    def set_ships(self):
        pl_border = RandomSetBoat(board=self.player_border, referi=self.referi)
        self.player_border = pl_border.place_all_ships()

        pc_border = RandomSetBoat(board=self.pc_border, referi=self.referi)
        self.pc_border = pc_border.place_all_ships()

    def default_init_borders(self):
        return [[Cell("0", False) for _ in range(cols)] for _ in range(rows)]


class Shoot:

    def __init__(self, player: Board, pc: Board):
        self.player = player
        self.pc = pc

    def shoot(self, row, col, shooter: Player):
        if shooter == Player.PLAYER:
            cell: Cell = self.pc.board[row-1][col-1]
            if cell.value == "1":
                shooted_board_cell: Cell = self.player.shooted_board[row-1][col-1]
                shooted_board_cell.value = "H"
                shooted_board_cell.is_shoted = True
                cell.is_shoted = True
                cell.value = "*"
                cell.ship.hit(player=shooter)
            else:
                cell.value = "*"
                cell.is_shoted = True
        else:
            cell: Cell = self.player.board[row-1][col-1]
            if cell.value == "1":
                shooted_board_cell: Cell = self.pc.shooted_board[row-1][col-1]
                shooted_board_cell.value = "H"
                shooted_board_cell.is_shoted = True
                cell.is_shoted = True
                cell.value = "*"
                cell.ship.hit(player=shooter)
            else:
                cell.value = "*"
                cell.is_shoted = True


def print_boards():
    player_printer = BorderPrinter(board=config.player, player_name="PLAYER")
    player_printer.print()
    pc_printer = BorderPrinter(board=config.pc, player_name="PC")
    pc_printer.print()


def validate_input(row: int, col: int):
    if row > rows or row < 1:
        return False
    if col > cols or col < 1:
        return False

    return True


def player_step(config: StartUpGameConfig):
    config.referi.print_accounts()
    print("TIME TO SHOOT")
    row = int(input("set row: "))
    col = int(input("set col: "))
    print(f"you choose row: {str(row)}, col: {str(col)}")
    if validate_input(row, col):
        shoot = Shoot(player=config.player, pc=config.pc)
        shoot.shoot(row=row, col=col, shooter=Player.PLAYER)
        print_boards()
    else:
        print("Incorect input value")


def pc_step(config: StartUpGameConfig):
    config.referi.print_accounts()
    print("TIME TO SHOOT")
    row = random.randint(0, rows - 1)
    col = random.randint(0, cols - 1)
    print(f"pc choose row: {str(row)}, col: {str(col)}")
    if validate_input(row, col):
        shoot = Shoot(player=config.player, pc=config.pc)
        shoot.shoot(row=row, col=col, shooter=Player.PC)
        print_boards()
    else:
        print("Incorect input value")


config = StartUpGameConfig()
print_boards()


def check_accounts(config: StartUpGameConfig):
    if config.referi.pc_ships == 0:
        return False
    if config.referi.player_ships == 0:
        return False
    else:
        return True


counter = 0
while check_accounts(config):
    if counter % 2 == 0:
        player_step(config=config)
    else:
        pc_step(config=config)
    counter += 1

config.referi.who_winner()
