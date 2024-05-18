

# import pandas as pd

import chess
import chess.engine

from archive.board_hex import HexBoard
import random


class StockFishEvaluateHexPosition:
    '''Takes in a board to find the next move and evaluate the next best position using stockfish
    Also, holds functions to convert our BOARD into FEN and back into our BOARD
    '''

    ENGINE_PATH = "D:\ChessData\stockfish\stockfish-windows-x86-64-avx2.exe"

    def __init__(self, board):
        self.hex_board = board.board
        self.active_color = 'black' if board.color_to_move == 7 else 'white'
        self.can_castle_kingside = {'white': not board.castle_states['white_king_moved'] and not board.castle_states[
            'KS_rook_w_moved'], 'black': not board.castle_states['black_king_moved'] and not board.castle_states['KS_rook_b_moved']}
        self.can_castle_queenside = {'white': not board.castle_states['white_king_moved'] and not board.castle_states[
            'QS_rook_w_moved'], 'black': not board.castle_states['black_king_moved'] and not board.castle_states['QS_rook_b_moved']}
        self.en_passant = "-" if not board.en_passant_square_fen else self.square_number_to_fen(
            board.en_passant_square_fen)
        self.halfmove_clock = 0
        self.fullmove_number = 1

        self.board = self.hex_to_board(hex(self.hex_board))

        self.fen = self.convert_to_fen(self.board, self.active_color, self.can_castle_kingside,
                                       self.can_castle_queenside, self.en_passant, self.halfmove_clock, self.fullmove_number)

        self.score = self.stockfish_evaluation(
            self.fen, StockFishEvaluateHexPosition.ENGINE_PATH, )
        # self.interpretted_score = self.interpret_score(self.score)

    def stockfish_next_move(self, engine_path=ENGINE_PATH, time_limit=0.01):
        board = chess.Board(self.fen)

        with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
            result = engine.play(board, chess.engine.Limit(time=time_limit))

            board.push(result.move)

        new_fen = board.fen()
        return new_fen

    def interpret_score(self, score):
        if score.is_mate():
            return f"Mate in {score.mate()}"
        else:
            return f"Centipawn score: {score.relative.score()}"

    def stockfish_evaluation(self, fen, engine_path=ENGINE_PATH, time_limit=0.01):
        board = chess.Board(fen)

        with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
            result = engine.analyse(board, chess.engine.Limit(time=time_limit))

        score = result['score']

        return score

    def square_number_to_fen(self, square_number):
        if square_number == -1:  # If no en passant target square
            return "-"

        files = "abcdefgh"
        ranks = "87654321"

        file = files[square_number % 8]
        rank = ranks[square_number // 8]

        return file + rank

    def hex_to_board(self, hex_string):
        hex_digits = [hex_string[i:i+1] for i in range(2, len(hex_string))]

        board = [[0] * 8 for _ in range(8)]
        for i in range(8):
            for j in range(8):
                board[i][j] = int(hex_digits[i * 8 + j], 16)

        return board

    def convert_to_fen(self, board, active_color, can_castle_kingside, can_castle_queenside, en_passant, halfmove_clock, fullmove_number):
        piece_map = {
            0: '', 1: 'P', 2: 'R', 3: 'N', 4: 'B', 5: 'Q', 6: 'K',
            9: 'p', 10: 'r', 11: 'n', 12: 'b', 13: 'q', 14: 'k'
        }

        fen_rows = []
        for row in board:
            fen_row = ""
            empty_count = 0
            for square in row:
                if square == 0:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += piece_map[square]
            if empty_count > 0:
                fen_row += str(empty_count)
            fen_rows.append(fen_row)

        piece_placement = "/".join(fen_rows)

        castling_rights = ""
        if can_castle_kingside['white']:
            castling_rights += "K"
        if can_castle_queenside['white']:
            castling_rights += "Q"
        if can_castle_kingside['black']:
            castling_rights += "k"
        if can_castle_queenside['black']:
            castling_rights += "q"
        if castling_rights == "":
            castling_rights = "-"

        active_color = 'b' if active_color == 'white' else 'w'

        en_passant = en_passant if en_passant else "-"

        fen = f"{piece_placement} {active_color} {castling_rights} {en_passant} {halfmove_clock} {fullmove_number}"
        return fen

    def fen_to_square_number(self, fen_square):
        if fen_square == "-":
            return -1

        files = "abcdefgh"
        ranks = "87654321"

        file = fen_square[0]
        rank = fen_square[1]

        file_index = files.index(file)
        rank_index = ranks.index(rank)

        square_number = rank_index * 8 + file_index

        return square_number

    def fen_to_board(self, fen):
        piece_to_hex = {
            'P': '1', 'R': '2', 'N': '3', 'B': '4', 'Q': '5', 'K': '6',
            'p': '9', 'r': 'a', 'n': 'b', 'b': 'c', 'q': 'd', 'k': 'e'
        }

        board = [['0' for _ in range(8)] for _ in range(8)]

        fen_parts = fen.split(' ')
        piece_placement = fen_parts[0]

        ranks = piece_placement.split('/')
        for rank_index, rank in enumerate(ranks):
            file_index = 0
            for char in rank:
                if char.isdigit():
                    file_index += int(char)
                else:
                    board[rank_index][file_index] = piece_to_hex[char]
                    file_index += 1

        hex_digits = [board[rank][file]
                      for rank in range(8) for file in range(8)]

        hex_string = '0x' + ''.join(hex_digits)
        integer_value = int(hex_string, 16)

        color_to_move = HexBoard.BLACK if fen_parts[1] == 'w' else HexBoard.WHITE

        castle_states = {'white_king_moved': True,
                         'black_king_moved': True,
                         'QS_rook_b_moved': True,
                         'QS_rook_w_moved': True,
                         'KS_rook_b_moved': True,
                         'KS_rook_w_moved': True, }
        if 'K' in fen_parts[2]:
            castle_states['white_king_moved'] = False
            castle_states['KS_rook_w_moved'] = False
        if 'Q' in fen_parts[2]:
            castle_states['white_king_moved'] = False
            castle_states['QS_rook_w_moved'] = False
        if 'k' in fen_parts[2]:
            castle_states['black_king_moved'] = False
            castle_states['KS_rook_b_moved'] = False
        if 'q' in fen_parts[2]:
            castle_states['black_king_moved'] = False
            castle_states['QS_rook_b_moved'] = False
        # print(castle_states)

        last_end_square = self.fen_to_square_number(
            fen_parts[3]) if fen_parts[3] != '-' else None
        can_en_passant = 1 if fen_parts[3] != '-' else 0
        if color_to_move == HexBoard.WHITE:
            en_passant_square_fen = last_end_square - 8 if last_end_square else None
        else:
            en_passant_square_fen = last_end_square + 8 if last_end_square else None

        board = HexBoard(board=integer_value, color_to_move=color_to_move, castle_states=castle_states,
                         last_end_square=last_end_square, en_passant_square_fen=en_passant_square_fen, can_en_passant=can_en_passant)

        return board


# import chess.pgn
# import chess.engine


# def stockfish_evaluation(engine_path, board, time_limit = 0.01):
#     engine = chess.engine.SimpleEngine.popen_uci(engine_path)
#     result = engine.analyse(board, chess.engine.Limit(time=time_limit))
#     engine.close()

#     # print(result)
#     return result['score']


# pgn_path = "D:\ChessData\lichess_db_standard_rated_2024-02.pgn"
# engine_path = "D:\ChessData\stockfish\stockfish-windows-x86-64-avx2.exe"

# pgn = open(pgn_path)
# df = pd.DataFrame(columns=["board", "evaluation"])


# first_game = chess.pgn.read_game(pgn)
# second_game = chess.pgn.read_game(pgn)

# board = first_game.board()
# for move in first_game.mainline_moves():
#     board.push(move)
#     eval = stockfish_evaluation(engine_path, board)

#     data = {"board": board, "evaluation": eval}
#     df.loc[len(df)] = data


# csv_file_path = "C:\\Users\\tmlaz\\Desktop\\chesspy\\output.csv"
# df.to_csv(csv_file_path, index=False)  # Set index=False to exclude row numbers in the CSV file


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
