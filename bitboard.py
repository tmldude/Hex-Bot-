class Bitboard:
    # Constants for colors
    WHITE = 0
    BLACK = 1

    # BOARD MASKS

    ALL_DEFINED = 0xffffffffffffffff

    # BOUNDARIES

    NOT_A_FILE = 0xfefefefefefefefe
    NOT_H_FILE = 0x7f7f7f7f7f7f7f7f

    NOT_AB_FILE = 0xfcfcfcfcfcfcfcfc
    NOT_GH_FILE = 0x3f3f3f3f3f3f3f3f

    NOT_RANK_1 = ~0xff
    NOT_RANK_8 = ~0xff00000000000000

    def __init__(self, fen: str) -> None:
        self.piece_boards, self.board_data = self.fen_to_bitboards(fen)

        self.combined_board = 0
        for bitboard in self.piece_boards.values():
            self.combined_board |= bitboard

    # MAIN BOARD FUNCTIONS

    def generate_attack_board(self, color_to_look_for) -> int:
        attack_board = 0x0

        if color_to_look_for == self.WHITE:
            attack_board |= self.rook_moves(self.piece_boards['R'])
            attack_board |= self.knight_moves(self.piece_boards['N'])
            attack_board |= self.bishop_moves(self.piece_boards['B'])
            attack_board |= self.queen_moves(self.piece_boards['Q'])
            attack_board |= self.king_moves(self.piece_boards['K'])
            attack_board |= self.pawn_attacks_white(self.piece_boards['P'])
        else:
            attack_board |= self.rook_moves(self.piece_boards['r'])
            attack_board |= self.knight_moves(self.piece_boards['n'])
            attack_board |= self.bishop_moves(self.piece_boards['b'])
            attack_board |= self.queen_moves(self.piece_boards['q'])
            attack_board |= self.king_moves(self.piece_boards['k'])
            attack_board |= self.pawn_attacks_black(self.piece_boards['p'])

        return attack_board & self.ALL_DEFINED

    """
    Output: 14x8x8 (last 2 are attack boards for white and black, resp.)
    """

    def generate_board_matrix(self) -> list[list[list[int]]]:

        boards = [self.piece_boards['R'],
                  self.piece_boards['N'],
                  self.piece_boards['B'],
                  self.piece_boards['Q'],
                  self.piece_boards['K'],
                  self.piece_boards['P'],
                  self.piece_boards['r'],
                  self.piece_boards['n'],
                  self.piece_boards['b'],
                  self.piece_boards['q'],
                  self.piece_boards['k'],
                  self.piece_boards['p'],
                  self.generate_attack_board(0),  # white attack board
                  self.generate_attack_board(1)  # black attack board
                  ]

        boards += self.board_data

        matrix = []
        for board in boards:
            matrix.append(Bitboard.bitboard_to_matrix(board))

        return matrix

    # FEN

    def fen_to_bitboards(self, fen: str) -> dict[str, int]:
        pieces = 'PNBRQKpnbrqk'
        boards = {piece: 0 for piece in pieces}

        split = fen.split(' ')
        positions = split[0]
        row = 0
        for rank in positions.split('/'):
            col = 0
            for char in rank:
                if char.isdigit():
                    col += int(char)
                else:
                    index = pieces.index(char)
                    board_index = 8 * (7 - row) + col
                    boards[char] |= 1 << board_index
                    col += 1
            row += 1

        color = 0 if split[1] == 'w' else 1
        castle_K = 1 if 'K' in split[2] else 0
        castle_Q = 1 if 'Q' in split[2] else 0
        castle_k = 1 if 'k' in split[2] else 0
        castle_q = 1 if 'q' in split[2] else 0
        en_passant = self.fen_to_square_number(
            split[3]) if split[3] != '-' else 0
        half_move = int(split[4])
        full_move = int(split[5]) if len(split) >= 5 else 0

        board_data = [color, castle_K, castle_Q, castle_k,
                      castle_q, en_passant, half_move, full_move]

        return boards, board_data

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

    # LINEAR MOVES

    @staticmethod
    def nortOne(b) -> int:
        return b << 8

    @staticmethod
    def soutOne(b) -> int:
        return b >> 8

    @staticmethod
    def eastOne(b) -> int:
        return (b << 1) & Bitboard.NOT_A_FILE

    # DIAG MOVES

    @staticmethod
    def noEaOne(b) -> int:
        return (b << 9) & Bitboard.NOT_A_FILE

    @staticmethod
    def soEaOne(b) -> int:
        return (b >> 7) & Bitboard.NOT_A_FILE

    @staticmethod
    def westOne(b) -> int:
        return (b >> 1) & Bitboard.NOT_H_FILE

    @staticmethod
    def soWeOne(b) -> int:
        return (b >> 9) & Bitboard.NOT_H_FILE

    @staticmethod
    def noWeOne(b) -> int:
        return (b << 7) & Bitboard.NOT_H_FILE

    @staticmethod
    def noNoEa(bitboard) -> int:
        return (bitboard << 17) & Bitboard.NOT_A_FILE

    # KNIGHT MOVES

    @staticmethod
    def noEaEa(bitboard) -> int:
        return (bitboard << 10) & Bitboard.NOT_AB_FILE

    @staticmethod
    def soEaEa(bitboard) -> int:
        return (bitboard >> 6) & Bitboard.NOT_AB_FILE

    @staticmethod
    def soSoEa(bitboard) -> int:
        return (bitboard >> 15) & Bitboard.NOT_A_FILE

    @staticmethod
    def noNoWe(bitboard) -> int:
        return (bitboard << 15) & Bitboard.NOT_H_FILE

    @staticmethod
    def noWeWe(bitboard) -> int:
        return (bitboard << 6) & Bitboard.NOT_GH_FILE

    @staticmethod
    def soWeWe(bitboard) -> int:
        return (bitboard >> 10) & Bitboard.NOT_GH_FILE

    @staticmethod
    def soSoWe(bitboard) -> int:
        return (bitboard >> 17) & Bitboard.NOT_H_FILE

    # SLIDE MOVES

    def _get_slide(self, bitboard, direction, boundary1, boundary2) -> int:
        next_boards = 0

        dir_bitboard: int = direction(bitboard)
        not_blocked = True

        while not_blocked and (dir_bitboard & boundary1) and (dir_bitboard & boundary2):
            next_boards |= dir_bitboard

            # update if hitting white or black piece to stop while loop
            not_blocked = dir_bitboard & self.combined_board == 0

            # moving up, down, left, right, or diag one position
            dir_bitboard = direction(dir_bitboard)

        added = False
        if dir_bitboard & ~boundary1 and not_blocked:
            next_boards |= dir_bitboard
            added = True

        if dir_bitboard & ~boundary2 and not_blocked and not added:
            next_boards |= dir_bitboard

        return next_boards

    def getNoSlide(self, bitboard) -> int:
        return self._get_slide(bitboard, Bitboard.nortOne, Bitboard.NOT_RANK_8, Bitboard.ALL_DEFINED)

    def getSoSlide(self, bitboard) -> int:
        return self._get_slide(bitboard, Bitboard.soutOne, Bitboard.NOT_RANK_1, Bitboard.ALL_DEFINED)

    def getEaSlide(self, bitboard) -> int:
        return self._get_slide(bitboard, Bitboard.eastOne, Bitboard.NOT_H_FILE, Bitboard.ALL_DEFINED)

    def getWeSlide(self, bitboard) -> int:
        return self._get_slide(bitboard, Bitboard.westOne, Bitboard.NOT_A_FILE, Bitboard.ALL_DEFINED)

    def getNoEaSlide(self, bitboard) -> int:
        return self._get_slide(bitboard, Bitboard.noEaOne, Bitboard.NOT_RANK_8, Bitboard.NOT_H_FILE)

    def getNoWeSlide(self, bitboard) -> int:
        return self._get_slide(bitboard, Bitboard.noWeOne, Bitboard.NOT_RANK_8, Bitboard.NOT_A_FILE)

    def getSoEaSlide(self, bitboard) -> int:
        return self._get_slide(bitboard, Bitboard.soEaOne, Bitboard.NOT_RANK_1, Bitboard.NOT_H_FILE)

    def getSoWeSlide(self, bitboard) -> int:
        return self._get_slide(bitboard, Bitboard.soWeOne, Bitboard.NOT_RANK_1, Bitboard.NOT_A_FILE)

    # PIECE MOVES

    def _get_moves(self, bitboard: int, direction_fns) -> int:
        next_boards = 0

        for get_dir_boards in direction_fns:
            boards = get_dir_boards(bitboard)
            next_boards |= boards

        return next_boards

    def knight_moves(self, bitboard: int) -> int:
        directions = [self.noNoEa, self.noEaEa, self.noNoWe, self.noWeWe,
                      self.soSoEa, self.soEaEa, self.soSoWe, self.soWeWe]
        return self._get_moves(bitboard, directions)

    def rook_moves(self, bitboard: int) -> int:
        directions = [self.getNoSlide, self.getEaSlide,
                      self.getSoSlide, self.getWeSlide]
        return self._get_moves(bitboard, directions)

    def bishop_moves(self, bitboard: int) -> int:
        directions = [self.getNoEaSlide, self.getNoWeSlide,
                      self.getSoEaSlide, self.getSoWeSlide]
        return self._get_moves(bitboard, directions)

    def queen_moves(self, bitboard: int) -> int:
        directions = [self.getNoSlide, self.getEaSlide, self.getSoSlide, self.getWeSlide,  # rook moves
                      self.getNoEaSlide, self.getNoWeSlide, self.getSoEaSlide, self.getSoWeSlide]  # bishop moves
        return self._get_moves(bitboard, directions)

    def king_moves(self, bitboard: int) -> int:
        directions = [self.nortOne, self.soutOne, self.eastOne, self.westOne,
                      self.noEaOne, self.noWeOne, self.soEaOne, self.soWeOne]
        return self._get_moves(bitboard, directions)

    # ATTACKS

    def pawn_attacks_white(self, bitboard) -> int:
        attacks = 0

        noWeOne_bitboard = self.noWeOne(bitboard) & self.NOT_H_FILE
        noEaOne_bitboard = self.noEaOne(bitboard) & self.NOT_A_FILE

        attacks |= noWeOne_bitboard
        attacks |= noEaOne_bitboard

        return attacks

    def pawn_attacks_black(self, bitboard) -> int:
        attacks = 0

        soWeOne_bitboard = self.soWeOne(bitboard) & self.NOT_H_FILE
        soEaOne_bitboard = self.soEaOne(bitboard) & self.NOT_A_FILE

        attacks |= soWeOne_bitboard
        attacks |= soEaOne_bitboard

        return attacks

    # UTILS

    """
    Given a board and a square, returns the hex number at the square
    other returns the square on a board not self
    """

    def binary_to_piece(self, square, other=None) -> int:
        if other:
            return other >> (square & 0x1)
        return self.combined_board >> (square & 0x1)

    @staticmethod
    def bitboard_to_matrix(bitboard: int) -> list[list[int]]:
        matrix = []
        for row in range(8):
            current_row = []
            for col in range(8):
                index = (7 - row) * 8 + col
                if bitboard & (1 << index):
                    current_row.append(1)
                else:
                    current_row.append(0)
            matrix.append(current_row)
        return matrix

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

    def print_board(self, other=None):
        print_str = ''
        for i in range(7, -1, -1):  # Start from 7 and decrement to 0
            for j in range(8):
                if other:
                    print_str = print_str + \
                        str(bin(self.binary_to_piece(
                            i*8 + j, other)))[2:] + " "
                else:
                    print_str = print_str + \
                        str(bin(self.binary_to_piece(
                            i*8 + j)))[2:] + " "

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

    def print_numboard():
        string = ''
        for i in range(7, -1, -1):  # Start from 7 and decrement to 0
            for j in range(8):
                string = string + str(i * 8 + j) + " "
            string = string + '\n'  # Add newline after each row

        print(string)

    def pprint_board(board):
        print_str = ''
        for i in range(7, -1, -1):
            for j in range(8):
                bit_position = i * 8 + j
                if board & (1 << bit_position):
                    print_str += '1 '  # Occupied
                else:
                    print_str += '0 '  # Empty
            print_str += '\n'
        print(print_str)