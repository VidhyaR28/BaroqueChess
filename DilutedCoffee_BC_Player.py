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

    frozenPieces = []
    kingR = 0
    kingC = 0
    cordR = 0
    cordC = 0

    for i in range(8):
        for j in range(8):
            item = currentState.board[i][j]
            if item == (15-track):
                # the enemy freezer; map all your frozen pieces
                movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
                for k in movedirection:
                    try:
                        if currentState.board[i+k[0]][j+k[1]] % 2 == track:
                            frozenPieces.append(currentState.board[i+k[0]][j+k[1]])
                    except:
                        dummy = None

            if item == (14+track):
                # My freezer to check whether it has an imitator next to it
                movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
                Freezerfreeze = False
                imiR = 0
                imiC = 0

                for k in movedirection:
                    try:
                        # found freezer
                        if currentState.board[i+k[0]][j+k[1]] == (9-track):
                            Freezerfreeze = True
                            imiR = i+k[0]
                            imiC = j+k[1]
                    except:
                        dummy = None

                if Freezerfreeze:
                    for k in movedirection:
                        try:
                            if currentState.board[imiR+k[0]][imiC+k[1]]%2 == track:
                                frozenPieces.append(currentState.board[imiR+k[0]][imiC+k[1]])
                        except:
                            dummy = None

            if item == (12+track):
                #My army's king
                kingR = i
                kingC = j

            if item == (4+track):
                #My army's coordinator
                cordR = i
                cordC = j


    for i in range(8):
        for j in range(8):
            # IMPORTANT: test whether your pieces are frozen. If so, skip the rest from here
            if currentState.board[i][j] % 2 == track:
                piece = currentState.board[i][j]
                if piece == 2 or piece == 3: #Pincer - Done
                    pincerMoves(currentState, i, j, piece, track)
                elif piece == 4 or piece == 5: #Coordinator - Done
                    coordinatorMoves(currentState, i, j, kingR, kingC, piece, track)
                elif piece == 6 or piece == 7: #Leaper - Done
                    leaperMoves(currentState, i, j, piece, track)
                elif piece == 8 or piece == 9: #Imitator
                    imitatorMoves(currentState, i, j, kingR, kingC, piece.lower())
                elif piece == 10 or piece == 11: #Withdrawer - Done
                    withdrawerMoves(currentState, i, j, piece, track)
                elif piece == 12 or piece == 13: #King - Done
                    kingMoves(currentState, i, j, cordR, cordC, piece, track)
                elif piece == 14 or piece == 15: #Freezer - Done
                    freezerMoves(currentState, i, j, piece)

def pincerMoves(currentState, r, c, piece, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0]]

    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]
        try:
            while currentState.board[temp_r][temp_c] == 0:
                newState = BC.BC_state(currentState.board)
                newState.board[temp_r][temp_c] = piece
                newState.board[r][c] = 0
                neighbour = [dir for dir in movedirection if dir != k]
                capturePiece = []
                captureR = []
                captureC = []
                capture = False
                for n in neighbour:
                    nR = temp_r + n[0]
                    nC = temp_c + n[1]
                    try:
                        if currentState.board[nR][nC]%2 != track:
                            if currentState.board[nR+n[0]][nC+n[1]]%2 == track:
                                capturePiece.append(currentState.board[temp_r][temp_c])
                                captureR.append(temp_r)
                                captureC.append(temp_c)
                                capture = True
                    except:
                        dummy = None
                if capture:
                    # pincer capture moves
                    count = 0
                    for i in capturePiece:
                        newState.board[captureR[count]][captureC[count]] = 0
                        count += 1
                    captureList.append([[r,c,temp_r,temp_c],newState])
                else:
                    # pincer non-capture moves
                    movesList.append([[r,c,temp_r,temp_c],newState])

                temp_r += k[0]
                temp_c += k[1]
        except:
            dummy = None


