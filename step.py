import abc
import random
from board import rows, cols
from shoot import Shoot, PlayerShoot, PcShoot
from config import StartUpGameConfig, print_boards


def validate_input(row: int, col: int):
    if row > rows or row < 1:
        return False
    if col > cols or col < 1:
        return False

    return True


class Step(abc.ABC):
    def __init__(self, config: StartUpGameConfig) -> None:
        self.config = config

    @abc.abstractmethod
    def step(self):
        pass


class PlayerStep(Step):

    def __init__(self, config: StartUpGameConfig) -> None:
        super().__init__(config)

    def step(self):
        self.config.referi.print_accounts()
        print("TIME TO SHOOT")
        row = int(input("set row: "))
        col = int(input("set col: "))
        print(f"you choose row: {str(row)}, col: {str(col)}")
        if validate_input(row, col):
            shoot: Shoot = PlayerShoot(
                player=self.config.player, pc=self.config.pc)
            shoot.shoot(row=row, col=col)
            print_boards(self.config)
        else:
            print("Incorect input value")


class PcStep(Step):

    def __init__(self, config: StartUpGameConfig) -> None:
        super().__init__(config)

    def step(self):
        self.config.referi.print_accounts()
        print("TIME TO SHOOT")
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        print(f"pc choose row: {str(row)}, col: {str(col)}")
        if validate_input(row, col):
            shoot: Shoot = PcShoot(
                player=self.config.player, pc=self.config.pc)
            shoot.shoot(row=row, col=col)
            print_boards(self.config)
        else:
            print("Incorect input value")
