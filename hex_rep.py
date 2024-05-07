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
COLOR_MASK = 8

'''NOT CURRENTLY BEING USED : Function takes in piece ?? outputs color integer??'''
def get_color(color_mask):
    if (color_mask & WHITE) != 0:
        return WHITE  # White piece
    elif (color_mask & BLACK) != 0:
        return BLACK  # Black piece
    else:
        return PIECE_MASK  # No piece at the specified position



'''Takes in a hex number, pops the rightmost digit, returns the popped digit and the hex number'''   
def pop_rightmost_hex_digit(number):
    popped_digit = number & 0xF 
    number >>= 0x4
    return popped_digit, number

'''Takes in a number and a digit to add, returns the number with the new digit'''
def add_rightmost_digit(number, digit_piece):
    digit_piece >>= 1
    updated_board = digit_piece | number 
    return updated_board

'''Takes in a hex number and a hex digit to add, returns the hex number with the new digit'''
def add_rightmost_hex_digit(number, digit_piece):
    digit_piece >>= 4
    updated_board = digit_piece | number 
    return updated_board

'''Given a file and rank, returns a number between 0-63 representing the board location'''
def square_to_bit_position(file, rank):
    return rank * 8 + file


'''removed the piece at the given square from 0-63, ie converts the hex number at this square to 0'''
def clear_piece(board, position):
    return board & ~(0xF << (position * 4))

'''adds the piece at the given square from 0-63, ie converts the hex number at this square to 0'''
def add_piece(board, square, piece):
    hex_piece = piece << (square * 4)
    updated_board = board | hex_piece
    return updated_board


'''Given a board and a square, returns the hex number at the square'''
def get_piece_from_square(board, square):
    whole_mask = board >> (square * 4) & 0xF
    return whole_mask

'''extracts the 64th digit from the hex number 
STATE: value === 0 (WHITE) then white to move
STATE: value === 8 (BLACK) then black to move
STATE: value === 0 + 1 (WHITE + 1) then white checkmate
STATE: value === 8 + 1 (BLACK + 1) then black checkmate
'''
def get_color_to_move_bit(board):
    return get_piece_from_square(board, 64)
    
'''extracts the 65th digit from the hex number
STATE: 0b0001  represents king side castle WHITE
STATE: 0b0010 represents queen side castle WHITE
STATE: 0b0100 represents king side caslte BLACK
STATE: 0b1000 represents queen side caslte BLACK

All state values are 0 for available and 1 for not available
- if king moves, all state set to 1
- if rook moves on queen or king side, that state is set to 1
- 
'''
def get_castle_bits(board):
    return get_piece_from_square(board, 65)

'''extracts the 66th digit from the hex number
the 66th digit will hold state 
value: 0 - NO EN passant
value: 1 - last move was a pawn that was moved 2
'''
def get_en_passant_state(board):
    return get_piece_from_square(board, 66)

'''this bit will hold the last piece that was moved stored in the 67th hex digit
helpful for en passant, if state en passant is 1, this will say if the last move is legal or not'''
def get_last_move_bits(board):
    return get_piece_from_square(board, 67)

'''
'''
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

'''
Prints board state: for starting board 
Game State: 0x0
Castling State: 0b0
En Passant State: 0x0
Last Move: 0x0

Board Values:
a b c d e c b a
9 9 9 9 9 9 9 9
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1
2 3 4 5 6 4 3 2
'''
def print_board(board):
    print("Game State: " + str(hex(get_color_to_move_bit(board))))
    print("Castling State: " + str(bin(get_castle_bits(board))))
    print("En Passant State: " + str(hex(get_en_passant_state(board))))
    print("Last Move: " + str(hex(get_last_move_bits(board))))

    print_str = ''
    for i in range(7, -1, -1):  # Start from 7 and decrement to 0
        for j in range(8):
            print_str = print_str + str(hex(get_piece_from_square(board, i * 8 + j)))[2:] + " "
        print_str = print_str + '\n'  # Add newline after each row
    
    print("\nBoard Values:")
    print(print_str)
    
'''for testing, prints, 
In starting positon 0 being the white rook, 63 being the black rook
        56 57 58 59 60 61 62 63
        48 49 50 51 52 53 54 55
        40 41 42 43 44 45 46 47
        32 33 34 35 36 37 38 39
        24 25 26 27 28 29 30 31
        16 17 18 19 20 21 22 23
        8 9 10 11 12 13 14 15
        0 1 2 3 4 5 6 7
    '''
