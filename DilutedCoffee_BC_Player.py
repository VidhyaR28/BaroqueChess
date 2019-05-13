#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Diluted Coffee is a Baroque Chess Player made by Vidhya Rajendran and Krishna Teja

"""

import BC_state_etc as BC
import heapq
import random
import time

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
global opponent
global friendly
global moveCount

CODE_TO_INIT = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}

pieceValue = {0: 0, 2: -100, 3: 100, 4: -500, 5: 500, 6: 500, 7: -500, 8: -900, 9: 900, 10: -500,
              11: 500, 12: 100000, 13: -100000, 14: -500, 15: 500}

WHITE = 1



def parameterized_minimax(currentState, alphaBeta=False, ply = 3, \
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
        provisional = -100000000
    else:
        provisional = 100000000

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


    return

def successors(currentState):
    """
    Takes in a list of successors and returns them
    :param currentState:
    :return:
    """
    result = []
    copy_state = currentState

    for move in legalMoves(state):
        result.append(changeState(copy_state, move))
    return result

def makeMove(currentState, currentRemark, timelimit=10):
    # Compute the new state for a move.
    # You should implement an anytime algorithm based on IDDFS.

    track = 0
    newState = BC.BC_state(currentState.board)
    if newState.whose_move == 'WHITE':
        track = 1
    else: track = 0

    global opponent
    opponent = [3-track, 5-track, 7-track, 9-track, 11-track, 13-track, 15-track]

    global friendly
    friendly = [2+track, 4+track, 6+track, 8+track, 10+track, 12+track, 14+track]

    king_r = 0
    king_c = 0
    for i in range(8):
        for j in range(8):
            piece = newState.board[i][j]
            if piece == (12+track):
                king_r = i
                king_c = j

    attackDir = kingCheckAttack(newState, king_r, king_c, track)
    if attackDir:
        states = kingAttackMove(newState, king_r, king_c, 12+track)
        for state in states:
            if not kingCheckAttack(state[1], king_r, king_c, track):
                return [[move, newState], newRemark] #____________________________________________DO IT
        return kingMinionMove(newState, king_r, king_c, attackDir, track) #_______________________

    else: generateStates(newState, timelimit)

    # Fix up whose turn it will be.
    newState.whose_move = 1 - currentState.whose_move

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    # Here is a placeholder in the right format but with made-up
    # numbers:
    move = ((6, 4), (3, 4))


    newRemark = remark()
    global moveCount
    moveCount += 1

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
                    if i+k[0] in range(8) and j+k[1] in range (8):
                        if currentState.board[i+k[0]][j+k[1]] in friendly:
                            frozenPieces.append(currentState.board[i+k[0]][j+k[1]])

            if item == (14+track):
                # My freezer to check whether it has an imitator next to it
                movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
                Freezerfreeze = False
                imiR = 0
                imiC = 0

                for k in movedirection:
                    if i+k[0] in range(8) and j+k[1] in range (8):
                        # found freezer
                        if currentState.board[i+k[0]][j+k[1]] == (9-track):
                            Freezerfreeze = True
                            imiR = i+k[0]
                            imiC = j+k[1]

                if Freezerfreeze:
                    for k in movedirection:
                        if imiR+k[0] in range(8) and imiC+k[1] in range(8):
                            if currentState.board[imiR+k[0]][imiC+k[1]] in friendly:
                                frozenPieces.append(currentState.board[imiR+k[0]][imiC+k[1]])

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
            piece = currentState.board[i][j]
            if piece not in frozenPieces and piece in friendly:
                if piece == 2 or piece == 3: #Pincer - Done
                    pincerMoves(currentState, i, j, piece, track)
                elif piece == 4 or piece == 5: #Coordinator - Done
                    coordinatorMoves(currentState, i, j, kingR, kingC, piece, track)
                elif piece == 6 or piece == 7: #Leaper - Done
                    leaperMoves(currentState, i, j, piece, track)
                elif piece == 8 or piece == 9: #Imitator - Done
                    imitatorMoves(currentState, i, j, kingR, kingC, piece, track)
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
        while temp_r in range(8) and temp_c in range(8) and currentState.board[temp_r][temp_c] == 0:
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
                if nR in range(8) and nC in range(8) and currentState.board[nR][nC] in opponent:
                    if nR+n[0] in range(8) and nC+n[1] in range(8) and currentState.board[nR+n[0]][nC+n[1]] in friendly:
                        capturePiece.append(currentState.board[temp_r][temp_c])
                        captureR.append(temp_r)
                        captureC.append(temp_c)
                        capture = True
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

def withdrawerMoves(currentState, r, c, piece, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
    captureMoves = []

    # withdrawer capture moves
    for k in movedirection:
        temp_r = r
        temp_c = c

        if temp_r+k[0] in range(8) and temp_c+k[1] in range(8):
            if currentState.board[temp_r+k[0]][temp_c+k[1]] in opponent:
                capture = False
                temp_r -= k[0]
                temp_c -= k[1]
                while temp_r in range(8) and temp_c in range(8) and currentState.board[temp_r][temp_c] == 0:
                    newState = BC.BC_state(currentState.board)
                    newState.board[temp_r][temp_c] = piece
                    newState.board[r][c] = 0
                    newState.board[r+k[0]][c+k[1]] = 0
                    captureList.append([r,c,temp_r,temp_c],newState)
                    capture = True
                    temp_c -= k[1]
                    temp_r -= k[0]

                if capture:
                    captureMoves.append([k[0], k[1]])
                    captureMoves.append([-k[0],-k[1]])

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
        if final:
            temp_r = final[0]+k[0]
            temp_c = final[1]+k[1]
            if temp_r in range(8) and temp_c in range(8) and currentState.board[temp_r][temp_c] in opponent:
                if temp_r+k[0] in range(8) and temp_c+k[1] in range(8):
                    if currentState.board[temp_r + k[0]][temp_c + k[1]] == 0:
                        newState = BC.BC_state(currentState.board)
                        newState.board[temp_r][temp_c] = 0
                        newState.board[r][c] = 0
                        newState.board[temp_r+k[0]][temp_c+k[1]] = piece
                        captureList.append([[r,c,temp_r+k[0],temp_c+k[1]], newState])


def coordinatorMoves(currentState, r, c, rk, ck, piece, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]
        while temp_r in range(8) and temp_c in range(8) and currentState.board[temp_r][temp_c] == 0:
            newState = BC.BC_state(currentState.board)
            newState.board[temp_r][temp_c] = piece
            newState.board[r][c] = 0
            if temp_r == rk or temp_c == ck:
                movesList.append([[r,c,temp_r,temp_c],newState])
            else:
                if newState.board[temp_r][ck] in opponent and newState.board[rk][temp_c] in opponent:
                    newState.board[temp_r][ck] = 0
                    newState.board[rk][temp_c] = 0
                    captureList.append([[r,c,temp_r,temp_c],newState])
                elif newState.board[temp_r][ck] in opponent:
                    newState.board[temp_r][ck] = 0
                    captureList.append([[r,c,temp_r,temp_c],newState])
                elif newState.board[rk][temp_c] in opponent:
                    newState.board[rk][temp_c] = 0
                    captureList.append([[r,c,temp_r,temp_c],newState])
                else:
                    movesList.append([[r,c,temp_r,temp_c],newState])

            temp_r += k[0]
            temp_c += k[1]


def kingMoves(currentState, r, c, rcord, ccord, piece, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        temp_r = r +k[0]
        temp_c = c +k[1]
        if temp_r in range(8) and temp_c in range(8):
            newState = BC.BC_state(currentState.board)
            newState.board[temp_r][temp_c] = piece
            newState.board[r][c] = 0

            if currentState.board[temp_r][temp_c] in opponent:
                captureList.append([[r,c,temp_r,temp_c],newState])
            elif currentState.board[temp_r][temp_c] == 0:
                #captures with coordinator
                if newState.board[temp_r][ccord] in opponent and newState.board[rcord][temp_c] in opponent:
                    newState.board[temp_r][ccord] = 0
                    newState.board[rcord][temp_c] = 0
                    captureList.append([[r, c, temp_r, temp_c], newState])
                elif newState.board[temp_r][ccord] in opponent:
                    newState.board[temp_r][ccord] = 0
                    captureList.append([[r, c, temp_r, temp_c], newState])
                elif newState.board[rcord][temp_c] in opponent:
                    newState.board[rcord][temp_c] = 0
                    captureList.append([[r, c, temp_r, temp_c], newState])
                else:
                    movesList.append([[r, c, temp_r, temp_c], newState])


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
        if r+k[0] in range(8) and c+k[1] in range(8):
            enemy = currentState.board[r+k[0]][c+k[1]]
            # King capture
            if enemy == (13 - track):
                newState.board[r+k[0]][c+k[1]] = piece
                captureList.append([[r, c, r+k[0], c+k[1]], newState])

            # Withdrawer capture
            if enemy == (11-track):
                temp_r = r-k[0]
                temp_c = r-k[1]
                while temp_r in range(8) and temp_c in range(8) and currentState.board[temp_r][temp_c] == 0:
                    newState.board[temp_r][temp_c] = piece
                    newState.board[r+k[0]][c+k[1]] = 0
                    captureList.append([[r, c, r-k[0], c-k[1]], newState])
                    temp_r -= k[0]
                    temp_c -= k[1]

            # Coordinator capture
            if enemy == (5-track):
                if r+k[0] == rk and rk != r:
                    if currentState.board[r][c+k[1]] == 0:
                        newState.board[r][c+k[1]] = piece
                        newState.board[r + k[0]][c + k[1]] = 0
                        captureList.append([[r, c, r, c + k[1]], newState])

                if r+k[0] == rk and c+k[1] == c:
                    if r+1 in range(8):
                        if currentState.board[r+1][c] == 0:
                            newState.board[r+1][c] = piece
                            newState.board[r + k[0]][c + k[1]] = 0
                            captureList.append([[r, c, r+1, c], newState])
                    if r-1 in range(8):
                        if currentState.board[r-1][c] == 0:
                            newState.board[r-1][c] = piece
                            newState.board[r + k[0]][c + k[1]] = 0
                            captureList.append([[r, c, r-1, c], newState])

                if c+k[0] == ck and ck != c:
                    if currentState.board[r+k[0]][c] == 0:
                        newState.board[r+k[0]][c] = piece
                        newState.board[r + k[0]][c + k[1]] = 0
                        captureList.append([[r, c, r+k[0], c], newState])

                if c+k[0] == ck and r+k[0] == r:
                    if c+1 in range(8):
                        if currentState.board[r][c+1] == 0:
                            newState.board[r][c+1] = piece
                            newState.board[r + k[0]][c + k[1]] = 0
                            captureList.append([[r, c, r, c+1], newState])
                    if c-1 in range(8):
                        if currentState.board[r][c-1] == 0:
                            newState.board[r][c-1] = piece
                            newState.board[r + k[0]][c + k[1]] = 0
                            captureList.append([[r, c, r, c-1], newState])

            # Leaper capture
            if enemy == (7 - track):
                temp_r = r+k[0]+k[0]
                temp_c= c+k[1]+k[1]
                if temp_r in range(8) and temp_c in range(8) and currentState.board[temp_r][temp_c] == 0:
                    newState.board[temp_r][temp_c] = piece
                    newState.board[r+k[0]][c+k[1]] = 0
                    captureList.append([[r, c, temp_r, temp_c], newState])


    # Dynamic analysis
    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]
        newState = BC.BC_state(currentState.board)
        newState.board[r][c] = 0
        while temp_r in range(8) and temp_c in range(8) and currentState.board[temp_r][temp_c] == 0:
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
            if temp_r+k[0] in range(8) and temp_c+k[1] in range(8) and currentState.board[temp_r+k[0]][temp_c+k[1]] == 0:
                newState.board[temp_r][temp_c] = 0
                newState.board[temp_r+k[0]][temp_c+k[1]] = piece
                captureList.append([[r, c, temp_r, temp_c], newState])


def imitatorDEval(currentState, r, c, rk, ck, track):
    # r,c are the moved coordinates of imitator
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
    cList = []

    for k in movedirection:
        temp_r = r+k[0]
        temp_c = c+k[1]
        if temp_r in range(8) and temp_c in range(8):
            enemy = currentState.board[temp_r][temp_c]
            # Pincer capture
            if enemy == (3-track) and k in movedirection[:4]:
                if temp_r+k[0] in range(8) and temp_c+k[1] in range(8) and currentState.board[temp_r+k[0]][temp_c+k[1]] in friendly:
                    cList.append([temp_r,temp_c])

            # Coordinate capture
            if enemy == (5-track) and (r != rk or c != ck):
                if (r+k[0],c+k[1]) in [(r,ck),(rk,c)]:
                    cList.append([r + k[0],c + k[1]])
    return cList


def move(currentState, r, c, k, item):
    temp_r = r+k[0]
    temp_c = c+k[1]
    while temp_r in range(8) and temp_c in range(8) and currentState.board[temp_r][temp_c] == 0:
        newState = BC.BC_state(currentState.board)
        newState.board[temp_r][temp_c] = item
        newState.board[r][c] = 0
        movesList.append([[r,c,temp_r,temp_c],newState])
        temp_r += k[0]
        temp_c += k[1]
    if temp_r in range(8) and temp_c in range(8):
        return [temp_r-k[0], temp_c-k[1]]
    else: return None


def kingCheckAttack(state, r, c, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]
        if temp_r in range(8) and temp_c in range(8):
            adj = state.board[temp_r][temp_c]
            if adj == (9-track): #Imitator
                return k
            if adj == (11-track): #Withdrawer
                return k
            if adj == (3-track): #Pincer
                return k

        while temp_r in range(8) and temp_c in range(8) and state.board[temp_r][temp_c] == 0:
            temp_r += k[0]
            temp_c += k[1]

        if temp_r in range(8) and temp_c in range(8):
            adj = state.board[temp_r][temp_c]
            if adj == (7-track): #Leaper
                return k
            if adj == (3-track) and k in movedirection[:4]: #Pincer
                return k
            if adj == (13-track) or adj == (5-track): #King-Coordinator
                return k
            if adj == (15-track): #Freezer
                return k
    return None


def kingAttackMove(state, r, c, piece):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
    returnList = []

    for k in movedirection:
        temp_r = r+k[0]
        temp_c = c+k[1]

        if temp_r in range(8) and temp_c in range(8) and state.board[temp_r][temp_c] == 0:
            newState = BC.BC_state(state.board)
            newState.board[r][c] = 0
            newState.board[temp_r][temp_c] = piece
            returnList.append([[r,c,temp_r,temp_c],newState])
    return returnList


def kingMinionMove(state, r, c, KK, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0]]
    closures = []
    for i in range(3):
        temp_r = r+(KK[0]*(i+1))
        temp_c = c+(KK[1]*(i+1))
        if temp_r in range(8) and temp_c in range(8) and state.board[temp_r][temp_c] == 0:
            closures.append((r+(KK[0]*(i+1)),c+(KK[1]*(i+1))))

    for i in range(8):
        for j in range(8):
            piece = state.board[i][j]
            if piece == (2+track) and KK in movedirection: # pincer
                move = tryMove(state,i,j,closures,piece)
                if move: return move
            if piece in friendly[1:]: # all other pieces
                move = tryMove(state,i,j,closures, piece)
                if move: return move

def tryMove(state, r, c, possibilities, piece):
    newState = BC.BC_state(state.board)
    newState.board[r][c] = 0
    for p in possibilities:
        if r == p[0]:
            val = abs(c-p[1])-1
            occupied = False
            minVal = min(c,p[1])
            while val > 0:
                if newState.board[r][minVal+1] != 0:
                    occupied = True
                minVal += 1
                val -= 1
            if not occupied:
                newState.board[r][p[1]] = piece
                return [[r,c,r,p[1]],newState]

        if c == p[1]:
            val = abs(r - p[0]) - 1
            occupied = False
            minVal = min(r, p[0])
            while val > 0:
                if newState.board[minVal + 1][c] != 0:
                    occupied = True
                minVal += 1
                val -= 1
            if not occupied:
                    newState.board[p[0]][c] = piece
                    return [[r, c, p[0], c], newState]

    return None



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
    global moveCount

    captureList = []
    movesList = []
    moveCount = 0

    if (playWhite == True):
        colourtrack = 1
    else:
        colourtrack = 0
    print("Hey, I'm super prepared at this point.")

    return


def basicStaticEval(state):
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


def remark():
    remarks = ["Your turn!", "Take that!", "Try to beat that!", "Think well before you move", "Best is yet to come!", "Come on!", "Lets get moving,"
                "Here you go!"]
    return random.choice(remarks)


def staticEval(state):
    """
        Compute a more thorough static evaluation of the given state.
        This is intended for normal competitive play.  How you design this
        function could have a significant impact on your player's ability
        to win games.

        :param state:
        :return:
        """
    returnval = 0

    for i in range(0, 8):
        for j in range(0, 8):
            if state.board[i][j] in [2, 3]:
                # Pincer
                returnval += pincerMobility(state, [i, j]) + pincerKill(state.board, [i, j])

            elif state.board[i][j] in [4, 5]:
                # Coordinator
                returnval += coordinatorKill(state, [i, j])

            elif state.board[i][j] in [6, 7]:
                # Leaper
                returnval += leaperKill(state, [i, j])

            elif state.board[i][j] in [10, 11]:
                # Withdrawer
                returnval += withdrawerKill(state, [i, j])

            elif state.board[i][j] in [12, 13]:
                # King
                returnval += kingCheck(state, [i, j])

            elif state.board[i][j] in [14, 15]:
                # Freezer
                returnval += freezerKill(state, [i, j])/2

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

    if board[k[0]][k[1]] in [2, 4, 6, 8, 10, 12, 14]:
        opponentPieces = [3, 5, 7, 9, 11, 13, 15]
    else:
        opponentPieces = [2, 4, 6, 8, 10, 12, 14]
    count = 0
    networth = 0

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

            if board[t[0]][t[1]] in opponentPieces:
                t[0] += s[0]
                t[1] += s[1]
                if t[0] in range(0, 8) and t[1] in range(0, 8):
                    if board[t[0]][t[1]] not in opponentPieces and board[t[0]][t[1]] != 0:
                        t[0] -= s[0]
                        t[1] -= s[1]
                        networth += pieceValue.get(board[t[0]][t[1]])
                        count += 1
    return networth*count


def freezerKill(state, k):
    board = state.board
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]

    if board[k[0]][k[1]] in [2, 4, 6, 8, 10, 12, 14]:
        opponentPieces = [3, 5, 7, 9, 11, 13, 15]
    else:
        opponentPieces = [2, 4, 6, 8, 10, 12, 14]

    count = 0
    networth = 0
    threatworth = 0
    threatcount = 0

    for s in movedirection:
        t = k
        t[0] += s[0]
        t[1] += s[1]
        while (t[0] in range(0, 8) and t[1] in range(0, 8) and board[t[0]][t[1]] != 0):
            if board[t[0]][t[1]] in opponentPieces:
                # do something
                networth = pieceValue.get(board[t[0]][t[1]])
                count += 1
            else:

                threatworth = pieceValue.get(board[t[0]][t[1]])
                threatcount += 1
    # the more things we freeze, the better off we are
    return (networth*count + threatworth*threatcount)/4

def kingCheck(state, k):
    # If king is around  a couple of different folks,
    board = state.board
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]

    if board[k[0]][k[1]] in [2, 4, 6, 8, 10, 12, 14]:
        opponentPieces = [3, 5, 7, 9, 11, 13, 15]
    else:
        opponentPieces = [2, 4, 6, 8, 10, 12, 14]

    count = 0

    for s in movedirection:
        t = k
        t[0] += s[0]
        t[1] += s[1]
        while (t[0] in range(0, 8) and t[1] in range(0, 8) and board[t[0]][t[1]] != 0):
            if board[t[0]][t[1]] in opponentPieces:
                if pieceValue.get(board[t[0]][t[1]]) < 0: count -= 800
                else: count += 800
            else:
                if pieceValue.get(board[t[0]][t[1]] < 0):
                    count -= 800
                else:
                    count += 800

    return count

def leaperKill(state, k):

    board = state.board
    # go north, south, east, west. Hit a block. Check if it's the other colour. If yes, go one step ahead and see if we
    # have a piece there. If yes, more points.
    count = 0
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    if board[k[0]][k[1]] in [2, 4, 6, 8, 10, 12, 14]:
        opponentPieces = [3, 5, 7, 9, 11, 13, 15]
    else:
        opponentPieces = [2, 4, 6, 8, 10, 12, 14]
    count = 0
    networth = 0

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

            if board[t[0]][t[1]] in opponentPieces:
                t[0] += s[0]
                t[1] += s[1]
                if t[0] in range(0, 8) and t[1] in range(0, 8):
                    if board[t[0]][t[1]] == 0:
                        t[0] -= s[0]
                        t[1] -= s[1]
                        networth += pieceValue.get(board[t[0]][t[1]])
                        count += 1
    return networth*count

def withdrawerKill(state, k):
    # if we have an item of opposite colour and on opposite side we have a blank, then we add value.
    board = state.board
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]

    count = 0

    if board[k[0]][k[1]] in [2, 4, 6, 8, 10, 12, 14]:
        opponentPieces = [3, 5, 7, 9, 11, 13, 15]
    else:
        opponentPieces = [2, 4, 6, 8, 10, 12, 14]

    for s in movedirection:
        t = k
        t[0] += s[0]
        t[1] += s[1]

        if board[t[0]][t[1]] in opponentPieces:
            if board[t[0] + s[0]][t[1] + s[1]]:
                count += pieceValue.get(board[t[0]][t[1]])

    return count

def coordinatorKill(state, k):
    board = state.board
    if board[k[0]][k[1]] in [2, 4, 6, 8, 10, 12, 14]:
        opponentPieces = [3, 5, 7, 9, 11, 13, 15]
        king = 12
    else:
        king = 13
        opponentPieces = [2, 4, 6, 8, 10, 12, 14]

    killValue = 0

    val = [-1, -1]
    for i in range(0, 8):
        for j in range(0, 8):
            if (board[i][j]) == king:
                val = [i, j]

    if board[k[0]][val[1]] != 0 and board[k[0]][val[1]] in opponentPieces:
        killValue += pieceValue.get(board[k[0]][val[1]])
    if board[val[0]][k[1]] != 0 and board[val[0]][k[1]] in opponentPieces:
        killValue += pieceValue.get(board[val[0]][k[1]])
    return killValue














