from hex_rep import add_piece, BLACK, PIECE_MASK, ROOK, BISHOP, QUEEN


def generate_pawn_moves(file, rank, color, board, piece):
    output = []

    # Determine direction of movement based on pawn color
    if color == 'white':
        direction = 1
    else:
        direction = -1

    # Check if pawn can move one square forward
    if 0 <= rank + direction < 8 and board[rank + direction][file] is None:
        output.append((file, rank + direction))

        # Check if pawn can move two squares forward from starting position
        if ((color == 'white' and rank == 1) or
           (color == 'black' and rank == 6)) and board[rank + 2 * direction][file] is None:
            output.append((file, rank + 2 * direction))

    # Check if pawn can capture diagonally
    if 0 <= file - 1 < 8 and 0 <= rank + direction < 8:
        if board[rank + direction][file - 1] is not None and board[rank + direction][file - 1].color != color:
            output.append((file - 1, rank + direction))
    if 0 <= file + 1 < 8 and 0 <= rank + direction < 8:
        if board[rank + direction][file + 1] is not None and board[rank + direction][file + 1].color != color:
            output.append((file + 1, rank + direction))

    return output


def generate_pawn_moves_ep(file, rank, color, board, piece, en_passant_target):
    output = []

    # Determine direction of movement based on pawn color
    if color == 'white':
        direction = 1
        starting_rank = 1
    else:
        direction = -1
        starting_rank = 6

    # Check if pawn can move one square forward
    if 0 <= rank + direction < 8 and board[rank + direction][file] is None:
        output.append((file, rank + direction))

        # Check if pawn can move two squares forward from starting position
        if rank == starting_rank and board[rank + 2 * direction][file] is None:
            output.append((file, rank + 2 * direction))

    # Check if pawn can capture diagonally
    if 0 <= file - 1 < 8 and 0 <= rank + direction < 8:
        if board[rank + direction][file - 1] is not None and board[rank + direction][file - 1].color != color:
            output.append((file - 1, rank + direction))
        elif (file - 1, rank + direction) == en_passant_target:
            output.append((file - 1, rank + direction))

    if 0 <= file + 1 < 8 and 0 <= rank + direction < 8:
        if board[rank + direction][file + 1] is not None and board[rank + direction][file + 1].color != color:
            output.append((file + 1, rank + direction))
        elif (file + 1, rank + direction) == en_passant_target:
            output.append((file + 1, rank + direction))

    return output


def generate_knight_moves(color, spot, board):
    num = 0b00010010110111100100011110001011
    output = 0

    while num != 0:
        curr = num & 0xF
        num >>= 4  # Move to the next group of 4 bits

        # Calculate potential moves
        if spot + 1 < 64 and (spot + 1) % 8 != 0:
            if curr == 1:
                output |= (spot + 2 * 8) + 1
            elif curr == 10:
                output |= (spot + 2 * 8) - 1
        if spot - 1 >= 0 and spot % 8 != 0:
            if curr == 1101:
                output |= (spot - 2 * 8) + 1
            elif curr == 1110:
                output |= (spot - 2 * 8) - 1
        if spot + 8 < 64:
            if curr == 100:
                output |= (spot + 1 * 8) + 2
            elif curr == 111:
                output |= (spot + 1 * 8) - 2
        if spot - 8 >= 0:
            if curr == 1000:
                output |= (spot - 1 * 8) + 2
            elif curr == 1011:
                output |= (spot - 1 * 8) - 2

    return output


def generate_knight_moves_1(file, rank, color, board, piece):

    # +2 = 00 = 0
    # +1 = 1 = 1
    # -1 = 10 = 2
    # -2 = 11 = 3
    num = 0b00010010110111100100011110001011

    output = 0

    old_square = file * 8 + rank
    is_left_edge = old_square % 8 == 0
    is_right_edge = old_square - 7 % 8 == 0

    print(is_left_edge, is_right_edge)

    while num > 0:
        curr = num & 0b1111
        new_file = 0
        new_rank = 0

        if curr == 0b1 and not is_right_edge:
            new_file = file + 2
            new_rank = rank + 1
        elif curr == 0b10 and not is_right_edge:
            new_file = file + 2
            new_rank = rank - 1
        elif curr == 0b1101:  # and not is_left_edge:
            new_file = file - 2
            new_rank = rank + 1
        elif curr == 0b1110:  # and not is_left_edge:
            new_file = file - 2
            new_rank = rank - 1
        elif curr == 0b100 and not is_right_edge:
            new_file = file + 1
            new_rank = rank + 2
        elif curr == 0b111:  # and not is_left_edge:
            new_file = file - 1
            new_rank = rank + 2
        elif curr == 0b1000 and not is_right_edge:
            new_file = file + 1
            new_rank = rank - 2
        elif curr == 0b1011:  # and not is_left_edge:
            new_file = file - 1
            new_rank = rank - 2

        # print(new_file, new_rank, bin(num))
        # new_file >= 8 or new_rank <= 8 or new_file < 0 or new_rank > 0
        new_square = new_rank * 8 + new_file
        if new_square < 0 or new_square >= 64:
            pass
        else:
            output = add_piece(board, new_square, color, piece, hexa=True)
            print(output)

        num = num >> 0b100
    print(hex(output))

    return output


