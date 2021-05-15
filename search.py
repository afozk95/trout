from typing import Any, Callable, Dict, Tuple, Optional
from abc import ABC
import random
import chess


class Searcher(ABC):
    def __init__(self) -> None:
        pass

    def search(self, board: chess.Board, **kwargs: Any) -> Tuple[float, chess.Move]:
        pass


class RandomSearcher(Searcher):
    def __init__(self) -> None:
        pass

    def search(self, board: chess.Board) -> Tuple[float, chess.Move]:
        return 0.0, random.choice(list(board.legal_moves))


class MinimaxSearcher(Searcher):
    def __init__(self, max_depth: int) -> None:
        self.max_depth = max_depth

    def search(self, board: chess.Board, value_func: Callable[[chess.Board], float]) -> Tuple[float, chess.Move]:
        return self.__class__._search(board, value_func, self.max_depth, 0)

    @classmethod
    def _search(cls, board: chess.Board, value_func: Callable[[chess.Board], float], max_depth: int, curr_depth: int = 0) -> Tuple[float, chess.Move]:
        assert max_depth >= 1, f"max_depth should be positive integer, {max_depth} is passed"

        if curr_depth == max_depth:
            return value_func(board), None

        # maximize
        if board.turn == chess.WHITE:
            best_valuation = -float("inf")
            best_move = None
            for move in board.legal_moves:
                board.push(move)
                valuation, _ = cls._search(board, value_func, max_depth, curr_depth+1)
                board.pop()
                if valuation > best_valuation:
                    best_valuation = valuation
                    best_move = move
        # minimize
        elif board.turn == chess.BLACK:
            best_valuation = float("inf")
            best_move = None
            for move in board.legal_moves:
                board.push(move)
                valuation, _ = cls._search(board, value_func, max_depth, curr_depth+1)
                board.pop()
                if valuation < best_valuation:
                    best_valuation = valuation
                    best_move = move

        return best_valuation, best_move


class AlphaBetaSearcher(Searcher):
    def __init__(self, max_depth: int, is_memory: bool = False) -> None:
        self.max_depth = max_depth
        self.is_memory = is_memory
        self.memory = {} if self.is_memory else None

    def search(self, board: chess.Board, value_func: Callable[[chess.Board], float]) -> Tuple[float, chess.Move]:
        best_valuation, best_move, memory = self.__class__._search(board, value_func, self.max_depth, self.memory, 0, -float("inf"), float("inf"))
        self.memory = memory
        return best_valuation, best_move

    @classmethod
    def _search(cls, board: chess.Board, value_func: Callable[[chess.Board], float], max_depth: int, memory: Optional[Dict[str, float]], curr_depth: int = 0, alpha: float = -float("inf"), beta: float = float("inf")) -> Tuple[float, chess.Move, Optional[Dict[str, float]]]:
        assert max_depth >= 1, f"max_depth should be positive integer, {max_depth} is passed"

        if curr_depth == max_depth:
            if memory is None:
                return value_func(board), None, None
            else:
                board_fen = board.fen()
                if board_fen in memory:
                    return memory[board_fen], None, memory
                else:
                    value = value_func(board)
                    memory[board_fen] = value
                    return value, None, memory

        # maximize
        if board.turn == chess.WHITE:
            best_valuation = -float("inf")
            best_move = None
            for move in board.legal_moves:
                board.push(move)
                valuation, _, memory = cls._search(board, value_func, max_depth, memory, curr_depth+1, best_valuation, beta)
                board.pop()
                if valuation > best_valuation:
                    best_valuation = valuation
                    best_move = move
                if best_valuation > beta:
                    return beta, best_move, memory
        # minimize
        elif board.turn == chess.BLACK:
            best_valuation = float("inf")
            best_move = None
            for move in board.legal_moves:
                board.push(move)
                valuation, _, memory = cls._search(board, value_func, max_depth, memory, curr_depth+1, alpha, best_valuation)
                board.pop()
                if valuation < best_valuation:
                    best_valuation = valuation
                    best_move = move
                if best_valuation < alpha:
                    return alpha, best_move, memory

        return best_valuation, best_move, memory


class AlphaBetaWithMemorySearcher(Searcher):
    def __init__(self, max_depth: int) -> None:
        self.max_depth = max_depth
        self.memory = {}

    def search(self, board: chess.Board, value_func: Callable[[chess.Board], float]) -> Tuple[float, chess.Move]:
        best_valuation, best_move, memory = self.__class__._search(board, value_func, self.max_depth, self.memory, 0, -float("inf"), float("inf"))
        self.memory = memory
        return best_valuation, best_move

    @classmethod
    def _search(cls, board: chess.Board, value_func: Callable[[chess.Board], float], max_depth: int, memory: Dict[str, float], curr_depth: int = 0, alpha: float = -float("inf"), beta: float = float("inf")) -> Tuple[float, chess.Move, Dict[str, float]]:
        assert max_depth >= 1, f"max_depth should be positive integer, {max_depth} is passed"

        if curr_depth == max_depth:
            board_fen = board.fen()
            if board_fen in memory:
                return memory[board_fen], None, memory
            else:
                value = value_func(board)
                memory[board_fen] = value
                return value, None, memory

        # maximize
        if board.turn == chess.WHITE:
            best_valuation = -float("inf")
            best_move = None
            for move in board.legal_moves:
                board.push(move)
                valuation, _, memory = cls._search(board, value_func, max_depth, memory, curr_depth+1, best_valuation, beta)
                board.pop()
                if valuation > best_valuation:
                    best_valuation = valuation
                    best_move = move
                if best_valuation > beta:
                    return beta, best_move, memory
        # minimize
        elif board.turn == chess.BLACK:
            best_valuation = float("inf")
            best_move = None
            for move in board.legal_moves:
                board.push(move)
                valuation, _, memory = cls._search(board, value_func, max_depth, memory, curr_depth+1, alpha, best_valuation)
                board.pop()
                if valuation < best_valuation:
                    best_valuation = valuation
                    best_move = move
                if best_valuation < alpha:
                    return alpha, best_move, memory

        return best_valuation, best_move, memory
