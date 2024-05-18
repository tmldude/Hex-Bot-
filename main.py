import random
import matplotlib.pyplot as plt
import numpy as np
import chess

from board_hexrep import HexBoard
from test_board import init_position

from sf_eval_hexpos import StockFishEvaluateHexPosition
from ai_hexboard import HexBoardAI
from ai_engine import EngineAI


def play_stockfish_ChessAIHexBoard():
    board = HexBoard(init_position().board, HexBoard.BLACK)
    board.print_board_hex()

    move = HexBoardAI(board).get_best_move(3, 'nega')
    move.print_board_hex()

    max_iter = 256
    i = 0
    while not move.game_is_over and i < max_iter:
        stock_fish_eval = StockFishEvaluateHexPosition(move)
        move = stock_fish_eval.stockfish_next_move()
        move = stock_fish_eval.fen_to_board(move)
        move.print_board_hex()

        move = HexBoardAI(move).get_best_move(3, 'nega')
        move.print_board_hex()

        i += 1


def simulate_games(num_games=5):
    max_moves = 256
    centipawn_loss_data = np.zeros((num_games, max_moves))

    for game in range(num_games):
        engine = EngineAI(chess.STARTING_BOARD_FEN)

        print(f"Simulating game {game + 1} / {num_games}")
        centipawn_losses = engine.play_stock_fish()
        for i in range(min(len(centipawn_losses), max_moves)):
            centipawn_loss_data[game, i] = centipawn_losses[i]

    # Calculate the average centipawn loss per move
    average_centipawn_loss_per_move = np.mean(centipawn_loss_data, axis=0)

    # Save the data
    np.save('centipawn_loss_data.npy', centipawn_loss_data)
    np.save('average_centipawn_loss_per_move.npy',
            average_centipawn_loss_per_move)

    # Plot the average centipawn loss per move
    plt.plot(range(1, max_moves + 1), average_centipawn_loss_per_move)
    plt.xlabel('Move Number')
    plt.ylabel('Average Centipawn Loss')
    plt.title('Average Centipawn Loss Per Move Over 1000 Games')
    plt.grid(True)
    plt.show()


