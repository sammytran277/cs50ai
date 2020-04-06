# Project 0b: Tic Tac Toe
# Implement the minimax algorithm to play perfect tic tac toe

"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
BOARD_LENGTH = 3
BOARD_WIDTH = 3
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
    # We will figure out who's turn it is by counting the number
    # of X's and O's, and then seeing if that number is even or odd
    xFreq = 0
    yFreq = 0

    for row in board:
        for square in row:
            if square == "X":
                xFreq += 1
            elif square == "O":
                yFreq += 1
    
    movesPlayed = xFreq + yFreq
    if movesPlayed % 2 == 0:
        return "X"
    else:
        return "O"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # We'll get all the legal moves by iterating through the whole board
    # and checking if the value of the board is set to EMPTY or not
    possibleActions = set()
    for i in range(BOARD_LENGTH):
        for j in range (BOARD_WIDTH):
            if board[i][j] == EMPTY:
                possibleActions.add((i, j))

    return possibleActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # We'll return the resulting board by first making a deep copy of the board, then
    # checking that the square is not already occupied
    newBoard = copy.deepcopy(board)
    
    # Check validity of action
    if newBoard[action[0]][action[1]] != EMPTY:
        print("Tried to play {}".format(action))
        raise UserWarning("Invalid move")
    else:
        newBoard[action[0]][action[1]] = player(board)

    return newBoard


def checkWin(board, win):
    """
    Returns the winner of the game, given a board and a winning combination to look for.
    """
    # To figure out if the winning combination is present, we'll look at each of the 3
    # sqaures and see if they are occupied by the same piece
    firstSquare = board[win[0][0]][win[0][1]]
    secondSquare = board[win[1][0]][win[1][1]]
    thirdSquare = board[win[2][0]][win[2][1]]
    
    if firstSquare == "X" and secondSquare == "X" and thirdSquare == "X":
        return "X"
    elif firstSquare == "O" and secondSquare == "O" and thirdSquare == "O":
        return "O"
    else:
        return None


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # To figure out who won the game, we'll iterate over all 8 possibilities,
    # checking if any of the winning possibilities are present in the board 
    wins = [[(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], 
            [(2, 0), (2, 1), (2, 2)], [(0, 0), (1, 0), (2, 0)], 
            [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)], 
            [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]

    for win in wins:
        result = checkWin(board, win)
        if result != None:
            return result
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # To determine if the game is over, we'll first check if our winner
    # function returns a player. If not, we'll see if there are any unoccupied
    # squares left on the board. If not, the game is over. 
    if winner(board) != None:
        return True

    numOccupiedSquares = 0
    for i in range(BOARD_LENGTH):
        for j in range(BOARD_WIDTH):
            if board[i][j] != EMPTY:
                numOccupiedSquares += 1

    if numOccupiedSquares == 9:
        return True
    else:
        return False    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Determine the winner by using the winner function as a helper
    winningPlayer = winner(board)

    if winningPlayer == "X":
        return 1
    elif winningPlayer == "O":
        return -1
    else:
        return 0


def maxValue(state):
    """
    Return the highest possible value that could come out of a given board state
    """
    # Maximizing function based on the lecture's pseudocode
    if terminal(state):
        return utility(state)
    v = float("-inf")
    for action in actions(state):
        v = max(v, minValue(result(state, action)))
    return v


def minValue(state):
    """
    Return the lowest possible value that could come out of a given board state
    """
    # Minimizing function based on the lecture's pseudocode
    if terminal(state):
        return utility(state)
    v = float("inf")
    for action in actions(state):
        v = min(v, maxValue(result(state, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # To implement minimax, we're going to get all the possible moves in a given
    # board and see what results from the position when the opponent plays optimally.
    # Out of all the possibilities, the one with the biggest value is chosen as the
    # optimal move to play
    currentPlayer = player(board)
    if currentPlayer == "X":
        # Optimization for when the computer is playing "X" and it is the first move
        if (board == initial_state()):
            return (0, 1)
        v = float("-inf")
        optimalAction = None
        for action in actions(board):
            valueOfAction = minValue(result(board, action))
            if valueOfAction > v:
                v = valueOfAction
                optimalAction = action
        return optimalAction
    else:
        v = float("inf")
        optimalAction = None
        for action in actions(board):
            valueOfAction = maxValue(result(board, action))
            if valueOfAction < v:
                v = valueOfAction
                optimalAction = action
        return optimalAction
