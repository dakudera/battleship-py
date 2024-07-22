from board import (
    Board, cols, rows,
    RandomSetBoat, Cell, ships, BorderPrinter
)
from ships import Referi


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


def print_boards(config: StartUpGameConfig):
    player_printer = BorderPrinter(board=config.player, player_name="PLAYER")
    player_printer.print()
    pc_printer = BorderPrinter(board=config.pc, player_name="PC")
    pc_printer.print()
