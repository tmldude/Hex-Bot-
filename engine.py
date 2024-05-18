import random
import chess
import chess.engine
import numpy as np
import torch
import torch.nn as nn
from bitboard import Bitboard
from eval import ChessEvaluator, MODEL_TYPES

MODEL_PATH = './models/chess_cnn_model_50k.pth'
SF_PATH = "/usr/local/opt/stockfish"

DECISIONS = {'minimax': 0,
             'negamax': 1}


class Engine:

    '''Takes in a board to find the next move and evaluate the next best position, using our AI'''

    def __init__(self,
                 board,
                 decisions=DECISIONS.get('minimax'),
                 model_type=MODEL_TYPES.get('torch'),
                 model_path=MODEL_PATH,
                 sf_level=7,
                 sf_path=SF_PATH):
        self.board = chess.Board(board)
        self.decisions = decisions  # 'mini' or 'nega'

        # self.model = load_model('./models/chess_model_250k.h5')
        self.model = ChessCNN()
        state_dict = torch.load('./models/chess_cnn_model_50k.pth')
        self.model.load_state_dict(state_dict)
        self.model.eval()

    def play_stock_fish(self):
        i = 0
        max_iter = 256

        board = self.board
        stockfish_first = random.randint(0, 1)
        print('stockfish White - Conv Net 50k Black' if stockfish_first else 'Conv Net 50k White - stockfish Black')

        centipawn_losses = []

        while not board.is_game_over() and i < max_iter:
            self.print_board_fancy(board)

            if stockfish_first:
                score, move = self.eval.stockfish(board)
                # print(f"initial_score_stock: {initial_score}")
                board.push(move)
            else:
                score = self.eval.model(board)
                # print(f"initial_score_CNN: {initial_score}")
                move = self.get_best_move(2)
                board.push(move)

            stockfish_first = 0 if stockfish_first else 1

            if score:
                centipawn_loss = abs(score)
                centipawn_losses.append(centipawn_loss)
                # print(f"Centipawn loss: {centipawn_loss}")
            else:
                centipawn_losses.append(1000)

            i += 1

        return centipawn_losses

    # GET NEXT MOVE

    def get_best_move(self, max_depth):
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        legal_moves = list(self.board.legal_moves)
        # Determine the current player's color
        color = 1 if self.board.turn == chess.WHITE else -1

        for move in legal_moves:
            self.board.push(move)
            if self.decisions == DECISIONS.get('minimax'):
                board_value = self._decide_minimax(
                    self.board, max_depth - 1, alpha, beta, False, color)
            elif self.decisions == DECISIONS.get('negamax'):
                board_value = self._decide_negamax(
                    self.board, max_depth - 1, alpha, beta, color)
            else:
                print('fuck')
                board_value = self._decide_negamax(
                    self.board, max_depth - 1, alpha, beta, color)
            self.board.pop()

            if board_value > best_value:
                best_value = board_value
                best_move = move

        return best_move

    def get_random_move(self):
        legal_moves = list(self.board.legal_moves)

        if legal_moves:
            chosen = random.choice(legal_moves)
            return chosen
        return None

    # DECISIONS

    def _decide_minimax(self, board, depth, alpha, beta, is_maximizing, color):
        if depth == 0 or board.is_game_over():
            return color * self.eval.model(board)

        legal_moves = list(board.legal_moves)

        if is_maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval = self._decide_minimax(board, depth - 1, alpha,
                                            beta, False, -color)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self._decide_minimax(
                    board, depth - 1, alpha, beta, True, -color)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def _decide_negamax(self, board, depth, alpha, beta, color):
        if depth == 0 or board.is_game_over():
            return color * self.eval.model(board)

        max_eval = float('-inf')
        legal_moves = list(board.legal_moves)

        for move in legal_moves:
            board.push(move)
            eval = -self._decide_negamax(board,
                                         depth - 1, -beta, -alpha, -color)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break

        return max_eval

    # UTILS

    @staticmethod
    def fen_to_tensor(fen):
        piece_list = ['P', 'N', 'B', 'R', 'Q',
                      'K', 'p', 'n', 'b', 'r', 'q', 'k']
        piece_dict = {piece: i for i, piece in enumerate(piece_list)}

        board = chess.Board(fen)
        tensor = np.zeros((12, 8, 8), dtype=np.float32)

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                piece_type = piece_dict[piece.symbol()]
                row, col = divmod(square, 8)
                tensor[piece_type, row, col] = 1

        return torch.tensor(tensor, dtype=torch.float32).unsqueeze(0)

    @staticmethod
    def fen_to_matrix(fen):
        bitboard = Bitboard(fen)
        return bitboard.generate_board_matrix()

    def print_board_fancy(self, board=None):
        if board is None:
            board = self.board

    # def evaluate_board_CNN(self, board):
    #     fen = board.fen()
    #     board_tensor = self.fen_to_matrix(fen)
    #     # print(f"Board Tensor: {board_tensor}")
    #     with torch.no_grad():
    #         output = self.model(board_tensor)
    #     # print(f"Model Output: {output}")
    #     return output.item()

    def evaluate_board_CNN(self, board):
        fen = board.fen()
        matrix = self.fen_to_matrix(fen)
        output = self.model.predict(matrix, verbose = 0)
    
        # print(output[0][0])
        return output[0][0]
    
    def get_piece_value(self, piece):
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        return values[piece.piece_type] if piece.color == chess.WHITE else -values[piece.piece_type]

    def get_random_move(self):
        legal_moves = list(self.board.legal_moves)

        if legal_moves:
            chosen = random.choice(legal_moves)
            return chosen
        return None

    def evaluate_board_CNN_torch(self, board):
        fen = board.fen()
        board_tensor = self.fen_to_tensor(fen)
        # print(f"Board Tensor: {board_tensor}")
        with torch.no_grad():
            output = self.model(board_tensor)
        # print(f"Model Output: {output}")
        return output.item()

    def evaluate_board_CNN(self, board):
        fen = board.fen()
        matrix = self.fen_to_matrix(fen)
        output = self.model.predict(matrix, verbose=0)

        # print(output[0][0])
        return output[0][0]

    def minimax(self, board, depth, alpha, beta, is_maximizing, color):
        if depth == 0 or board.is_game_over():
            return color * self.evaluate_board_CNN_torch(board)

        legal_moves = list(board.legal_moves)

        if is_maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha,
                                        beta, False, -color)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.minimax(
                    board, depth - 1, alpha, beta, True, -color)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def negamax(self, board, depth, alpha, beta, color):
        if depth == 0 or board.is_game_over():
            return color * self.evaluate_board_CNN_torch(board)

        max_eval = float('-inf')
        legal_moves = list(board.legal_moves)

        for move in legal_moves:
            board.push(move)
            eval = -self.negamax(board, depth - 1, -beta, -alpha, -color)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break

        return max_eval

    def get_best_move(self, max_depth, engine=None):
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        legal_moves = list(self.board.legal_moves)
        color = 1 if self.board.turn == chess.WHITE else -1 # Determine the current player's color

        for move in legal_moves:
            self.board.push(move)
            if engine == 'mini':
                board_value = self.minimax(
                    self.board, max_depth - 1, alpha, beta, False, color)
            elif engine == 'nega':
                board_value = self.negamax(
                    self.board, max_depth - 1, alpha, beta, color)
            else:
                print('fuck')
                board_value = self.negamax(
                    self.board, max_depth - 1, alpha, beta, color)
            self.board.pop()

            if board_value > best_value:
                best_value = board_value
                best_move = move

        return best_move

    def print_board_fancy(self, board):
        unicode_pieces = {
            'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
            'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
        }
        print("  a b c d e f g h")
        print(" +-----------------+")
        for rank in range(8, 0, -1):
            print(f"{rank}|", end=" ")
            for file in range(1, 9):
                piece = board.piece_at(chess.square(file - 1, rank - 1))
                if piece:
                    print(unicode_pieces[piece.symbol()], end=" ")
                else:
                    print(".", end=" ")
            print(f"|{rank}")
        print(" +-----------------+")
        print("  a b c d e f g h")

    def play_stock_fish(self):
        max_iter = 256
        i = 0

        board = self.board
        who_goes_first = random.randint(0, 1)
        print('stockfish White - Conv Net 50k Black' if who_goes_first else 'Conv Net 50k White - stockfish Black')

        centipawn_losses = []

        while not board.is_game_over() and i < max_iter:
            self.print_board_fancy(board)

            if who_goes_first:
                stock = StockFishEvalBoard(board)
                initial_score = stock.stockfish_evaluation()

                # print(f"initial_score_stock: {initial_score}")
                move = stock.stockfish_next_move()
                board.push(move)
            else:
                initial_score = self.evaluate_board_CNN_torch(board)

                # print(f"initial_score_CNN: {initial_score}")
                move = self.get_best_move(4, 'nega')
                board.push(move)

            who_goes_first = 0 if who_goes_first else 1

            if initial_score:
                centipawn_loss = abs(initial_score)
                centipawn_losses.append(centipawn_loss)
                # print(f"Centipawn loss: {centipawn_loss}")
            else:
                centipawn_losses.append(1000)

            i += 1

        return centipawn_losses
