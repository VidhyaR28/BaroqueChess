#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Diluted Coffee is a Baroque Chess Player made by Vidhya Rajendran and Krishna Teja

"""

import BC_state_etc as BC
import heapq

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

CODE_TO_INIT = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}


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

    priorityqueue = []
    if alphaBeta == False:
        free = 0
    else:
        free = 1 # CHANGE THIS AFTER IMPLEMENTING ALPHA-BETA

    if ply == 0:
        returnVal = {'CURRENT_STATE_STATIC_VAL': basicStaticEval(currentState), 'N_STATES_EXPANDED': 1,
                     'N_STATIC_EVALS': 1, 'N_CUTOFFS': free}
        return basicStaticEval(currentState)
    if currentState.whose_move == 1:
        provisional = -100000
    else:
        provisional = 100000

    # for s in generate states
    global movesList

    for s in successors(currentState): # CAN'T USE MOVESLIST, HAVE TO GENERATE KIDS.
        heapq.heappush(priorityqueue, s)

    for s in priorityqueue:
        newVal = parameterized_minimax(s, alphaBeta, ply - 1, useBasicStaticEval, useZobristHashing)
        if ((currentState.whose_move == 1 and newVal > provisional)
                or (currentState.whose_move == 0 and newVal < provisional)):
            provisional = newVal
            provisional.update('N_STATES_EXPANDED', len(s) + 1)
            provisional.update('N_STATIV_EVALS', len(s) + 1) # when will this not be same in minimax?


    pass


def successors(currentState):
    """
    Takes in a list of successors and returns them
    :param currentState:
    :return:
    """

    return []





def makeMove(currentState, currentRemark, timelimit=10):
    # Compute the new state for a move.
    # You should implement an anytime algorithm based on IDDFS.

    # The following is a placeholder that just copies the current state.

    newState = BC.BC_state(currentState.board)
    # print("Enters makeMove")
    # SHIFT TO THE GENERATE STATES FUNCTION

                # print("Enters the iterating forloop of makeMove ")
    generateStates(newState, timelimit)
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


def generateStates(currentState, time):
    """
    Generates a list of possible states
    :param currentState: BC_state_etc -> class BC_state
    :param time:
    :return:
    """
    if currentState.whose_move == 'WHITE':
        track = 1
    else: track = 0

    for i in range(8):
        for j in range(8):
            # IMPORTANT: test whether your pieces are frozen. If so, skip the rest from here
            if currentState.board[i][j] % 2 == track:
                piece = currentState.board[i][j]
                if piece == 2 or piece == 3: #Pincer - Done
                    pincerMoves(currentState, i, j, piece, track)
                elif piece == 4 or piece == 5: #Coordinator - Done
                    coordinatorMoves(currentState, i, j, piece, track)
                elif piece == 6 or piece == 7: #Leaper - Done
                    leaperMoves(currentState, i, j, piece, track)
                elif piece == 8 or piece == 9: #Imitator
                    allDirMoves(currentState, i, j, piece.lower())
                elif piece == 10 or piece == 11: #Withdrawer - Done
                    withdrawerMoves(currentState, i, j, piece, track)
                elif piece == 12 or piece == 13: #King - Done
                    kingMoves(currentState, i, j, piece, track)
                elif piece == 14 or piece == 15: #Freezer - Done
                    freezerMoves(currentState, i, j, piece)

def pincerMoves(currentState, r, c, piece, track):
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    for k in movedirection:
        final = move(currentState, r, c, k, piece)
        if pincerCapture(currentState, r, c, final, track, piece):
           #delete the last state in the moves list because that is a duplicate


def pincerCapture(currentState, r, c, final, track, piece):
    possiblities = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    capture = False

    capturePiece = []
    captureR = []
    captureC = []
    for k in possiblities:
        temp_r = final[0]
        temp_c = final[1]
        temp_r += k[0]
        temp_c += k[1]

        try:
            if currentState.board[temp_r][temp_c]%2 != track:
                if currentState.board[temp_r+k[0]][temp_c+k[1]]%2 == track:
                    capturePiece.append(currentState.board[temp_r][temp_c])
                    captureR.append(temp_r)
                    captureC.append(temp_c)
                    capture = True
        except:
            # do nothing

    newState = BC.BC_state(currentState.board)
    newState.board[r][c] = 0
    newState.board[final[0]][final[1]] = piece
    count = 0
    for i in capturePiece:
        newState.board[captureR[count]][captureC[count]] = 0
        count += 1
    captureList.append([newState, capturePiece])

    return capture


def withdrawerMoves(currentState, r, c, piece, track):
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]
    captureMoves = []

    #withdrawerCapture states
    for k in movedirection:
        temp_r = r
        temp_c = c

        try:
            if currentState.board[temp_r+k[0]][temp_c+k[1]]%2 != track:
                captureMoves.append([k[0],k[1]])
                captureMoves.append([-k[0],-k[1]])
                capturePiece = currentState.board[temp_r+k[0]][temp_c+k[1]]
                temp_c -= k[1]
                temp_r -= k[0]
                while (temp_c in range(8) and temp_r in range(8) and currentState.board[temp_r][temp_c] == 0):
                    newState = BC.BC_state(currentState.board)
                    newState.board[temp_r][temp_c] = piece
                    newState.board[r][c] = 0
                    newState.board[r+k[0]][c+k[1]] = 0
                    captureList.append([newState, capturePiece])
                    temp_c -= k[1]
                    temp_r -= k[0]
        except:
            # do nothing

    noncaptureMoves = [k for k in movedirection if k not in captureMoves]
    #withdrawer general moves
    for k in noncaptureMoves:
        final = move(currentState, r, c, k, piece)


def leaperMoves(currentState, r, c, piece, track):
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]

    for k in movedirection:
        final = move(currentState, r, c, k, piece)

        #leaperCapture
        temp_r = final[0]+k[0]
        temp_c = final[1]+k[1]
        if currentState.board[temp_r][temp_c]%2 != track:
            if currentState.board[temp_r + k[0]][temp_c + k[1]] == 0:
                newState = BC.BC_state(currentState.board)
                capturePiece = newState.board[temp_r][temp_c]
                newState.board[temp_r][temp_c] = 0
                newState.board[r][c] = 0
                newState.board[temp_r+k[0]][temp_c+k[1]] = piece
                captureList.append([newState, capturePiece])

def coordinatorMoves(currentState, r, c, piece, track):

    myKing = 0
    rk = 0
    ck = 0
    if track == 1: myKing = 13
    else: myKing = 12

    #Locating the king
    for i in range(8):
        for j in range(8):
            if currentState.board[i][j] == myKing:
                rk = i
                ck = j

    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]

    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]
        while (temp_c in range(8) and temp_r in range(8) and currentState.board[temp_r][temp_c] == 0):
            newState = BC.BC_state(currentState.board)
            newState.board[temp_r][temp_c] = piece
            newState.board[r][c] = 0
            if temp_r == rk or temp_c == ck:
                movesList.append(newState)
            else:
                if newState.board[temp_r][ck]%2 != track and newState.board[rk][temp_c]%2 != track:
                    capturePiece = [newState.board[temp_r][ck],newState.board[rk][temp_c]]
                    newState.board[temp_r][ck] = 0
                    newState.board[rk][temp_c] = 0
                    captureList.append([newState, capturePiece])
                elif newState.board[temp_r][ck] % 2 != track:
                    capturePiece = newState.board[temp_r][ck]
                    newState.board[temp_r][ck] = 0
                    captureList.append([newState, capturePiece])
                elif newState.board[rk][temp_c]%2 != track:
                    capturePiece = newState.board[rk][temp_c]
                    newState.board[rk][temp_c] = 0
                    captureList.append([newState, capturePiece])
                else:
                    movesList.append(newState)

            temp_r += k[0]
            temp_c += k[1]

def kingMoves(currentState, r, c, piece, track):
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]

    for k in movedirection:
        temp_r = r
        temp_c = c
        temp_r += k[0]
        temp_c += k[1]

        try:
            if currentState.board[temp_r][temp_c]%2 != track:
                newState = BC.BC_state(currentState.board)
                capturePiece = newState.board[temp_r][temp_c]
                newState.board[temp_r][temp_c] = piece
                newState.board[r][c] = 0
                captureList.append([newState, capturePiece])
            elif currentState.board[temp_r][temp_c] == 0:
                newState = BC.BC_state(currentState.board)
                newState.board[temp_r][temp_c] = piece
                newState.board[r][c] = 0
                movesList.append(newState)
        except:
            # Do nothing


def freezerMoves(currentState, r, c, piece):
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]

    for k in movedirection:
        final = move(currentState, r, c, k, piece)


def imitatorMoves(currentState, r, c, piece, track):
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]

    imitatingPiece = []
    for k in movedirection:
        temp_r = r
        temp_c = c
        temp_r += k[0]
        temp_c += k[1]

        try:
            if currentState.board[temp_r][temp_c] % 2 != track:
                imitatingPiece.append(CODE_TO_INIT[currentState.board[temp_r][temp_c]])
        except:
            # Do nothing

    if len(imitatingPiece) == 0:
        #move like a queen
    else:
        for newRole in imitatingPiece:
            if newRole.lower() == 'p':






def move(currentState, r, c, k, item):
    # item in the form of number
    temp_c = c + k[1]
    temp_r = r + k[0]
    while (temp_c in range(8) and temp_r in range(8) and currentState.board[temp_r][temp_c] == 0):
        newState = BC.BC_state(currentState.board)
        newState.board[temp_r][temp_c] = item
        newState.board[r][c] = 0
        movesList.append(newState)
        # print("plusMoves r: ", temp_r, ", Temp c:", temp_c)
        temp_c += k[1]
        temp_r += k[0]

    return [temp_r - k[0], temp_c - k[1]]


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

    # send in functions to everything, take a value as return and then sum it up.

    # assign a couple of values for each state.

    # loop through entire board. if piece == specific piece, send to a function which evaluates significance

    evalboard = state.board
    returnval = 0

    for i in range(0, 8):
        for j in range(0, 8):
            if state.board[i][j] == 'p':
                # mobility check
                # King Safety Check
                #
                returnval += pincerMobility(state.board, (i, j))

    return returnval

def pincerMobility(state, k):
    board = state.board


    movedirection =  [[1, 0], [-1, 0], [0, 1], [0, -1]]
    count = 0
    for s in movedirection:
        if board[k[0] + s[0]][k[1] + s[1]] == 0:
            count += 1
    return count*5


def pincerKill(state, k):
    board = state.board

    # go north, south, east, west. Hit a block. Check if it's the other colour. If yes, go one step ahead and see if we
    # have a piece there. If yes, more points.
    count = 0
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    if state.whoseturn == WHITE:
        opponentPieces = [2, 4, 6, 8, 10, 12, 14]
    else:
        opponentPieces = [3, 5, 7, 9, 11, 13, 15]

    for s in movedirection:

        t = k

        # checks in a direction. Loops through blank spaces, checks if it's an opponent. If true, checks if our
        # our piece exists right after.

        #checking for blank spaces
        while(t[0] in range(0, 8) and t[1] in range(0, 8) and board[t[0]][t[1]] == 0):
            t[0] += s[0]
            t[1] += s[1]

        # avoiding an index out of bounds exception
            if t[0] == 8:
                t[0] -= 1
            elif t[0] == -1:
                t[0] += 1
            elif t[1] == 8:
                t[1] -= 1
            elif t[1] == -1:
                t[1] += 1

            # this can't be generalised, so split into 4
            # check if the other piece is opponent, if yes jump 1 step and check if its our piece
            if s[0] == 1 and s[1] == 0:
                if board[t[0]][t[1]] in opponentPieces and t[0] < 7:
                    t[0] += 1
                    if board[t[0]][t[1]] not in opponentPieces and board[t[0]][t[1]] != 0:
                        count += 1
            if s[0] == -1 and s[1] == 0:
                if board[t[0]][t[1]] in opponentPieces and t[0] > 0:
                    t[0] -= 1
                    if board[t[0]][t[1]] not in opponentPieces and board[t[0]][t[1]] != 0:
                        count += 1
            if s[0] == 0 and s[1] == 1:
                if board[t[0]][t[1]] in opponentPieces and t[1] < 7:
                    t[0] += 1
                    if board[t[0]][t[1]] not in opponentPieces and board[t[0]][t[1]] != 0:
                        count += 1
            if s[0] == 0 and s[1] == -1:
                if board[t[0]][t[1]] in opponentPieces and t[1] > 0:
                    t[0] -= 1
                    if board[t[0]][t[1]] not in opponentPieces and board[t[0]][t[1]] != 0:
                        count += 1


        # if s[0] == 1 and s[1] == 0:
        #     t = 0
        #     while k[0] + s[0] + t <= 7 and board[k[0] + s[0] + t][k[1]] == 0:
        #         t += 1
        #
        #     # avoiding an index out of bounds exception
        #     if k[0] + s[0] + t == 8:
        #         t -= 1
        #
        #     if board[k[0] + s[0] + t] in opponentPieces and k[0] + s[0] + t < 7:
        #         t+= 1
        #         if board[k[1] + s[1] + t] not in opponentPieces and board[k[0] + s[0] + t][k[1]] != 0:
        #             count += 1


    return count # count times some factor