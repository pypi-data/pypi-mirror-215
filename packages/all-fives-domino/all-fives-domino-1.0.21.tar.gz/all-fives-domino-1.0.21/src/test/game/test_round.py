from src.main.game.DominoRound import DominoRound
from src.main.game.Brain import AllFivesGreedyBrain, RandomBrain
from src.main.game.Player import Player
from src.main.game.Game import Game


def test_round_initialization():
    # Initialize a round and check there's a valid starting setup
    game = Game(Player(RandomBrain()), Player(RandomBrain()))
    round = DominoRound(Player(RandomBrain()), Player(RandomBrain()), game)

    assert round.board.origin is not None
    assert round.board.origin.is_double