def main():
    # engine = EngineAI(chess.STARTING_BOARD_FEN)
    # print(engine.get_best_move(5, 'nega'))
    # print(engine.get_best_move(5, 'mini'))
    engine = EngineAI(chess.STARTING_BOARD_FEN)

    engine.play_stock_fish()
    # simulate_games()
    # board2 = Board(test_en_passant().board, Board.BLACK, en_passant_square_fen=41)
    # board2.print_board_hex()

    # move1 = EvaluateBoard(board2).getRandomMove()
    # move1.print_board_hex()

    # stock_fish_eval = StockFishEvaluateHexPosition(move1)
    # move2 = stock_fish_eval.stockfish_next_move()
    # move2 = stock_fish_eval.fen_to_board(move2)
    # move2.print_board_hex()

    # move3 = EvaluateBoard(move2).getRandomMove()
    # move3.print_board_hex()

    # board2.print_board_hex()

    # print(stock_fish_eval.fen)
    # print(stock_fish_eval.score)
    # print(stock_fish_eval.interpretted_score)
    # stock_fish_eval.fen_to_hex(stock_fish_eval.fen)

    # print(hex(board.board))
    # print(hex_to_board(hex(board.board)))
    # board.print_board_hex()

    # # Example hex string
    # hex_string = "0xa b c d e c b a9 9 9 9 9 9 9 90 0 0 0 0 0 0 00 0 0 0 0 0 0 00 0 0 0 0 0 0 0 0 0 0 0 0 0 0 01 1 1 1 1 1 1 12 3 4 5 6 4 3 2"

    # # Convert the hex string to a board representation
    # board = hex_to_board(hex_string)

    # # Example parameters
    # active_color = 'white' if board.color_to_move == Board.BLACK else 'black'
    # can_castle_kingside = {'white': not board.castle_states['white_king_moved'] and not board.castle_states['KS_rook_w_moved'], 'black': not board.castle_states['black_king_moved'] and not board.castle_states['KS_rook_b_moved']}
    # can_castle_queenside = {'white': not board.castle_states['white_king_moved'] and not board.castle_states['QS_rook_w_moved'], 'black': not board.castle_states['black_king_moved'] and not board.castle_states['QS_rook_b_moved']}
    # en_passant = "-" if not board.en_passant_square_fen else square_number_to_fen(board.en_passant_square_fen)
    # halfmove_clock = 0
    # fullmove_number = 1

    # # # Convert the board to FEN
    # fen = convert_to_fen(hex_to_board(hex(board.board)), active_color, can_castle_kingside, can_castle_queenside, en_passant, halfmove_clock, fullmove_number)
    # print(fen)
    # print("======================")

    # board2 = Board(test_en_passant().board, Board.BLACK, en_passant_square_fen=41)
    # board2.print_board_hex(board2.board)
    # print(hex_to_board(hex(board2.board)))

    # active_color = 'white' if board2.color_to_move == Board.BLACK else 'black'
    # can_castle_kingside = {'white': not board2.castle_states['white_king_moved'] and not board2.castle_states['KS_rook_w_moved'], 'black': not board2.castle_states['black_king_moved'] and not board2.castle_states['KS_rook_b_moved']}
    # can_castle_queenside = {'white': not board2.castle_states['white_king_moved'] and not board2.castle_states['QS_rook_w_moved'], 'black': not board2.castle_states['black_king_moved'] and not board2.castle_states['QS_rook_b_moved']}
    # en_passant = "-" if not board2.en_passant_square_fen else square_number_to_fen(board2.en_passant_square_fen)
    # halfmove_clock = 0
    # fullmove_number = 1

    # print(board2.en_passant_square_fen)

    # fen2 = convert_to_fen(hex_to_board(hex(board2.board)), active_color, can_castle_kingside, can_castle_queenside, en_passant, halfmove_clock, fullmove_number)

    # print(fen2)

    # engine_path = "D:\ChessData\stockfish\stockfish-windows-x86-64-avx2.exe"

    # score = stockfish_evaluation(engine_path, fen)
    # print(score)

    # score = stockfish_evaluation(engine_path, fen2)
    # print(score)


def play_game(board):
    legal_moves = board.generate_all_possible_next_board_states()

    best_move = None
    best_score = -9999

    # for move in legal_moves:

    # gameover = False
    current_state = board.generate_all_possible_next_board_states()
    # while i < max_moves and not gameover:
    #     board = random.choice(current_state)
    #     # chosen.print_board_hex()
    #     # chosen.print_board_hex(chosen.attack_board)

    #     current_state = board.generate_all_possible_next_board_states()
    #     i += 1

    # board.print_board_hex()


class ChessEnv:
    PIECE_VALUES = {
        'P': 1,  # Pawn
        'N': 3,  # Knight
        'B': 3,  # Bishop
        'R': 5,  # Rook
        'Q': 9,  # Queen
        'K': 0   # King (usually not counted for intermediate rewards)
    }

    def __init__(self, ):
        self.board = init_position()
        self.next_states = self.board.generate_all_possible_next_board_states()

    def init_board(self):
        return HexBoard(init_position(), HexBoard.BLACK)

    def next_states(self):
        return self.board.generate_all_possible_next_board_states()

    def apply_move(self):
        return

    def get_reward(self):
        if self.is_game_over():
            if self.is_checkmate():
                return 1 if self.turn == self.WHITE else -1
            elif self.is_draw():
                return 0
        return self.material_balance()

    def material_balance(self):
        white_material = sum(self.PIECE_VALUES[piece]
                             for piece in self.get_pieces(self.WHITE))
        black_material = sum(self.PIECE_VALUES[piece]
                             for piece in self.get_pieces(self.BLACK))
        return white_material - black_material


if __name__ == "__main__":
    main()


# 0xabc0dcba00000000a00200011000000000000000900000000001111043465032
# 0xabc0dcba00000000a00200011000000000000000900000000001111043465032
