from hex_rep import Board


def init_position() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    board.add_piece(1, board.WHITE | board.KNIGHT)
    board.add_piece(2, board.WHITE | board.BISHOP)
    board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    for i in range(8, 16):
        board.add_piece(i, board.WHITE | board.PAWN)
    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)

    return board

def castle_test() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    # board.add_piece(1, board.WHITE | board.KNIGHT)
    # board.add_piece(2, board.WHITE | board.BISHOP)
    # board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    # board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    for i in range(8, 16):
        if i != 12:
            board.add_piece(i, board.WHITE | board.PAWN)
    # board.add_piece( 17, board.BLACK | board.PAWN)
    # board.add_piece( 22, board.BLACK | board.PAWN)
    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)
    board.add_piece(36, board.BLACK | board.ROOK)


    return board

def move_out_of_block() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    # board.add_piece(1, board.WHITE | board.KNIGHT)
    # board.add_piece(2, board.WHITE | board.BISHOP)
    # board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    # board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(12, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    for i in range(8, 16):
        if i != 12:
            board.add_piece(i, board.WHITE | board.PAWN)
    # board.add_piece( 17, board.BLACK | board.PAWN)
    # board.add_piece( 22, board.BLACK | board.PAWN)
    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)
    board.add_piece(36, board.BLACK | board.ROOK)


    return board

def test_promo() -> Board:
    board = Board()
    board.board = 0x0
    # board.add_piece(0, board.WHITE | board.ROOK)
    # board.add_piece(1, board.WHITE | board.KNIGHT)
    # board.add_piece(2, board.WHITE | board.BISHOP)
    # board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    # board.add_piece(5, board.WHITE | board.BISHOP)
    # board.add_piece(6, board.WHITE | board.KNIGHT)
    # board.add_piece(7, board.WHITE | board.ROOK)
    for i in range(8, 9):
        if i != 12:
            board.add_piece(i, board.WHITE | board.PAWN)
    # board.add_piece( 17, board.BLACK | board.PAWN)
    # board.add_piece( 22, board.BLACK | board.PAWN)
    # for i in range(48, 56):
    #     board.add_piece(i, board.BLACK | board.PAWN)
    # board.add_piece(56, board.BLACK | board.ROOK)
    # board.add_piece(57, board.BLACK | board.KNIGHT)
    # board.add_piece(58, board.BLACK | board.BISHOP)
    # board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    # board.add_piece(61, board.BLACK | board.BISHOP)
    # board.add_piece(62, board.BLACK | board.KNIGHT)
    # board.add_piece(63, board.BLACK | board.ROOK)
    # board.add_piece(36, board.BLACK | board.ROOK)

    board.add_piece(50, board.WHITE | board.PAWN)
    # board.add_piece(0, board.WHITE | board.ROOK)

    # board.add_piece(7, board.WHITE | board.ROOK)




    return board


def test_position() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    board.add_piece(1, board.WHITE | board.KNIGHT)
    # board.add_piece( 2, board.WHITE | board.BISHOP)
    board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    # board.add_piece( 7, board.WHITE | board.ROOK)
    # board.add_piece(32, board.WHITE | board.PAWN)
    board.add_piece(39, board.WHITE | board.PAWN)
    board.add_piece(35, board.WHITE | board.BISHOP)

    for i in range(9, 13):
        board.add_piece(i, board.WHITE | board.PAWN)
    # for i in range(48, 56):
    #     board.add_piece( i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    # board.add_piece( 60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)

    # board.add_piece( 33, board.WHITE | board.KNIGHT)
    board.add_piece(44, board.WHITE | board.ROOK)
    board.add_piece(47, board.BLACK | board.ROOK)
    board.add_piece(40, board.WHITE | board.PAWN)
    board.add_piece(23, board.BLACK | board.PAWN)

    board.color_to_move = 0x0
    board.last_end_square = 0x0
    board.castle_states = 0x0
    board.can_en_passant = 0x0
    return board


def test_sliding() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    board.add_piece(1, board.WHITE | board.KNIGHT)
    board.add_piece(2, board.WHITE | board.BISHOP)
    board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    board.add_piece(32, board.WHITE | board.PAWN)
    board.add_piece(39, board.WHITE | board.PAWN)

    # for i in range(8, 16):
    #     board.add_piece( i, board.WHITE | board.PAWN)
    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)

    # board.add_piece( 33, board.WHITE | board.KNIGHT)
    board.add_piece(36, board.WHITE | board.ROOK)

    board.color_to_move = 0x0
    board.last_end_square = 0x0
    board.castle_states = 0x0
    board.can_en_passant = 0x0

    return board


def test_en_passant() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    board.add_piece(1, board.WHITE | board.KNIGHT)
    board.add_piece(2, board.WHITE | board.BISHOP)
    board.add_piece(3, board.WHITE | board.QUEEN)
    board.add_piece(4, board.WHITE | board.KING)
    board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    # for i in range(8, 16):
    #     board.add_piece( i, board.WHITE | board.PAWN)
    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)

    board.add_piece(33, board.BLACK | board.PAWN)
    board.add_piece(32, board.WHITE | board.PAWN)

    board.color_to_move = 0x0
    board.last_end_square = 33
    board.castle_states = 0x0
    board.can_en_passant = 0x1

    return board


