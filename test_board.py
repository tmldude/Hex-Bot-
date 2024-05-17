from board_hexrep import HexBoard

PAWN = 1
ROOK = 2
KNIGHT = 3
BISHOP = 4
QUEEN = 5
KING = 6

# Constants for colors
WHITE = 0
BLACK = 8

PIECE_MASK = 7
COLOR_MASK = 8

'''Given a board and a square, returns the hex number at the square'''


def get_piece_from_square(board, square):
    whole_mask = board >> (square * 4) & 0xF
    return whole_mask


def print_bin_board_hex(board):
    print_str = ''
    for i in range(7, -1, -1):  # Start from 7 and decrement to 0
        for j in range(8):
            print_str = print_str + \
                str(hex(get_piece_from_square(board, i * 8 + j)))[2:] + " "
        print_str = print_str + '\n'  # Add newline after each row

    print("\n hex Board Values:")
    print(print_str)


NOT_A_FILE = 0xfffffff0fffffff0fffffff0fffffff0fffffff0fffffff0fffffff0fffffff0
NOT_H_FILE = 0xfffffff0fffffff0fffffff0fffffff0fffffff0fffffff0fffffff0fffffff
NOT_AB_FILE = 0xffffff00ffffff00ffffff00ffffff00ffffff00ffffff00ffffff00ffffff00
NOT_GH_FILE = 0xffffff00ffffff00ffffff00ffffff00ffffff00ffffff00ffffff00ffffff


def knight_moves(friendly_pieces=None, enemy_pieces=None, bitboard=(BLACK | KNIGHT) << (25 * 4)):

    # print(hex(bitboard))

    # Knight moves in all directions based on the knight's position
    noNoEa = (bitboard << (17*4)) & NOT_A_FILE
    print(hex(noNoEa))
    noEaEa = (bitboard << (10*4)) & NOT_AB_FILE
    print(hex(noEaEa))

    soEaEa = (bitboard >> (6*4)) & NOT_AB_FILE
    print(hex(soEaEa))
    if soEaEa:
        print("in")

    soSoEa = (bitboard >> (15*4)) & NOT_A_FILE
    noNoWe = (bitboard << (15*4)) & NOT_H_FILE
    noWeWe = (bitboard << (6*4)) & NOT_GH_FILE
    soWeWe = (bitboard >> (10*4)) & NOT_GH_FILE
    soSoWe = (bitboard >> (17*4)) & NOT_H_FILE

    all_moves = noNoEa | noEaEa | soEaEa | soSoEa | noNoWe | noWeWe | soWeWe | soSoWe

    # valid_moves = all_moves & ~friendly_pieces  # Exclude friendly pieces
    # valid_moves = valid_moves | (valid_moves & enemy_pieces)  # Include enemy pieces (captures)

    # print(hex(all_moves))
    print_bin_board_hex(all_moves)
    return all_moves


knight_moves()
i = 0
bit = 1

while i < 10:
    bit = 0 if bit else 1
    print(bit)
    i += 1


tall = ['man', 'mike']
small = ['teddy']

tall += small
print(tall)


# # string = ''
# # for i in range(8):
# #     counter = 0
# #     for j in range(8):
# #         string = string + str(i * 8 + j) + " "
# #     if counter % 8 == 0:
# #         string = string + '\n'

# # print(string)

# thing = '''ABCEDCBA
# 99999999
# 00000000
# 00000000
# 00000000
# 00000000
# 11111111
# 23465432'''

# print(len(thing))

def init_position() -> HexBoard:
    board = HexBoard()
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


def castle_test() -> HexBoard:
    board = HexBoard()
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


def move_out_of_block() -> HexBoard:
    board = HexBoard()
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


def test_promo() -> HexBoard:
    board = HexBoard()
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


def test_position() -> HexBoard:
    board = HexBoard()
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


def test_sliding() -> HexBoard:
    board = HexBoard()
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


def test_en_passant() -> HexBoard:
    board = HexBoard(en_passant_square_fen=41)
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
    # board.en_passant_square_fen = 41

    return board


def test_king() -> HexBoard:
    board = HexBoard()
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


def test_draw() -> HexBoard:
    board = HexBoard()
    board.board = 0x0
    board.add_piece(59, board.BLACK | board.ROOK)
    board.add_piece(61, board.BLACK | board.ROOK)
    board.add_piece(47, board.BLACK | board.ROOK)
    board.add_piece(24, board.BLACK | board.ROOK)
    board.add_piece(52, board.BLACK | board.ROOK)

    board.add_piece(36, board.WHITE | board.KING)
    board.add_piece(60, board.BLACK | board.KING)

    return board
