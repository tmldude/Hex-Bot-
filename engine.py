from enum import Enum
import random
import chess
import chess.engine
import numpy as np
import torch
import torch.nn as nn
from bitboard import Bitboard
from eval import ChessEvaluator, ModelTypes
from cnn import ChessCNN
from archive.mcts import MCTS


class DecisionTypes(Enum):
    MINIMAX = 0
    NEGAMAX = 1
    MCTS = 2


class ChessEngine:

    '''Takes in a board to find the next move and evaluate the next best position, using our AI'''

    def __init__(self,
                 fen,
                 evaluator,
                 dec_type=DecisionTypes.MINIMAX,
                 depth=3):
        self.board = chess.Board(fen)
        self.dec_type = dec_type  # 'mini' or 'nega'
        self._evaluator = evaluator
        self.depth = depth

    def eval_stockfish(self, board):
        return self._evaluator.stockfish(board)

    def eval_model(self, board, move_num):
        return self._evaluator.model_score(board)

    def play_stockfish(self):
        i = 0
        max_iter = 256

        board = self.board
        stockfish_first = random.randint(0, 1)
        print('stockfish White - Conv Net 50k Black' if stockfish_first else 'Conv Net 50k White - stockfish Black')

        centipawn_losses = []

        while not board.is_game_over() and i < max_iter:
            self.print_board_fancy(board)

            if stockfish_first:
                score, move = self.eval_stockfish(board)
                # print(f"initial_score_stock: {initial_score}")
                board.push(move)
            else:
                score = self.eval_model(board, i)
                # print(f"initial_score_CNN: {initial_score}")
                move = self.get_best_move(self.depth, i)
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

    def get_best_move(self, max_depth, move_num):
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        legal_moves = list(self.board.legal_moves)
        # Determine the current player's color
        color = 1 if self.board.turn == chess.WHITE else -1

        for move in legal_moves:
            self.board.push(move)
            if self.dec_type == DecisionTypes.MINIMAX:
                board_value = self._decide_minimax(
                    self.board, max_depth - 1, alpha, beta, False, color, move_num)
            elif self.dec_type == DecisionTypes.NEGAMAX:
                board_value = self._decide_negamax(
                    self.board, max_depth - 1, alpha, beta, color, move_num)
            else:
                board_value = self._decide_negamax(
                    self.board, max_depth - 1, alpha, beta, color, move_num)
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

    def _decide_minimax(self, board, depth, alpha, beta, is_maximizing, color, move_num):
        if depth == 0 or board.is_game_over():
            return color * self.eval_model(board, move_num)

        legal_moves = list(board.legal_moves)

        if is_maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                board.push(move)
                eval = self._decide_minimax(board, depth - 1, alpha,
                                            beta, False, -color, move_num+1)
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
                    board, depth - 1, alpha, beta, True, -color, move_num+1)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def _decide_negamax(self, board, depth, alpha, beta, color, move_num):
        if depth == 0 or board.is_game_over():
            return color * self.eval_model(board, move_num)

        max_eval = float('-inf')
        legal_moves = list(board.legal_moves)

        for move in legal_moves:
            board.push(move)
            eval = -self._decide_negamax(board,
                                         depth - 1, -beta, -alpha, -color, move_num+1)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break

        return max_eval

    # UTILS
    def print_board_fancy(self, board=None):
        if board is None:
            board = self.board

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
