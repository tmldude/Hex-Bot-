from multiprocessing import Pool, cpu_count, freeze_support
import torch
import torch.nn as nn
import torch.optim as optim

import chess
import chess.pgn
import chess.engine

import pandas as pd

from hex_rep import Board
from evaluate import StockFishEvaluate

import chess
import chess.engine
import random
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np

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
    piece_dict = {
        'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,
        'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11
    }
    board = chess.Board(fen)
    tensor = np.zeros((12, 8, 8), dtype=np.float32)
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_type = piece_dict[piece.symbol()]
            row, col = divmod(square, 8)
            tensor[piece_type, row, col] = 1
    
    return tensor


def init_engine():
    global engine
    engine = chess.engine.SimpleEngine.popen_uci("D:/ChessData/stockfish/stockfish-windows-x86-64-avx2.exe")

def evaluate_position(board, time_limit=0.01):
    info = engine.analyse(board, chess.engine.Limit(time=time_limit))
    score = info['score'].relative.score(mate_score=100000)
    return score

def process_moves(moves):
    board = chess.Board()
    evaluations = []
    for move in moves:
        board.push(move)
        fen = board.fen()
        evaluation = evaluate_position(board)
        evaluations.append((fen, evaluation))

    print(moves)
    return evaluations

def parse_and_evaluate_pgn(pgn_path, output_path, max_games=10000):
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
            print(f"Collected {games_processed} games")
        
    with Pool(cpu_count(), initializer=init_engine) as pool:
        results = pool.map(process_moves, data)
    
    evaluations = [item for sublist in results for item in sublist]
    
    with open(output_path, 'w') as f:
        json.dump(evaluations, f)



class ChessCNN(nn.Module):
    def __init__(self):
        super(ChessCNN, self).__init__()
        self.conv1 = nn.Conv2d(12, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(128 * 8 * 8, 512)
        self.fc2 = nn.Linear(512, 1)
    
    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = x.view(-1, 128 * 8 * 8)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def train_chess_cnn(model, data_loader, epochs=10):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    for epoch in range(epochs):
        running_loss = 0.0

        for positions, evaluations in data_loader:
            optimizer.zero_grad()
            outputs = model(positions)
            loss = criterion(outputs, evaluations.unsqueeze(1))
            loss.backward()
            optimizer.step()
        
        avg_loss = running_loss / len(data_loader)
        print(f'Epoch {epoch+1}/{epochs}, Loss: {loss.item()}, Avrg_Loss: {avg_loss}')



if __name__ == "__main__":
    freeze_support()

    engine_path = "D:/ChessData/stockfish/stockfish-windows-x86-64-avx2.exe"
    # data = generate_dataset(engine_path, num_samples=1000)  

    pgn_path = "D:\ChessData\lichess_db_standard_rated_2024-02.pgn"
    output_path = r"C:\Users\tmlaz\Desktop\chesspy\chess_from_pgn.json"

    parse_and_evaluate_pgn(pgn_path, output_path, max_games=100)

    # json_file = "chess_dataset.json"
    # dataset = ChessDataset(json_file)
    # data_loader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)

    # model = ChessCNN()
    # train_chess_cnn(model, data_loader)

    # model_path = r"C:\Users\tmlaz\Desktop\chesspy\chess_cnn_model.pth"
    # # optimizer_path = r"C:\Users\tmlaz\Desktop\chesspy\chess_cnn_optimizer.pth"

    # torch.save(model.state_dict(), model_path)
    # # torch.save(optimizer.state_dict(), optimizer_path)





# engine_path = "D:\ChessData\stockfish\stockfish-windows-x86-64-avx2.exe"

# data = generate_dataset(engine_path, num_samples=100000)

# model = ChessCNN()
# data_loader = ...  # Create a DataLoader with your training data
# train_chess_cnn(model, data_loader)


# pgn = open(pgn_path)
# df = pd.DataFrame(columns=["board", "evaluation"])

# first_game = chess.pgn.read_game(pgn)
# second_game = chess.pgn.read_game(pgn)

# board = first_game.board()
# for move in first_game.mainline_moves():
#     eval = StockFishEvaluate.stockfish_evaluation(move)

#     data = {"board": board, "evaluation": eval}
#     df.loc[len(df)] = data




