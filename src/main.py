
from Screen import Game
from Settings import init_settings

if __name__ == '__main__':
    init_settings()
    print('Loaded settings!')

    game = Game()
    game.start_game()
