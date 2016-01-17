# 6.034 Fall 2010 Lab 3: Games
# Name: <Aman Raj, Dhanendra Jain>
# Email: <amraj@cs.stonybrook.edu, dhjain@cs.stonybrook.edu>

from util import INFINITY
import copy

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 0

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 0

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)
#run_game(human_player, basic_player)
#run_game(human_player, basic_player)

## Or watch the computer play against itself:
#run_game(random_player, basic_player)

#Running game between new player with new_evaluation and basic player with basic_evaluation
#run_game(new_player, basic_player, winNum=4)
#run_game(new_player, basic_player, winNum=3)
#run_game(basic_player, random_player)

from basicplayer import nodes_expanded
#printing nodes expanded in new player
print "Expanded nodes in new player:",nodes_expanded

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """    
    raise NotImplementedError


## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)


nodesExpanded = 0
## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)

## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.
def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
		      is_terminal_fn=is_terminal):

    tuple = minimaxAlphaBeta(board,depth,NEG_INFINITY,INFINITY,True);
    
    #Getting final nodes expanded value in nodesExpanded
    global nodesExpanded
    nodesExpanded = nodesExpanded + tuple[2]
    col = compareBoard(board,tuple[1])
    return col


"""
This function alpha beta search with pruning on the given board state and return a new board state with its evaluated value.
@param board: current board instance
@param depth: depth upto which search will run
@param alpha:
@param beta:
@param is_max: For checking between max player and min player
@param eval_fn: evauation function
@param get_next_moves_fn:
@param is_terminal_fn:
@param verbose:
@return value: (evaluated value of board, board)
"""  
def minimaxAlphaBeta(board, depth, alpha, beta,isMax,eval_fn = new_evaluate,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = True):
            
    if depth == 0:
        #returns evalutated value of the board, board, expanded node 
        return (eval_fn(board),board,1)

    countExpanded = 1
    if not isMax:
        newBoard = {}
        value = NEG_INFINITY
        for currentBoard in get_next_moves_fn(board):
            
            value1 = minimaxAlphaBeta(currentBoard[1],depth-1,alpha,beta,True)
            countExpanded = countExpanded + value1[2]
            if value != max(value,value1[0]):
                value = max(value,value1[0])
                newBoard = copy.deepcopy(currentBoard)

            alpha = max(value,alpha)

            #print "Alpha , Beta, depth ", alpha," ",beta," ",depth
            if beta <= alpha:
                break    #beta cutoff
        return (value,newBoard[1], countExpanded)

    else:
        newBoard = {}
        value = INFINITY
        for currentBoard in get_next_moves_fn(board):
            value1 = minimaxAlphaBeta(currentBoard[1],depth-1,alpha,beta,False)
            countExpanded = countExpanded + value1[2]
            if value != min(value,value1[0]):
                value = min(value,value1[0])
                newBoard = copy.deepcopy(currentBoard)

            beta = min(value,beta)
            #print "Alpha , Beta, depth ", alpha," ",beta," ",depth
            if beta <= alpha:
                break       #alpha cutoff
        return (value,newBoard[1],countExpanded)



## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
#alphabeta_player = lambda board: alpha_beta_search(board,
#                                                   depth=8,
#                                                   eval_fn=focused_evaluate)
alphabeta_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=new_evaluate)

## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)
#run_game(human_player, alphabeta_player)
#run_game(random_player, alphabeta_player)
#run_game(basic_player, alphabeta_player)

#Running game between alphabeta player with new_evaluation and basic player with basic_evaluation
run_game(alphabeta_player, basic_player, winNum=4)
#run_game(alphabeta_player, basic_player, winNum=3)
#run_game(alphabeta_player, random_player,winNum=4)

#printing nodes expanded in alpha-beta
print "Expanded nodes in apha-beta:",nodesExpanded


## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

#def better_evaluate(board):
#    raise NotImplementedError

# Comment this line after you've fully implemented better_evaluate
better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
# better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)
    
## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (None)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "15"
WHAT_I_FOUND_INTERESTING = "Got to implement minmax and alpha-beta"
WHAT_I_FOUND_BORING = ""
NAME = "Aman Raj, Dhanendra Jain"
EMAIL = "amraj@cs.stonybrook.edu, dhjain@cs.stonybrook.edu"

