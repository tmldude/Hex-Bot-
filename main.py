import chess
from hex_rep import Board

from StockFishEvalHex import StockFishEvaluateHexPosition
from ChessAIHexBoard import ChessAIHexBoard

from EngineAI import EngineAI




def init_position() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    board.add_piece(1, board.WHITE | board.KNIGHT)
    board.add_piece(2, board.WHITE | board.BISHOP)
    board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    for i in range(8, 16):
        board.add_piece(i, board.WHITE | board.PAWN)
    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)

    return board

def castle_test() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    # board.add_piece(1, board.WHITE | board.KNIGHT)
    # board.add_piece(2, board.WHITE | board.BISHOP)
    # board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    # board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    for i in range(8, 16):
        if i != 12:
            board.add_piece(i, board.WHITE | board.PAWN)
    # board.add_piece( 17, board.BLACK | board.PAWN)
    # board.add_piece( 22, board.BLACK | board.PAWN)
    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)
    board.add_piece(36, board.BLACK | board.ROOK)


    return board

def move_out_of_block() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    # board.add_piece(1, board.WHITE | board.KNIGHT)
    # board.add_piece(2, board.WHITE | board.BISHOP)
    # board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    # board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(12, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    for i in range(8, 16):
        if i != 12:
            board.add_piece(i, board.WHITE | board.PAWN)
    # board.add_piece( 17, board.BLACK | board.PAWN)
    # board.add_piece( 22, board.BLACK | board.PAWN)
    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)
    board.add_piece(36, board.BLACK | board.ROOK)


    return board

def test_promo() -> Board:
    board = Board()
    board.board = 0x0
    # board.add_piece(0, board.WHITE | board.ROOK)
    # board.add_piece(1, board.WHITE | board.KNIGHT)
    # board.add_piece(2, board.WHITE | board.BISHOP)
    # board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    # board.add_piece(5, board.WHITE | board.BISHOP)
    # board.add_piece(6, board.WHITE | board.KNIGHT)
    # board.add_piece(7, board.WHITE | board.ROOK)
    for i in range(8, 9):
        if i != 12:
            board.add_piece(i, board.WHITE | board.PAWN)
    # board.add_piece( 17, board.BLACK | board.PAWN)
    # board.add_piece( 22, board.BLACK | board.PAWN)
    # for i in range(48, 56):
    #     board.add_piece(i, board.BLACK | board.PAWN)
    # board.add_piece(56, board.BLACK | board.ROOK)
    # board.add_piece(57, board.BLACK | board.KNIGHT)
    # board.add_piece(58, board.BLACK | board.BISHOP)
    # board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    # board.add_piece(61, board.BLACK | board.BISHOP)
    # board.add_piece(62, board.BLACK | board.KNIGHT)
    # board.add_piece(63, board.BLACK | board.ROOK)
    # board.add_piece(36, board.BLACK | board.ROOK)

    board.add_piece(50, board.WHITE | board.PAWN)
    # board.add_piece(0, board.WHITE | board.ROOK)

    # board.add_piece(7, board.WHITE | board.ROOK)




    return board

def test_position() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    board.add_piece(1, board.WHITE | board.KNIGHT)
    # board.add_piece( 2, board.WHITE | board.BISHOP)
    board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    # board.add_piece( 7, board.WHITE | board.ROOK)
    # board.add_piece(32, board.WHITE | board.PAWN)
    board.add_piece(39, board.WHITE | board.PAWN)
    board.add_piece(35, board.WHITE | board.BISHOP)

    for i in range(9, 13):
        board.add_piece(i, board.WHITE | board.PAWN)
    # for i in range(48, 56):
    #     board.add_piece( i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    # board.add_piece( 60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)

    # board.add_piece( 33, board.WHITE | board.KNIGHT)
    board.add_piece(44, board.WHITE | board.ROOK)
    board.add_piece(47, board.BLACK | board.ROOK)
    board.add_piece(40, board.WHITE | board.PAWN)
    board.add_piece(23, board.BLACK | board.PAWN)

    board.color_to_move = 0x0
    board.last_end_square = 0x0
    board.castle_states = 0x0
    board.can_en_passant = 0x0
    return board

