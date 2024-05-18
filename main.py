import matplotlib.pyplot as plt
import numpy as np

from models.engine import ChessEngine
from eval import ChessEvaluator, ModelTypes
from omend import OMEnd

MODEL_PATH = './models/chess_cnn_model_50k.pth'
# SF_PATH = "/usr/games/stockfish"
SF_PATH = "D:/ChessData/stockfish/stockfish-windows-x86-64-avx2.exe"

engine_path = "D:/ChessData/stockfish/stockfish-windows-x86-64-avx2.exe"
model_path = r"\models\chess_cnn_model_50k.pth"
model_path2 = r"\models\chess_model_250k.h5"

open_path = r'C:\Users\tmlaz\Desktop\chesspy\models\chess_model_opening.h5'
mid_path = r'C:\Users\tmlaz\Desktop\chesspy\models\chess_model_mid.h5'
end_path = r'C:\Users\tmlaz\Desktop\chesspy\models\chess_model_end.h5'

def simulate_games(num_games=1):    

    max_moves = 256
    centipawn_loss_data_mini = np.zeros((num_games, max_moves))

    game_num = 0
    for game in range(num_games):
        engine = OMEnd(open_path, mid_path, end_path, model_depth=1, sf_level=2,
                 sf_path=SF_PATH)

        print(f"Simulating game {game + 1} / {num_games}")
        centipawn_losses = engine.play_stockfish()
        for i in range(min(len(centipawn_losses), max_moves)):
            centipawn_loss_data_mini[game, i] = centipawn_losses[i]

             # Save the data
        average_centipawn_loss_per_move_mini = np.mean(centipawn_loss_data_mini, axis=0)
        np.save('centipawn_loss_data_omend_mini.npy', centipawn_loss_data_mini)
        np.save('average_centipawn_loss_per_move_omend_mini.npy',
                average_centipawn_loss_per_move_mini)

    # Calculate the average centipawn loss per move
    average_centipawn_loss_per_move_mini = np.mean(centipawn_loss_data_mini, axis=0)

   
def plot():
    average_centipawn_loss_per_move_mini = np.load('average_centipawn_loss_per_move_omend_mini.npy')
    average_centipawn_loss_per_move_nega = np.load('average_centipawn_loss_per_move_omend_nega.npy')
    average_centipawn_loss_per_move_250k = np.load('data/average_centipawn_loss_per_move_250k_mini.npy')
    average_centipawn_loss_per_move_50k = np.load('data/average_centipawn_loss_per_move_50k_mini.npy')


    print("Shape of average_centipawn_loss_per_move_mini:",
          average_centipawn_loss_per_move_mini.shape)
    print("Shape of average_centipawn_loss_per_move_nega:",
          average_centipawn_loss_per_move_nega.shape)

    new_mini = average_centipawn_loss_per_move_mini[:50]
    new_nega = average_centipawn_loss_per_move_nega[:50]
    fifty = average_centipawn_loss_per_move_250k[:50]
    twofifty = average_centipawn_loss_per_move_50k[:50]

    plt.plot(range(1, 51), new_mini, label='Mini')
    # plt.plot(range(1, 51), new_nega, label='Nega')
    plt.plot(range(1, 51), fifty, label='50k Mini')
    plt.plot(range(1, 51), twofifty, label='250k Mini')


    plt.xlabel('Move Number')
    plt.ylabel('Average Centipawn Loss')
    plt.title('Average Centipawn Loss Per Move Over 25 Games')
    plt.grid(True)
    plt.legend()
    plt.show()

def main():
    # print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))    

    simulate_games()
    plot()


if __name__ == "__main__":
    main()
