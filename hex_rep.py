

class Board:
    ''' 
    Board class for representing a chess board 

    INDEXES: bits 0-255 (hex bit 0-63)
    256 bit, 64 hex bit representation. Every 4 bits (1hex) is a piece
    0___ -> the piece mask
    _000 -> the color of the piece
    
    important outputs: Board.getallnextboardstates 
        -> outputs all legal moves from a position including thier game states
        

    Bits beyond 256 are state bits: 
    the 64th hex bit
    STATE: value === 0 (WHITE) then white to move
    STATE: value === 8 (BLACK) then black to move
    STATE: value === 0 + 1 (WHITE + 1) then white checkmate
    STATE: value === 8 + 1 (BLACK + 1) then black checkmate
    
    the 65th digit from the hex number
    STATE: 0b0001  represents king side castle WHITE
    STATE: 0b0010 represents queen side castle WHITE
    STATE: 0b0100 represents king side caslte BLACK
    STATE: 0b1000 represents queen side caslte BLACK

    All state values are 0 for available and 1 for not available
    - if king moves, all state set to 1
    - if rook moves on queen or king side, that state is set to 1
    

    extracts the 66th digit from the hex number
    the 66th digit will hold state 
    value: 0 - NO EN passant
    value: 1 - last move was a pawn that was moved 2

    67th
    this bit will hold where the last piece square ended on - for en passant
    00xx where xx is a number between 0-63
    
    ARCHIVE LAST MOVE # this bit will hold the last piece that was moved stored in the 67th hex digit
                      # helpful for en passant, if state en passant is 1, this will say if the last move is legal or not'''

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

    # COLOR_TO_MOVE = 64
    # CASTLE_STATES = 65
    # EN_PASSANT_STATE = 66
    # LAST_END_SQUARE = 67

    ALL_DEFINED = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
    
    NOT_RANK_1 = ~0x00000000000000000000000000000000000000000000000000000000ffffffff
    NOT_RANK_8 = ~0xffffffff00000000000000000000000000000000000000000000000000000000



    @staticmethod
    def noNoEa(x):
        return (x << (17 * 4)) & Board.NOT_A_FILE

    @staticmethod
    def noEaEa(x):
        return (x << (10 * 4)) & Board.NOT_AB_FILE

    @staticmethod
    def soEaEa(x):
        return (x >> (6 * 4)) & Board.NOT_AB_FILE

    @staticmethod
    def soSoEa(x):
        return (x >> (15 * 4)) & Board.NOT_A_FILE

    @staticmethod
    def noNoWe(x):
        return (x << (15 * 4)) & Board.NOT_H_FILE

    @staticmethod
    def noWeWe(x):
        return (x << (6 * 4)) & Board.NOT_GH_FILE

    @staticmethod
    def soWeWe(x):
        return (x >> (10 * 4)) & Board.NOT_GH_FILE

    @staticmethod
    def soSoWe(x):
        return (x >> (17 * 4)) & Board.NOT_H_FILE
    
    @staticmethod
    def nortOne(b):
        return b << (8 * 4)
    
    @staticmethod
    def soutOne(b):
        return b >> (8 * 4)

    @staticmethod
    def eastOne(b):
        return (b << (1*4)) & Board.NOT_A_FILE

    @staticmethod
    def noEaOne(b):
        return (b << (9*4)) & Board.NOT_A_FILE

    @staticmethod
    def soEaOne(b):
        return (b >> (7*4)) & Board.NOT_A_FILE

    @staticmethod
    def westOne(b):
        return (b >> (1*4)) & Board.NOT_H_FILE

    @staticmethod
    def soWeOne(b):
        return (b >> (9*4)) & Board.NOT_H_FILE

    @staticmethod
    def noWeOne(b):
        return (b << (7*4)) & Board.NOT_H_FILE



    def __init__(self, board=None, color_to_move=WHITE, attack_board = 0x0, last_end_square=0x0, can_en_passant=0x0,fpgn=None) -> None:
        self.board = board
        # print(self.board)
        self.color_to_move = color_to_move
        self.last_end_square = last_end_square
        self.castle_states = 0
        self.can_en_passant= can_en_passant

        if board == None: 
            self.testPos()
            # self.getStartPos()

        self.whitePiece, self.blackPiece = self.getWhiteBlackMasks()
        # self.attack_squares = attack_board        
        self.special_board_states: list[list] = [] 
        # next_boards = []

        self.pawn_attacks = 0x0
        self.knight_attacks = 0x0
        self.rook_attacks = 0x0
        self.bishop_attacks = 0x0
        self.queen_attacks = 0x0
        self.king_attacks = 0x0

    def testPos(self):
        self.board = 0x0
        self.add_piece(0, self.WHITE | self.ROOK)
        self.add_piece( 1, self.WHITE | self.KNIGHT)
        # self.add_piece( 2, self.WHITE | self.BISHOP)
        self.add_piece( 3, self.WHITE | self.QUEEN)
        self.add_piece( 4, self.WHITE | self.KING)
        # self.add_piece( 5, self.WHITE | self.BISHOP)
        self.add_piece( 6, self.WHITE | self.KNIGHT)
        self.add_piece( 7, self.WHITE | self.ROOK)
        self.add_piece(32, self.WHITE | self.PAWN)
        self.add_piece(39, self.WHITE | self.PAWN)
        self.add_piece( 35, self.WHITE | self.BISHOP)

        
        # for i in range(8, 16):
        #     self.add_piece( i, self.WHITE | self.PAWN)
        # for i in range(48, 56):
        #     self.add_piece( i, self.BLACK | self.PAWN)
        self.add_piece( 56, self.BLACK | self.ROOK)
        self.add_piece( 57, self.BLACK | self.KNIGHT)
        self.add_piece( 58, self.BLACK | self.BISHOP)
        self.add_piece( 59, self.BLACK | self.QUEEN)
        # self.add_piece( 60, self.BLACK | self.KING)
        self.add_piece( 61, self.BLACK | self.BISHOP)
        self.add_piece( 62, self.BLACK | self.KNIGHT)
        self.add_piece( 63, self.BLACK | self.ROOK)
        
        # self.add_piece( 33, self.WHITE | self.KNIGHT)
        self.add_piece( 44, self.WHITE | self.ROOK)

        self.color_to_move = 0x0
        self.last_end_square = 0x0
        self.castle_states = 0x0
        self.can_en_passant= 0x0

    def slidingTest(self):
        self.board = 0x0
        self.add_piece(0, self.WHITE | self.ROOK)
        self.add_piece( 1, self.WHITE | self.KNIGHT)
        self.add_piece( 2, self.WHITE | self.BISHOP)
        self.add_piece( 3, self.WHITE | self.QUEEN)
        self.add_piece( 4, self.WHITE | self.KING)
        self.add_piece( 5, self.WHITE | self.BISHOP)
        self.add_piece( 6, self.WHITE | self.KNIGHT)
        self.add_piece( 7, self.WHITE | self.ROOK)
        self.add_piece(32, self.WHITE | self.PAWN)
        self.add_piece(39, self.WHITE | self.PAWN)
        
        # for i in range(8, 16):
        #     self.add_piece( i, self.WHITE | self.PAWN)
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
        
        # self.add_piece( 33, self.WHITE | self.KNIGHT)
        self.add_piece( 36, self.WHITE | self.ROOK)

        self.color_to_move = 0x0
        self.last_end_square = 0x0
        self.castle_states = 0x0
        self.can_en_passant= 0x0

    def testEnPassant(self):
        self.board = 0x0
        self.add_piece(0, self.WHITE | self.ROOK)
        self.add_piece( 1, self.WHITE | self.KNIGHT)
        self.add_piece( 2, self.WHITE | self.BISHOP)
        self.add_piece( 3, self.WHITE | self.QUEEN)
        self.add_piece( 4, self.WHITE | self.KING)
        self.add_piece( 5, self.WHITE | self.BISHOP)
        self.add_piece( 6, self.WHITE | self.KNIGHT)
        self.add_piece( 7, self.WHITE | self.ROOK)
        # for i in range(8, 16):
        #     self.add_piece( i, self.WHITE | self.PAWN)
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
        
        self.add_piece( 33, self.BLACK | self.PAWN)
        self.add_piece( 32, self.WHITE | self.PAWN)

        self.color_to_move = 0x0
        self.last_end_square = 33
        self.castle_states = 0x0
        self.can_en_passant= 0x1

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

        # print(hex(whiteMask), hex(blackMask))

        return whiteMask, blackMask


    '''Takes in a hex number and a hex digit to add, returns the hex number with the new digit'''
    def add_rightmost_hex_digit(self, number, digit_piece):
        updated_board = (number << 4) | digit_piece
        return updated_board

    '''removed the piece at the given square from 0-63, ie converts the hex number at this square to 0'''
    def clear_piece(self, position):
        self.board = self.board & ~(0xF << (position * 4))

    '''adds the piece at the given square from 0-63, ie converts the hex number at this square to 0'''
    def add_piece(self, square, piece):
        hex_piece = piece << (square * 4)
        self.board = self.board | hex_piece

    '''Given a board and a square, returns the hex number at the square
    other returns the square on a board not self'''
    def get_piece_from_square(self, square, other=None):
        if other:
            return other >> (square * 4) & 0xF
        return self.board >> (square * 4) & 0xF
    
    def set_square(self, square, num):
        self.clear_piece(square)
        self.add_piece(square, num)

    '''a board with 1 piece one it ie 100100000000
    looks for the 1 piece and returns how many squares from the beginning it is
    for en passant past move square check'''
    def get_square_from_piece(self,hex_number):
        count = 0
        while hex_number & 0xF == 0:
            hex_number >>= 4
            count += 1
            if hex_number == 0:
                return None  # No non-zero hex digit found
        return count
        
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
        print("Game State: " + str(hex(self.color_to_move)))
        print("Castling State: " + str(bin(self.castle_states)))
        print("En Passant State: " + str(hex(self.can_en_passant)))
        print("Last Move: " + str(hex(self.last_end_square)))

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


    def knight_moves(self, piece, start_square):
        next_boards = []

        bitboard = piece << (start_square * 4) 
        next_boards.append(bitboard)

        clear = 0xF << (start_square * 4)

        noNoEa = self.noNoEa(clear)
        noEaEa = self.noEaEa(clear)
        soEaEa = self.soEaEa(clear)
        soSoEa = self.soSoEa(clear)
        noNoWe = self.noNoWe(clear)
        noWeWe = self.noWeWe(clear)
        soWeWe = self.soWeWe(clear)
        soSoWe = self.soSoWe(clear)

        next_boards.append(noNoEa)
        next_boards.append(noEaEa)
        next_boards.append(soEaEa)
        next_boards.append(soSoEa)
        next_boards.append(noNoWe)
        next_boards.append(noWeWe)
        next_boards.append(soWeWe)
        next_boards.append(soSoWe)

        self.knight_attacks |= noNoEa | noEaEa | soEaEa | soSoEa | noNoWe | noWeWe | soWeWe | soSoWe

        return next_boards
    

    def pawn_moves_white(self, piece, start_square):
        next_boards = []

        bitboard = piece << (start_square * 4) 
        clear = 0xF << (start_square * 4)

        nortOne =  self.nortOne(bitboard) & ~self.whitePiece & ~self.blackPiece
        nortOne_clear = self.nortOne(clear) & ~self.whitePiece & ~self.blackPiece
        
        noWeOne = self.noWeOne(bitboard) & self.NOT_H_FILE & ~self.whitePiece & self.blackPiece
        noEaOne = self.noEaOne(bitboard) & self.NOT_A_FILE & ~self.whitePiece & self.blackPiece

        noWeOne_clear = self.noWeOne(clear) & self.NOT_H_FILE & ~self.whitePiece & self.blackPiece
        noEaOne_clear = self.noEaOne(clear) & self.NOT_A_FILE & ~self.whitePiece & self.blackPiece

        if self.can_en_passant:
            last_end = self.last_end_square

            # print(last_end, start_square)
            if last_end >= 32 and last_end <= 39 and start_square >= 32 and start_square <= 39:
                # print('in')

                if last_end == start_square - 1:
                    next_boards.append((((self.board ^ bitboard)) | self.noWeOne(bitboard)) & ~(0xF << (last_end * 4)))
                    self.pawn_attacks = self.pawn_attacks | self.noWeOne(clear)
                if last_end == start_square + 1:
                    next_boards.append((((self.board ^ bitboard)) | self.noEaOne(bitboard)) & ~(0xF << (last_end * 4)))
                    self.pawn_attacks = self.pawn_attacks | self.noEaOne(clear)


        if (start_square >= 8 and start_square <= 15 and nortOne):
            nortTwo = self.nortOne(nortOne) & ~self.whitePiece & ~self.blackPiece
            if nortTwo:
                nortTwo_clear = self.nortOne(nortOne_clear) & ~self.whitePiece & ~self.blackPiece
                # print(self.get_square_from_piece(nortTwo_clear))
                self.special_board_states.append([((self.board ^ bitboard) & ~nortTwo_clear) | nortTwo, self.get_square_from_piece(nortTwo_clear), 1])

        if noWeOne: 
            next_boards.append(((self.board ^ bitboard) & ~noWeOne_clear) | noWeOne)
            # self.pawn_attacks = self.pawn_attacks | noWeOne_clear

        if noEaOne:
            next_boards.append(((self.board ^ bitboard) & ~noEaOne_clear) | noEaOne)
            # self.pawn_attacks = self.pawn_attacks | noEaOne_clear

        if nortOne:
            next_boards.append(((self.board ^ bitboard) & ~nortOne_clear) | nortOne)
            # self.pawn_attacks = self.pawn_attacks | nortOne_clear

        self.pawn_attacks = self.pawn_attacks | self.noWeOne(clear)
        self.pawn_attacks = self.pawn_attacks | self.noEaOne(clear)

        return next_boards
    
    
    def pawn_moves_black(self, piece, start_square):
        next_boards = []

        bitboard = piece << (start_square * 4) 
        clear = 0xF << (start_square * 4)

        soutOne = self.soutOne(bitboard) & ~self.whitePiece & ~self.blackPiece
        soutOne_clear = self.soutOne(clear) & ~self.whitePiece & ~self.blackPiece
        
        soWeOne = self.soWeOne(bitboard) & self.NOT_H_FILE & ~self.blackPiece & self.whitePiece
        soEaOne = self.soEaOne(bitboard) & self.NOT_A_FILE & ~self.blackPiece & self.whitePiece

        soWeOne_clear = self.soWeOne(clear) & self.NOT_H_FILE & ~self.blackPiece & self.whitePiece
        soEaOne_clear = self.soEaOne(clear) & self.NOT_A_FILE & ~self.blackPiece & self.whitePiece

        if self.can_en_passant:
            last_end = (self.last_end_square)

            if last_end >= 24 and last_end <= 31 and start_square >= 24 and start_square <= 31:
                if last_end == start_square - 1:
                    next_boards.append((((self.board ^ bitboard)) | self.soWeOne(bitboard)) & ~(0xF << (last_end * 4)))
                    self.pawn_attacks = self.pawn_attacks | self.soWeOne(clear)
                if last_end == start_square + 1:
                    next_boards.append((((self.board ^ bitboard)) | self.soEaOne(bitboard)) & ~(0xF << (last_end * 4)))
                    self.pawn_attacks = self.pawn_attacks | self.soEaOne(clear)

        if (start_square >= 48 and start_square <= 55 and soutOne):
            soutTwo = self.soutOne(soutOne) & ~self.whitePiece & ~self.blackPiece
            if soutTwo:
                soutTwo_clear = self.soutOne(soutOne_clear) & ~self.whitePiece & ~self.blackPiece
                self.special_board_states.append([((self.board ^ bitboard) & ~soutTwo_clear) | soutTwo, self.get_square_from_piece(soutTwo_clear), 1])

        if soWeOne: 
            next_boards.append(((self.board ^ bitboard) & ~soWeOne_clear) | soWeOne)
            # self.pawn_attacks = self.pawn_attacks | soWeOne_clear

        if soEaOne:
            next_boards.append(((self.board ^ bitboard) & ~soEaOne_clear) | soEaOne)
            # self.pawn_attacks = self.pawn_attacks | soEaOne_clear

        if soutOne:
            next_boards.append(((self.board ^ bitboard) & ~soutOne_clear) | soutOne)
            # self.pawn_attacks = self.pawn_attacks | soutOne_clear

        self.pawn_attacks = self.pawn_attacks | self.soWeOne(clear)
        self.pawn_attacks = self.pawn_attacks | self.soEaOne(clear)

        return next_boards


    
    def getNoSlide(self, bitboard, clear, attack_square_to_add):
        next_boards = []

        color_to_move = self.color_to_move

        nortOne_clear = self.nortOne(clear)
                
        not_blocked = nortOne_clear & self.whitePiece == 0 if color_to_move == self.WHITE else nortOne_clear & self.blackPiece == 0 

        opposite_taken = False
        
        while nortOne_clear & self.NOT_RANK_8 and not_blocked and not opposite_taken:
            
            opposite_taken = nortOne_clear & self.blackPiece != 0 if color_to_move == self.WHITE else nortOne_clear & self.whitePiece != 0

            next_boards.append(nortOne_clear)
            attack_square_to_add = attack_square_to_add | nortOne_clear

            nortOne_clear = self.nortOne(nortOne_clear)
            not_blocked = nortOne_clear & self.whitePiece == 0 if color_to_move == self.WHITE else nortOne_clear & self.blackPiece == 0
            
            if not not_blocked:
                attack_square_to_add = attack_square_to_add | nortOne_clear
        
        if nortOne_clear & ~self.NOT_RANK_8 and not_blocked and not opposite_taken:
            next_boards.append(nortOne_clear)
            attack_square_to_add = attack_square_to_add | nortOne_clear

        return next_boards


    def getSoSlide(self, bitboard, clear, attack_square_to_add):
        next_boards = []

        color_to_move = self.color_to_move

        soutOne_clear = self.soutOne(clear)
                
        not_blocked = soutOne_clear & self.whitePiece == 0 if color_to_move == self.WHITE else soutOne_clear & self.blackPiece == 0 

        opposite_taken = False
        
        while soutOne_clear & self.NOT_RANK_1 and not_blocked and not opposite_taken:
            opposite_taken = soutOne_clear & self.blackPiece != 0 if color_to_move == self.WHITE else soutOne_clear & self.whitePiece != 0
            
            next_boards.append(soutOne_clear)
            attack_square_to_add = attack_square_to_add | soutOne_clear
            
            soutOne_clear = self.soutOne(soutOne_clear)
            not_blocked = soutOne_clear & self.whitePiece == 0 if color_to_move == self.WHITE else soutOne_clear & self.blackPiece == 0
           
            if not not_blocked:
                attack_square_to_add = attack_square_to_add | soutOne_clear


        if soutOne_clear & ~self.NOT_RANK_1 and not_blocked and not opposite_taken:
            next_boards.append(soutOne_clear)
            attack_square_to_add = attack_square_to_add | soutOne_clear


        return next_boards


    def getEaSlide(self, bitboard, clear, attack_square_to_add):
        next_boards = []

        color_to_move = self.color_to_move

        eastOne_clear = self.eastOne(clear)
                
        not_blocked = eastOne_clear & self.whitePiece == 0 if color_to_move == self.WHITE else eastOne_clear & self.blackPiece == 0 

        opposite_taken = False
        
        while eastOne_clear & self.NOT_H_FILE and not_blocked and not opposite_taken:
            opposite_taken = eastOne_clear & self.blackPiece != 0 if color_to_move == self.WHITE else eastOne_clear & self.whitePiece != 0

            next_boards.append(eastOne_clear)
            attack_square_to_add = attack_square_to_add | eastOne_clear

            eastOne_clear = self.eastOne(eastOne_clear)
            not_blocked = eastOne_clear & self.whitePiece == 0 if color_to_move == self.WHITE else eastOne_clear & self.blackPiece == 0
           
            if not not_blocked:
                attack_square_to_add = attack_square_to_add | eastOne_clear
          
        if eastOne_clear & ~self.NOT_H_FILE and not_blocked and not opposite_taken:
            next_boards.append(eastOne_clear)
            attack_square_to_add = attack_square_to_add | eastOne_clear



        return next_boards


    def getWeSlide(self, bitboard, clear, attack_square_to_add):
        next_boards = []

        color_to_move = self.color_to_move

        westOne_clear = self.westOne(clear)
                
        not_blocked = westOne_clear & self.whitePiece == 0 if color_to_move == self.WHITE else westOne_clear & self.blackPiece == 0 

        opposite_taken = False
        
        while westOne_clear & self.NOT_A_FILE and not_blocked and not opposite_taken:
            opposite_taken = westOne_clear & self.blackPiece != 0 if color_to_move == self.WHITE else westOne_clear & self.whitePiece != 0

            next_boards.append(westOne_clear)
            attack_square_to_add = attack_square_to_add | westOne_clear
            
            westOne_clear = self.westOne(westOne_clear)
            not_blocked = westOne_clear & self.whitePiece == 0 if color_to_move == self.WHITE else westOne_clear & self.blackPiece == 0

            if not not_blocked:
                attack_square_to_add = attack_square_to_add | westOne_clear


        if westOne_clear & ~self.NOT_A_FILE and not_blocked and not opposite_taken:
            next_boards.append(westOne_clear)
            attack_square_to_add = attack_square_to_add | westOne_clear

       

        return next_boards
    
    
    def getNoEaSlide(self, bitboard, clear, attack_square_to_add):
        next_boards = []

        color_to_move = self.color_to_move

        noEaOne_clear = self.noEaOne(clear)
    
        not_blocked = noEaOne_clear & self.whitePiece == 0 if color_to_move == self.WHITE else noEaOne_clear & self.blackPiece == 0 

        opposite_taken = False
        
        while noEaOne_clear & self.NOT_RANK_8 and noEaOne_clear & self.NOT_H_FILE and not_blocked and not opposite_taken:
            opposite_taken = noEaOne_clear & self.blackPiece != 0 if color_to_move == self.WHITE else noEaOne_clear & self.whitePiece != 0
            
            next_boards.append(noEaOne_clear)
            attack_square_to_add = attack_square_to_add | noEaOne_clear
            
            noEaOne_clear = self.noEaOne(noEaOne_clear)
            not_blocked = noEaOne_clear & self.whitePiece == 0 if color_to_move == self.WHITE else noEaOne_clear & self.blackPiece == 0
            
            if not not_blocked:
                attack_square_to_add = attack_square_to_add | noEaOne_clear


        if noEaOne_clear & ~self.NOT_RANK_8 and not_blocked and not opposite_taken:
            next_boards.append(noEaOne_clear)
            attack_square_to_add = attack_square_to_add | noEaOne_clear


        if noEaOne_clear & ~self.NOT_H_FILE and not_blocked and not opposite_taken:
            next_boards.append(noEaOne_clear)
            attack_square_to_add = attack_square_to_add | noEaOne_clear


        return next_boards
    
    def getNoWeSlide(self, bitboard, clear, attack_square_to_add):
        next_boards = []

        color_to_move = self.color_to_move

        noWeOne_clear = self.noWeOne(clear)
    
        not_blocked = noWeOne_clear & self.whitePiece == 0 if color_to_move == self.WHITE else noWeOne_clear & self.blackPiece == 0 

        opposite_taken = False
        
        while noWeOne_clear & self.NOT_RANK_8 and noWeOne_clear & self.NOT_A_FILE and not_blocked and not opposite_taken:
            opposite_taken = noWeOne_clear & self.blackPiece != 0 if color_to_move == self.WHITE else noWeOne_clear & self.whitePiece != 0
            
            next_boards.append(noWeOne_clear)
            attack_square_to_add = attack_square_to_add | noWeOne_clear

            noWeOne_clear = self.noWeOne(noWeOne_clear)
            not_blocked = noWeOne_clear & self.whitePiece == 0 if color_to_move == self.WHITE else noWeOne_clear & self.blackPiece == 0
            
            if not not_blocked:
                attack_square_to_add = attack_square_to_add | noWeOne_clear


           
        if noWeOne_clear & ~self.NOT_RANK_8 and not_blocked and not opposite_taken:
            next_boards.append(noWeOne_clear)
            attack_square_to_add = attack_square_to_add | noWeOne_clear

         
        if noWeOne_clear & ~self.NOT_A_FILE and not_blocked and not opposite_taken:
            next_boards.append(noWeOne_clear)
            attack_square_to_add = attack_square_to_add | noWeOne_clear


        return next_boards
    
    def getSoEaSlide(self, bitboard, clear, attack_square_to_add):
        next_boards = []

        color_to_move = self.color_to_move

        soEaOne_clear = self.soEaOne(clear)
    
        not_blocked = soEaOne_clear & self.whitePiece == 0 if color_to_move == self.WHITE else soEaOne_clear & self.blackPiece == 0 

        opposite_taken = False
        
        while soEaOne_clear & self.NOT_RANK_1 and soEaOne_clear & self.NOT_H_FILE and not_blocked and not opposite_taken:
            opposite_taken = soEaOne_clear & self.blackPiece != 0 if color_to_move == self.WHITE else soEaOne_clear & self.whitePiece != 0

            next_boards.append(soEaOne_clear)
            attack_square_to_add = attack_square_to_add | soEaOne_clear

            soEaOne_clear = self.soEaOne(soEaOne_clear)
            not_blocked = soEaOne_clear & self.whitePiece == 0 if color_to_move == self.WHITE else soEaOne_clear & self.blackPiece == 0

            if not not_blocked:
                attack_square_to_add = attack_square_to_add | soEaOne_clear

          
        if soEaOne_clear & ~self.NOT_RANK_1 and not_blocked and not opposite_taken:
            next_boards.append(soEaOne_clear)
            attack_square_to_add = attack_square_to_add | soEaOne_clear

          

        if soEaOne_clear & ~self.NOT_H_FILE and not_blocked and not opposite_taken:
            next_boards.append(soEaOne_clear)
            attack_square_to_add = attack_square_to_add | soEaOne_clear


        return next_boards
    
    def getSoWeSlide(self, bitboard, clear, attack_square_to_add):
        next_boards = []

        color_to_move = self.color_to_move

        soWeOne_clear = self.soWeOne(clear)
    
        not_blocked = soWeOne_clear & self.whitePiece == 0 if color_to_move == self.WHITE else soWeOne_clear & self.blackPiece == 0 

        opposite_taken = False
        
        while soWeOne_clear & self.NOT_RANK_1 and soWeOne_clear & self.NOT_A_FILE and not_blocked and not opposite_taken:
            opposite_taken = soWeOne_clear & self.blackPiece != 0 if color_to_move == self.WHITE else soWeOne_clear & self.whitePiece != 0

            next_boards.append(soWeOne_clear)
            attack_square_to_add = attack_square_to_add | soWeOne_clear

            soWeOne_clear = self.soWeOne(soWeOne_clear)
            not_blocked = soWeOne_clear & self.whitePiece == 0 if color_to_move == self.WHITE else soWeOne_clear & self.blackPiece == 0

            if not not_blocked:
                attack_square_to_add = attack_square_to_add | soWeOne_clear

        if soWeOne_clear & ~self.NOT_RANK_1 and not_blocked and not opposite_taken:
            next_boards.append(soWeOne_clear)
            attack_square_to_add = attack_square_to_add | soWeOne_clear


        if soWeOne_clear & ~self.NOT_A_FILE and not_blocked and not opposite_taken:
            next_boards.append(soWeOne_clear)
            attack_square_to_add = attack_square_to_add | soWeOne_clear

        print('here')
        print(hex(attack_square_to_add))

        return next_boards
        
    
    def getSlide(self, clear, direction, boundary1, boundary2, attack_square_to_add):
        next_boards = []

        color_to_move = self.color_to_move
        dir_clear = direction(clear)
    
        # conditions
        not_blocked = dir_clear & self.whitePiece == 0 if color_to_move == self.WHITE else dir_clear & self.blackPiece == 0 
        opposite_taken = False

        # add boards
        while not_blocked and not opposite_taken and dir_clear & boundary1 and (boundary2 is None or dir_clear & boundary2):
            opposite_taken = dir_clear & self.blackPiece != 0 if color_to_move == self.WHITE else dir_clear & self.whitePiece != 0

            next_boards.append(dir_clear)
            attack_square_to_add |= dir_clear

            dir_clear = direction(dir_clear)
            not_blocked = dir_clear & self.whitePiece == 0 if color_to_move == self.WHITE else dir_clear & self.blackPiece == 0

            if not not_blocked:
                attack_square_to_add = attack_square_to_add | dir_clear

        
        if dir_clear & ~boundary1 and not_blocked and not opposite_taken:
            next_boards.append(dir_clear)

        if boundary2 is not None and dir_clear & ~boundary2 and not_blocked and not opposite_taken:
            next_boards.append(dir_clear)


        return next_boards


    def rook_moves(self, piece, start_square):
        next_boards = []

        bitboard = piece << (start_square * 4) # square the piece is on with piece 
        next_boards.append(bitboard)

        clear = 0xF << (start_square * 4) # square the piece is on with 0xf
        
        noSlide = self.getNoSlide(bitboard, clear, self.rook_attacks)
        eaSlide = self.getEaSlide(bitboard, clear, self.rook_attacks)
        soSlide = self.getSoSlide(bitboard, clear, self.rook_attacks)
        weSlide = self.getWeSlide(bitboard, clear, self.rook_attacks)

        next_boards += noSlide
        next_boards += eaSlide
        next_boards += soSlide
        next_boards += weSlide

        print('hrheg')
        print(hex(self.rook_attacks))

        return next_boards

    def bishop_moves(self, piece, start_square):
        next_boards = []

        bitboard = piece << (start_square * 4) # square the piece is on with piece 
        next_boards.append(bitboard)

        clear = 0xF << (start_square * 4) # square the piece is on with 0xf

        noEaSlide = self.getNoEaSlide(bitboard, clear, self.bishop_attacks)
        noWeSlide = self.getNoWeSlide(bitboard, clear, self.bishop_attacks)
        soEaSlide = self.getSoEaSlide(bitboard, clear, self.bishop_attacks)
        soWeSlide = self.getSoWeSlide(bitboard, clear, self.bishop_attacks)

        next_boards += (noEaSlide)
        next_boards += (noWeSlide)
        next_boards += (soEaSlide)
        next_boards += (soWeSlide)
        

        self.bishop_attacks = noEaSlide | noWeSlide | soEaSlide | soWeSlide

        return next_boards
    
    def queen_moves(self, piece, start_square):
        next_boards = []

        bitboard = piece << (start_square * 4)
        next_boards.append(bitboard)

        clear = 0xF << (start_square * 4) 
        
        noSlide = self.getNoSlide(bitboard, clear, self.queen_attacks)
        eaSlide = self.getEaSlide(bitboard, clear, self.queen_attacks)
        soSlide = self.getSoSlide(bitboard, clear, self.queen_attacks)
        weSlide = self.getWeSlide(bitboard, clear, self.queen_attacks)

        next_boards+=(noSlide)
        next_boards+=(eaSlide)
        next_boards+=(soSlide)
        next_boards+=(weSlide)

        noEaSlide = self.getNoEaSlide(bitboard, clear, self.queen_attacks)
        noWeSlide = self.getNoWeSlide(bitboard, clear, self.queen_attacks)
        soEaSlide = self.getSoEaSlide(bitboard, clear, self.queen_attacks)
        soWeSlide = self.getSoWeSlide(bitboard, clear, self.queen_attacks)

        next_boards+=(noEaSlide)
        next_boards+=(noWeSlide)
        next_boards+=(soEaSlide)
        next_boards+=(soWeSlide)

        # self.queen_attacks = noSlide | eaSlide | soSlide | weSlide | noEaSlide | noWeSlide | soEaSlide | soWeSlide

        return next_boards
    
    def king_moves(self, piece, start_square):
        new_boards = []

        bitboard = piece << (start_square * 4)
        clear = 0xF << (start_square * 4) 

        nortOne = self.nortOne(bitboard)
        soutOne = self.soutOne(bitboard)
        eastOne = self.eastOne(bitboard)
        westOne = self.westOne(bitboard)
        noEaOne = self.noEaOne(bitboard)
        noWeOne = self.noWeOne(bitboard)
        soEaOne = self.soEaOne(bitboard)
        soWeOne = self.soWeOne(bitboard)

        nortOne_clear = self.nortOne(clear)
        soutOne_clear = self.soutOne(clear)
        eastOne_clear = self.eastOne(clear)
        westOne_clear = self.westOne(clear)
        noEaOne_clear = self.noEaOne(clear)
        noWeOne_clear = self.noWeOne(clear)
        soEaOne_clear = self.soEaOne(clear)
        soWeOne_clear = self.soWeOne(clear)

        color_check = self.whitePiece if self.color_to_move == self.WHITE else self.blackPiece

        # if clear & self.NOT_RANK_8 & self.attack_squares & color_check == 0:
        #     new_boards.append(((self.board ^ bitboard) & ~nortOne_clear) | nortOne)

        return new_boards
        



    '''Given any board hex representation,
    outputs a list of other board hex representations 
    of each possible other game state '''
    def get_all_possible_next_board_states(self):
        pos_moves = 0

        next_rook_boards = []
        next_bishop_boards = []
        next_queen_boards = []
        next_knight_boards = []
        next_pawn_boards = []
        next_king_boards = []


        for i in range(64):
            
            square = self.get_piece_from_square(i)
            piece = square & self.PIECE_MASK
            color = square & self.COLOR_MASK


            if square == 0:
                pass
            elif square == self.PAWN | self.WHITE and self.color_to_move == self.WHITE:
                next_pawn_boards.append(self.pawn_moves_white(square, i))
            elif square == self.PAWN | self.BLACK and self.color_to_move == self.BLACK:
                next_pawn_boards.append(self.pawn_moves_black(square, i))
            elif color != self.color_to_move:
                pass
            elif piece == self.KNIGHT:
                next_knight_boards.append(self.knight_moves(square, i))

            elif square == self.ROOK:
                next_rook_boards.append(self.rook_moves(square, i))

            elif square == self.BISHOP:
                next_bishop_boards.append(self.bishop_moves(square, i))

            elif square == self.QUEEN:
                next_queen_boards.append(self.queen_moves(square, i))

            elif square == self.KING:
                next_king_boards.append(self.king_moves(square, i))


        all_boards = []
        next_move = self.BLACK if self.color_to_move == self.WHITE else self.WHITE


        valid_moves_w = lambda x: x & ~self.whitePiece | (x & self.blackPiece) 
        valid_moves_b = lambda x: x & ~self.blackPiece  | (x & self.whitePiece) 


        # print(hex(valid_moves))
        
        # for board in next_rook_boards:
        #     for move in board:
        #         self.print_board_hex(move)
        # # print(next_rook_boards)
        # for board in next_knight_boards:
        #     for move in board:
        #         self.print_board_hex(move)
        
        # print(next_knight_boards)
        # print(next_bishop_boards)
        # print(next_queen_boards)
        # print(next_king_boards)
        # print(next_pawn_boards)

        ALL_WHITE_KNIGHTS = 0x3333333333333333333333333333333333333333333333333333333333333333

        print(hex(self.pawn_attacks))
        print(hex(self.rook_attacks))
        print(hex(self.knight_attacks))
        print(hex(self.bishop_attacks))
        print(hex(self.queen_attacks))
        print(hex(self.king_attacks))



        knight_attack_board_base = self.pawn_attacks | self.rook_attacks | self.bishop_attacks | self.queen_attacks | self.king_attacks
        print(hex(knight_attack_board_base))
        # for knight_piece_moves in next_knight_boards:
        #     if knight_piece_moves:
        #         current_piece = knight_piece_moves.pop(0)
        #         for move in knight_piece_moves:
        #             # print(hex(move))
        #             if valid_moves_w(move):
        #                 temp = 0x0
        #                 temp = (self.board ^ current_piece) # remove current piece 
        #                 temp = temp & ~move # removes the piece at the move 
        #                 temp = temp | (move & ALL_WHITE_KNIGHTS) # adds the new piece with the right value
        #                 # print(hex(temp))
        #     # print("=====")

        # for rook_move_pieces in next_rook_boards:
        #     if rook_move_pieces: 
        #         current_piece = rook_move_pieces.pop(0)
        #         for move in rook_move_pieces:
        #             # print(hex(move))


                


        # for next_board_hex_only in next_boards:
        #     # self.print_board_hex(next_board_hex_only)
        #     all_boards.append(Board(board = next_board_hex_only, color_to_move=next_move, attack_board=self.attack_squares))

        # for hex_rep, end_square, en_passant in self.special_board_states:
        #     all_boards.append(Board(board = hex_rep, color_to_move=next_move, attack_board=self.attack_squares,
        #                          end_square=end_square, can_en_passant=en_passant ))

        # for board in all_boards:
        #     board.print_board_hex()

        # self.print_board_hex(self.attack_squares)


        

def main():
    
    board = Board()
    # board.print_board_hex()
    # board.number_)

    # print(get_all_possible_next_board_states(board, white_pieces, black_pieces))

    board.get_all_possible_next_board_states()
    # board.number_)



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


