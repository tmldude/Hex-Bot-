

class Board:
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

    NOT_A_FILE = 0xfffffff0fffffff0fffffff0fffffff0fffffff0fffffff0fffffff0fffffff0
    NOT_H_FILE = 0xfffffff0fffffff0fffffff0fffffff0fffffff0fffffff0fffffff0fffffff
    NOT_AB_FILE = 0xffffff00ffffff00ffffff00ffffff00ffffff00ffffff00ffffff00ffffff00
    NOT_GH_FILE = 0xffffff00ffffff00ffffff00ffffff00ffffff00ffffff00ffffff00ffffff

    COLOR_TO_MOVE = 64
    CASTLE_STATES = 65
    EN_PASSANT_STATE = 66
    LAST_PIECE_MOVED = 67

    ALL_DEFINED = 0x0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff


    def __init__(self, board=None, color_to_move=WHITE, last_move=None, fpgn=None) -> None:
        self.board = board
        # print(board)
        if board:
            self.set_color_to_move_bit(color_to_move) 
            self.set_last_move_bits(last_move if board else last_move)
            self.set_castle_state(0)
            self.set_en_passant_state(0x0)

        if board == None: 
            self.getStartPos()
        self.whitePiece, self.blackPiece = self.getWhiteBlackMasks()
        # print(hex(self.whitePiece))
        # print(hex(self.blackPiece))

        # self.print_board_hex(self.whitePiece)
        # self.print_board_hex(self.blackPiece)


    def getStartPos(self):
        self.board = 0x0
        self.add_piece(0, self.WHITE | self.ROOK)
        self.add_piece( 1, self.WHITE | self.KNIGHT)
        self.add_piece( 2, self.WHITE | self.BISHOP)
        self.add_piece( 3, self.WHITE | self.QUEEN)
        self.add_piece( 4, self.WHITE | self.KING)
        self.add_piece( 5, self.WHITE | self.BISHOP)
        self.add_piece( 6, self.WHITE | self.KNIGHT)
        self.add_piece( 7, self.WHITE | self.ROOK)
        for i in range(8, 16):
            self.add_piece( i, self.WHITE | self.PAWN)
        for i in range(48, 56):
            self.add_piece( i, self.BLACK | self.PAWN)
        self.add_piece( 56, self.BLACK | self.ROOK)
        self.add_piece( 57, self.BLACK | self.KNIGHT)
        self.add_piece( 58, self.BLACK | self.BISHOP)
        self.add_piece( 59, self.BLACK | self.QUEEN)
        self.add_piece( 60, self.BLACK | self.KING)
        self.add_piece( 61, self.BLACK | self.BISHOP)
        self.add_piece( 62, self.BLACK | self.KNIGHT)
        self.add_piece( 63, self.BLACK | self.ROOK)

        self.add_piece( 64, 0x0) # setting white to move
        self.add_piece( 65, 0x0) # setting all castling to 0
        self.add_piece( 66, 0x0) # setting en passant to false
        self.add_piece( 67, 0x0) # setting last move to 0

        # self.add_piece( 32, self.WHITE | self.KNIGHT)

    def getWhiteBlackMasks(self):
        whiteMask = 0
        blackMask = 0

        for i in range(63, -1, -1):

            square = self.get_piece_from_square(i)
            piece = square & self.PIECE_MASK
            color = square & self.COLOR_MASK

            if color == self.WHITE and piece != 0:
                whiteMask = self.add_rightmost_hex_digit(whiteMask, 0xF)
                blackMask = self.add_rightmost_hex_digit(blackMask, 0x0)
            elif color == self.BLACK and piece != 0:
                whiteMask = self.add_rightmost_hex_digit(whiteMask, 0x0)
                blackMask = self.add_rightmost_hex_digit(blackMask, 0xF)
            else: 
                whiteMask = self.add_rightmost_hex_digit(whiteMask, 0x0)
                blackMask = self.add_rightmost_hex_digit(blackMask, 0x0)

        return whiteMask, blackMask


    '''Takes in a hex number, pops the rightmost digit, returns the popped digit and the hex number'''   
    def pop_rightmost_hex_digit(self, number):
        popped_digit = number & 0xF 
        number >>= 0x4
        return popped_digit, number

    '''Takes in a binary number and a digit to add, returns the number with the new digit'''
    def add_rightmost_digit(number, digit_piece):
        digit_piece >>= 1
        updated_board = digit_piece | number 
        return updated_board

    '''Takes in a hex number and a hex digit to add, returns the hex number with the new digit'''
    def add_rightmost_hex_digit(self, number, digit_piece):
        updated_board = (number << 4) | digit_piece
        return updated_board
    
    '''Takes in a hex number and a hex digit to add, returns the hex number with the new digit'''
    def add_leftmost_hex_digit(self, number, digit_piece):
        updated_board = (number << 4) | digit_piece
        return updated_board
    
    '''Given a file and rank, returns a number between 0-63 representing the board location'''
    def square_to_bit_position(self, file, rank):
        return rank * 8 + file

    '''removed the piece at the given square from 0-63, ie converts the hex number at this square to 0'''
    def clear_piece(self, position):
        self.board & ~(0xF << (position * 4))

    '''adds the piece at the given square from 0-63, ie converts the hex number at this square to 0'''
    def add_piece(self, square, piece):
        hex_piece = piece << (square * 4)
        self.board = self.board | hex_piece

    '''Given a board and a square, returns the hex number at the square'''
    def get_piece_from_square(self, square, other=None):
        if other:
            return other >> (square * 4) & 0xF
        return self.board >> (square * 4) & 0xF

    '''Given a board and a square, returns the hex number at the square'''
    def get_piece_from_square_bin(self, square):
        whole_mask = self.board >> (square) & 0b1
        return whole_mask

    '''extracts the 64th digit from the hex number 
    STATE: value === 0 (WHITE) then white to move
    STATE: value === 8 (BLACK) then black to move
    STATE: value === 0 + 1 (WHITE + 1) then white checkmate
    STATE: value === 8 + 1 (BLACK + 1) then black checkmate
    '''
    def get_color_to_move_bit(self):
        return self.get_piece_from_square(self.COLOR_TO_MOVE)
    
    def set_color_to_move_bit(self, num):
        self.clear_piece(self.COLOR_TO_MOVE)
        self.add_piece(self.COLOR_TO_MOVE, num)
    
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
    def get_castle_bits(self):
        return self.get_piece_from_square(self.CASTLE_STATES)
    
    def set_castle_state(self, num):
        self.clear_piece(self.CASTLE_STATES)
        self.add_piece(self.CASTLE_STATES, num)

    '''extracts the 66th digit from the hex number
    the 66th digit will hold state 
    value: 0 - NO EN passant
    value: 1 - last move was a pawn that was moved 2
    '''
    def get_en_passant_state(self):
        return self.get_piece_from_square(self.EN_PASSANT_STATE)
    
    def set_en_passant_state(self, num):
        self.clear_piece(self.EN_PASSANT_STATE)
        self.add_piece(self.EN_PASSANT_STATE, num)

    '''this bit will hold the last piece that was moved stored in the 67th hex digit
    helpful for en passant, if state en passant is 1, this will say if the last move is legal or not'''
    def get_last_move_bits(self):
        return self.get_piece_from_square(self.LAST_PIECE_MOVED)
    
    def set_last_move_bits(self, num):
        self.clear_piece(self.LAST_PIECE_MOVED)
        self.add_piece(self.LAST_PIECE_MOVED, num)

    def pawn_moved_2():
        print("not im")

   

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
    def print_game_state(self):
        print("Game State: " + str(hex(self.get_color_to_move_bit())))
        print("Castling State: " + str(bin(self.get_castle_bits())))
        print("En Passant State: " + str(hex(self.get_en_passant_state())))
        print("Last Move: " + str(hex(self.get_last_move_bits())))

        print_str = ''
        for i in range(7, -1, -1):  # Start from 7 and decrement to 0
            for j in range(8):
                print_str = print_str + str(hex(self.get_piece_from_square(i * 8 + j)))[2:] + " "
            print_str = print_str + '\n'  # Add newline after each row
        
        print("\nBoard Values:")
        print(print_str)

    def print_board_hex(self, other=None):
        print_str = ''
        for i in range(7, -1, -1):  # Start from 7 and decrement to 0
            for j in range(8):
                if other: 
                    print_str = print_str + str(hex(self.get_piece_from_square(i * 8 + j, other)))[2:] + " "
                else: 
                    print_str = print_str + str(hex(self.get_piece_from_square(i * 8 + j)))[2:] + " "

            print_str = print_str + '\n'  # Add newline after each row
        
        print("\n hex Board Values:")
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
    def number_board(self):
        string = ''
        for i in range(7, -1, -1):  # Start from 7 and decrement to 0
            for j in range(8):
                string = string + str(i * 8 + j) + " "
            string = string + '\n'  # Add newline after each row
        
        print(string)


    def knight_moves(self, bitboard):
        new_boards = []

        # Knight moves in all directions based on the knight's position
        noNoEa = (bitboard << (17*4) ) & self.NOT_A_FILE 
        noEaEa = (bitboard << (10*4)) & self.NOT_AB_FILE
        soEaEa = (bitboard >>  (6*4)) & self.NOT_AB_FILE
        soSoEa = (bitboard >> (15*4)) & self.NOT_A_FILE 
        noNoWe = (bitboard << (15*4)) & self.NOT_H_FILE 
        noWeWe = (bitboard <<  (6*4)) & self.NOT_GH_FILE
        soWeWe = (bitboard >> (10*4)) & self.NOT_GH_FILE
        soSoWe = (bitboard >> (17*4)) & self.NOT_H_FILE 

        valid_moves = noNoEa | noEaEa | soEaEa | soSoEa | noNoWe | noWeWe | soWeWe | soSoWe

        if self.get_color_to_move_bit() == self.WHITE:
            valid_moves = valid_moves & ~self.whitePiece  # Exclude friendly pieces
            valid_moves = valid_moves | (valid_moves & self.blackPiece)  # Include enemy pieces (captures)
        else:
            valid_moves = valid_moves & ~self.blackPiece  # Exclude friendly pieces
            valid_moves = valid_moves | (valid_moves & self.whitePiece)  # Include enemy pieces (captures)

        past_move = self.WHITE | self.KNIGHT if self.get_color_to_move_bit() == self.WHITE else self.BLACK | self.KNIGHT
        next_to_move = self.BLACK if self.get_color_to_move_bit() == self.WHITE else self.WHITE

        if noNoEa & valid_moves:
            new_boards.append(Board((self.board ^ bitboard) | noNoEa, next_to_move, past_move))
 
        if noEaEa & valid_moves: 
            new_boards.append(Board((self.board ^ bitboard) | noEaEa,next_to_move, past_move))

        if soEaEa & valid_moves: 
            new_boards.append(Board((self.board ^ bitboard) | soEaEa,next_to_move, past_move))
 
        if soSoEa & valid_moves: 
            new_boards.append(Board((self.board ^ bitboard) | soSoEa,next_to_move, past_move))

        if noNoWe & valid_moves: 
            new_boards.append(Board((self.board ^ bitboard) | noNoWe,next_to_move, past_move))
 
        if noWeWe & valid_moves: 
            new_boards.append(Board((self.board ^ bitboard) | noWeWe,next_to_move, past_move))

        if soWeWe & valid_moves: 
            new_boards.append(Board((self.board ^ bitboard) | soWeWe,next_to_move, past_move))

        if soSoWe & valid_moves: 
            new_boards.append(Board((self.board ^ bitboard) | soSoWe,next_to_move, past_move))

        return new_boards


    '''Given any board hex representation,
    outputs a list of other board hex representations 
    of each possible other game state '''
    def get_all_possible_next_board_states(self):
        pos_moves = 0

        color_to_move = self.get_color_to_move_bit()
        castle_rights = self.get_castle_bits()
        en_passant_state = self.get_en_passant_state()
        last_move = self.get_last_move_bits()

        all_pos_states = []

        for i in range(64):
            square = self.get_piece_from_square(i)
            piece = square & self.PIECE_MASK
            color = square & self.COLOR_MASK


            if color != color_to_move or square == 0:
                pass
            elif piece == self.KNIGHT:
                all_pos_states += self.knight_moves(square << (i * 4))


        print([hex(move.board) for move in all_pos_states])

        

def main():
    
    board = Board()
    # board.print_board_hex()
    # board.number_board()

    # print(get_all_possible_next_board_states(board, white_pieces, black_pieces))

    board.get_all_possible_next_board_states()



if __name__ == "__main__":
    main()


# '''NOT CURRENTLY BEING USED : Function takes in piece ?? outputs color integer??'''
#     def get_color(self, color_mask):
#         if (color_mask & WHITE) != 0:
#             return WHITE  # White piece
#         elif (color_mask & BLACK) != 0:
#             return BLACK  # Black piece
#         else:
#             return PIECE_MASK  # No piece at the specified position


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