def generate_knight_moves_2(color, spot, board, piece):

    # +2 = 00 = 0
    # +1 = 1 = 1
    # -1 = 10 = 2
    # -2 = 11 = 3
    num = 0b00010010110111100100011110001011

    output = 0

    while num != 0:
        curr = num & 0b1111
        new_spot = spot

        if curr == 0b1:
            new_spot = (new_spot + 2 * 8) + 1
        elif curr == 0b10:
            new_spot = (new_spot + 2 * 8) - 1
        elif curr == 0b1101:
            new_spot = (new_spot - 2 * 8) + 1
        elif curr == 0b1110:
            new_spot = (new_spot - 2 * 8) - 1
        elif curr == 0b100:
            new_spot = (new_spot + 1 * 8) + 2
        elif curr == 0b111:
            new_spot = (new_spot + 1 * 8) - 2
        elif curr == 0b1000:
            new_spot = (new_spot - 1 * 8) + 2
        if curr == 0b1011:
            new_spot = (new_spot - 1 * 8) - 2
        else:
            # print(bin(curr), "not on board")
            pass

        if new_spot >= 64 or new_spot < 0:
            pass
        else:
            output = add_piece(output, new_spot, BLACK, PIECE_MASK)

        num = num >> 0b100

    return output


def generate_knight_moves_3(color, spot, board):

    # +2 = 00 = 0
    # +1 = 1 = 1
    # -1 = 10 = 2
    # -2 = 11 = 3
    num = 0b00010010110111100100011110001011

    output = 0

    while num != 0:
        curr = num & 0xF
        if spot + 1 >= 64 or spot - 1 <= 0:
            pass
        elif curr == 1:
            output = output >> 7 | ((spot + 2 * 8) + 1)
        elif curr == 10:
            output = output >> 7 | (spot + 2 * 8) - 1
        elif curr == 1101:
            output = output >> 7 | (spot - 2 * 8) + 1
        elif curr == 1110:
            output = output >> 7 | (spot - 2 * 8) - 1
        elif curr == 100:
            output = output >> 7 | (spot + 1 * 8) + 2
        elif curr == 111:
            output = output >> 7 | (spot + 1 * 8) - 2
        elif curr == 1000:
            output = output >> 7 | (spot - 1 * 8) + 2
        if curr == 1011:
            output = output >> 7 | (spot - 1 * 8) - 2
        else:
            print(curr, "not on board")
    return output


def generate_bishop_moves(pos, color, board):
    pos += 1  # 0-based -> 1-based

    output_boards = []

    # UP-LEFT MOVES
    inc = 9
    idx = pos + inc
    while idx % 8 != 0:
        square = board[idx]
        if square != 0:  # Blocked
            if square - color >= 0:  # If enemy piece
                output_boards.append(
                    add_piece(board, idx, color, BISHOP))  # Capture
            break
        else:
            output_boards.append(add_piece(board, idx, color, BISHOP))  # Move

        # Edge check
        if idx % 8 == 0:
            break

        idx += inc

    # UP-RIGHT MOVES
    inc = 7
    idx = pos + inc
    while idx % 8 != 0:
        square = board[idx]
        if square != 0:  # Blocked
            if square - color >= 0:  # If enemy piece
                output_boards.append(
                    add_piece(board, idx, color, BISHOP))  # Capture
            break
        else:
            output_boards.append(add_piece(board, idx, color, BISHOP))  # Move

        # Edge check
        if idx % 8 == 1:
            break

        idx += inc

    # DOWN-LEFT MOVES
    inc = -7
    idx = pos + inc
    while idx <= 64:
        square = board[idx]
        if square != 0:  # Blocked
            if square - color >= 0:  # If enemy piece
                output_boards.append(
                    add_piece(board, idx, color, BISHOP))  # Capture
            break
        else:
            output_boards.append(add_piece(board, idx, color, BISHOP))  # Move

        # Edge check
        if idx % 8 == 0:
            break

        idx += inc

    # DOWN-RIGHT MOVES
    inc = -9
    idx = pos + inc
    while idx >= 1:
        square = board[idx]
        if square != 0:  # Blocked
            if square - color >= 0:  # If enemy piece
                output_boards.append(
                    add_piece(board, idx, color, BISHOP))  # Capture
            break
        else:
            output_boards.append(add_piece(board, idx, color, BISHOP))  # Move

        # Edge check
        if idx % 8 == 1:
            break

        idx += inc

    return output_boards


