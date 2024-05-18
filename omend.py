import chess
from engine import ChessEngine, DecisionTypes
from eval import ChessEvaluator, ModelTypes

OPENING_LIMIT = 15
MIDGAME_LIMIT = 30


class OMEnd(ChessEngine):

    def __init__(self,
                 openings_path,
                 midgames_path,
                 endgames_path,
                 sf_path,
                 sf_level=7):
        self.opening_eval = ChessEvaluator(
            ModelTypes.KERAS, openings_path, sf_level, sf_path)

        self.midgame_eval = ChessEvaluator(
            ModelTypes.KERAS, midgames_path, sf_level, sf_path)

        self.endgame_eval = ChessEvaluator(
            ModelTypes.KERAS, endgames_path, sf_level, sf_path)

        super().__init__(chess.STARTING_BOARD_FEN, self.opening_eval,
                         dec_type=DecisionTypes.MINIMAX, depth=1)

    def eval_model(self, board, move_num):
        if 0 <= move_num < OPENING_LIMIT:
            self._evaluator = self.opening_eval
            return super().eval_model(board, move_num)

        elif OPENING_LIMIT <= move_num < MIDGAME_LIMIT:
            self._evaluator = self.midgame_eval
            return super().eval_model(board, move_num)

        else:
            self._evaluator = self.endgame_eval
            return super().eval_model(board, move_num)
