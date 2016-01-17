from util import memoize, run_search_function

def basic_evaluate(board):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified. 
    """
    #import random
    #return random.randint(1,100)
    if board.is_game_over():
    #     # If the game has been won, we know that it must have been
    #     # won or ended by the previous move.
    #     # The previous move was made by our opponent.
    #     # Therefore, we can't have won, so return -1000.
    #     # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
         score = board.longest_chain(board.get_current_player_id()) * 10
    #     # Prefer having your pieces in the center of the board.
         for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)

    return score

"""
This function evaluates a board and return the score of the board.
Evaluation strategy discussed in Project Report doc
"""
def new_evaluate(board):
    score = 0
    score_1 = 0
    score_2 = 0
    
    score = board.longest_chain(board.get_current_player_id()) * 10
    
    #check in each column
    for col in range(7):
        #Get the index of the first cell in the specified column that is filled.
        top = board.get_height_of_column(col)
        if top == -1:
            continue        #If Column is filled, check other columns
        top = top + 1
        if top > board.board_height - 1:
            continue        #If Column is empty, check other columns

        #if current player, it calculates its score
        if board.get_cell(top, col) == board.get_current_player_id():
            len = board._max_length_from_cell(top, col)
            if len == 3:
                score_1 = score_1 + 100     #If maximum length containing this cell is 3, assign 100
            if len == 2:
                score_1 = score_1 + 25      #If maximum length containing this cell is 2, assign 25
            if len == 1:
                score_1 = score_1 + 5       #If maximum length containing this cell is 1, assign 5
        elif board.get_cell(top, col) == board.get_other_player_id():       #if other player, it calculates its score
            len = board._max_length_from_cell(top, col)
            if len == 3:
                score_2 = score_2 + 200     #If maximum length containing this cell is 3, assign 200, as this is for opponent player so assigned a higher score so that current player tries to stop other player from wining
            if len == 2:
                score_2 = score_2 + 25      #If maximum length containing this cell is 2, assign 25
            if len == 1:
                score_2 = score_2 + 5       #If maximum length containing this cell is 1, assign 5

    #Return score after deducting the score of the other player
    score = score + score_1 - score_2

    return score


def get_all_next_moves(board):
    """ Return a generator of all moves that the current player could take from this position """
    from connectfour import InvalidMoveException

    for i in xrange(7):
        try:
            yield (i, board.do_move(i))
        except InvalidMoveException:
            pass

def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.is_game_over()


nodes_expanded = 0

def minimax(board, depth, eval_fn = basic_evaluate,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = True):
    """
    Do a minimax search to the specified depth on the specified board.

    board -- the ConnectFourBoard instance to evaluate
    depth -- the depth of the search tree (measured in maximum distance from a leaf to the root)
    eval_fn -- (optional) the evaluation function to use to give a value to a leaf of the tree; see "focused_evaluate" in the lab for an example

    Returns an integer, the column number of the column that the search determines you should add a token to
    """
    tuple = minimaxUtil(board,depth,True, basic_evaluate)
    
    #Getting final nodes expanded value in nodesExpanded
    global nodes_expanded
    nodes_expanded = nodes_expanded + tuple[2]
    col = compareBoard(board,tuple[1])
    return col

#return next board with maximum score for max player, also returns expanded nodes in tuple
def returnMax(array):

    score = array[0][0]
    board = array[0][1]
    expNodes = 1

    for tuple in array:
        expNodes = expNodes + tuple[2]
        if tuple[0] > score:
            score = tuple[0]
            board = tuple[1]

    return (score,board,expNodes)

#return next board with minimum score for min player, also returns expanded nodes in tuple
def returnMin(array):

    score = array[0][0]
    board = array[0][1]
    expNodes = 1

    for tuple in array:
        expNodes = expNodes + tuple[2]
        if tuple[0] < score:
            score = tuple[0]
            board = tuple[1]

    return (score,board,expNodes)

#This function compares 2 boards
def compareBoard(board, move_board):
    print "board", board
    for row in range(6):
        for col in range(7):
            if board.get_cell(row, col) != move_board.get_cell(row,col):
                return col

"""
This function does min-max search on the given board state and return a new board state with its evaluated value.
@param board: current board instance
@param depth: depth upto which search will run
@param is_max: For checking between max player and min player
@param eval_fn: evaluation function
@param get_next_moves_fn:
@param is_terminal_fn:
@param verbose:
@return value: (evaluated value of board, board)
"""
def minimaxUtil(board, depth,isMax, eval_fn,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = True):

    if depth == 0:
        #returns evalutated value of the board, board, expanded node 
        return (eval_fn(board),board,1)

    scoreArray = []
    for currentBoard in get_next_moves_fn(board):
        if board.get_current_player_id() == 1:
            scoreArray.append(minimaxUtil(currentBoard[1],depth-1,not isMax, new_evaluate))
        else:   
            scoreArray.append(minimaxUtil(currentBoard[1],depth-1,not isMax, basic_evaluate))
            
    if isMax:
        return returnMax(scoreArray)

    return returnMin(scoreArray)


def rand_select(board):
    """
    Pick a column by random
    """
    import random
    moves = [move for move, new_board in get_all_next_moves(board)]
    return moves[random.randint(0, len(moves) - 1)]


random_player = lambda board: rand_select(board)
basic_player = lambda board: minimax(board, depth=4, eval_fn=basic_evaluate)
#new player with new evaluate function
new_player = lambda board: minimax(board, depth=4, eval_fn=new_evaluate)
progressive_deepening_player = lambda board: run_search_function(board, search_fn=minimax, eval_fn=basic_evaluate)

