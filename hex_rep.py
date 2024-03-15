# Define constants for piece types
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


# for testing only
# piece_english = {0:'WHITE', 1: 'PAWN', 2: 'ROOK', 3: 'KNIGHT', 4: 'BISHOP', 5:'QUEEN',6:'KING',7:'NO_PIECE', 8:'BLACK'}

def square_to_bit_position(file, rank):
    # Assuming the chessboard is represented with files a-h and ranks 1-8
    return 1 << (rank * 8 + file)

def get_color(color_mask):
    if (color_mask & WHITE) != 0:
        return WHITE  # White piece
    elif (color_mask & BLACK) != 0:
        return BLACK  # Black piece
    else:
        return PIECE_MASK  # No piece at the specified position
    

# print(len(str(bin(square_to_bit_position(5,4)))))
    
def print_labeled_bitboard(bitboard, label):
    print(f"{label} Bitboard:")
    for rank in range(7, -1, -1):
        for file in range(8):
            square = 8 * rank + file
            if bitboard & (1 << square):
                print("1", end=" ")
            else:
                print("0", end=" ")
        print()

def pop_rightmost_hex_digit(hex_number, hexa=True):    
    popped_digit = hex_number & 0xF 
    if hexa:
        hex_number = hex_number >> 0x4 
        popped_hex_number = hex(popped_digit)[2:].upper()
    else:
        hex_number = hex_number >> 0x1
        popped_hex_number = hex(popped_digit)[2:]

    
    popped_hex_number = hex(popped_digit)[2:].upper()  # Remove '0x' prefix and convert to uppercase
    
    return popped_hex_number, hex_number

def add_rightmost_hex_digit(board, color, piece, hexa=True):
    hex_piece = color | piece

    if hexa:
        hex_piece = hex_piece >> 4
    else: 
        hex_piece = hex_piece >> 1

    updated_board = hex_piece | board 
    return updated_board

def print_board(board, hexa = True):
    x = board
    curr = ''
    counter = 0
    while x != 0x0:

        rightmost, x = pop_rightmost_hex_digit(x, hexa)
        curr += rightmost
        counter += 1

        if counter % 8 == 0:
            curr += '\n'
        if counter > 100:
            break
    
    while len(curr) <= 71:            
        curr += '0'
        counter += 1 
        if counter % 8 == 0:
            curr += '\n'

    print(curr[::-1])

def clear_piece(bitboard, position):
    return bitboard & ~(1 << position)            

def add_piece(board, square, color, piece, hexa=True):
    hex_piece = color | piece

    if hexa:
        hex_piece = hex_piece << (square * 4)
        updated_board = clear_piece(board, square * 4)

    else: 
        hex_piece = hex_piece << (square)
        updated_board = clear_piece(board, square)

    updated_board = hex_piece | updated_board 
    return updated_board



def get_spots(board, square):
    whole_mask = board >> (square * 4) & 0xF

    piece_mask = whole_mask & 111
    color_mask = whole_mask & 1000

    if piece_mask == 0:
        return PIECE_MASK, PIECE_MASK
    
    return piece_mask, color_mask

def get_move(piece0, color0, spot0, piece1, color1, spot1, board):
    pos_moves = 0

    # if piece0 == PAWN:
    #     pos_moves = generate_pawn_moves(color0, spot0, board)
    if piece0 == KNIGHT:
        pos_moves = generate_knight_moves(color0, spot0, board)
    # if piece0 == BISHOP:
    #     pos_moves = generate_bishop_moves(color0, spot0, board)
    # if piece0 == ROOK:
    #     pos_moves = generate_rook_moves(color0, spot0, board)
    # if piece0 == QUEEN:
    #     pos_moves = generate_queen_moves(color0, spot0, board)
    # if piece0 == KING:
    #     pos_moves = generate_king_moves(color0, spot0, board)
        

def main():
    board = 0x0

    # print(board)
    board = add_piece(board, 0, WHITE, ROOK)
    board = add_piece(board, 1, WHITE, KNIGHT)
    board = add_piece(board, 2, WHITE, BISHOP)
    board = add_piece(board, 3, WHITE, QUEEN)
    board = add_piece(board, 4, WHITE, KING)
    board = add_piece(board, 5, WHITE, BISHOP)
    board = add_piece(board, 6, WHITE, KNIGHT)
    board = add_piece(board, 7, WHITE, ROOK)
    board = add_piece(board, 56, BLACK, ROOK)
    board = add_piece(board, 57, BLACK, KNIGHT)
    board = add_piece(board, 58, BLACK, BISHOP)
    board = add_piece(board, 59, BLACK, QUEEN)
    board = add_piece(board, 60, BLACK, KING)
    board = add_piece(board, 61, BLACK, BISHOP)
    board = add_piece(board, 62, BLACK, KNIGHT)
    board = add_piece(board, 63, BLACK, ROOK)

    for i in range(48, 56):
        board = add_piece(board, i, BLACK, PAWN)
    for i in range(8, 16):
        board = add_piece(board, i, WHITE, PAWN)

    print_board(board)

    # coordinates = input("from ") 
    # file0, rank0 = int(coordinates[0]), int(coordinates[1])
    # coordinates = input("to ") 
    # file1, rank1 = int(coordinates[0]), int(coordinates[1])

    # spot0 = file0 * 8 + rank0
    # spot1 = file1 * 8 + rank1

    # piece0, color0 = get_spots(board, spot0)
    # piece1, color1 = get_spots(board, spot1)

    # print(get_spots(board, spot0), get_spots(board, spot1))

    # new_board = get_move(piece0, color0, spot0, piece1, color1, spot1, board)
    # print_board(generate_knight_moves(7, 1, BLACK, board, KNIGHT))
    # print_board(generate_knight_moves(6, 2, BLACK, board, KNIGHT))

    # print_board(generate_knight_moves(0, 0, BLACK, board, KNIGHT))
    # number_board()
    print(hex(board))

