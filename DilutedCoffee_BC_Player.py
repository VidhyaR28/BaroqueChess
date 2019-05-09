#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Diluted Coffee is a Baroque Chess Player made by Vidhya Rajendran and Krishna Teja

"""

import BC_state_etc as BC

"""
BLACK_PINCER      = 2
BLACK_COORDINATOR = 4
BLACK_LEAPER      = 6
BLACK_IMITATOR    = 8
BLACK_WITHDRAWER  = 10
BLACK_KING        = 12
BLACK_FREEZER     = 14

WHITE_PINCER      = 3
WHITE_COORDINATOR = 5
WHITE_LEAPER      = 7
WHITE_IMITATOR    = 9
WHITE_WITHDRAWER  = 11
WHITE_KING        = 13
WHITE_FREEZER     = 15
"""

global colourtrack
global movesList
global captureList


def parameterized_minimax(currentState, alphaBeta=False, ply=3, \
                          useBasicStaticEval=True, useZobristHashing=False):
    """
    Implement this testing function for your agent's basic
    capabilities here.
    :param currentState:
    :param alphaBeta:
    :param ply:
    :param useBasicStaticEval:
    :param useZobristHashing:
    :return:
    """
    """
    Pseudocode: 
    
    Procedure minimax(board, whoseMove, plyLeft):
        if plyLeft == 0: return staticValue(board)
        if whoseMove == ‘Max’: provisional = -100000 else: provisional = 100000
        for s in successors(board, whoseMove):
            newVal = minimax(s, other(whoseMove), plyLeft-1) if (whoseMove == ‘Max’ and newVal > provisional
        or (whoseMove == ‘Min’ and newVal < provisional): 
            provisional = newVal
        return provisional
    """


    """
    When useBasicStaticEval is true, you'll evaluate leaf nodes of your search tree with your own implementation of 
    the following function: White pincers are worth 1, the White king is worth 100, and all other White pieces are 
    worth 2. Black pieces have the same values as their white counterparts, but negative. When useBasicStaticEval is 
    False, you should use your own, more discriminating function. The value of the function is the sum of the values of 
    the pieces on the board in the given state.
    """



    pass


def makeMove(currentState, currentRemark, timelimit=10):
    # Compute the new state for a move.
    # You should implement an anytime algorithm based on IDDFS.

    # The following is a placeholder that just copies the current state.

    newState = BC.BC_state(currentState.board)
    # print("Enters makeMove")
    for i in range(8):
        for j in range(8):
            if newState.board[i][j] % 2 == colourtrack:
                # print("Enters the iterating forloop of makeMove ")
                generateStates(newState, newState.board[i][j], i, j, timelimit)
    # kt: newstate should be temp, parse through temp, and then make change?

    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    move = ((6, 4), (3, 4))

    # Make up a new remark
    # KT: Make a function called remark generator. Loop through 15 remarks
    newRemark = "I'll think harder in some future game. Here's my move"

    return [[move, newState], newRemark]


def generateStates(currentState, piece, r, c, time):
    """
    Generates a list of possible states
    :param currentState: BC_state_etc -> class BC_state
    :param piece: The actual piece, numeric value (Pincer, Imitator, etc)
    :param r: row
    :param c: column
    :param time:
    :return:
    """
    print("Piece", piece)
    if piece == 2 or piece == 3:
        straightMoves(currentState, r, c, piece)
    elif piece == 4 or piece == 5:
        allDirMoves(currentState, r, c, 'c')
    elif piece == 6 or piece == 7:
        allDirMoves(currentState, r, c, 'l') #leaper moves are different
    elif piece == 8 or piece == 9:
        allDirMoves(currentState, r, c, 'i')
    elif piece == 10 or piece == 11:
        allDirMoves(currentState, r, c, 'w')
    elif piece == 12 or piece == 13:
        oneStepMoves(currentState, r, c, 'k')
    elif piece == 14 or piece == 15:
        allDirMoves(currentState, r, c, 'f')

def straightMoves(currentState, r, c, item):
    """
    plusMoves has been renamed as straightMoves for naming simplicity
    Generates states in North, East, West, South.
    :param currentState:
    :param r:
    :param c:
    :param item:
    :param direction:
    :return:
    """
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1]] # moves in North, South, East, West

    for k in movedirection:
        temp_c = c
        temp_r = r

        temp_c += k[1]
        temp_r += k[0]
        while (temp_c in range(0, 7) and temp_r in range(0, 7) and currentState.board[temp_r][temp_c] == 0):
            newState = BC.BC_state(currentState.board)
            newState.board[r][temp_c] = item
            newState.board[r][c] = 0
            movesList.append(newState)
            # print("plusMoves r: ", temp_r, ", Temp c:", temp_c)
            temp_c += k[1]
            temp_r += k[0]






def diagMoves (currentState, r, c, item):
    """
    :param currentState:
    :param r:
    :param c:
    :param item:
    :return:
    """
    movedirection = [[1, 1], [-1, -1], [-1, 1], [1, -1]]  # moves in SE, NW,
    for k in movedirection:
        temp_c = c
        temp_r = r

        temp_c += k[1]
        temp_r += k[0]
        while (temp_c in range(0, 7) and temp_r in range(0, 7) and currentState.board[temp_r][temp_c] == 0):
            newState = BC.BC_state(currentState.board)
            newState.board[r][temp_c] = item
            newState.board[r][c] = 0
            movesList.append(newState)
            # print("Diagmoves r: ", temp_r, ", Temp c:", temp_c)
            temp_c += k[1]
            temp_r += k[0]



def allDirMoves(currentState, r, c, item):
    """
    All direction move basically combines plusmoves and diagonal moves
    :return:
    """

    straightMoves(currentState, r, c, item)
    diagMoves(currentState, r, c, item)


def oneStepMoves(currentState, r, c, item):
    """
    :param currentState:
    :param r:
    :param c:
    :param item:
    :return:
    """
    movedirection = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, 1]]

    for k in movedirection:
        temp_c = c
        temp_r = r

        temp_c += k[1]
        temp_r += k[0]
        if (temp_c in range(0, 7) and temp_r in range(0, 7) and currentState.board[temp_r][temp_c] == 0):
            newState = BC.BC_state(currentState.board)
            newState.board[r][temp_c] = item
            newState.board[r][c] = 0
            movesList.append(newState)
            # print("Diagmoves r: ", temp_r, ", Temp c:", temp_c)



    # temp_c = c
    # temp_r = r
    # if temp_c != 7:
    #     temp_c += 1
    #     while (temp_c != 7 and currentState.board[r][temp_c] == 0):
    #         newState = BC.BC_state(currentState)
    #         newState.board[r][temp_c] = item
    #         newState.board[r][c] = 0
    #         movesList.append(newState)
    #         temp_c += 1





def nickname():
    return "Diluted Coffee"


def introduce():
    return "I'm Diluted Coffee, and I am an aspiring Baroque Chess player."


def prepare(player2Nickname, playWhite = False):
    """
    Here the game master will give your agent the nickname of
    the opponent agent, in case your agent can use it in some of
    the dialog responses.  Other than that, this function can be
    used for initializing data structures, if needed.
    :param player2Nickname:
    :return:
    """
    global colourtrack
    global captureList
    global movesList
    captureList = []
    movesList = []

    if (playWhite == True):
        # keep track of white/black
        colourtrack = 1
    else:
        colourtrack = 0
    print("Hey, I'm super prepared at this point.")

    return


def basicStaticEval(state):
    """
    Use the simple method for state evaluation described in the spec.
    This is typically used in parameterized_minimax calls to verify
    that minimax and alpha-beta pruning work correctly.
    :param state:
    :return:
    """
    """
    When useBasicStaticEval is true, you'll evaluate leaf nodes of your search tree with your own implementation of the 
    following function: White pincers are worth 1, the White king is worth 100, and all other White pieces are worth 2. 
    Black pieces have the same values as their white counterparts, but negative. When useBasicStaticEval is False, you 
    should use your own, more discriminating function. The value of the function is the sum of the values of the pieces 
    on the board in the given state.
    """
    # iterate through the whole thing. Sum up
    # if it's white, negative of the same. P, p = 1
    # K, k = 100; All other white are 2 Black's the same, but in negative.

    totalEval = 0

    for i in range(8):
        for j in range(8):
            # Coordinator, Leaper, Imitator, Withdrawer, Freezer
            if state.board[i][j] in  [4, 6, 8, 10, 14]:
                totalEval += -2
            elif state.board[i][j] in [5, 7, 9, 11, 15]:
                totalEval += 2

            # Pincer
            elif state.board[i][j] == 2:
                totalEval += -1
            elif state.board[i][j] == 3:
                totalEval += 1

            # King
            elif state.board[i][j] == 12:
                totalEval += - 100
            elif state.board[i][j] == 13:
                totalEval += 100

    return totalEval




def staticEval(state):
    """
    Compute a more thorough static evaluation of the given state.
    This is intended for normal competitive play.  How you design this
    function could have a significant impact on your player's ability
    to win games.

    :param state:
    :return:
    """
    pass


# WHITE = 1
#
# INITIAL = parse('''
# c l i w k i l f
# p p p p p p p p
# - - - - - - - -
# - - - - - - - -
# - - - - - - - -
# - - - - - - - -
# P P P P P P P P
# F L I W K I L C
# ''')
#
# def parse(bs):  # bs is board string
#     """Translate a board string into the list of lists representation."""
#     b = [[0, 0, 0, 0, 0, 0, 0, 0] for r in range(8)]
#     rs9 = bs.split("\n")
#     rs8 = rs9[1:]  # eliminate the empty first item.
#     for iy in range(8):
#         rss = rs8[iy].split(' ')
#         for jx in range(8):
#             b[iy][jx] = INIT_TO_CODE[rss[jx]]
#     return b



# def test_starting_board():
#     print("1")
#     import BC_state_etc as BC
#     print(2)
#     init_state = BC.BC_state(INITIAL, WHITE)
#     print(init_state)
#
#
# if __name__ == "__main__":
#     test_starting_board()
