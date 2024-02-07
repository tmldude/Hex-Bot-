class ChessBitboard:
    def __init__(self, hex_number):
        self.hex_number = hex_number

    def get_piece_type(self, square):
        """
        Get the piece type (P, R, N, B, Q, K) from the hexadecimal number at the given square.

        Args:
        - square (int): The square number (0-63) representing the position on the chessboard.

        Returns:
        - str: The piece type extracted from the hexadecimal number.
        """
        hex_digit = self.get_hex_digit(square)
        piece_types = {'0': '.', '1': 'P', '2': 'R', '3': 'N', '4': 'B', '5': 'Q', '6': 'K', '7': 'p', '8': 'r', '9': 'n', 'A': 'b', 'B': 'q', 'C': 'k'}
        return piece_types[hex_digit]

    def get_piece_color(self, square):
        """
        Get the piece color (white or black) from the hexadecimal number at the given square.

        Args:
        - square (int): The square number (0-63) representing the position on the chessboard.

        Returns:
        - str: The piece color extracted from the hexadecimal number.
        """
        hex_digit = self.get_hex_digit(square)
        if hex_digit in {'0', '1', '2', '3', '4', '5', '6'}:
            return 'white'
        elif hex_digit in {'7', '8', '9', 'A', 'B', 'C'}:
            return 'black'
        else:
            return 'unknown'

    def get_hex_digit(self, square):
        """
        Get the hexadecimal digit from the hexadecimal number at the given square.

        Args:
        - square (int): The square number (0-63) representing the position on the chessboard.

        Returns:
        - str: The hexadecimal digit extracted from the hexadecimal number.
        """
        print(self.hex_number[square])
        return self.hex_number[square]

# Example Usage
hex_number = "123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF"
bitboard = ChessBitboard(hex_number)

# Get piece type and color for square 0 (a8)
print("Piece type at square 0:", bitboard.get_piece_type(55))  # Output: 'R'
print("Piece color at square 0:", bitboard.get_piece_color(55))  # Output: 'black'