def withdrawerMoves(currentState, r, c, piece, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
    captureMoves = []

    # withdrawer capture moves
    for k in movedirection:
        temp_r = r
        temp_c = c

        try:
            if currentState.board[temp_r+k[0]][temp_c+k[1]]%2 != track:
                capture = False
                temp_r -= k[0]
                temp_c -= k[1]
                try:
                    while currentState.board[temp_r][temp_c] == 0:
                        newState = BC.BC_state(currentState.board)
                        newState.board[temp_r][temp_c] = piece
                        newState.board[r][c] = 0
                        newState.board[r+k[0]][c+k[1]] = 0
                        captureList.append([r,c,temp_r,temp_c],newState)
                        capture = True
                        temp_c -= k[1]
                        temp_r -= k[0]
                except:
                    dummy = None
                if capture:
                    captureMoves.append([k[0], k[1]])
                    captureMoves.append([-k[0],-k[1]])
        except:
            dummy = None

    # withdrawer non-capture moves
    noncaptureMoves = [k for k in movedirection if k not in captureMoves]

    for k in noncaptureMoves:
        final = move(currentState, r, c, k, piece)


def leaperMoves(currentState, r, c, piece, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        # leaper non-capture moves
        final = move(currentState, r, c, k, piece)

        # leaper Capture moves
        temp_r = final[0]+k[0]
        temp_c = final[1]+k[1]
        try:
            if currentState.board[temp_r][temp_c]%2 != track:
                if currentState.board[temp_r + k[0]][temp_c + k[1]] == 0:
                    newState = BC.BC_state(currentState.board)
                    newState.board[temp_r][temp_c] = 0
                    newState.board[r][c] = 0
                    newState.board[temp_r+k[0]][temp_c+k[1]] = piece
                    captureList.append([[r,c,temp_r+k[0],temp_c+k[1]], newState])
        except:
            dummy = None

def coordinatorMoves(currentState, r, c, rk, ck, piece, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]
        try:
            while currentState.board[temp_r][temp_c] == 0:
                newState = BC.BC_state(currentState.board)
                newState.board[temp_r][temp_c] = piece
                newState.board[r][c] = 0
                if temp_r == rk or temp_c == ck:
                    movesList.append([[r,c,temp_r,temp_c],newState])
                else:
                    if newState.board[temp_r][ck]%2 != track and newState.board[rk][temp_c]%2 != track:
                        newState.board[temp_r][ck] = 0
                        newState.board[rk][temp_c] = 0
                        captureList.append([[r,c,temp_r,temp_c],newState])
                    elif newState.board[temp_r][ck] % 2 != track:
                        newState.board[temp_r][ck] = 0
                        captureList.append([[r,c,temp_r,temp_c],newState])
                    elif newState.board[rk][temp_c]%2 != track:
                        newState.board[rk][temp_c] = 0
                        captureList.append([[r,c,temp_r,temp_c],newState])
                    else:
                        movesList.append([[r,c,temp_r,temp_c],newState])

                temp_r += k[0]
                temp_c += k[1]
        except:
            dummy = None


def kingMoves(currentState, r, c, rcord, ccord, piece, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        temp_r = r +k[0]
        temp_c = c +k[1]
        try:
            newState = BC.BC_state(currentState.board)
            newState.board[temp_r][temp_c] = piece
            newState.board[r][c] = 0

            if currentState.board[temp_r][temp_c]%2 != track:
                captureList.append([[r,c,temp_r,temp_c],newState])
            elif currentState.board[temp_r][temp_c] == 0:
                #captures with coordinator
                if newState.board[temp_r][ccord] % 2 != track and newState.board[rcord][temp_c] % 2 != track:
                    newState.board[temp_r][ccord] = 0
                    newState.board[rcord][temp_c] = 0
                    captureList.append([[r, c, temp_r, temp_c], newState])
                elif newState.board[temp_r][ccord] % 2 != track:
                    newState.board[temp_r][ccord] = 0
                    captureList.append([[r, c, temp_r, temp_c], newState])
                elif newState.board[rcord][temp_c] % 2 != track:
                    newState.board[rcord][temp_c] = 0
                    captureList.append([[r, c, temp_r, temp_c], newState])
                else:
                    movesList.append([[r, c, temp_r, temp_c], newState])

        except:
            dummy = None


def freezerMoves(currentState, r, c, piece):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        final = move(currentState, r, c, k, piece)


def imitatorMoves(currentState, r, c, rk, ck, piece, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    # Stationary analysis
    for k in movedirection:
        newState = BC.BC_state(currentState.board)
        newState.board[r][c] = 0
        try:
            enemy = currentState.board[r+k[0]][c+k[1]]
            # King capture
            if enemy == (13 - track):
                newState.board[r+k[0]][c+k[1]] = piece
                captureList.append([[r, c, r+k[0], c+k[1]], newState])

            # Withdrawer capture
            if enemy == (11-track):
                try:
                    temp_r = r-k[0]
                    temp_c = r-k[1]
                    while currentState.board[temp_r][temp_c] == 0:
                        newState.board[temp_r][temp_c] = piece
                        newState.board[r+k[0]][c+k[1]] = 0
                        captureList.append([[r, c, r-k[0], c-k[1]], newState])
                        temp_r -= k[0]
                        temp_c -= k[1]
                except:
                    dummy = None

            # Coordinator capture
            if enemy == (5-track):
                if r+k[0] == rk and rk != r:
                    if r in range(8) and c+k[1] in range(8):
                        if currentState.board[r][c+k[1]] == 0:
                            newState.board[r][c+k[1]] = piece
                            newState.board[r + k[0]][c + k[1]] = 0
                            captureList.append([[r, c, r, c + k[1]], newState])

                if r+k[0] == rk and c+k[1] == c:
                    if r+1 in range(8) and c in range(8):
                        if currentState.board[r+1][c] == 0:
                            newState.board[r+1][c] = piece
                            newState.board[r + k[0]][c + k[1]] = 0
                            captureList.append([[r, c, r+1, c], newState])
                    if r-1 in range(8) and c in range(8):
                        if currentState.board[r-1][c] == 0:
                            newState.board[r-1][c] = piece
                            newState.board[r + k[0]][c + k[1]] = 0
                            captureList.append([[r, c, r-1, c], newState])

                if c+k[0] == ck and ck != c:
                    if r+k[0] in range(8) and c in range(8):
                        if currentState.board[r+k[0]][c] == 0:
                            newState.board[r+k[0]][c] = piece
                            newState.board[r + k[0]][c + k[1]] = 0
                            captureList.append([[r, c, r+k[0], c], newState])

                if c+k[0] == ck and r+k[0] == r:
                    if r in range(8) and c+1 in range(8):
                        if currentState.board[r][c+1] == 0:
                            newState.board[r][c+1] = piece
                            newState.board[r + k[0]][c + k[1]] = 0
                            captureList.append([[r, c, r, c+1], newState])
                    if r in range(8) and c-1 in range(8):
                        if currentState.board[r][c-1] == 0:
                            newState.board[r][c-1] = piece
                            newState.board[r + k[0]][c + k[1]] = 0
                            captureList.append([[r, c, r, c-1], newState])

            # Leaper capture
            if enemy == (7 - track):
                temp_r = r+k[0]+k[0]
                temp_c= c+k[1]+k[1]
                if temp_r in range(8) and temp_c in range(8):
                    if currentState.board[temp_r][temp_c] == 0:
                        newState.board[temp_r][temp_c] = piece
                        newState.board[r+k[0]][c+k[1]] = 0
                        captureList.append([[r, c, temp_r, temp_c], newState])
        except:
            dummy = None



    # Dynamic analysis
    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]
        try:
            newState = BC.BC_state(currentState.board)
            newState.board[r][c] = 0
            while currentState.board[temp_r][temp_c] == 0:
                cap = imitatorDEval(currentState, temp_r, temp_c, rk, ck, track)
                if len(cap) == 0:
                    newState.board[temp_r][temp_c] = piece
                    movesList.append([[r, c, temp_r, temp_c], newState])
                else:
                    for li in cap:
                        newState.board[li[0]][li[1]] = 0
                    newState.board[temp_r][temp_c] = piece
                    captureList.append([[r, c, temp_r, temp_c], newState])
                temp_r += k[0]
                temp_c += k[1]

            # Leaper capture
            if currentState.board[temp_r][temp_c] == (7 - track):
                if currentState.board[temp_r+k[0]][temp_c+k[1]] == 0:
                    newState.board[temp_r][temp_c] = 0
                    newState.board[temp_r+k[0]][temp_c+k[1]] = piece
                    captureList.append([[r, c, temp_r, temp_c], newState])
        except:
            dummy = None


def imitatorDEval(currentState, r, c, rk, ck, track):
    # r,c are the moved coordinates of imitator
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
    cList = []

    for k in movedirection:
        try:
            enemy = currentState.board[r + k[0]][c + k[1]]
            # Pincer capture
            if enemy == (3-track) and k in movedirection[:4]:
                    try:
                        if currentState.board[r+k[0]+k[0]][c+k[1]+k[1]]%2 == track:
                            cList.append([r + k[0],c + k[1]])
                    except:
                        dummy = None

            # Coordinate capture
            if enemy == (5-track) and (r != rk or c != ck):
                if (r+k[0],c+k[1]) in [(r,ck),(rk,c)]:
                    cList.append([r + k[0],c + k[1]])
        except:
            dummy = None

    return cList


def move(currentState, r, c, k, item):
    temp_r = r + k[0]
    temp_c = c + k[1]
    try:
        while currentState.board[temp_r][temp_c] == 0:
            newState = BC.BC_state(currentState.board)
            newState.board[temp_r][temp_c] = item
            newState.board[r][c] = 0
            movesList.append([[r,c,temp_r,temp_c],newState])
            temp_r += k[0]
            temp_c += k[1]
    except:
        dummy = None

    return [temp_r-k[0], temp_c-k[1]]


def nickname():
    return "Brew"


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