def generate_knight_moves(file, rank, color, board, piece):

    # +2 = 00 = 0
    # +1 = 1 = 1
    # -1 = 10 = 2
    # -2 = 11 = 3
    num = 0b00010010110111100100011110001011

    output = 0

    old_square = file * 8 + rank
    is_left_edge = old_square % 8 == 0
    is_right_edge = old_square - 7 % 8 == 0

    print(is_left_edge,is_right_edge)

    while num > 0:
        curr = num & 0b1111
        new_file = 0 
        new_rank = 0

        if curr == 0b1 and not is_right_edge:
            new_file = file + 2 
            new_rank = rank + 1
        elif curr == 0b10 and not is_right_edge:
            new_file = file + 2 
            new_rank = rank - 1        
        elif curr == 0b1101:# and not is_left_edge:
            new_file = file - 2 
            new_rank = rank + 1
        elif curr == 0b1110:# and not is_left_edge:
            new_file = file - 2 
            new_rank = rank - 1
        elif curr == 0b100 and not is_right_edge:
            new_file = file + 1 
            new_rank = rank + 2
        elif curr == 0b111:# and not is_left_edge:
            new_file = file - 1 
            new_rank = rank + 2
        elif curr == 0b1000 and not is_right_edge: 
            new_file = file + 1 
            new_rank = rank - 2     
        elif curr == 0b1011:# and not is_left_edge:
            new_file = file - 1
            new_rank = rank - 2
        
        # print(new_file, new_rank, bin(num))
        # new_file >= 8 or new_rank <= 8 or new_file < 0 or new_rank > 0
        new_square = new_rank * 8 + new_file
        if new_square < 0 or new_square >=64:
            pass 
        else:
            output = add_piece(board, new_square, color, piece, hexa=True)
            print(output)

        num = num >> 0b100
    print(hex(output))

    return output

def number_board():
    '''for testing, prints
        0 1 2 3 4 5 6 7 
        8 9 10 11 12 13 14 15 
        16 17 18 19 20 21 22 23 
        24 25 26 27 28 29 30 31 
        32 33 34 35 36 37 38 39 
        40 41 42 43 44 45 46 47 
        48 49 50 51 52 53 54 55 
        56 57 58 59 60 61 62 63 
    '''

    string = ''
    for i in range(8):
        counter = 0
        for j in range(8):
            string = string + str(i * 8 + j) + " "
        if counter % 8 == 0:
            string = string + '\n'

    print(string)


# def generate_knight_moves(color, spot, board, piece):

#     # +2 = 00 = 0
#     # +1 = 1 = 1
#     # -1 = 10 = 2
#     # -2 = 11 = 3
#     num = 0b00010010110111100100011110001011

#     output = 0

#     while num != 0:
#         curr = num & 0b1111
#         new_spot = spot
    
#         if curr == 0b1:
#            new_spot = (new_spot + 2 * 8) + 1
#         elif curr == 0b10:
#            new_spot = (new_spot + 2 * 8) - 1
#         elif curr == 0b1101:
#            new_spot = (new_spot - 2 * 8) + 1
#         elif curr == 0b1110:
#            new_spot = (new_spot - 2 * 8) - 1
#         elif curr == 0b100:
#            new_spot = (new_spot + 1 * 8) + 2 
#         elif curr == 0b111:
#            new_spot = (new_spot + 1 * 8) - 2
#         elif curr == 0b1000: 
#            new_spot = (new_spot - 1 * 8) + 2     
#         if curr == 0b1011: 
#            new_spot = (new_spot - 1 * 8) - 2
#         else:
#             # print(bin(curr), "not on board")
#             pass
        
#         if new_spot >= 64 or new_spot < 0:
#             pass
#         else:
#             output = add_piece(output, new_spot, BLACK, PIECE_MASK)


#         num = num >> 0b100

#     return output




# def generate_knight_moves(color, spot, board):

#     # +2 = 00 = 0
#     # +1 = 1 = 1
#     # -1 = 10 = 2
#     # -2 = 11 = 3
#     num = 0b00010010110111100100011110001011

#     output = 0

#     while num != 0:
#         curr = num & 0xF
#         if spot + 1 >= 64 or spot - 1 <= 0:
#             pass
#         elif curr == 1:
#             output = output >> 7 | ((spot + 2 * 8) + 1)
#         elif curr == 10:
#            output = output >> 7 | (spot + 2 * 8) - 1
#         elif curr == 1101:
#            output = output >> 7 | (spot - 2 * 8) + 1
#         elif curr == 1110:
#            output = output >> 7 | (spot - 2 * 8) - 1
#         elif curr == 100:
#            output = output >> 7 | (spot + 1 * 8) + 2 
#         elif curr == 111:
#            output = output >> 7 | (spot + 1 * 8) - 2
#         elif curr == 1000: 
#            output = output >> 7 | (spot - 1 * 8) + 2     
#         if curr == 1011: 
#            output = output >> 7 | (spot - 1 * 8) - 2
#         else:
#             print(curr, "not on board")
    
#     return output

if __name__ == "__main__":
    main()


