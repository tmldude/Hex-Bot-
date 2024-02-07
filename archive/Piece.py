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

GAMEOVER = False

piece_english = {0:'WHITE', 1: 'PAWN', 2: 'ROOK', 3: 'KNIGHT', 4: 'BISHOP', 5:'QUEEN',6:'KING',7:'NO_PIECE', 8:'BLACK'}

def square_to_bit_position(file, rank):
    # Assuming the chessboard is represented with files a-h and ranks 1-8
    return 1 << (rank * 8 + file)


def int_only_place_on_board(file, rank):
    board = 0

    while file != 0:
        f = file % 10

        while rank != 0:
            r = rank % 10
            board |= square_to_bit_position(f, r)

            rank //= 10
        file //= 10

    return board 



def place_on_board(file, rank):
    board = 0

    for f in file:
        for r in rank: 
            board |= square_to_bit_position(f, r)

    return board

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

def get_color(move, white, black):
    if (white & move) != 0:
        return WHITE  # White piece
    elif (black & move) != 0:
        return BLACK  # Black piece
    else:
        return PIECE_MASK  # No piece at the specified position
    
def get_piece_type(move_board, all_piece_bitboards):
    pawn, rook, knight, bishop, queen, king = all_piece_bitboards
    if (pawn & move_board):
        return PAWN 
    if (rook & move_board):
        return ROOK 
    if (knight & move_board):
        return KNIGHT 
    if (bishop & move_board):
        return BISHOP 
    if (queen & move_board):
        return QUEEN 
    if (king & move_board):
        return KING 
    return PIECE_MASK 


def clear_piece(bit_board, file, rank):
    return bit_board & ~(1 << position)


    # return (piece_bitboard & color_bitboard & (1 << position)) != 0

        
def main():
    pawn = place_on_board([0, 1, 2, 3, 4, 5, 6, 7], [1, 6])
    rook = place_on_board([0, 7], [0, 7])
    knight = place_on_board([1, 6], [0, 7])
    bishop = place_on_board([2, 5], [0, 7])
    queen = place_on_board([3], [0, 7])
    king = place_on_board([4], [0, 7])

    all_piece_bitboards = [pawn, rook, knight, bishop, queen, king]

    black = place_on_board([0, 1, 2, 3, 4, 5, 6, 7], [6, 7])
    white = place_on_board([0, 1, 2, 3, 4, 5, 6, 7], [0, 1])

    all = place_on_board([0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 6, 7])

    coordinates = input("from ") 
    file0, rank0 = int(coordinates[0]), int(coordinates[1])
    coordinates = input("to ") 
    file1, rank1 = int(coordinates[0]), int(coordinates[1])


    move_board = place_on_board([file0], [rank0])
    to_board = place_on_board([file1], [rank1])

    color = get_color(move_board, white, black)
    print(piece_english[color])

    piece_type = get_piece_type(move_board, all_piece_bitboards)
    print(piece_english[piece_type])









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



    


    # all = place_on_board([0, 1, 2, 3, 4, 5, 6, 7], [1, 6])


    # print_labeled_bitboard(pawn, 'pawn')
    # print_labeled_bitboard(rook, 'rook')
    # print_labeled_bitboard(knight, 'knight')    
    # print_labeled_bitboard(bishop, 'bishop')    
    # print_labeled_bitboard(queen, 'queen')    
    # print_labeled_bitboard(king, 'king')
    # print_labeled_bitboard(white, 'white')    
    # print_labeled_bitboard(black, 'black')    
    # print_labeled_bitboard(all, 'all')



    # pieces, = initialize()
    
    # print(f"Bitboards are numbers: {all_bitboards['wp']}, {all_bitboards['bp']}\n=============\n")
    # print(f"In binary, they represent the board position for each piece. \nHere are the white pawn and black pawn bitboards: {bin(all_bitboards['wp'])}, {bin(all_bitboards['bp'])}\n=============\n")
    # print(f"| - or operationing all the bit boards get different results \n'all_bitboards['wp']' | 'all_bitboards['bp']' = {all_bitboards['wp'] | all_bitboards['bp']} = {bin(all_bitboards['wp'] | all_bitboards['bp'])})")
    # print(f"the final board looks like this in decimal and binary: {all_bitboards['a']}, {bin(all_bitboards['a'])}")
    # print_labeled_bitboard(all_bitboards['a'], "All Pieces")
    # print(f'8 bit difference in size between black pawn only and full board \n{bin(all_bitboards["bp"])}\n{bin(all_bitboards["a"])}')
    # print(f'Here are the white piece black piece boards: \n{bin(all_bitboards["w"])}\n{bin(all_bitboards["b"])}')


    # # input("Enter the file (1-8): ")    
    # print_labeled_bitboard(all_bitboards['a'], "First")
    # coordinates = input("Enter filerank with nothing separating: ") 
    # file, rank = int(coordinates[0]), int(coordinates[1])
    # print(file, rank)
    # position = rank * 8 + file
    # print(check_exists(all_bitboards["a"], position))

    # color = get_color(all_bitboards["w"], all_bitboards["b"], position)
    # color_text = 'white' if color == 1 else 'black' if color == -1 else 'no_piece'
    # print(color_text)

   
    # if color == 0:  # change into break later
    #     print('no piece')
    # else:
    #     color_bitboard = all_bitboards["w"] if color == 1 else all_bitboards["b"] 

    #     piece_type = get_piece_type(all_bitboards["a"], file, rank, color_bitboard)
    #     print(piece_type)
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


