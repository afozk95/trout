import chess
from player import ComputerPlayer
from search import AlphaBetaSearcher
from value import PieceSumValuator


def init():
    print("Welcome! I'm trout, a simple chess engine implemented in Python.")


def ask_new_game() -> bool:
    while True:
        answer = input("Do you want to play a chess game against me? [(y)es or (n)o]\n")
        if answer.lower() in ["y", "yes"]:
            return True
        elif answer.lower() in ["n", "no"]:
            return False
        else:
            print("Valid answers are: y / yes or n / no")


def ask_color() -> chess.Color:
    while True:
        answer = input("Which color do you want to play? [(w)hite or (b)lack]\n")
        if answer.lower() in ["w", "white"]:
            return chess.WHITE
        elif answer.lower() in ["b", "black"]:
            return chess.BLACK
        else:
            print("Valid answers are: w / white or b / black")


def ask_move(board: chess.Board) -> chess.Move:
    while True:
        answer = input("Your move?\n")
        legal_moves_str = ", ".join([str(move) for move in board.legal_moves])
        try:
            move = chess.Move.from_uci(answer)
            if board.is_legal(move):
                return move
            else:
                print(f"Not a legal move! Legal moves: [{legal_moves_str}]")
        except:
            print(f"Cannot parse move! Legal moves: [{legal_moves_str}]")


def print_computer_move(move: chess.Move) -> None:
    print(f"Computer plays {move}")


def print_user_move(move: chess.Move) -> None:
    print(f"You play {move}")


def print_board(board: chess.Board, user_color: chess.Color) -> None:
    if user_color == chess.WHITE:
        print(board)
    else:
        print(board.transform(chess.flip_horizontal).transform(chess.flip_vertical))


def play_game(user_color = chess.Color) -> None:
    valuator = PieceSumValuator(is_use_piece_position_values=True, is_use_game_status=True)
    searcher = AlphaBetaSearcher(max_depth=4)
    computer_player = ComputerPlayer(searcher, valuator)
    b = chess.Board()

    print("Game starts.")
    print_board(b, user_color)
    print()

    while True:
        if b.turn == user_color:
            user_move = ask_move(b)
            print_user_move(user_move)
            b.push(user_move)
            print_board(b, user_color)
        else:
            _, computer_move = computer_player.get_move(b)
            print_computer_move(computer_move)
            b.push(computer_move)
            print_board(b, user_color)

        if b.is_game_over():
            print(b.result())
            break
        print()


def main():
    init()
    while ask_new_game():
        user_color = ask_color()
        play_game(user_color)


if __name__ == "__main__":
    main()
