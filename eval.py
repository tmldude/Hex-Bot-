import chess
import torch
from cnn import ChessCNN
from bitboard import Bitboard
import numpy as np

import tensorflow as tf
from tensorflow.keras.models import load_model


MODEL_TYPES = {'torch': 0,
               'keras': 1}


class ChessEvaluator:
    '''
    Takes in a board to find the next move and evaluate the next best position using stockfish
    Also, holds functions to convert our BOARD into FEN and back into our BOARD
    '''

    def __init__(self,
                 model_type,
                 model_path,
                 sf_level,
                 sf_path):
        self.model_type = model_type
        self.model_path = model_path

        if self.model_type == MODEL_TYPES.get('torch'):
            self.model = ChessCNN()
            state_dict = torch.load(model_path, map_location=torch.device('cpu'))
            self.model.load_state_dict(state_dict)
            self.model.eval()
        else:  # KERAS
            self.model = load_model(model_path)

        # STOCKFISH

        self.sf_level = sf_level
        self.sf_path = sf_path

        self.sf_engine = chess.engine.SimpleEngine.popen_uci(self.sf_path)
        self.sf_engine.configure({"Skill Level": self.sf_level})

    def stockfish(self, board, time_limit=0.01):
        with self.sf_engine.popen_uci(self.sf_path) as sf:
            score = sf.analyse(board, chess.engine.Limit(
                time=time_limit))['score'].relative.score()

            move = sf.play(board, chess.engine.Limit(time=time_limit)).move

        return score, move

    def model_score(self, board):
        if self.model_type == MODEL_TYPES.get('torch'):
            return self._cnn_torch_score(board)
        else:
            return self._cnn_keras_score(board)

    def _cnn_torch_score(self, board):
        fen = board.fen()
        board_tensor = self.fen_to_tensor(fen)
        # print(f"Board Tensor: {board_tensor}")
        with torch.no_grad():
            output = self.model(board_tensor)
        # print(f"Model Output: {output}")
        return output.item()

    def _cnn_keras_score(self, board):
        fen = board.fen()
        matrix = self.fen_to_matrix(fen)
        output = self.model.predict(matrix, verbose=0)

        # print(output[0][0])
        return output[0][0]

    @staticmethod
    def count_pieces(board):
        return sum([ChessEvaluator.get_piece_value(piece) for piece in board.piece_map().values()])

    @staticmethod
    def get_piece_value(piece):
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }
        return values[piece.piece_type] if piece.color == chess.WHITE else -values[piece.piece_type]
    
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
        piece_map = {
            'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,
            'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11
        }
        board = chess.Board(fen)
        matrix = np.zeros((8, 8, 12), dtype=int)
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                row, col = divmod(square, 8)
                matrix[row, col, piece_map[piece.symbol()]] = 1
        return np.expand_dims(matrix, axis=0)


    @staticmethod
    def fen_to_matrix_OMEnd(fen):
        bitboard = Bitboard(fen)
        return bitboard.generate_board_matrix()
