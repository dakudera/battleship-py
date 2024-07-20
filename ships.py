import array
import abc
from enum import Enum


class Player(Enum):
    PLAYER = 1
    PC = 2


class Referi:

    def __init__(self, player_ships, pc_ships):
        self.player_ships = player_ships
        self.pc_ships = pc_ships

    def update_player(self):
        self.player_ships -= 1

    def update_pc(self):
        self.pc_ships -= 1

    def print_accounts(self):
        print(f"PLEYER: {self.player_ships} PC: {self.pc_ships}")

    def who_winner(self):
        if self.player_ships > 0 and self.pc_ships == 0:
            print("PLAYER WIN!!!")
        else:
            print("PC WIN!!!")


class Deck:

    def __init__(self, coord: tuple, is_alive: bool):
        self.coord = coord
        self.is_alive = is_alive


class Ship:

    def __init__(self, is_alive: bool, size: int, referi: Referi, decks=None) -> None:
        self.observers = set()
        self.is_alive = is_alive
        self.size = size
        self.referi = referi

    def set_decks(self, decks):
        self.decks = decks

    def set_is_alive(self, is_alive):
        self.is_alive = is_alive

    def attach_observer(self, referi: Referi):
        self.observers.add(referi)

    def hit(self, player: Player):
        if player == Player.PLAYER:
            self.referi.update_pc()
        else:
            self.referi.update_player()
