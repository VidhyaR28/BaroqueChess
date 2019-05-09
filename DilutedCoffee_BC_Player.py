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
    for i in range(8):
        for j in range(8):
            if newState.board[i][j] % 2 == colourtrack:
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
    if piece == 2 or piece == 3:
        plusMoves(currentState, r, c, piece)
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

def plusMoves(currentState, r, c, item, direction):
    """
    Generates states in North, East, West, South.
    :param currentState:
    :param r:
    :param c:
    :param item:
    :param direction:
    :return:
    """
    # east moves

    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1]] # moves in North, South, East, West
    # temp_c = c
    # temp_r = r
    for k in movedirection:
        temp_c = c
        temp_r = r
        if temp_c == 7 and temp_r == 7:
            temp_c += k[1]
            temp_r += k[0]
            # temp_c, temp_r belongsto [0, 7]
            # while (temp_c >= 0 and temp_c <= 7 and  temp_r >= 0 and temp_r <= 7 and currentState.board[temp_r][temp_c] == 0):
            while (temp_c in range(0, 7) and temp_r in range(0, 7) and currentState.board[temp_r][temp_c] == 0):
                newState = BC.BC_state(currentState)
                newState.board[r][temp_c] = item
                newState.board[r][c] = 0
                movesList.append(newState)
                temp_c += k[1]
                temp_r += k[0]






    temp_c = c
    temp_r = r
    if temp_c != 7:
        temp_c += 1
        while (temp_c != 7 and currentState.board[r][temp_c] == 0):
            newState = BC.BC_state(currentState)
            newState.board[r][temp_c] = item
            newState.board[r][c] = 0
            movesList.append(newState)
            temp_c += 1





def nickname():
    return "Diluted Coffee"


def introduce():
    return "I'm Diluted Coffee, and I am an aspiring Baroque Chess player."


def prepare(player2Nickname, playWhite):
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
    print("Colour ", colourtrack)
    return


def basicStaticEval(state):
    """
    Use the simple method for state evaluation described in the spec.
    This is typically used in parameterized_minimax calls to verify
    that minimax and alpha-beta pruning work correctly.
    :param state:
    :return:
    """

    pass


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
