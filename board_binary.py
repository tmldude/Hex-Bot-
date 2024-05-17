from utils import add_rightmost_hex_digit


class BinaryBoard:
    '''
    Board class for representing a chess board

    INDEXES: bits 0-255 (hex bit 0-63)
    256 bit, 64 hex bit representation. Every 4 bits (1hex) is a piece
    0___ -> the piece mask
    _000 -> the color of the piece

    important outputs: Board.getallnebitboardtboardstates
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


    ebitboardtracts the 66th digit from the hex number
    the 66th digit will hold state
    value: 0 - NO EN passant
    value: 1 - last move was a pawn that was moved 2

    67th
    this bit will hold where the last piece square ended on - for en passant
    00xbitboard where bitboardbitboard is a number between 0-63

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

    NOT_A_FILE = 0b1111111011111110111111101111111011111110111111101111111011111110
    NOT_H_FILE = 0b111111101111111011111110111111101111111011111110111111101111111

    NOT_AB_FILE = 0b111111100111111100111111100111111100111111100111111100111111100111111100
    NOT_GH_FILE = 0b1111111001111111001111111001111111001111111001111111001111111001111111

    NOT_RANK_1 = ~0b000000000000000000000000000000000000000000000000000000001111111
    NOT_RANK_8 = ~0b111111100000000000000000000000000000000000000000000000000000000

    # COLOR_TO_MOVE = 64
    # CASTLE_STATES = 65
    # EN_PASSANT_STATE = 66
    # LAST_END_SQUARE = 67

    def __init__(self, fen: str) -> None:
        piece_boards = self.fen_to_binary_boards(fen)

        self.combined_board = 0
        for bitboard in self.piece_boards.values():
            self.combined_board |= bitboard

        self.pawns_white = piece_boards['P']
        self.knights_white = piece_boards['N']
        self.bishops_white = piece_boards['B']
        self.rooks_white = piece_boards['R']
        self.queens_white = piece_boards['Q']
        self.kings_white = piece_boards['K']

        self.pawns_black = piece_boards['p']
        self.knights_black = piece_boards['n']
        self.bishops_black = piece_boards['b']
        self.rooks_black = piece_boards['r']
        self.queens_black = piece_boards['q']
        self.kings_black = piece_boards['k']

    """
    Given a board and a square, returns the hex number at the square
    other returns the square on a board not self
    """

    def binary_to_piece(self, square, other=None) -> int:
        if other:
            return other >> (square & 0x1)
        return self.combined_board >> (square & 0x1)

    # FEN

    def fen_to_binary_boards(fen: str) -> dict[str, int]:
        pieces = 'PNBRQKpnbrqk'
        boards = {piece: 0 for piece in pieces}

        positions = fen.split(' ')[0]
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

        return boards

    # MOVES

    @staticmethod
    def nortOne(b) -> int:
        return b << 8

    @staticmethod
    def soutOne(b) -> int:
        return b >> 8

    @staticmethod
    def eastOne(b) -> int:
        return (b << 1) & BinaryBoard.NOT_A_FILE

    @staticmethod
    def noEaOne(b) -> int:
        return (b << 9) & BinaryBoard.NOT_A_FILE

    @staticmethod
    def soEaOne(b) -> int:
        return (b >> 7) & BinaryBoard.NOT_A_FILE

    @staticmethod
    def westOne(b) -> int:
        return (b >> 1) & BinaryBoard.NOT_H_FILE

    @staticmethod
    def soWeOne(b) -> int:
        return (b >> 9) & BinaryBoard.NOT_H_FILE

    @staticmethod
    def noWeOne(b) -> int:
        return (b << 7) & BinaryBoard.NOT_H_FILE

    @staticmethod
    def noNoEa(bitboard) -> int:
        return (bitboard << 17) & BinaryBoard.NOT_A_FILE

    @staticmethod
    def noEaEa(bitboard) -> int:
        return (bitboard << 10) & BinaryBoard.NOT_AB_FILE

    @staticmethod
    def soEaEa(bitboard) -> int:
        return (bitboard >> 6) & BinaryBoard.NOT_AB_FILE

    @staticmethod
    def soSoEa(bitboard) -> int:
        return (bitboard >> 15) & BinaryBoard.NOT_A_FILE

    @staticmethod
    def noNoWe(bitboard) -> int:
        return (bitboard << 15) & BinaryBoard.NOT_H_FILE

    @staticmethod
    def noWeWe(bitboard) -> int:
        return (bitboard << 6) & BinaryBoard.NOT_GH_FILE

    @staticmethod
    def soWeWe(bitboard) -> int:
        return (bitboard >> 10) & BinaryBoard.NOT_GH_FILE

    @staticmethod
    def soSoWe(bitboard) -> int:
        return (bitboard >> 17) & BinaryBoard.NOT_H_FILE

    # SLIDE MOVES

    # TODO: fix bitboard masks
    def _get_slide(self, bitboard, direction, boundary1, boundary2):
        next_boards: list[int] = []

        dir_bitboard: int = direction(bitboard)
        not_blocked = True

        while not_blocked and (dir_bitboard & boundary1) and (dir_bitboard & boundary2):
            next_boards.append(dir_bitboard)

            # update if hitting white or black piece to stop while loop
            not_blocked = dir_bitboard & self.combined_board == 0
            # print(hex(not_blocked))
            # moving up, down, left, right, or diag one position
            dir_bitboard = direction(dir_bitboard)

        added = False
        if dir_bitboard & ~boundary1 and not_blocked:
            next_boards.append(dir_bitboard)
            added = True

        if dir_bitboard & ~boundary2 and not_blocked and not added:
            next_boards.append(dir_bitboard)

        return next_boards

    def getNoSlide(self, bitboard) -> list[int]:
        return self._get_slide(bitboard, BinaryBoard.nortOne, BinaryBoard.NOT_RANK_8, BinaryBoard.ALL_DEFINED)

    def getSoSlide(self, bitboard) -> list[int]:
        return self._get_slide(bitboard, BinaryBoard.soutOne, BinaryBoard.NOT_RANK_1, BinaryBoard.ALL_DEFINED)

    def getEaSlide(self, bitboard) -> list[int]:
        return self._get_slide(bitboard, BinaryBoard.eastOne, BinaryBoard.NOT_H_FILE, BinaryBoard.ALL_DEFINED)

    def getWeSlide(self, bitboard) -> list[int]:
        return self._get_slide(bitboard, BinaryBoard.westOne, BinaryBoard.NOT_A_FILE, BinaryBoard.ALL_DEFINED)

    def getNoEaSlide(self, bitboard) -> list[int]:
        return self._get_slide(bitboard, BinaryBoard.noEaOne, BinaryBoard.NOT_RANK_8, BinaryBoard.NOT_H_FILE)

    def getNoWeSlide(self, bitboard) -> list[int]:
        return self._get_slide(bitboard, BinaryBoard.noWeOne, BinaryBoard.NOT_RANK_8, BinaryBoard.NOT_A_FILE)

    def getSoEaSlide(self, bitboard) -> list[int]:
        return self._get_slide(bitboard, BinaryBoard.soEaOne, BinaryBoard.NOT_RANK_1, BinaryBoard.NOT_H_FILE)

    def getSoWeSlide(self, bitboard) -> list[int]:
        return self._get_slide(bitboard, BinaryBoard.soWeOne, BinaryBoard.NOT_RANK_1, BinaryBoard.NOT_A_FILE)

    # PIECE MOVES

    def _get_moves(self, bitboard: int, direction_fns) -> list[int]:
        nebitboardt_boards: list[int] = []

        for get_dir_boards in direction_fns:
            boards = get_dir_boards(bitboard)

            if type(boards) == list:
                nebitboardt_boards += boards
            else:
                nebitboardt_boards.append(boards)

        return nebitboardt_boards

    def knight_moves(self, bitboard: int) -> list[int]:
        directions = [self.noNoEa, self.noEaEa, self.noNoWe, self.noWeWe,
                      self.soSoEa, self.soEaEa, self.soSoWe, self.soWeWe]
        return self._get_moves(bitboard, directions)

    def rook_moves(self, bitboard: int) -> list[int]:
        directions = [self.getNoSlide, self.getEaSlide,
                      self.getSoSlide, self.getWeSlide]
        return self._get_moves(bitboard, directions)

    def bishop_moves(self, bitboard: int) -> list[int]:
        directions = [self.getNoEaSlide, self.getNoWeSlide,
                      self.getSoEaSlide, self.getSoWeSlide]
        return self._get_moves(bitboard, directions)

    def queen_moves(self, bitboard: int) -> list[int]:
        directions = [self.getNoSlide, self.getEaSlide, self.getSoSlide, self.getWeSlide,  # rook moves
                      self.getNoEaSlide, self.getNoWeSlide, self.getSoEaSlide, self.getSoWeSlide]  # bishop moves
        return self._get_moves(bitboard, directions)

    def king_moves(self, bitboard: int) -> list[int]:
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

            square = self.binary_to_piece(i)
            piece = square & BinaryBoard.PIECE_MASK
            # print(bin(piece), bin(square), bin(self.PIECE_MASK))
            color = square & BinaryBoard.COLOR_MASK

            bitboard = 0x1 << (i * 4)

            if square == 0 or color != color_to_look_for:
                continue
            elif piece == BinaryBoard.PAWN and color == BinaryBoard.WHITE:
                attack_board |= self.pawn_attacks_white(bitboard)

            elif piece == BinaryBoard.PAWN and color == BinaryBoard.BLACK:
                attack_board |= self.pawn_attacks_black(bitboard)

            elif piece == BinaryBoard.KNIGHT:
                for move in self.knight_moves(bitboard):
                    attack_board |= move

            elif piece == BinaryBoard.ROOK:
                for move in self.rook_moves(bitboard):
                    attack_board |= move

            elif piece == BinaryBoard.BISHOP:
                for move in self.bishop_moves(bitboard):
                    attack_board |= move

            elif piece == BinaryBoard.QUEEN:
                for move in self.queen_moves(bitboard):
                    attack_board |= move

            elif piece == BinaryBoard.KING:
                for move in self.king_moves(bitboard):
                    attack_board |= move

        return attack_board

    # UTILS

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


def main():
    pass


if __name__ == "__main__":
    main()