def generate_rook_moves(pos, color, board):
    pos += 1  # 0-based -> 1-based

    output_boards = []

    # LEFT MOVES
    inc = 1
    idx = pos + inc
    while idx % 8 != 0:
        square = board[idx]
        if square != 0:  # Blocked
            if square - color >= 0:  # If enemy piece
                output_boards.append(
                    add_piece(board, idx, color, ROOK))  # Capture
            break
        else:
            output_boards.append(add_piece(board, idx, color, ROOK))  # Move

        idx += inc

    # RIGHT MOVES
    inc = -1
    idx = pos + inc
    while idx % 8 != 0:
        square = board[idx]
        if square != 0:  # Blocked
            if square - color >= 0:  # If enemy piece
                output_boards.append(
                    add_piece(board, idx, color, ROOK))  # Capture
            break
        else:
            output_boards.append(add_piece(board, idx, color, ROOK))  # Move

        idx += inc

    # UP MOVES
    inc = 8
    idx = pos + inc
    while idx <= 64:
        square = board[idx]
        if square != 0:  # Blocked
            if square - color >= 0:  # If enemy piece
                output_boards.append(
                    add_piece(board, idx, color, ROOK))  # Capture
            break
        else:
            output_boards.append(add_piece(board, idx, color, ROOK))  # Move
        idx += inc

    # DOWN MOVES
    inc = -8
    idx = pos + inc
    while idx >= 1:
        square = board[idx]
        if square != 0:  # Blocked
            if square - color >= 0:  # If enemy piece
                output_boards.append(
                    add_piece(board, idx, color, ROOK))  # Capture
            break
        else:
            output_boards.append(add_piece(board, idx, color, ROOK))  # Move
        idx += inc

    return output_boards


def generate_queen_moves(file, rank, color, board, piece):
    pos += 1  # 0-based -> 1-based

    output_boards = []

    # UP-LEFT MOVES
    inc = 9
    idx = pos + inc
    while idx % 8 != 0:
        square = board[idx]
        if square != 0:  # Blocked
            if square - color >= 0:  # If enemy piece
                output_boards.append(
                    add_piece(board, idx, color, QUEEN))  # Capture
            break
        else:
            output_boards.append(add_piece(board, idx, color, QUEEN))  # Move

        # Edge check
        if idx % 8 == 0:
            break

        idx += inc

    # UP-RIGHT MOVES
    inc = 7
    idx = pos + inc
    while idx % 8 != 0:
        square = board[idx]
        if square != 0:  # Blocked
            if square - color >= 0:  # If enemy piece
                output_boards.append(
                    add_piece(board, idx, color, QUEEN))  # Capture
            break
        else:
            output_boards.append(add_piece(board, idx, color, QUEEN))  # Move

        # Edge check
        if idx % 8 == 1:
            break

        idx += inc

    # DOWN-LEFT MOVES
    inc = -7
    idx = pos + inc
    while idx <= 64:
        square = board[idx]
        if square != 0:  # Blocked
            if square - color >= 0:  # If enemy piece
                output_boards.append(
                    add_piece(board, idx, color, QUEEN))  # Capture
            break
        else:
            output_boards.append(add_piece(board, idx, color, QUEEN))  # Move

        # Edge check
        if idx % 8 == 0:
            break

        idx += inc

    # DOWN-RIGHT MOVES
    inc = -9
    idx = pos + inc
    while idx >= 1:
        square = board[idx]
        if square != 0:  # Blocked
            if square - color >= 0:  # If enemy piece
                output_boards.append(
                    add_piece(board, idx, color, QUEEN))  # Capture
            break
        else:
            output_boards.append(add_piece(board, idx, color, QUEEN))  # Move

        # Edge check
        if idx % 8 == 1:
            break

        idx += inc

     # LEFT MOVES
    inc = 1
    idx = pos + inc
    while idx % 8 != 0:
        square = board[idx]
        if square != 0:  # Blocked
            if square - color >= 0:  # If enemy piece
                output_boards.append(
                    add_piece(board, idx, color, QUEEN))  # Capture
            break
        else:
            output_boards.append(add_piece(board, idx, color, QUEEN))  # Move

        idx += inc

    # RIGHT MOVES
    inc = -1
    idx = pos + inc
    while idx % 8 != 0:
        square = board[idx]
        if square != 0:  # Blocked
            if square - color >= 0:  # If enemy piece
                output_boards.append(
                    add_piece(board, idx, color, QUEEN))  # Capture
            break
        else:
            output_boards.append(add_piece(board, idx, color, QUEEN))  # Move

        idx += inc

    # UP MOVES
    inc = 8
    idx = pos + inc
    while idx <= 64:
        square = board[idx]
        if square != 0:  # Blocked
            if square - color >= 0:  # If enemy piece
                output_boards.append(
                    add_piece(board, idx, color, QUEEN))  # Capture
            break
        else:
            output_boards.append(add_piece(board, idx, color, QUEEN))  # Move
        idx += inc

    # DOWN MOVES
    inc = -8
    idx = pos + inc
    while idx >= 1:
        square = board[idx]
        if square != 0:  # Blocked
            if square - color >= 0:  # If enemy piece
                output_boards.append(
                    add_piece(board, idx, color, QUEEN))  # Capture
            break
        else:
            output_boards.append(add_piece(board, idx, color, QUEEN))  # Move
        idx += inc

    return output_boards


def is_square_attacked(rank, file, color, board):
    pass


def generate_king_moves(pos, color, board, opp_side_attacks):
    output_boards = []

    return output_boards
