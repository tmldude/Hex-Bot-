from hex_rep import get_move


# from evaluation import evaluate
import random
def evaluate():
    return random.uniform(-10, 10)


class Node:
    '''
    Class Node which represents each state in the minimax decision tree

    Board -> the hex representation of the board we have that has
    Eval -> the ML evaluation of the board (currently just a random num)
    Next_Moves -> all possible next moves generated from the move logic (currently unimplemented)

    TO DO:  
    1. Decide how you want the nodes to chain together or if they do not because minimax is an exhaustive decision algo
    2. Build out the minimiax 
    3. Build out the alpha-beta optimization 
    
    '''
    def __init__(self, board: int) -> None:
        self.board = board 
        self.eval = evaluate() # evaluate(board)
        self.next_moves = get_move(board)


# builds decision tree based on next moves and evaluation 
def mini_max():
    return 'Unimplemented'