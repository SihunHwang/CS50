"""
Tic Tac Toe Player
"""

import math
import copy
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_X =[]
    num_O =[]
    for row in board:
        num_X_row = row.count(X)
        num_X.append(num_X_row)
        num_O_row = row.count(O)
        num_O.append(num_O_row)
    if sum(num_X) > sum(num_O):
        return O
    else :
        return X

    raise NotImplementedError
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set()
    i=0
    for row in board:
        j=0
        for column in row:
            if column == EMPTY :
                actions_set.add((i,j))
            j=j+1
        i+=1
    return actions_set
    


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board) :
        raise Exception
    result_board = copy.deepcopy(board)
    result_board[action[0]][action[1]] = player(board)
    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def check_for(a):
        if [a,a,a] in board:
            return True
        list =[]
        for row in board:
            for cell in row:
                list.append(cell)
        for position in range(3):
            if list[position]==a and list[position+3]==a and list[position+6]==a :
                return True
        if list[4]==a:
            if list[0]==a and list[8]==a:
                return True
            elif list[2]==a and list[6]==a:
                return True
        else :
            return None
    
    if check_for(O):
        return O
    elif check_for(X):
        return X
    else :
        return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    list =[]
    for row in board:
        for cell in row:
            list.append(cell)
    if EMPTY not in list or winner(board) is not None:
        return True
    else :
        return False
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)==X:
        return 1
    elif winner(board)==O:
        return -1
    else :
        return 0
    raise NotImplementedError

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v    

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v    
    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X:
        v = -math.inf
        for action in actions(board):
            x = min_value(result(board, action))    
            if x > v:
                v = x
                best_move = action
    else:
        v = math.inf
        for action in actions(board):
            x = max_value(result(board, action))    
            if x < v:
                v = x
                best_move = action
    return best_move
