


'''
To Do:
1. Figure out how to convert PGN or FPG from the lichess database into the (x,y) -> (hex representation of the board state, eval)
2. Build out an excel file via an automation process for every game state 
    (we are looking at 10's of thousands of games since each month is 30gb of data)3
3. Use the data to train a conv net <- this is a later problem 

'''
# you'll want to use pandas 


import pandas as pd
import chess.pgn
import chess.engine


def stockfish_evaluation(engine_path, board, time_limit = 0.01):
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    result = engine.analyse(board, chess.engine.Limit(time=time_limit))
    engine.close()

    # print(result)
    return result['score']


pgn_path = "D:\ChessData\lichess_db_standard_rated_2024-02.pgn"
engine_path = "D:\ChessData\stockfish\stockfish-windows-x86-64-avx2.exe"

pgn = open(pgn_path)
df = pd.DataFrame(columns=["board", "evaluation"])


first_game = chess.pgn.read_game(pgn)
second_game = chess.pgn.read_game(pgn)

board = first_game.board()
for move in first_game.mainline_moves():
    board.push(move)
    eval = stockfish_evaluation(engine_path, board)

    data = {"board": board, "evaluation": eval}
    df.loc[len(df)] = data



csv_file_path = "C:\\Users\\tmlaz\\Desktop\\chesspy\\output.csv"
df.to_csv(csv_file_path, index=False)  # Set index=False to exclude row numbers in the CSV file


# board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

# result = stockfish_evaluation(engine, board)
# print(result)






# pgn = open(directory_path)
# first_game = chess.pgn.read_game(pgn)
# first_game = chess.pgn.read_game(pgn)

# print(first_game.headers["Event"])

# print(first_game.eval())

# board = first_game.board()
# for move in first_game.mainline_moves():
#     print(move)
#     board.push(move)

# print(board)







# files = list_files(directory_path)
# print(files)

# def pgn_to_hex():
#     return "unimplemented"


# Print the moves of the first game in the PGN file
# if games_list:
#     first_game = games_list[0]
#     print("Moves of the first game:")
#     print(first_game.mainline_moves())
# else:
#     print("No games found in the PGN file.")



# def list_files(directory):
#     """
#     List all files and directories in the specified directory.

#     Args:
#     - directory (str): The directory path to list.

#     Returns:
#     - files_list (list): A list containing the names of all files and directories in the specified directory.
#     """
#     files_list = os.listdir(directory)
#     return files_list