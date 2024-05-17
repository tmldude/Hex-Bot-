'''Takes in a hex number and a hex digit to add, returns the hex number with the new digit'''


def add_rightmost_hex_digit(number, digit_piece) -> int:
    updated_board: int = (number << 4) | digit_piece
    return updated_board


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


def print_number_board():
    string = ''
    for i in range(7, -1, -1):  # Start from 7 and decrement to 0
        for j in range(8):
            string = string + str(i * 8 + j) + " "
        string = string + '\n'  # Add newline after each row

    print(string)
