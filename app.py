from game import (
    StartUpGameConfig, print_boards,
    Step, PlayerStep, PcStep
)


def check_accounts(config: StartUpGameConfig):
    if config.referi.pc_ships == 0:
        return False
    if config.referi.player_ships == 0:
        return False
    else:
        return True


def play_game():
    config = StartUpGameConfig()
    player_step: Step = PlayerStep(config)
    pc_step: Step = PcStep(config)
    print_boards(config=config)
    counter = 0
    while check_accounts(config):
        if counter % 2 == 0:
            player_step.step()
        else:
            pc_step.step()
        counter += 1

    config.referi.who_winner()


if __name__ == "__main__":
    play_game()
