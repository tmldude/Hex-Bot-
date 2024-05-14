'''Takes in a hex number and a hex digit to add, returns the hex number with the new digit'''


def add_rightmost_hex_digit(number, digit_piece) -> int:
    updated_board: int = (number << 4) | digit_piece
    return updated_board


'''a board with 1 piece one it ie 100100000000
looks for the 1 piece and returns how many squares from the beginning it is
for en passant past move square check'''


def get_square_from_piece(hex_number) -> int:
    count: int = 0
    while hex_number & 0xF == 0:
        hex_number >>= 4
        count += 1
        if hex_number == 0:
            return None  # No non-zero hex digit found
    return count
