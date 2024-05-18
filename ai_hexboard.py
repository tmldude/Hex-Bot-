

# import pandas as pd

import chess
import chess.engine

from board_hexrep import HexBoard
import random


class HexBoardAI:
    '''Takes in a board to find the next move and evaluate the next best position, using our AI'''

    def __init__(self, board):
        self.board = board

    def get_random_move(self):
        all_curr = self.board.generate_all_possible_next_board_states()

        if all_curr:
            chosen = random.choice(all_curr)
            return chosen
        return self.board

    def evaluate_board(self, board):
        return board.get_reward()

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0 or board.game_is_over:
            return self.evaluate_board(board)

        legal_moves = board.generate_all_possible_next_board_states()

        if is_maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                eval = self.minimax(move, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                eval = self.minimax(move, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def negamax(self, board, depth, alpha, beta, color):
        if depth == 0 or board.game_is_over:
            return color * self.evaluate_board(board)

        max_eval = float('-inf')
        legal_moves = board.generate_all_possible_next_board_states()

        for move in legal_moves:
            new_board = move
            eval = -self.negamax(new_board, depth - 1, -beta, -alpha, -color)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        return max_eval

    def get_best_move(self, max_depth, engine):
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        legal_moves = self.board.generate_all_possible_next_board_states()

        for move in legal_moves:
            if engine == 'mini':
                board_value = self.minimax(
                    move, max_depth - 1, alpha, beta, False)
            if engine == 'nega':
                board_value = self.negamax(
                    move, max_depth - 1, alpha, beta, False)
            else:
                board_value = self.get_random_move(
                    move, max_depth - 1, alpha, beta, False)

            if board_value > best_value:
                best_value = board_value
                best_move = move  # Store the best move as the new board state

        return best_move
