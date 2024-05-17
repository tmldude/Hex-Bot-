from multiprocessing import Pool, cpu_count, freeze_support

import chess
import chess.pgn
import chess.engine

# import pandas as pd
import numpy as np

import random
import json
from torch.utils.data import Dataset
import torch


'''These 2 functions generate a random dataset, slow moving'''


def generate_position(engine, depth=20):
    board = chess.Board()
    moves = list(board.legal_moves)
    for _ in range(random.randint(1, 30)):
        move = random.choice(moves)
        board.push(move)
        moves = list(board.legal_moves)
        if board.is_game_over():
            break
    info = engine.analyse(board, chess.engine.Limit(depth=depth))
    evaluation = info["score"].relative.score(mate_score=100000)
    return board.fen(), evaluation


def generate_dataset(engine_path, num_samples=1000, depth=20):
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    data = []
    for _ in range(num_samples):
        fen, evaluation = generate_position(engine, depth)
        data.append((fen, evaluation))
    engine.close()

    with open("chess_dataset.json", "w") as f:
        json.dump(data, f)

    return data


class ChessDataset(Dataset):
    def __init__(self, json_file):
        with open(json_file, "r") as f:
            self.data = json.load(f)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        fen, evaluation = self.data[idx]
        tensor = fen_to_tensor(fen)
        evaluation = np.array(evaluation, dtype=np.float32)
        return tensor, evaluation


def fen_to_tensor(fen):
    piece_list = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
    piece_dict = {piece: i for i, piece in enumerate(piece_list)}

    board = chess.Board(fen)
    tensor = np.zeros((12, 8, 8), dtype=np.float32)

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_type = piece_dict[piece.symbol()]
            row, col = divmod(square, 8)
            tensor[piece_type, row, col] = 1

    return torch.tensor(tensor, dtype=torch.float32)


def init_engine():
    global engine
    engine = chess.engine.SimpleEngine.popen_uci(
        "D:/ChessData/stockfish/stockfish-windows-x86-64-avx2.exe")


def evaluate_position(board, time_limit=0.01):
    info = engine.analyse(board, chess.engine.Limit(time=time_limit))
    score = info['score'].relative.score(mate_score=1000)
    return score


def process_moves(moves):
    board = chess.Board()
    opening = []
    middlegame = []
    endgame = []
    i = 0
    for move in moves:
        board.push(move)
        fen = board.fen()
        evaluation = evaluate_position(board)

        if i < 15:
            opening.append((fen, evaluation))
        elif i < 30:
            middlegame.append((fen, evaluation))
        else:
            endgame.append((fen, evaluation))

        i = 0

    return opening, middlegame, endgame


def parse_and_evaluate_pgn(pgn_path, max_games=10000):
    with open(pgn_path, 'r') as pgn_file:
        games_processed = 0
        data = []

        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None or games_processed >= max_games:
                break

            moves = list(game.mainline_moves())
            data.append(moves)
            games_processed += 1

            if games_processed % 1000 == 0:
                print(f"Collected {games_processed} games")

    with Pool(cpu_count(), initializer=init_engine) as pool:
        opening, middlegame, endgame = pool.map(process_moves, data)

    open_evaluations = [item for sublist in opening for item in sublist]
    middle_evaluations = [item for sublist in middlegame for item in sublist]
    end_evaluations = [item for sublist in endgame for item in sublist]

    print(len(open_evaluations), len(middle_evaluations), len(end_evaluations))

    with open('chess_dataset_open.json', 'w') as f:
        json.dump(open_evaluations, f)

    with open('chess_dataset_middle.json', 'w') as f:
        json.dump(middle_evaluations, f)

    with open('chess_dataset_end.json', 'w') as f:
        json.dump(end_evaluations, f)


if __name__ == "__main__":
    freeze_support()

    engine_path = "D:/ChessData/stockfish/stockfish-windows-x86-64-avx2.exe"
    pgn_path = "D:\ChessData\lichess_db_standard_rated_2024-02.pgn"
    # output_path = r"C:\Users\tmlaz\Desktop\chesspy\chess_from_pgn_250000.json"

    parse_and_evaluate_pgn(pgn_path, max_games=5)
