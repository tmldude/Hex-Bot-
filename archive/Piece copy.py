# Define constants for piece types
PAWN = 0
ROOK = 1
KNIGHT = 2
BISHOP = 3
QUEEN = 4
KING = 5

# Constants for colors
WHITE = 1
BLACK = -1

GAMEOVER = False

def square_to_bit_position(file, rank):
    # Assuming the chessboard is represented with files a-h and ranks 1-8
    return 1 << (rank * 8 + file)

def initialize_pawn_bitboard(color):
    # color can be 'white' or 'black'
    pawn_rank = 1 if color == 'white' else 6
    pawn_bitboard = 0

    # Set bits for all pawns in the starting rank
    for file in range(8):
        pawn_bitboard |= square_to_bit_position(file, pawn_rank)

    return pawn_bitboard

def initialize_rook_bitboard(color):
    rank = 0 if color == 'white' else 7  # Rooks start on the first or eighth rank
    rook_bitboard = 0

    # Set bits for both rooks in the starting rank
    for file in [0, 7]:
        rook_bitboard |= square_to_bit_position(file, rank)

    return rook_bitboard

def initialize_knight_bitboard(color):
    rank = 0 if color == 'white' else 7  # Knights start on the first or eighth rank
    knight_bitboard = 0

    # Set bits for both knights in the starting rank
    for file in [1, 6]:  # Assuming knights start on files 1 and 6
        knight_bitboard |= square_to_bit_position(file, rank)

    return knight_bitboard

def initialize_bishop_bitboard(color):
    rank = 0 if color == 'white' else 7  # Bishops start on the first or eighth rank
    bishop_bitboard = 0

    # Set bits for both bishops in the starting rank
    for file in [2, 5]:  # Assuming bishops start on files 2 and 5
        bishop_bitboard |= square_to_bit_position(file, rank)

    return bishop_bitboard

def initialize_king_bitboard(color):
    rank = 0 if color == 'white' else 7  # Kings start on the first or eighth rank
    king_bitboard = 0

    # Set bits for both kings in the starting rank
    for file in [4]:  # Assuming kings start in the center (file 4)
        king_bitboard |= square_to_bit_position(file, rank)

    return king_bitboard

def initialize_queen_bitboard(color):
    rank = 0 if color == 'white' else 7  # Queens start on the first or eighth rank
    queen_bitboard = 0

    # Set bits for both queens in the starting rank
    for file in [3]:  # Assuming queens start in the center (file 3)
        queen_bitboard |= square_to_bit_position(file, rank)

    return queen_bitboard

def print_bitboard(bitboard):
    for rank in range(7, -1, -1):
        for file in range(8):
            square = 8 * rank + file
            if bitboard & (1 << square):
                print("1", end=" ")
            else:
                print("0", end=" ")
        print()


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


def initialize():

    white_queen_bitboard = initialize_queen_bitboard('white')
    black_queen_bitboard = initialize_queen_bitboard('black')

    white_king_bitboard = initialize_king_bitboard('white')
    black_king_bitboard = initialize_king_bitboard('black')

    white_bishop_bitboard = initialize_bishop_bitboard('white')
    black_bishop_bitboard = initialize_bishop_bitboard('black')

    white_knight_bitboard = initialize_knight_bitboard('white')
    black_knight_bitboard = initialize_knight_bitboard('black')

    white_rook_bitboard = initialize_rook_bitboard('white')
    black_rook_bitboard = initialize_rook_bitboard('black')

    white_pawn_bitboard = initialize_pawn_bitboard('white')
    black_pawn_bitboard = initialize_pawn_bitboard('black')

    all_pieces_bitboard = (
        white_pawn_bitboard | white_rook_bitboard | white_knight_bitboard |
        white_bishop_bitboard | white_queen_bitboard | white_king_bitboard |
        black_pawn_bitboard | black_rook_bitboard | black_knight_bitboard |
        black_bishop_bitboard | black_queen_bitboard | black_king_bitboard
    )

    white_bitboard = (white_pawn_bitboard | white_rook_bitboard | white_knight_bitboard |
        white_bishop_bitboard | white_queen_bitboard | white_king_bitboard)
    black_bitboard = (black_pawn_bitboard | black_rook_bitboard | black_knight_bitboard |
        black_bishop_bitboard | black_queen_bitboard | black_king_bitboard)

    return [{'wp': white_pawn_bitboard, 'wr': white_rook_bitboard, 'wk': white_knight_bitboard, \
        'wb': white_bishop_bitboard, 'wq': white_queen_bitboard, 'wK': white_king_bitboard,\
        'bp':black_pawn_bitboard, 'br':black_rook_bitboard, 'bk':black_knight_bitboard,\
        'bb':black_bishop_bitboard, 'bq':black_queen_bitboard, 'bK':black_king_bitboard},{
        'a':all_pieces_bitboard, 'w':white_bitboard, 'b':black_bitboard} ]

