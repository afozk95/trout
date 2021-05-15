from typing import Tuple
from abc import ABC
import chess
import random
from constants import (
    GameStatus,
    PIECE_VALUES,
    PIECE_POSITION_VALUES,
)


import time
import functools


class Valuator(ABC):
    def __init__(self) -> None:
        pass

    def evaluate(self, board: chess.Board) -> float:
        pass


class RandomValuator(Valuator):
    def __init__(self, min_val: float = -1.0, max_val: float = 1.0) -> None:
        assert min_val < max_val, "min_val should be less than max_val"
        self.min_val = min_val
        self.max_val = max_val
    
    def evaluate(self, board: chess.Board) -> float:
        return random.uniform(self.min_val, self.max_val)


class PieceSumValuator(Valuator):
    def __init__(self, is_use_piece_position_values: bool = False, is_use_game_status: bool = False) -> None:
        self.is_use_piece_position_values = is_use_piece_position_values
        self.is_use_game_status = is_use_game_status

    # TODO: implement, right now defaults to GameStatus.ALL
    def get_game_status(self, board: chess.Board) -> GameStatus:
        return GameStatus.ALL

    # used by evaluate_slow
    def get_sum_piece_values(self, board: chess.Board) -> Tuple[float, float]:
        white_total_piece_value = 0
        black_total_piece_value = 0
        for square_int, piece in board.piece_map().items():
            if piece.color == chess.WHITE:
                white_total_piece_value += PIECE_VALUES[piece.piece_type]
            else:
                black_total_piece_value += PIECE_VALUES[piece.piece_type]

        return white_total_piece_value, black_total_piece_value

    # used by evaluate_slow
    def get_sum_piece_position_values(self, board: chess.Board) -> Tuple[float, float]:
        white_total_piece_position_value = 0
        black_total_piece_position_value = 0
        for square_int, piece in board.piece_map().items():
            if piece.color == chess.WHITE:
                white_total_piece_position_value += PIECE_POSITION_VALUES[piece.piece_type][piece.color][self.get_game_status(board) if self.is_use_game_status else GameStatus.ALL][square_int]
            else:
                black_total_piece_position_value += PIECE_POSITION_VALUES[piece.piece_type][piece.color][self.get_game_status(board) if self.is_use_game_status else GameStatus.ALL][square_int]

        return white_total_piece_position_value, black_total_piece_position_value

    def evaluate_slow(self, board: chess.Board) -> float:
        white_total_piece_value, black_total_piece_value = self.get_sum_piece_values(board)
        evaluation = white_total_piece_value - black_total_piece_value

        if self.is_use_piece_position_values:
            white_total_piece_position_value, black_total_piece_position_value = self.get_sum_piece_position_values(board)
            piece_position_evaluation = white_total_piece_position_value - black_total_piece_position_value
            evaluation += piece_position_evaluation

        return evaluation
    
    def evaluate(self, board: chess.Board) -> float:
        value = 0
        for square_int, piece in board.piece_map().items():
            value += (1 if piece.color else -1) * (PIECE_VALUES[piece.piece_type] + (1 if self.is_use_piece_position_values else 0) * PIECE_POSITION_VALUES[piece.piece_type][piece.color][self.get_game_status(board) if self.is_use_game_status else GameStatus.ALL][square_int])

        return value
