from typing import Tuple
import chess
from search import Searcher
from value import Valuator


class ComputerPlayer:
    def __init__(self, searcher: Searcher, valuator: Valuator) -> None:
        self.searcher = searcher
        self.valuator = valuator
    
    def get_move(self, board: chess.Board) -> Tuple[float, chess.Move]:
        return self.searcher.search(board, value_func=self.valuator.evaluate)