def check_exists(all_pieces_bitboard, position):
    return (all_pieces_bitboard & (1 << position)) != 0

def get_color(white_bitboard, black_bitboard, position):
    if (white_bitboard & (1 << position)) != 0:
        return 1  # White piece
    elif (black_bitboard & (1 << position)) != 0:
        return -1  # Black piece
    else:
        return 0  # No piece at the specified position
    
def get_piece_type(all_pieces_bitboard, curr_board, file, rank):
    position = rank * 8 + file
    print(bin(position))
    
    # Check if the position is occupied by a piece of the specified color
    if (all_pieces_bitboard & curr_board):
        return True 
    return False 

def checkall(all_bitboards):
    for key in all_bitboards.keys():
        if key == 'a' or key == 'w' or key == 'b':
            pass
        # else:




def clear_piece(bitboard, position):
    return bitboard & ~(1 << position)


    # return (piece_bitboard & color_bitboard & (1 << position)) != 0


def generate_knight_moves(square):
    # Generate all possible knight moves from a given square
    x, y = square % 8, square // 8
    moves = []

    for dx, dy in [(1, 2), (2, 1), (-1, 2), (-2, 1),
                   (-1, -2), (-2, -1), (1, -2), (2, -1)]:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 8 and 0 <= new_y < 8:
            moves.append(new_x + new_y * 8)

    return moves
        
def main():
    pieces, special = initialize()
    
    print(f"Bitboards are numbers: {all_bitboards['wp']}, {all_bitboards['bp']}\n=============\n")
    print(f"In binary, they represent the board position for each piece. \nHere are the white pawn and black pawn bitboards: {bin(all_bitboards['wp'])}, {bin(all_bitboards['bp'])}\n=============\n")
    print(f"| - or operationing all the bit boards get different results \n'all_bitboards['wp']' | 'all_bitboards['bp']' = {all_bitboards['wp'] | all_bitboards['bp']} = {bin(all_bitboards['wp'] | all_bitboards['bp'])})")
    print(f"the final board looks like this in decimal and binary: {all_bitboards['a']}, {bin(all_bitboards['a'])}")
    print_labeled_bitboard(all_bitboards['a'], "All Pieces")
    print(f'8 bit difference in size between black pawn only and full board \n{bin(all_bitboards["bp"])}\n{bin(all_bitboards["a"])}')
    print(f'Here are the white piece black piece boards: \n{bin(all_bitboards["w"])}\n{bin(all_bitboards["b"])}')


    # input("Enter the file (1-8): ")    
    print_labeled_bitboard(all_bitboards['a'], "First")
    coordinates = input("Enter filerank with nothing separating: ") 
    file, rank = int(coordinates[0]), int(coordinates[1])
    print(file, rank)
    position = rank * 8 + file
    print(check_exists(all_bitboards["a"], position))

    color = get_color(all_bitboards["w"], all_bitboards["b"], position)
    color_text = 'white' if color == 1 else 'black' if color == -1 else 'no_piece'
    print(color_text)

   
    if color == 0:  # change into break later
        print('no piece')
    else:
        color_bitboard = all_bitboards["w"] if color == 1 else all_bitboards["b"] 

        piece_type = get_piece_type(all_bitboards["a"], file, rank, color_bitboard)
        print(piece_type)
    # piece_type = get_piece_type(all_bitboards['a'], color, file_to_check, rank_to_check)

    # while True: 
    #     file, rank = map(int, coordinates.split())
    #     if 

    #     all_pieces_bitboard = clear_piece(all_pieces_bitboard, file, rank)
  
# while(not GAMEOVER):
        
        # Define constants for piece types
# PAWN = 0
# ROOK = 1
# KNIGHT = 2
# BISHOP = 3
# QUEEN = 4
# KING = 5


if __name__ == "__main__":
    main()