def number_board():
    string = ''
    for i in range(7, -1, -1):  # Start from 7 and decrement to 0
        for j in range(8):
            string = string + str(i * 8 + j) + " "
        string = string + '\n'  # Add newline after each row
    
    print(string)

    
def get_knight_moves(board, square, color):
    return None


def get_all_possible_next_board_states(board):
    pos_moves = 0

    color_to_move = get_color_to_move_bit(board)
    castle_rights = get_castle_bits(board)
    en_passant_state = get_en_passant_state(board)
    last_move = get_last_move_bits(board)

    all_pos_states = []

    for i in range(64):
        square = get_piece_from_square(i)
        piece = square & PIECE_MASK
        color = square & COLOR_MASK

        if color != color_to_move or square == 0:
            pass
        elif piece == KNIGHT:
            get_knight_moves(board, square, color_to_move)
        

def main():
    board = 0x0

    board = add_piece(board, 0, WHITE | ROOK)
    board = add_piece(board, 1, WHITE | KNIGHT)
    board = add_piece(board, 2, WHITE | BISHOP)
    board = add_piece(board, 3, WHITE | QUEEN)
    board = add_piece(board, 4, WHITE | KING)
    board = add_piece(board, 5, WHITE | BISHOP)
    board = add_piece(board, 6, WHITE | KNIGHT)
    board = add_piece(board, 7, WHITE | ROOK)
    for i in range(8, 16):
        board = add_piece(board, i, WHITE | PAWN)
    for i in range(48, 56):
        board = add_piece(board, i, BLACK | PAWN)
    board = add_piece(board, 56, BLACK | ROOK)
    board = add_piece(board, 57, BLACK | KNIGHT)
    board = add_piece(board, 58, BLACK | BISHOP)
    board = add_piece(board, 59, BLACK | QUEEN)
    board = add_piece(board, 60, BLACK | KING)
    board = add_piece(board, 61, BLACK | BISHOP)
    board = add_piece(board, 62, BLACK | KNIGHT)
    board = add_piece(board, 63, BLACK | ROOK)
    

    board = add_piece(board, 64, 0x0) # setting white to move
    board = add_piece(board, 65, 0x0) # setting all castling to 0
    board = add_piece(board, 66, 0x0) # setting en passant to false
    board = add_piece(board, 67, 0x0) # setting last move to 0

    print_board(board)
    board = clear_piece(board, 0)
    print_board(board)

    number_board()

  



if __name__ == "__main__":
    main()


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

# def generate_knight_moves(file, rank, color, board, piece):

#     # +2 = 00 = 0
#     # +1 = 1 = 1
#     # -1 = 10 = 2
#     # -2 = 11 = 3
#     num = 0b00010010110111100100011110001011

#     output = 0

#     old_square = file * 8 + rank
#     is_left_edge = old_square % 8 == 0
#     is_right_edge = old_square - 7 % 8 == 0

#     print(is_left_edge,is_right_edge)

#     while num > 0:
#         curr = num & 0b1111
#         new_file = 0 
#         new_rank = 0

#         if curr == 0b1 and not is_right_edge:
#             new_file = file + 2 
#             new_rank = rank + 1
#         elif curr == 0b10 and not is_right_edge:
#             new_file = file + 2 
#             new_rank = rank - 1        
#         elif curr == 0b1101:# and not is_left_edge:
#             new_file = file - 2 
#             new_rank = rank + 1
#         elif curr == 0b1110:# and not is_left_edge:
#             new_file = file - 2 
#             new_rank = rank - 1
#         elif curr == 0b100 and not is_right_edge:
#             new_file = file + 1 
#             new_rank = rank + 2
#         elif curr == 0b111:# and not is_left_edge:
#             new_file = file - 1 
#             new_rank = rank + 2
#         elif curr == 0b1000 and not is_right_edge: 
#             new_file = file + 1 
#             new_rank = rank - 2     
#         elif curr == 0b1011:# and not is_left_edge:
#             new_file = file - 1
#             new_rank = rank - 2
        
#         # print(new_file, new_rank, bin(num))
#         # new_file >= 8 or new_rank <= 8 or new_file < 0 or new_rank > 0
#         new_square = new_rank * 8 + new_file
#         if new_square < 0 or new_square >=64:
#             pass 
#         else:
#             output = add_piece(board, new_square, color, piece, hexa=True)
#             print(output)

#         num = num >> 0b100
#     print(hex(output))

#     return output


# for testing only
# piece_english = {0:'WHITE', 1: 'PAWN', 2: 'ROOK', 3: 'KNIGHT', 4: 'BISHOP', 5:'QUEEN',6:'KING',7:'NO_PIECE', 8:'BLACK'}
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