def test_king() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(0, board.WHITE | board.ROOK)
    board.add_piece(1, board.WHITE | board.KNIGHT)
    board.add_piece(2, board.WHITE | board.BISHOP)
    board.add_piece(3, board.WHITE | board.QUEEN)
    # board.add_piece( 4, board.WHITE | board.KING)
    board.add_piece(5, board.WHITE | board.BISHOP)
    board.add_piece(6, board.WHITE | board.KNIGHT)
    board.add_piece(7, board.WHITE | board.ROOK)
    for i in range(8, 16):
        board.add_piece(i, board.WHITE | board.PAWN)
    # board.add_piece( 17, board.BLACK | board.PAWN)
    # board.add_piece( 22, board.BLACK | board.PAWN)
    board.add_piece(32, board.WHITE | board.KING)

    for i in range(48, 56):
        board.add_piece(i, board.BLACK | board.PAWN)
    board.add_piece(56, board.BLACK | board.ROOK)
    board.add_piece(57, board.BLACK | board.KNIGHT)
    board.add_piece(58, board.BLACK | board.BISHOP)
    board.add_piece(59, board.BLACK | board.QUEEN)
    board.add_piece(60, board.BLACK | board.KING)
    board.add_piece(61, board.BLACK | board.BISHOP)
    board.add_piece(62, board.BLACK | board.KNIGHT)
    board.add_piece(63, board.BLACK | board.ROOK)
    board.add_piece(17, board.BLACK | board.ROOK)

    return board

def test_draw() -> Board:
    board = Board()
    board.board = 0x0
    board.add_piece(59, board.BLACK | board.ROOK)
    board.add_piece(61, board.BLACK | board.ROOK)
    board.add_piece(47, board.BLACK | board.ROOK)
    board.add_piece(24, board.BLACK | board.ROOK)
    board.add_piece(52, board.BLACK | board.ROOK)


    board.add_piece(36, board.WHITE | board.KING)
    board.add_piece(60, board.BLACK | board.KING)



    return board


import random

def main():
    board = Board(test_draw().board, Board.BLACK)
    board.print_board_hex()
    board.print_board_hex(board.attack_board)

    all_curr = board.generate_all_possible_next_board_states()

    for move in all_curr:
        move.print_board_hex()

    board2 = Board(init_position().board, Board.BLACK)
    # print(board2.get_reward())
    print(board.get_reward())


    # chosen = random.choice(all_curr)

    # chosen.print_board_hex()
    # chosen.print_board_hex(chosen.attack_board)

    # print("===========================")
    # second_moves = chosen.generate_all_possible_next_board_states()
    # for move in second_moves:
    #     move.print_board_hex()

    # second_move = random.choice(second_moves)

    # second_move.print_board_hex()
    # second_move.print_board_hex(second_move.attack_board)

    # play_game()





def play_game():
    board = Board(init_position().board, Board.BLACK)

    max_moves = 256

    i = 0
    gameover = False
    current_state = board.generate_all_possible_next_board_states()
    while i < max_moves and not gameover:
        board = random.choice(current_state)
        # chosen.print_board_hex()
        # chosen.print_board_hex(chosen.attack_board)

        current_state = board.generate_all_possible_next_board_states()
        i += 1


    board.print_board_hex()




import numpy as np
import random


class ChessEnv:
    PIECE_VALUES = {
        'P': 1,  # Pawn
        'N': 3,  # Knight
        'B': 3,  # Bishop
        'R': 5,  # Rook
        'Q': 9,  # Queen
        'K': 0   # King (usually not counted for intermediate rewards)
    }

    def __init__(self, ):
        self.board = init_position()
        self.next_states = self.board.generate_all_possible_next_board_states()

    def init_board(self):
        return Board(init_position(), Board.BLACK)
    
    def next_states(self):
        return self.board.generate_all_possible_next_board_states()
    
    def apply_move(self):
        return 
    
    def get_reward(self):
        # Define your reward logic here
        if self.is_game_over():
            if self.is_checkmate():
                return 1 if self.turn == self.WHITE else -1
            elif self.is_draw():
                return 0
        # Intermediate rewards can be added here
        return self.material_balance()
    
    def material_balance(self):
        # Calculate material balance as a simple heuristic
        white_material = sum(self.PIECE_VALUES[piece] for piece in self.get_pieces(self.WHITE))
        black_material = sum(self.PIECE_VALUES[piece] for piece in self.get_pieces(self.BLACK))
        return white_material - black_material

class QLearningAgent:
    def __init__(self, action_space, state_space, alpha=0.1, gamma=0.99, epsilon=0.1):
        self.q_table = np.zeros((state_space, action_space))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.action_space = action_space

    def select_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(range(self.action_space))
        return np.argmax(self.q_table[state])

    def update(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.alpha * td_error


def train_agent(episodes=1000):
    env = Board(init_position().board, Board.BLACK)
    agent = QLearningAgent(action_space=len(env.next_states), state_space=1000)  # Adjust state_space

    max_moves = 256
    max_depth = 3

    for episode in range(episodes):
        env = Board(init_position().board, Board.BLACK)
        depth=0
        done = False
        i = 0
        while not done and i < max_moves:
            action = agent.select_action(state)
            next_state, reward, done = env.step(action)
            agent.update(state, action, reward, next_state)
            state = next_state
            
            i += 1
            depth += 1
            if depth >= max_depth:
                break



if __name__ == "__main__":
    # main()
    
    train_agent(episodes=10000)


# 0xabc0dcba00000000a00200011000000000000000900000000001111043465032
# 0xabc0dcba00000000a00200011000000000000000900000000001111043465032