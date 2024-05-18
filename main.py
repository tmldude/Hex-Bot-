import matplotlib.pyplot as plt
import numpy as np
import chess

from tests import init_position
from engine import Engine


def simulate_games(num_games=5):
    max_moves = 256
    centipawn_loss_data = np.zeros((num_games, max_moves))

    for game in range(num_games):
        engine = Engine(chess.STARTING_BOARD_FEN)

        print(f"Simulating game {game + 1} / {num_games}")
        centipawn_losses = engine.play_stockfish()
        for i in range(min(len(centipawn_losses), max_moves)):
            centipawn_loss_data[game, i] = centipawn_losses[i]

    # Calculate the average centipawn loss per move
    average_centipawn_loss_per_move = np.mean(centipawn_loss_data, axis=0)

    # Save the data
    np.save('centipawn_loss_data.npy', centipawn_loss_data)
    np.save('average_centipawn_loss_per_move.npy',
            average_centipawn_loss_per_move)

    # Plot the average centipawn loss per move
    plt.plot(range(1, max_moves + 1), average_centipawn_loss_per_move)
    plt.xlabel('Move Number')
    plt.ylabel('Average Centipawn Loss')
    plt.title('Average Centipawn Loss Per Move Over 1000 Games')
    plt.grid(True)
    plt.show()


def main():
    simulate_games()


if __name__ == "__main__":
    main()
