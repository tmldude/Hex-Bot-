import chess
import torch
from cnn import ChessCNN
# from tensorflow.keras.models import load_model


def load_model(model_path):
    pass


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
                time=time_limit)).score.relative.score()
            move = sf.play(board, chess.engine.Limit(time=time_limit)).move

        return score, move

    def model(self, board):
        if self.model_type == MODEL_TYPES.get('torch'):
            return self._cnn_torch_score(board)
        else:
            return self._cnn_keras_score(board)

    def _cnn_torch_score(self, board):
        fen = board.fen()
        board_tensor = self.fen_to_matrix(fen)
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
