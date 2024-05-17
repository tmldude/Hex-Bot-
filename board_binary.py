from utils import pprint_binboard


class BinaryBoard:

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
        self.piece_boards = self.fen_to_binary_boards(fen)

        self.combined_board = 0
        for bitboard in self.piece_boards.values():
            self.combined_board |= bitboard

    """
    Given a board and a square, returns the hex number at the square
    other returns the square on a board not self
    """

    def binary_to_piece(self, square, other=None) -> int:
        if other:
            return other >> (square & 0x1)
        return self.combined_board >> (square & 0x1)

    # FEN

    def fen_to_binary_boards(self, fen: str) -> dict[str, int]:
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

        return boards

    # LINEAR MOVES

    @staticmethod
    def nortOne(b) -> int:
        return b << 8

    @staticmethod
    def soutOne(b) -> int:
        return b >> 8

    @staticmethod
    def eastOne(b) -> int:
        return (b << 1) & BinaryBoard.NOT_A_FILE

    # DIAG MOVES

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

    # KNIGHT MOVES

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
        return self._get_slide(bitboard, BinaryBoard.nortOne, BinaryBoard.NOT_RANK_8, BinaryBoard.ALL_DEFINED)

    def getSoSlide(self, bitboard) -> int:
        return self._get_slide(bitboard, BinaryBoard.soutOne, BinaryBoard.NOT_RANK_1, BinaryBoard.ALL_DEFINED)

    def getEaSlide(self, bitboard) -> int:
        return self._get_slide(bitboard, BinaryBoard.eastOne, BinaryBoard.NOT_H_FILE, BinaryBoard.ALL_DEFINED)

    def getWeSlide(self, bitboard) -> int:
        return self._get_slide(bitboard, BinaryBoard.westOne, BinaryBoard.NOT_A_FILE, BinaryBoard.ALL_DEFINED)

    def getNoEaSlide(self, bitboard) -> int:
        return self._get_slide(bitboard, BinaryBoard.noEaOne, BinaryBoard.NOT_RANK_8, BinaryBoard.NOT_H_FILE)

    def getNoWeSlide(self, bitboard) -> int:
        return self._get_slide(bitboard, BinaryBoard.noWeOne, BinaryBoard.NOT_RANK_8, BinaryBoard.NOT_A_FILE)

    def getSoEaSlide(self, bitboard) -> int:
        return self._get_slide(bitboard, BinaryBoard.soEaOne, BinaryBoard.NOT_RANK_1, BinaryBoard.NOT_H_FILE)

    def getSoWeSlide(self, bitboard) -> int:
        return self._get_slide(bitboard, BinaryBoard.soWeOne, BinaryBoard.NOT_RANK_1, BinaryBoard.NOT_A_FILE)

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

    # MAIN FUNCTIONS

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
    Output: 8 x 8 x 14 tensor (last 2 are attack boards for white and black, resp.)
    """

    def generate_board_tensor(self) -> list[list[list[int]]]:
        boards = []

        boards.append(self.piece_boards['R'])
        boards.append(self.piece_boards['N'])
        boards.append(self.piece_boards['B'])
        boards.append(self.piece_boards['Q'])
        boards.append(self.piece_boards['K'])
        boards.append(self.piece_boards['P'])
        boards.append(self.piece_boards['r'])
        boards.append(self.piece_boards['n'])
        boards.append(self.piece_boards['b'])
        boards.append(self.piece_boards['q'])
        boards.append(self.piece_boards['k'])
        boards.append(self.piece_boards['p'])

        boards.append(self.generate_attack_board(0))  # white attack board
        boards.append(self.generate_attack_board(1))  # black attack board

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


TEST_FENS = ["rnbqkbnr/pppppppp/8/1p7/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0",
             "1rq2bnr/p3p1pp/1p2bk2/2pP1p2/5PnN/3P2PP/PP2P3/1RBQKBNR w - - 7 15",
             "r1bq1kn1/pppp4/2n4r/3Pp1pP/2B2p2/b2QP2P/PPP1KP2/RNB3NR w - - 3 10",
             "r1bqk1nr/p1pp1p1p/1pn1p3/6p1/8/1PP1BPP1/P1Q1P2P/RN2KBNR w KQkq - 0 8"]


def main():
    fen_string = TEST_FENS[0]
    board = BinaryBoard(fen_string)
    pprint_binboard(board.combined_board)
    pprint_binboard(board.generate_attack_board(0))
    pprint_binboard(board.generate_attack_board(1))
    print(bin(board.generate_attack_board(1)))


if __name__ == "__main__":
    main()
