import abc
from . import Board, Cell, Player


class Shoot(abc.ABC):

    def __init__(self, player: Board, pc: Board):
        self.player = player
        self.pc = pc

    @abc.abstractmethod
    def shoot(self, row, col, shooter: Player):
        pass


class PlayerShoot(Shoot):

    def __init__(self, player: Board, pc: Board):
        super().__init__(player, pc)

    def shoot(self, row, col):
        cell: Cell = self.pc.board[row-1][col-1]
        shooted_board_cell: Cell = self.player.shooted_board[row-1][col-1]
        if cell.value == "1":
            shooted_board_cell.value = "H"
            shooted_board_cell.is_shoted = True
            cell.is_shoted = True
            cell.value = "*"
            cell.ship.hit(player=Player.PLAYER)
        else:
            shooted_board_cell.value = "*"
            shooted_board_cell.is_shoted = True


class PcShoot(Shoot):

    def __init__(self, player: Board, pc: Board):
        super().__init__(player, pc)

    def shoot(self, row, col):
        cell: Cell = self.player.board[row-1][col-1]
        if cell.value == "1":
            shooted_board_cell: Cell = self.pc.shooted_board[row-1][col-1]
            shooted_board_cell.value = "H"
            shooted_board_cell.is_shoted = True
            cell.is_shoted = True
            cell.value = "*"
            cell.ship.hit(player=Player.PC)
        else:
            cell.value = "*"
            cell.is_shoted = True
