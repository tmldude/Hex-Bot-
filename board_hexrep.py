from utils import add_rightmost_hex_digit


class HexBoard:
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

    # this bit will hold the last piece that was moved stored in the 67th hex digit
    ARCHIVE LAST MOVE
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

    # BOARD MASKS

    ALL_DEFINED = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

    ALL_WHITE = 0x0
    ALL_WHITE_PAWNS = 0x1111111111111111111111111111111111111111111111111111111111111111
    ALL_WHITE_ROOKS = 0x2222222222222222222222222222222222222222222222222222222222222222
    ALL_WHITE_KNIGHTS = 0x3333333333333333333333333333333333333333333333333333333333333333
    ALL_WHITE_BISHOPS = 0x4444444444444444444444444444444444444444444444444444444444444444
    ALL_WHITE_QUEENS = 0x5555555555555555555555555555555555555555555555555555555555555555
    ALL_WHITE_KINGS = 0x6666666666666666666666666666666666666666666666666666666666666666

    ALL_BLACK = 0x8888888888888888888888888888888888888888888888888888888888888888
    ALL_BLACK_PAWNS = ALL_WHITE_PAWNS | ALL_BLACK
    ALL_BLACK_ROOKS = ALL_WHITE_ROOKS | ALL_BLACK
    ALL_BLACK_KNIGHTS = ALL_WHITE_KNIGHTS | ALL_BLACK
    ALL_BLACK_BISHOPS = ALL_WHITE_BISHOPS | ALL_BLACK
    ALL_BLACK_QUEENS = ALL_WHITE_QUEENS | ALL_BLACK
    ALL_BLACK_KINGS = ALL_WHITE_KINGS | ALL_BLACK

    # BOUNDARIES

    NOT_A_FILE = 0xfffffff0fffffff0fffffff0fffffff0fffffff0fffffff0fffffff0fffffff0
    NOT_H_FILE = 0xfffffff0fffffff0fffffff0fffffff0fffffff0fffffff0fffffff0fffffff
    NOT_AB_FILE = 0xffffff00ffffff00ffffff00ffffff00ffffff00ffffff00ffffff00ffffff00
    NOT_GH_FILE = 0xffffff00ffffff00ffffff00ffffff00ffffff00ffffff00ffffff00ffffff

    NOT_RANK_1 = ~0x00000000000000000000000000000000000000000000000000000000ffffffff
    NOT_RANK_8 = ~0xffffffff00000000000000000000000000000000000000000000000000000000

    # COLOR_TO_MOVE = 64
    # CASTLE_STATES = 65
    # EN_PASSANT_STATE = 66
    # LAST_END_SQUARE = 67

    @staticmethod
    def noNoEa(x) -> int:
        return (x << (17 * 4)) & HexBoard.NOT_A_FILE

    @staticmethod
    def noEaEa(x) -> int:
        return (x << (10 * 4)) & HexBoard.NOT_AB_FILE

    @staticmethod
    def soEaEa(x) -> int:
        return (x >> (6 * 4)) & HexBoard.NOT_AB_FILE

    @staticmethod
    def soSoEa(x) -> int:
        return (x >> (15 * 4)) & HexBoard.NOT_A_FILE

    @staticmethod
    def noNoWe(x) -> int:
        return (x << (15 * 4)) & HexBoard.NOT_H_FILE

    @staticmethod
    def noWeWe(x) -> int:
        return (x << (6 * 4)) & HexBoard.NOT_GH_FILE

    @staticmethod
    def soWeWe(x) -> int:
        return (x >> (10 * 4)) & HexBoard.NOT_GH_FILE

    @staticmethod
    def soSoWe(x) -> int:
        return (x >> (17 * 4)) & HexBoard.NOT_H_FILE

    @staticmethod
    def nortOne(b) -> int:
        return b << (8 * 4)

    @staticmethod
    def soutOne(b) -> int:
        return b >> (8 * 4)

    @staticmethod
    def eastOne(b) -> int:
        return (b << (1*4)) & HexBoard.NOT_A_FILE

    @staticmethod
    def noEaOne(b) -> int:
        return (b << (9*4)) & HexBoard.NOT_A_FILE

    @staticmethod
    def soEaOne(b) -> int:
        return (b >> (7*4)) & HexBoard.NOT_A_FILE

    @staticmethod
    def westOne(b) -> int:
        return (b >> (1*4)) & HexBoard.NOT_H_FILE

    @staticmethod
    def soWeOne(b) -> int:
        return (b >> (9*4)) & HexBoard.NOT_H_FILE

    @staticmethod
    def noWeOne(b) -> int:
        return (b << (7*4)) & HexBoard.NOT_H_FILE

    def __init__(self, board=0, color_to_move=0, last_end_square=0x0, can_en_passant=0x0, en_passant_square_fen=None, castle_states=None, fpgn=None) -> None:
        self.board = board
        # print(self.board)
        # self.color_to_move = self.WHITE if color_to_move == self.BLACK else self.BLACK
        self.color_to_move = color_to_move
        self.last_end_square = last_end_square

        self.castle_states = castle_states if castle_states else {'white_king_moved': False,
                                                                  'black_king_moved': False,
                                                                  'QS_rook_b_moved': False,
                                                                  'QS_rook_w_moved': False,
                                                                  'KS_rook_b_moved': False,
                                                                  'KS_rook_w_moved': False, }

        self.can_en_passant = can_en_passant
        self.special_board_states: list[list] = []

        self.white_pieces, self.black_pieces = self._get_color_masks()
        self.attack_board = self.generate_attack_board(self.color_to_move)
        self.check_mate = False
        self.draw = False
        self.game_is_over = False
        self.en_passant_square_fen = en_passant_square_fen

        # self.print_board_hex()
        # self.print_board_hex(self.attack_board)

        # self.print_board_hex(self.generate_attack_board(color = self.WHITE if color_to_move == self.BLACK else self.WHITE))

    def _get_color_masks(self) -> tuple[int, int]:
        white_mask = 0
        black_mask = 0

        for i in range(63, -1, -1):

            square = self.get_piece_from_square(i)
            piece = square & self.PIECE_MASK
            color = square & self.COLOR_MASK

            if color == self.WHITE and piece != 0:
                white_mask = add_rightmost_hex_digit(white_mask, 0xF)
                black_mask = add_rightmost_hex_digit(black_mask, 0x0)
            elif color == self.BLACK and piece != 0:
                white_mask = add_rightmost_hex_digit(white_mask, 0x0)
                black_mask = add_rightmost_hex_digit(black_mask, 0xF)
            else:
                white_mask = add_rightmost_hex_digit(white_mask, 0x0)
                black_mask = add_rightmost_hex_digit(black_mask, 0x0)

        # print(hex(whiteMask), hex(blackMask))

        return white_mask, black_mask

    '''adds the piece at the given square from 0-63, ie converts the hex number at this square to 0'''

    def add_piece(self, square, piece):
        hex_piece = piece << (square * 4)
        self.board = self.board | hex_piece

    '''removed the piece at the given square from 0-63, ie converts the hex number at this square to 0'''

    def clear_piece(self, position):
        self.board = self.board & ~(0xF << (position * 4))

    def set_square(self, square, num):
        self.clear_piece(square)
        self.add_piece(square, num)

        '''Given a board and a square, returns the hex number at the square
    other returns the square on a board not self'''

    def get_piece_from_square(self, square, other=None) -> int:
        if other:
            return other >> (square * 4) & 0xF
        return self.board >> (square * 4) & 0xF

    '''a board with 1 piece one it ie 00100000000
    looks for the 1 piece and returns how many squares from the beginning it is
    for en passant past move square check'''

    def get_square_from_piece(self, hex_number) -> int:
        count: int = 0
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
                print_str = print_str + \
                    str(hex(self.get_piece_from_square(i * 8 + j)))[2:] + " "
            print_str = print_str + '\n'  # Add newline after each row

        print("\nBoard Values:")
        print(print_str)

    def print_board_hex(self, other=None):
        print_str = ''
        for i in range(7, -1, -1):  # Start from 7 and decrement to 0
            for j in range(8):
                if other:
                    print_str = print_str + \
                        str(hex(self.get_piece_from_square(
                            i * 8 + j, other)))[2:] + " "
                else:
                    print_str = print_str + \
                        str(hex(self.get_piece_from_square(
                            i * 8 + j)))[2:] + " "

            print_str = print_str + '\n'  # Add newline after each row

        print("\n hex Board Values:")
        print(print_str)

    '''
    for testing, prints,
    In starting positon 0 being the white rook, 63 being the black rook
            56 57 58 59 60 61 62 63
            48 49 50 51 52 53 54 55
            40 41 42 43 44 45 46 47
            32 33 34 35 36 37 38 39
            24 25 26 27 28 29 30 31
            16 17 18 19 20 21 22 23
             8  9 10 11 12 13 14 15
             0  1  2  3  4  5  6  7
    '''
    @staticmethod
    def print_number_board():
        string = ''
        for i in range(7, -1, -1):  # Start from 7 and decrement to 0
            for j in range(8):
                string = string + str(i * 8 + j) + " "
            string = string + '\n'  # Add newline after each row

        print(string)

    # MOVE FUNCTIONS

    # SLIDE MOVES

    def _getSlide(self, clear, direction, boundary1, boundary2):
        next_boards: list[int] = []

        dir_clear: int = direction(clear)
        not_blocked = True

        while not_blocked and (dir_clear & boundary1) and (dir_clear & boundary2):
            self.black_pieces != 0 if self.color_to_move == self.WHITE else dir_clear & self.white_pieces != 0
            next_boards.append(dir_clear)

            # update if hitting white or black piece to stop while loop
            not_blocked = dir_clear & self.white_pieces == 0 | dir_clear & self.black_pieces == 0
            # print(hex(not_blocked))
            # moving up, down, left, right, or diag one position
            dir_clear = direction(dir_clear)

        added = False
        if dir_clear & ~boundary1 and not_blocked:
            next_boards.append(dir_clear)
            added = True

        if dir_clear & ~boundary2 and not_blocked and not added:
            next_boards.append(dir_clear)

        return next_boards

    def getNoSlide(self, clear) -> list[int]:
        return self._getSlide(clear, HexBoard.nortOne, HexBoard.NOT_RANK_8, HexBoard.ALL_DEFINED)

    def getSoSlide(self, clear) -> list[int]:
        return self._getSlide(clear, HexBoard.soutOne, HexBoard.NOT_RANK_1, HexBoard.ALL_DEFINED)

    def getEaSlide(self, clear) -> list[int]:
        return self._getSlide(clear, HexBoard.eastOne, HexBoard.NOT_H_FILE, HexBoard.ALL_DEFINED)

    def getWeSlide(self, clear) -> list[int]:
        return self._getSlide(clear, HexBoard.westOne, HexBoard.NOT_A_FILE, HexBoard.ALL_DEFINED)

    def getNoEaSlide(self, clear) -> list[int]:
        return self._getSlide(clear, HexBoard.noEaOne, HexBoard.NOT_RANK_8, HexBoard.NOT_H_FILE)

    def getNoWeSlide(self, clear) -> list[int]:
        return self._getSlide(clear, HexBoard.noWeOne, HexBoard.NOT_RANK_8, HexBoard.NOT_A_FILE)

    def getSoEaSlide(self, clear) -> list[int]:
        return self._getSlide(clear, HexBoard.soEaOne, HexBoard.NOT_RANK_1, HexBoard.NOT_H_FILE)

    def getSoWeSlide(self, clear) -> list[int]:
        return self._getSlide(clear, HexBoard.soWeOne, HexBoard.NOT_RANK_1, HexBoard.NOT_A_FILE)

    # PAWN MOVES

    def pawn_moves_white(self, piece, start_square) -> list[int]:
        next_boards: list[int] = []

        bitboard = piece << (start_square * 4)
        clear = 0xF << (start_square * 4)

        nortOne = self.nortOne(
            bitboard) & ~self.white_pieces & ~self.black_pieces
        nortOne_clear = self.nortOne(
            clear) & ~self.white_pieces & ~self.black_pieces

        noWeOne = self.noWeOne(
            bitboard) & self.NOT_H_FILE & ~self.white_pieces & self.black_pieces
        noEaOne = self.noEaOne(
            bitboard) & self.NOT_A_FILE & ~self.white_pieces & self.black_pieces

        noWeOne_clear = self.noWeOne(
            clear) & self.NOT_H_FILE & ~self.white_pieces & self.black_pieces
        noEaOne_clear = self.noEaOne(
            clear) & self.NOT_A_FILE & ~self.white_pieces & self.black_pieces

        if self.can_en_passant:
            last_end = self.last_end_square

            # print(last_end, start_square)
            if last_end >= 32 and last_end <= 39 and start_square >= 32 and start_square <= 39:
                # print('in')

                if last_end == start_square - 1:
                    # next_boards.append((((self.board ^ bitboard)) | self.noWeOne(bitboard)) & ~(0xF << (last_end * 4)))
                    next_boards.append((((self.board ^ bitboard)) | self.noWeOne(
                        bitboard)) & ~(0xF << (last_end * 4)))

                    # self.pawn_attacks = self.pawn_attacks | self.noWeOne(clear)
                if last_end == start_square + 1:
                    next_boards.append((((self.board ^ bitboard)) | self.noEaOne(
                        bitboard)) & ~(0xF << (last_end * 4)))
                    # self.pawn_attacks = self.pawn_attacks | self.noEaOne(clear)

        if (start_square >= 8 and start_square <= 15 and nortOne):
            nortTwo = self.nortOne(
                nortOne) & ~self.white_pieces & ~self.black_pieces
            if nortTwo:
                nortTwo_clear = self.nortOne(
                    nortOne_clear) & ~self.white_pieces & ~self.black_pieces
                # print(self.get_square_from_piece(nortTwo_clear))
                self.special_board_states.append(
                    [((self.board ^ bitboard) & ~nortTwo_clear) | nortTwo, self.get_square_from_piece(nortTwo_clear), 1, self.get_square_from_piece(nortOne_clear)])

        if nortOne:
            # promotion check
            if start_square >= 48 and start_square <= 55:
                next_boards.append(
                    ((self.board ^ bitboard) & ~nortOne_clear) | (nortOne_clear & HexBoard.ALL_WHITE_ROOKS))
                next_boards.append(
                    ((self.board ^ bitboard) & ~nortOne_clear) | (nortOne_clear & HexBoard.ALL_WHITE_KNIGHTS))
                next_boards.append(
                    ((self.board ^ bitboard) & ~nortOne_clear) | (nortOne_clear & HexBoard.ALL_WHITE_BISHOPS))
                next_boards.append(
                    ((self.board ^ bitboard) & ~nortOne_clear) | (nortOne_clear & HexBoard.ALL_WHITE_QUEENS))
            else:
                next_boards.append(
                    ((self.board ^ bitboard) & ~nortOne_clear) | nortOne)

        if noWeOne:
            next_boards.append(
                ((self.board ^ bitboard) & ~noWeOne_clear) | noWeOne)

        if noEaOne:
            next_boards.append(
                ((self.board ^ bitboard) & ~noEaOne_clear) | noEaOne)

        return next_boards

    def pawn_moves_black(self, piece, start_square) -> list[int]:
        next_boards: list[int] = []

        bitboard = piece << (start_square * 4)
        clear = 0xF << (start_square * 4)

        soutOne = self.soutOne(
            bitboard) & ~self.white_pieces & ~self.black_pieces
        soutOne_clear = self.soutOne(
            clear) & ~self.white_pieces & ~self.black_pieces

        soWeOne = self.soWeOne(
            bitboard) & self.NOT_H_FILE & ~self.black_pieces & self.white_pieces
        soEaOne = self.soEaOne(
            bitboard) & self.NOT_A_FILE & ~self.black_pieces & self.white_pieces

        soWeOne_clear = self.soWeOne(
            clear) & self.NOT_H_FILE & ~self.black_pieces & self.white_pieces
        soEaOne_clear = self.soEaOne(
            clear) & self.NOT_A_FILE & ~self.black_pieces & self.white_pieces

        if self.can_en_passant:
            last_end = (self.last_end_square)

            if last_end >= 24 and last_end <= 31 and start_square >= 24 and start_square <= 31:
                if last_end == start_square - 1:
                    next_boards.append((((self.board ^ bitboard)) | self.soWeOne(
                        bitboard)) & ~(0xF << (last_end * 4)))
                if last_end == start_square + 1:
                    next_boards.append((((self.board ^ bitboard)) | self.soEaOne(
                        bitboard)) & ~(0xF << (last_end * 4)))

        if (start_square >= 48 and start_square <= 55 and soutOne):
            soutTwo = self.soutOne(
                soutOne) & ~self.white_pieces & ~self.black_pieces
            if soutTwo:
                soutTwo_clear = self.soutOne(
                    soutOne_clear) & ~self.white_pieces & ~self.black_pieces
                self.special_board_states.append(
                    [((self.board ^ bitboard) & ~soutTwo_clear) | soutTwo, self.get_square_from_piece(soutTwo_clear), 1, self.get_square_from_piece(soutOne_clear)])

        if soutOne:
            if start_square >= 8 and start_square <= 15:
                next_boards.append(
                    ((self.board ^ bitboard) & ~soutOne_clear) | (soutOne_clear & HexBoard.ALL_BLACK_ROOKS))
                next_boards.append(
                    ((self.board ^ bitboard) & ~soutOne_clear) | (soutOne_clear & HexBoard.ALL_BLACK_KNIGHTS))
                next_boards.append(
                    ((self.board ^ bitboard) & ~soutOne_clear) | (soutOne_clear & HexBoard.ALL_BLACK_BISHOPS))
                next_boards.append(
                    ((self.board ^ bitboard) & ~soutOne_clear) | (soutOne_clear & HexBoard.ALL_BLACK_QUEENS))
            else:
                next_boards.append(
                    ((self.board ^ bitboard) & ~soutOne_clear) | soutOne)

        if soWeOne:
            next_boards.append(
                ((self.board ^ bitboard) & ~soWeOne_clear) | soWeOne)

        if soEaOne:
            next_boards.append(
                ((self.board ^ bitboard) & ~soEaOne_clear) | soEaOne)

        return next_boards

    def pawn_attacks_white(self, clear) -> int:
        attacks = 0

        noWeOne_clear = self.noWeOne(clear) & self.NOT_H_FILE
        noEaOne_clear = self.noEaOne(clear) & self.NOT_A_FILE

        attacks |= noWeOne_clear
        attacks |= noEaOne_clear

        return attacks

    def pawn_attacks_black(self, clear) -> int:
        attacks = 0

        soWeOne_clear = self.soWeOne(clear) & self.NOT_H_FILE
        soEaOne_clear = self.soEaOne(clear) & self.NOT_A_FILE

        attacks |= soWeOne_clear
        attacks |= soEaOne_clear

        return attacks

    # PIECE MOVES

    def _get_moves(self, clear: int, direction_fns) -> list[int]:
        next_boards: list[int] = []

        for get_dir_boards in direction_fns:
            boards = get_dir_boards(clear)

            if type(boards) == list:
                next_boards += boards
            else:
                next_boards.append(boards)

        return next_boards

    def knight_moves(self, clear: int) -> list[int]:
        directions = [self.noNoEa, self.noEaEa, self.noNoWe, self.noWeWe,
                      self.soSoEa, self.soEaEa, self.soSoWe, self.soWeWe]
        return self._get_moves(clear, directions)

    def rook_moves(self, clear: int) -> list[int]:
        directions = [self.getNoSlide, self.getEaSlide,
                      self.getSoSlide, self.getWeSlide]
        return self._get_moves(clear, directions)

    def bishop_moves(self, clear: int) -> list[int]:
        directions = [self.getNoEaSlide, self.getNoWeSlide,
                      self.getSoEaSlide, self.getSoWeSlide]
        return self._get_moves(clear, directions)

    def queen_moves(self, clear: int) -> list[int]:
        directions = [self.getNoSlide, self.getEaSlide, self.getSoSlide, self.getWeSlide,  # rook moves
                      self.getNoEaSlide, self.getNoWeSlide, self.getSoEaSlide, self.getSoWeSlide]  # bishop moves
        return self._get_moves(clear, directions)

    def king_moves(self, clear: int) -> list[int]:
        directions = [self.nortOne, self.soutOne, self.eastOne, self.westOne,
                      self.noEaOne, self.noWeOne, self.soEaOne, self.soWeOne]
        return self._get_moves(clear, directions)

    def generate_attack_board(self, color_to_look_for) -> int:
        attack_board = 0x0
        # print(hex(self.attack_board))

        # print(color)
        # self.print_board_hex(board)
        # if other:
        #     print(hex(self.board))
        #     print(hex(other))
        for i in range(64):
            # print(i)

            square = self.get_piece_from_square(i)
            piece = square & HexBoard.PIECE_MASK
            # print(bin(piece), bin(square), bin(self.PIECE_MASK))
            color = square & HexBoard.COLOR_MASK

            clear = 0xF << (i * 4)  # 0xf00000000000

            if square == 0 or color != color_to_look_for:
                continue
            elif piece == HexBoard.PAWN and color == HexBoard.WHITE:
                attack_board |= self.pawn_attacks_white(clear)

            elif piece == HexBoard.PAWN and color == HexBoard.BLACK:
                attack_board |= self.pawn_attacks_black(clear)

            elif piece == HexBoard.KNIGHT:
                for move in self.knight_moves(clear):
                    attack_board |= move

            elif piece == HexBoard.ROOK:
                for move in self.rook_moves(clear):
                    attack_board |= move

            elif piece == HexBoard.BISHOP:
                for move in self.bishop_moves(clear):
                    attack_board |= move

            elif piece == HexBoard.QUEEN:
                for move in self.queen_moves(clear):
                    attack_board |= move

            elif piece == HexBoard.KING:
                for move in self.king_moves(clear):
                    attack_board |= move

        return attack_board

    def check_king_side_castle(self, color):
        square1 = 0xF << ((5 if color == self.BLACK else 61) * 4)
        square2 = 0xF << ((6 if color == self.BLACK else 62) * 4)

        not_king_moved = not self.castle_states['white_king_moved'] if color == self.BLACK else not self.castle_states['black_king_moved']
        not_rook_moved = not self.castle_states['KS_rook_w_moved'] if color == self.BLACK else not self.castle_states['KS_rook_b_moved']

        # print(self.attack_board & square1, self.attack_board & square2, not_king_moved, not_rook_moved)
        square1_not_check_and_no_piece = self.attack_board & square1 == 0 and self.white_pieces & square1 == 0 and self.black_pieces & square1 == 0
        square2_not_check_and_no_piece = self.attack_board & square2 == 0 and self.white_pieces & square2 == 0 and self.black_pieces & square2 == 0

        # print( self.attack_board & square2, self.white_pieces & self.black_pieces & square2)

        if square1_not_check_and_no_piece and square2_not_check_and_no_piece and not_king_moved and not_rook_moved:
            return True
        return False

    def check_queen_side_castle(self, color):
        # print(color)
        square1 = 0xF << ((2 if color == self.BLACK else 58) * 4)
        square2 = 0xF << ((3 if color == self.BLACK else 59) * 4)
        square3 = 0xF << ((1 if color == self.BLACK else 57) * 4)

        # print(hex(square1), hex(square2))
        # print(hex(self.attack_board), hex(self.attack_board))
        # print(hex(self.attack_board & square1), hex(self.attack_board & square2))

        not_king_moved = not self.castle_states['white_king_moved'] if color == self.BLACK else not self.castle_states['black_king_moved']
        not_rook_moved = not self.castle_states['QS_rook_w_moved'] if color == self.BLACK else not self.castle_states['QS_rook_b_moved']
        no_piece_on_3 = self.white_pieces & square3 == 0 and self.black_pieces & square3 == 0
        square1_not_check_and_no_piece = self.attack_board & square1 == 0 and self.white_pieces & square1 == 0 and self.black_pieces & square1 == 0
        square2_not_check_and_no_piece = self.attack_board & square2 == 0 and self.white_pieces & square2 == 0 and self.black_pieces & square2 == 0

        # print(square1_not_check_and_no_piece, square2_not_check_and_no_piece)
        # print(not_king_moved, not_rook_moved, no_piece_on_3, self.attack_board & square1, self.attack_board & square2)

        if square1_not_check_and_no_piece and square2_not_check_and_no_piece and no_piece_on_3 and not_king_moved and not_rook_moved:
            return True
        return False

    # def get_boards_from_moves_lists(color_board, valid_move_check, initial_location, move_list):

    def get_check_status(self, king_square):
        if king_square & self.attack_board:
            return True
        return False

    '''Given any board hex representation,
    outputs a list of other board hex representations
    of each possible other game state '''

    def generate_all_possible_next_board_states(self) -> int:
        # self.print_board_hex()
        next_rook_boards: list[int] = []
        next_bishop_boards: list[int] = []
        next_queen_boards: list[int] = []
        next_knight_boards: list[int] = []
        next_pawn_boards: list[int] = []
        next_king_boards: list[int] = []

        # white_king_loc = 0
        # black_king_loc = 1

        for i in range(64):

            square = self.get_piece_from_square(i)
            piece = square & HexBoard.PIECE_MASK
            color = square & HexBoard.COLOR_MASK

            clear = 0xF << (i * 4)  # 0xf00000000000
            bitboard = square << (i * 4)  # 0x300000000000

            if square == 0 or color == self.color_to_move:
                continue
            elif piece == HexBoard.PAWN and color == HexBoard.WHITE:
                next_pawn_boards.append(self.pawn_moves_white(square, i))

            elif piece == HexBoard.PAWN and color == HexBoard.BLACK:
                next_pawn_boards.append(self.pawn_moves_black(square, i))

            elif piece == HexBoard.KNIGHT:
                temp = [bitboard]
                temp += (self.knight_moves(clear))
                next_knight_boards.append(temp)

            elif piece == HexBoard.ROOK:
                temp = [bitboard]
                temp += (self.rook_moves(clear))
                next_rook_boards.append(temp)

            elif piece == HexBoard.BISHOP:
                temp = [bitboard]
                temp += (self.bishop_moves(clear))
                next_bishop_boards.append(temp)

            elif piece == HexBoard.QUEEN:
                temp = [bitboard]
                temp += (self.queen_moves(clear))
                next_queen_boards.append(temp)

            elif piece == HexBoard.KING:
                # print('in')
                temp = [bitboard]
                temp += (self.king_moves(clear))
                next_king_boards.append(temp)

        def valid_moves_w(x): return x & ~self.white_pieces | (
            x & self.black_pieces)

        def valid_moves_b(x): return x & ~self.black_pieces | (
            x & self.white_pieces)

        all_boards: list[HexBoard] = []
        next_color = HexBoard.WHITE if self.color_to_move == HexBoard.BLACK else HexBoard.BLACK
        valid_move_check = valid_moves_w if self.color_to_move == HexBoard.BLACK else valid_moves_b

        # print(next_king_boards)
        king_location = next_king_boards[0][0]

        IN_CHECK = False
        if king_location & self.attack_board:
            IN_CHECK = True

        king_side_castle = self.check_king_side_castle(
            self.color_to_move) if not IN_CHECK else False
        queen_side_castle = self.check_queen_side_castle(
            self.color_to_move) if not IN_CHECK else False

        if king_side_castle:
            new_castle_state = self.castle_states.copy()
            if self.color_to_move:  # white
                temp = 0x0
                temp = self.board ^ king_location
                temp = temp & ~(0xF << (7 * 4))
                temp = temp | 0x6200000

                new_castle_state['white_king_moved'] = True
                new_castle_state['QS_rook_w_moved'] = True
                new_castle_state['KS_rook_w_moved'] = True

                all_boards.append(
                    HexBoard(board=temp, color_to_move=next_color, castle_states=new_castle_state))
            else:  # black
                temp = 0x0
                temp = self.board ^ king_location
                temp = temp & ~(0xF << (63 * 4))
                temp = temp | 0x0620000000000000000000000000000000000000000000000000000000000000
                new_castle_state['black_king_moved'] = True
                new_castle_state['QS_rook_b_moved'] = True
                new_castle_state['KS_rook_b_moved'] = True

                all_boards.append(
                    HexBoard(board=temp, color_to_move=next_color, castle_states=new_castle_state))

        if queen_side_castle:
            new_castle_state = self.castle_states.copy()
            if self.color_to_move:  # white
                temp = 0x0
                temp = self.board ^ king_location
                temp = temp & ~(0xF << (0 * 4))
                temp = temp | 0x2600
                # self.print_board_hex(temp)
                new_castle_state['white_king_moved'] = True
                new_castle_state['QS_rook_w_moved'] = True
                new_castle_state['KS_rook_w_moved'] = True

                all_boards.append(
                    HexBoard(board=temp, color_to_move=next_color, castle_states=new_castle_state))
            else:  # black
                temp = 0x0
                temp = self.board ^ king_location
                temp = temp & ~(0xF << (56 * 4))
                temp = temp | 0x260000000000000000000000000000000000000000000000000000000000

                new_castle_state['black_king_moved'] = True
                new_castle_state['QS_rook_b_moved'] = True
                new_castle_state['KS_rook_b_moved'] = True

                all_boards.append(
                    HexBoard(board=temp, color_to_move=next_color, castle_states=new_castle_state))

        # self.print_board_hex(king_location)
        king_piece_moves = next_king_boards[0][1:]
        # print(king_piece_moves)
        # all_king = 0
        # print('inaa')
        if king_piece_moves:
            # print('in')
            color_board = HexBoard.ALL_WHITE_KINGS if self.color_to_move == HexBoard.BLACK else HexBoard.ALL_BLACK_KINGS
            # for each move of this king (skip idx 0 -- 'current pos')
            for move in king_piece_moves:

                # print("---------")
                # print(hex(move))
                # print(hex(Board.ALL_DEFINED))
                # self.print_board_hex((move))

                if valid_move_check(move) and move and not move & self.attack_board and move & HexBoard.ALL_DEFINED:
                    # all_king |= move
                    # print('inee')
                    # self.print_board_hex((move))
                    # print(hex(self.attack_board))

                    # print("innn")
                    # print(hex(valid_move_check(move)), not move)
                    # self.print_board_hex((move))
                    # print(hex(self.board))

                    temp = 0x0
                    temp = (self.board ^ king_location)  # remove current piece
                    # print(hex(temp))

                    temp = temp & ~move   # removes the piece at the move
                    # print(hex(temp))
                    # adds the new piece with the right value
                    # self.print_board_hex((temp))
                    temp = temp | (move & color_board)
                    # print(hex(temp))
                    # self.print_board_hex(self.attack_board)

                    new_castle_states = self.castle_states
                    if not self.castle_states['white_king_moved'] or not self.castle_states['black_king_moved']:
                        new_castle_states = self.castle_states.copy()
                        if self.color_to_move == HexBoard.WHITE:
                            new_castle_states['white_king_moved'] = True
                        if self.color_to_move == HexBoard.BLACK:
                            new_castle_states['black_king_moved'] = True

                    all_boards.append(HexBoard(
                        board=temp, color_to_move=next_color, castle_states=new_castle_states))
                # print("---------")
                    # self.print_board_hex(Board(board=temp, color_to_move=next_color, castle_states=self.castle_states).attack_board)

        for special_board, last_move_square, en_passant, en_pass_fen in self.special_board_states:
            all_boards.append(HexBoard(board=special_board, color_to_move=next_color, last_end_square=last_move_square,
                              can_en_passant=en_passant, castle_states=self.castle_states, en_passant_square_fen=en_pass_fen))

            # print(hex((special_board)))
            # (Board(board=special_board, color_to_move=next_color,
            #                         last_end_square=last_move_square, can_en_passant=en_passant)).print_board_hex()
            # self.print_board_hex(Board(board=special_board, color_to_move=next_color,
            #                         last_end_square=last_move_square, can_en_passant=en_passant).attack_board)

        for pawn in next_pawn_boards:
            for move in pawn:
                all_boards.append(HexBoard(
                    board=move, color_to_move=next_color, castle_states=self.castle_states))

                # self.print_board_hex(move)
                # self.print_board_hex(Board(board=move, color_to_move=next_color).attack_board)

        for knight in next_knight_boards:
            if knight:
                # pop the first piece -- which we set to be the square the knight is moving from
                current_piece = knight[0]
                color_board = HexBoard.ALL_WHITE_KNIGHTS if self.color_to_move == HexBoard.BLACK else HexBoard.ALL_BLACK_KNIGHTS

                # for each move of this knight (skip idx 0 -- 'current pos')
                for move in knight[1:]:
                    # check if valid for white or black (TODO: black)
                    # print("---------")

                    if valid_move_check(move) and move and (move & HexBoard.ALL_DEFINED):
                        temp = 0x0
                        # print(hex(move))

                        # remove current piece
                        temp = (self.board ^ current_piece)
                        # print(self.color_to_move, hex(temp), hex(self.board), hex(current_piece))
                        temp = temp & ~move   # removes the piece at the move
                        # print(hex(temp))
                        # adds the new piece with the right value
                        temp = temp | (move & color_board)
                        # print(hex(temp))

                        all_boards.append(HexBoard(
                            board=temp, color_to_move=next_color, castle_states=self.castle_states))
                        # self.print_board_hex(temp)
                        # self.print_board_hex(Board(board=temp, color_to_move=next_color).attack_board)
                    # print("------------------")

        for rook in next_rook_boards:
            if rook:
                # pop the first piece -- which we set to be the square the rook is moving from
                current_piece = rook[0]
                color_board = HexBoard.ALL_WHITE_ROOKS if self.color_to_move == HexBoard.BLACK else HexBoard.ALL_BLACK_ROOKS

                # for each move of this rook (skip idx 0 -- 'current pos')
                for move in rook[1:]:
                    # check if valid for white or black (TODO: black)
                    if valid_move_check(move) and move and (move & HexBoard.ALL_DEFINED):
                        temp = 0x0
                        # remove current piece
                        temp = (self.board ^ current_piece)
                        temp = temp & ~move   # removes the piece at the move
                        # adds the new piece with the right value
                        temp = temp | (move & color_board)

                        new_castle_states = self.castle_states
                        if not self.castle_states['QS_rook_b_moved'] and self.get_square_from_piece(move) == 56:
                            new_castle_states = self.castle_states.copy()
                            new_castle_states['QS_rook_b_moved'] = True
                        if not self.castle_states['QS_rook_w_moved'] and self.get_square_from_piece(move) == 0:
                            new_castle_states = self.castle_states.copy()
                            new_castle_states['QS_rook_w_moved'] = True
                        if not self.castle_states['KS_rook_b_moved'] and self.get_square_from_piece(move) == 63:
                            new_castle_states = self.castle_states.copy()
                            new_castle_states['KS_rook_b_moved'] = True
                        if not self.castle_states['KS_rook_w_moved'] and self.get_square_from_piece(move) == 7:
                            new_castle_states = self.castle_states.copy()
                            new_castle_states['KS_rook_w_moved'] = True

                        all_boards.append(HexBoard(
                            board=temp, color_to_move=next_color, castle_states=new_castle_states))
                        # self.print_board_hex(temp)
                        # self.print_board_hex(Board(board=temp, color_to_move=next_color, castle_states=self.castle_states).attack_board)

        for bishop_piece_moves in next_bishop_boards:
            if bishop_piece_moves:
                # pop the first piece -- which we set to be the square the bishop is moving from
                current_piece = bishop_piece_moves[0]
                color_board = HexBoard.ALL_WHITE_BISHOPS if self.color_to_move == self.BLACK else HexBoard.ALL_BLACK_BISHOPS

                # for each move of this bishop (skip idx 0 -- 'current pos')
                for move in bishop_piece_moves[1:]:
                    # check if valid for white or black (TODO: black)
                    if valid_move_check(move) and move and (move & HexBoard.ALL_DEFINED):
                        temp = 0x0
                        # remove current piece
                        temp = (self.board ^ current_piece)
                        temp = temp & ~move   # removes the piece at the move
                        # adds the new piece with the right value
                        temp = temp | (move & color_board)

                        all_boards.append(HexBoard(
                            board=temp, color_to_move=next_color, castle_states=self.castle_states))
                        # print(hex((temp)))
                        # print(hex((Board(board=temp, color_to_move=next_color, castle_states=self.castle_states).attack_board)))
                        # self.print_board_hex(temp)
                        # self.print_board_hex(Board(board=temp, color_to_move=next_color, castle_states=self.castle_states).attack_board)

        for queen_piece_moves in next_queen_boards:
            if queen_piece_moves:
                # pop the first piece -- which we set to be the square the queen is moving from
                current_piece = queen_piece_moves[0]
                color_board = HexBoard.ALL_WHITE_QUEENS if self.color_to_move == HexBoard.BLACK else HexBoard.ALL_BLACK_QUEENS

                # for each move of this queen (skip idx 0 -- 'current pos')
                for move in queen_piece_moves[1:]:
                    # check if valid for white or black (TODO: black)
                    if valid_move_check(move) and move and (move & HexBoard.ALL_DEFINED):
                        temp = 0x0
                        # remove current piece
                        temp = (self.board ^ current_piece)
                        temp = temp & ~move   # removes the piece at the move
                        # adds the new piece with the right value
                        temp = temp | (move & color_board)

                        all_boards.append(HexBoard(
                            board=temp, color_to_move=next_color, castle_states=self.castle_states))

                        # self.print_board_hex(temp)
                        # self.print_board_hex(Board(board=temp, color_to_move=next_color, castle_states=self.castle_states).attack_board)

        available_moves = []
        if IN_CHECK:
            for possible_state in all_boards:
                # since the board already checks if a king move is legal
                # only check to see if the king is not on its original square or it has moved
                if king_location & possible_state.board == 0:
                    available_moves.append(possible_state)

                # blocking pieces, pieces moving in the way of the king
                new_attack_board = possible_state.generate_attack_board(
                    self.color_to_move)
                # self.print_board_hex(possible_state.generate_attack_board(self.color_to_move))

                if new_attack_board & king_location == 0:
                    available_moves.append(possible_state)
                    # possible_state.print_board_hex()

        else:
            # making sure the piece cannot move to create a check
            for possible_state in all_boards:
                new_attack_board = possible_state.generate_attack_board(
                    self.color_to_move)
                if new_attack_board & king_location == 0:
                    available_moves.append(possible_state)

        if not available_moves:
            self.game_is_over = True

            if king_location & self.attack_board:
                self.check_mate = True
                print('black wins' if self.color_to_move else 'white_wins')
            else:
                print('draw')
                self.draw = True

        # for move in available_moves:
        #     print(hex(move.board))
        #     self.print_board_hex(move.attack_board)

        return available_moves

    def material_balance(self):
        PIECE_VALUES = {
            self.PAWN: 1,  # Pawn
            self.KNIGHT: 3,  # Knight
            self.BISHOP: 3,  # Bishop
            self.ROOK: 5,  # Rook
            self.QUEEN: 9,
        }

        white_total = 0
        black_total = 0
        for i in range(64):
            square = self.get_piece_from_square(i)
            color = square & self.COLOR_MASK
            piece = square & self.PIECE_MASK

            if color == self.WHITE:
                white_total += PIECE_VALUES[piece] if PIECE_VALUES.get(
                    piece) else 0
            else:
                black_total += PIECE_VALUES[piece] if PIECE_VALUES.get(
                    piece) else 0

        # print(white_total, black_total)
        return white_total - black_total

    def get_reward(self):
        # Define your reward logic here
        if self.game_is_over:
            if self.check_mate:
                return 1 if self.color_to_move == self.WHITE else -1
            elif self.draw:
                return 0
        # Intermediate rewards can be added here
        return self.material_balance()

    # def is_game_over(self):
    #     return self.game_is_over

    def step(self, action):
        print(action)
        return self.generate_all_possible_next_board_states()[action], self.get_reward(), self.game_is_over


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
