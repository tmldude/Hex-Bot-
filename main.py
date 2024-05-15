from hex_rep import Board


def init_position() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    board.add_piece(1, board.WHITE | board.KNIGHT)
    board.add_piece(2, board.WHITE | board.BISHOP)
    board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    for i in range(8, 16):
        board.add_piece(i, board.WHITE | board.PAWN)
    # board.add_piece( 17, board.BLACK | board.PAWN)
    # board.add_piece( 22, board.BLACK | board.PAWN)
    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)

    return board

def castle_test() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    # board.add_piece(1, board.WHITE | board.KNIGHT)
    # board.add_piece(2, board.WHITE | board.BISHOP)
    # board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    # board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    for i in range(8, 16):
        if i != 12:
            board.add_piece(i, board.WHITE | board.PAWN)
    # board.add_piece( 17, board.BLACK | board.PAWN)
    # board.add_piece( 22, board.BLACK | board.PAWN)
    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)
    board.add_piece(36, board.BLACK | board.ROOK)


    return board

def move_out_of_block() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    # board.add_piece(1, board.WHITE | board.KNIGHT)
    # board.add_piece(2, board.WHITE | board.BISHOP)
    # board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    # board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(12, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    for i in range(8, 16):
        if i != 12:
            board.add_piece(i, board.WHITE | board.PAWN)
    # board.add_piece( 17, board.BLACK | board.PAWN)
    # board.add_piece( 22, board.BLACK | board.PAWN)
    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)
    board.add_piece(36, board.BLACK | board.ROOK)


    return board

def test_promo() -> Board:
    board = Board()
    board.board = 0x0
    # board.add_piece(0, board.WHITE | board.ROOK)
    # board.add_piece(1, board.WHITE | board.KNIGHT)
    # board.add_piece(2, board.WHITE | board.BISHOP)
    # board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    # board.add_piece(5, board.WHITE | board.BISHOP)
    # board.add_piece(6, board.WHITE | board.KNIGHT)
    # board.add_piece(7, board.WHITE | board.ROOK)
    for i in range(8, 9):
        if i != 12:
            board.add_piece(i, board.WHITE | board.PAWN)
    # board.add_piece( 17, board.BLACK | board.PAWN)
    # board.add_piece( 22, board.BLACK | board.PAWN)
    # for i in range(48, 56):
    #     board.add_piece(i, board.BLACK | board.PAWN)
    # board.add_piece(56, board.BLACK | board.ROOK)
    # board.add_piece(57, board.BLACK | board.KNIGHT)
    # board.add_piece(58, board.BLACK | board.BISHOP)
    # board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    # board.add_piece(61, board.BLACK | board.BISHOP)
    # board.add_piece(62, board.BLACK | board.KNIGHT)
    # board.add_piece(63, board.BLACK | board.ROOK)
    # board.add_piece(36, board.BLACK | board.ROOK)

    board.add_piece(50, board.WHITE | board.PAWN)
    # board.add_piece(0, board.WHITE | board.ROOK)

    # board.add_piece(7, board.WHITE | board.ROOK)




    return board


def test_position() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    board.add_piece(1, board.WHITE | board.KNIGHT)
    # board.add_piece( 2, board.WHITE | board.BISHOP)
    board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    # board.add_piece( 7, board.WHITE | board.ROOK)
    # board.add_piece(32, board.WHITE | board.PAWN)
    board.add_piece(39, board.WHITE | board.PAWN)
    board.add_piece(35, board.WHITE | board.BISHOP)

    for i in range(9, 13):
        board.add_piece(i, board.WHITE | board.PAWN)
    # for i in range(48, 56):
    #     board.add_piece( i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    # board.add_piece( 60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)

    # board.add_piece( 33, board.WHITE | board.KNIGHT)
    board.add_piece(44, board.WHITE | board.ROOK)
    board.add_piece(47, board.BLACK | board.ROOK)
    board.add_piece(40, board.WHITE | board.PAWN)
    board.add_piece(23, board.BLACK | board.PAWN)

    board.color_to_move = 0x0
    board.last_end_square = 0x0
    board.castle_states = 0x0
    board.can_en_passant = 0x0
    return board


def test_sliding() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    board.add_piece(1, board.WHITE | board.KNIGHT)
    board.add_piece(2, board.WHITE | board.BISHOP)
    board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    board.add_piece(32, board.WHITE | board.PAWN)
    board.add_piece(39, board.WHITE | board.PAWN)

    # for i in range(8, 16):
    #     board.add_piece( i, board.WHITE | board.PAWN)
    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)

    # board.add_piece( 33, board.WHITE | board.KNIGHT)
    board.add_piece(36, board.WHITE | board.ROOK)

    board.color_to_move = 0x0
    board.last_end_square = 0x0
    board.castle_states = 0x0
    board.can_en_passant = 0x0

    return board


def test_en_passant() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    board.add_piece(1, board.WHITE | board.KNIGHT)
    board.add_piece(2, board.WHITE | board.BISHOP)
    board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    # for i in range(8, 16):
    #     board.add_piece( i, board.WHITE | board.PAWN)
    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)

    board.add_piece(33, board.BLACK | board.PAWN)
    board.add_piece(32, board.WHITE | board.PAWN)

    board.color_to_move = 0x0
    board.last_end_square = 33
    board.castle_states = 0x0
    board.can_en_passant = 0x1

    return board


def test_king() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    board.add_piece(1, board.WHITE | board.KNIGHT)
    board.add_piece(2, board.WHITE | board.BISHOP)
    board.add_piece(3, board.WHITE | board.QUEEN)
    # board.add_piece( 4, board.WHITE | board.KING)
    board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    for i in range(8, 16):
        board.add_piece(i, board.WHITE | board.PAWN)
    # board.add_piece( 17, board.BLACK | board.PAWN)
    # board.add_piece( 22, board.BLACK | board.PAWN)
    board.add_piece(32, board.WHITE | board.KING)

    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)
    board.add_piece(17, board.BLACK | board.ROOK)

    return board

import random

def main():

    # board = Board(move_out_of_block().board, Board.BLACK)
    # print(board)

    # board.print_board_hex()
    # board.print_board_hex(board.attack_board)

    # # print(get_all_possible_next_board_states(board, white_pieces, black_pieces))

    # all_curr = board.generate_all_possible_next_board_states()

    # for move in all_curr:
    #     move.print_board_hex()

    # chosen = random.choice(all_curr)

    # chosen.print_board_hex()
    # chosen.print_board_hex(chosen.attack_board)

    # print("===========================")
    # second_moves = chosen.generate_all_possible_next_board_states()
    # for move in second_moves:
    #     move.print_board_hex()

    # second_move = random.choice(second_moves)

    # second_move.print_board_hex()
    # second_move.print_board_hex(second_move.attack_board)

    play_game()





def play_game():
    board = Board(init_position().board, Board.BLACK)

    max_moves = 256

    i = 0
    gameover = False
    current_state = board.generate_all_possible_next_board_states()
    while i < max_moves and not gameover:
        board = random.choice(current_state)
        # chosen.print_board_hex()
        # chosen.print_board_hex(chosen.attack_board)

        current_state = board.generate_all_possible_next_board_states()
        i += 1


    board.print_board_hex()







if __name__ == "__main__":
    main()


# 0xabc0dcba00000000a00200011000000000000000900000000001111043465032
# 0xabc0dcba00000000a00200011000000000000000900000000001111043465032