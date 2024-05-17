

import pandas as pd

import chess
import chess.engine

from hex_rep import Board
import random

class StockFishEvalBoard:
    '''Takes in a board to find the next move and evaluate the next best position using stockfish
    Also, holds functions to convert our BOARD into FEN and back into our BOARD
    '''

    ENGINE_PATH = "D:\ChessData\stockfish\stockfish-windows-x86-64-avx2.exe"

    def __init__(self, board):
        self.board = board

    def stockfish_evaluation(self, time_limit=0.01):
        board = self.board
        
        with chess.engine.SimpleEngine.popen_uci(StockFishEvalBoard.ENGINE_PATH) as engine:
            result = engine.analyse(board, chess.engine.Limit(time=time_limit))
            
        score = result['score']
        
        return score.relative.score()
    
    def stockfish_next_move(self, time_limit=0.01):
        with chess.engine.SimpleEngine.popen_uci(StockFishEvalBoard.ENGINE_PATH) as engine:
            result = engine.play(self.board, chess.engine.Limit(time=time_limit))
        return result.move

