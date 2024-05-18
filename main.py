import json
import matplotlib.pyplot as plt
import numpy as np
import chess

from tests import init_position
from engine import ChessEngine
from eval import ChessEvaluator, ModelTypes

MODEL_PATH = './models/chess_cnn_model_50k.pth'
SF_PATH = "/usr/local/opt/stockfish"

engine_path = "D:/ChessData/stockfish/stockfish-windows-x86-64-avx2.exe"
model_path = r"C:\Users\tmlaz\Desktop\chesspy\models\chess_cnn_model_50k.pth"
model_path2 = r"C:\Users\tmlaz\Desktop\chesspy\models\chess_model_250k.h5"

optimizer_path = r"C:\Users\tmlaz\Desktop\chesspy\chess_cnn_optimizer_250k.pth"

def simulate_games(num_games=5):    

    max_moves = 256
    centipawn_loss_data_mini = np.zeros((num_games, max_moves))

    for game in range(num_games):
        engine = Engine(chess.STARTING_BOARD_FEN,
                 decisions=0,
                 model_type=0,
                 model_path=model_path,
                 sf_level=7,
                 sf_path=engine_path,
                 depth=1)

        print(f"Simulating game {game + 1} / {num_games}")
        centipawn_losses = engine.play_stockfish()
        for i in range(min(len(centipawn_losses), max_moves)):
            centipawn_loss_data_mini[game, i] = centipawn_losses[i]

    # Calculate the average centipawn loss per move
    average_centipawn_loss_per_move_mini = np.mean(centipawn_loss_data_mini, axis=0)

    # Save the data
    np.save('centipawn_loss_data_50k_mini.npy', centipawn_loss_data_mini)
    np.save('average_centipawn_loss_per_move_50k_mini.npy',
            average_centipawn_loss_per_move_mini)

    max_moves = 256
    centipawn_loss_data_nega = np.zeros((num_games, max_moves))

    for game in range(num_games):
        engine = Engine(chess.STARTING_BOARD_FEN,
                 decisions=1,
                 model_type=0,
                 model_path=model_path,
                 sf_level=7,
                 sf_path=engine_path,
                 depth=3)

        print(f"Simulating game {game + 1} / {num_games}")
        centipawn_losses = engine.play_stockfish()
        for i in range(min(len(centipawn_losses), max_moves)):
            centipawn_loss_data_nega[game, i] = centipawn_losses[i]

    # Calculate the average centipawn loss per move
    average_centipawn_loss_per_move_nega = np.mean(
        centipawn_loss_data_nega, axis=0)

    # Save the data
    np.save('centipawn_loss_data_50k_nega.npy', centipawn_loss_data_nega)
    np.save('average_centipawn_loss_per_move_50k_nega.npy',
            average_centipawn_loss_per_move_nega)
    
    # # Plot the average centipawn loss per move
    # plt.plot(range(1, 50), average_centipawn_loss_per_move_mini)
    # plt.plot(range(1, 50), average_centipawn_loss_per_move_nega)
    # plt.xlabel('Move Number')
    # plt.ylabel('Average Centipawn Loss')
    # plt.title('Average Centipawn Loss Per Move Over 25 Games')
    # plt.grid(True)
    # plt.show()


def main():
    simulate_games()
    average_centipawn_loss_per_move_mini = np.load('average_centipawn_loss_per_move_50k_mini.npy')
    average_centipawn_loss_per_move_nega = np.load('average_centipawn_loss_per_move_50k_nega.npy')

    # Print the shapes of the arrays to debug
    print("Shape of average_centipawn_loss_per_move_mini:",
          average_centipawn_loss_per_move_mini.shape)
    print("Shape of average_centipawn_loss_per_move_nega:",
          average_centipawn_loss_per_move_nega.shape)

    # Select the first 50 values
    new_mini = average_centipawn_loss_per_move_mini[:50]
    new_nega = average_centipawn_loss_per_move_nega[:50]

    # Plot the average centipawn loss per move
    plt.plot(range(1, 51), new_mini, label='Mini')
    plt.plot(range(1, 51), new_nega, label='Nega')
    plt.xlabel('Move Number')
    plt.ylabel('Average Centipawn Loss')
    plt.title('Average Centipawn Loss Per Move Over 25 Games')
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