def test_sliding() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    board.add_piece(1, board.WHITE | board.KNIGHT)
    board.add_piece(2, board.WHITE | board.BISHOP)
    board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    board.add_piece(32, board.WHITE | board.PAWN)
    board.add_piece(39, board.WHITE | board.PAWN)

    # for i in range(8, 16):
    #     board.add_piece( i, board.WHITE | board.PAWN)
    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)

    # board.add_piece( 33, board.WHITE | board.KNIGHT)
    board.add_piece(36, board.WHITE | board.ROOK)

    board.color_to_move = 0x0
    board.last_end_square = 0x0
    board.castle_states = 0x0
    board.can_en_passant = 0x0

    return board

def test_en_passant() -> Board:
    board = Board(en_passant_square_fen=41)
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    board.add_piece(1, board.WHITE | board.KNIGHT)
    board.add_piece(2, board.WHITE | board.BISHOP)
    board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    # for i in range(8, 16):
    #     board.add_piece( i, board.WHITE | board.PAWN)
    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)

    board.add_piece(33, board.BLACK | board.PAWN)
    board.add_piece(32, board.WHITE | board.PAWN)

    board.color_to_move = 0x0
    board.last_end_square = 33
    board.castle_states = 0x0
    board.can_en_passant = 0x1
    # board.en_passant_square_fen = 41

    return board

def test_king() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    board.add_piece(1, board.WHITE | board.KNIGHT)
    board.add_piece(2, board.WHITE | board.BISHOP)
    board.add_piece(3, board.WHITE | board.QUEEN)
    # board.add_piece( 4, board.WHITE | board.KING)
    board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    for i in range(8, 16):
        board.add_piece(i, board.WHITE | board.PAWN)
    # board.add_piece( 17, board.BLACK | board.PAWN)
    # board.add_piece( 22, board.BLACK | board.PAWN)
    board.add_piece(32, board.WHITE | board.KING)

    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)
    board.add_piece(17, board.BLACK | board.ROOK)

    return board

def test_draw() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(59, board.BLACK | board.ROOK)
    board.add_piece(61, board.BLACK | board.ROOK)
    board.add_piece(47, board.BLACK | board.ROOK)
    board.add_piece(24, board.BLACK | board.ROOK)
    board.add_piece(52, board.BLACK | board.ROOK)


    board.add_piece(36, board.WHITE | board.KING)
    board.add_piece(60, board.BLACK | board.KING)



    return board




def play_stockfish_ChessAIHexBoard():
    board = Board(init_position().board, Board.BLACK)
    board.print_board_hex()

    move = ChessAIHexBoard(board).get_best_move(3, 'nega')
    move.print_board_hex()
    
    max_iter = 256
    i = 0
    while not move.game_is_over and i < max_iter:
        stock_fish_eval = StockFishEvaluateHexPosition(move)
        move = stock_fish_eval.stockfish_next_move()
        move = stock_fish_eval.fen_to_board(move)
        move.print_board_hex()
        
        move = ChessAIHexBoard(move).get_best_move(3, 'nega')
        move.print_board_hex()


        i += 1



import numpy as np
import matplotlib.pyplot as plt


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
    np.save('average_centipawn_loss_per_move.npy', average_centipawn_loss_per_move)
    
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



    simulate_games()
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




import numpy as np
import random


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
        return Board(init_position(), Board.BLACK)
    
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
        white_material = sum(self.PIECE_VALUES[piece] for piece in self.get_pieces(self.WHITE))
        black_material = sum(self.PIECE_VALUES[piece] for piece in self.get_pieces(self.BLACK))
        return white_material - black_material


if __name__ == "__main__":
    main()
    


# 0xabc0dcba00000000a00200011000000000000000900000000001111043465032
# 0xabc0dcba00000000a00200011000000000000000900000000001111043465032