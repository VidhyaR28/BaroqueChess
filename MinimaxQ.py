#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Brew is a Baroque Chess Player made by Vidhya Rajendran and Krishna Teja

"""

import new_BC_state_etc as BC
import heapq
import random
import time
import math
import numpy



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
global inputtime
global IDDFStrack
global ENDTIME


# NEW STUFF START___________________________________________________________________________________
global W
global episodes
episodes = 0

# NEW STUFF END


# Zobrist stuff
global ZOBTAB
global ZOBHASH



CODE_TO_INIT = {0: '-', 2: 'p', 3: 'P', 4: 'c', 5: 'C', 6: 'l', 7: 'L', 8: 'i', 9: 'I',
                10: 'w', 11: 'W', 12: 'k', 13: 'K', 14: 'f', 15: 'F'}

pieceValue = {0: 0, 2: -900, 3: 900, 4: -1000, 5: 1000, 6: -1100, 7: 1100, 8: -1200, 9: 1200, 10: -1300,
              11: 1300, 12: 100000, 13: -100000, 14: -1400, 15: 1400}

WHITE = 1
BLACK = 0

global statesExpanded
global numberEvals
global cutoff
global chosenMove


def parameterized_minimax(currentState, alphaBeta= True, ply = 3, useBasicStaticEval = False, useZobristHashing= True):
    global statesExpanded
    global numberEvals
    global cutoff
    global chosenMove
    global inputtime

    statesExpanded = 0
    numberEvals = 0
    cutoff = 0
    # print("Param minimax")
    chosen = miniMax(currentState, ply, -math.inf, math.inf, 0) #, 0.9*inputtime)
    # [piece, (r,c), (temp_r,temp_c)] is the format for chosenMove
    chosenMove = chosen[1]
    dict = {'CURRENT_STATE_STATIC_VAL': chosen[0], 'N_STATES_EXPANDED': statesExpanded, 'N_STATIC_EVALS': numberEvals,
            'N_CUTOFFS': cutoff}
    return dict


# NEW STUFF START________________________________________________________________________________________
def miniMax(state, depth, a, b, power):
    global inputtime
    global iterDepthTrack
    global statesExpanded
    global numberEvals
    global cutoff
    global IDDFStrack
    global ZOBHASH
    global ENDTIME
    global chosenMove
    global W
    global check
    global episodes
    ALPHA = 1 / (episodes + 1)
    GAMMA = 0.9

    if depth == 0 or (ENDTIME - time.time() < 0.3):
        numberEvals += 1
        value = featureRL(state)
        return [value, None]


    moves = successors(state)

    if IDDFStrack > 1:
        moves.insert(0, chosenMove)

    track = state.whose_move
    val = None
    Bstate = None  # [moves]
    multiplier = 0

    for child in moves:
        statesExpanded += 1
        function = miniMax(statify(state, child, track), depth - 1, a, b, power+1)

        if track == 1:
            val = -1 * math.inf
            multiplier = 1
            if function[0] > val:
                Bstate = child
                val = function[0]
            if val > b:
                cutoff += 1
                break
            if val > a:
                a = val
        else:
            val = math.inf
            multiplier = -1
            if function[0] < val:
                Bstate = child
                val = function[0]
            if val < a:
                cutoff += 1
                break
            if val < b:
                b = val

    diff = ( multiplier * reward(state) + (GAMMA**power) * val ) - featureRL(state)
    for i in range(6):
        W[i] = W[i] + ALPHA * diff * check[i]

    return [val, Bstate]


def reward(state):
    # material value
    board = state.board
    count = 0
    for i in range(8):
        for j in range(8):
            count += pieceValue[board[i][j]]
    return count

# NEW STUFF END


def Zobrist():
    # We need to loop through every item on board, give every piece a randomly generated value,
    # XOR stuff? and then, get a "has" . This hash should point to a dictionary, K (Zob hash) -> Value (tuple of data)
    # UPDATE MINIMAX WITH ZOBRIST STUFF
    global ZOBTAB

    """
    constant indices
    white_pawn := 1
    white_rook := 2
    # etc.
    black_king := 12
    function init_zobrist():
    # fill a table of random numbers/bitstrings
    table := a 2-d array of size 64×12
       for i from 1 to 64:  # loop over the board, represented as a linear array
           for j from 1 to 12:      # loop over the pieces
               table[i][j] = random_bitstring()
    function hash(board):
       h := 0
       for i from 1 to 64:      # loop over the board positions
           if board[i] != empty:
               j := the piece at board[i], as listed in the constant indices, above
               h := h XOR table[i][j]
       return h
    """
    # init = [[4, 6, 8, 10, 12, 8, 6, 14], [2, 2, 2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3], [15, 7, 9, 11, 13, 9, 7, 5]]
    for i in range (0, 65):
        for j in range (0, 13):
            # insert a random value
            ZOBTAB[i][j] = random.getrandbits(24)
    return

def ZobristHash(board):
    """
    Calculates the hash value of a particular states and returns it.
    Store: Best move, alpha, beta, static eval

    :param state:
    :return:
    """
    global ZOBTAB
    tabulartrack = 0

    h = 0

    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] != 0:
                val = ZOBTAB[tabulartrack][board[i][j]]
                h = h^val
            tabulartrack += 1
    return h


def makeMove(currentState, currentRemark, timelimit=10):
    global inputtime
    # TIMER COMPONENT
    start_time = time.time()

    track = 0
    if currentState.whose_move == 1:
        track = 1
    else:
        track = 0
    board = currentState.board

    global opponent
    opponent = [3 - track, 5 - track, 7 - track, 9 - track, 11 - track, 13 - track, 15 - track]

    global friendly
    friendly = [2 + track, 4 + track, 6 + track, 8 + track, 10 + track, 12 + track, 14 + track]

    king_r = 0
    king_c = 0
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece == (12 + track):
                king_r = i
                king_c = j

    attackDir = kingCheckAttack(board, king_r, king_c, track)
    if attackDir:
        attackMove = kingAttackMove(board, king_r, king_c, 12 + track, track)
        # attackMove in the format [piece, (r,c), (temp_r,temp_c)]
        if attackMove:
            newState = statify(currentState, attackMove, track)
            strMove = stringify(attackMove)
            return [[strMove, newState], "Phew! Close save!"]

        finalSave = kingMinionMove(board, king_r, king_c, attackDir, track)
        # finalSave in the format [piece, (r,c), (temp_r,temp_c)]
        if finalSave:
            newState = statify(currentState, finalSave, track)
            strMove = stringify(finalSave)
            return [[strMove, newState], "Phew! Close save!"]

    # IDDFS
    depth = 1
    # outMove = ((0, 0), (0, 0))
    # outState = BC.BC_state()
    # newRemark = ""
    global IDDFStrack
    IDDFStrack = 0
    global ENDTIME
    ENDTIME = start_time + timelimit
    while (ENDTIME - time.time() > 0.3):
        print("IDDFS: ", IDDFStrack)
        parameterized_minimax(currentState, True, IDDFStrack, False, False)
        IDDFStrack += 1
        # where is the depth increasing???


    global chosenMove
    outState = statify(currentState, chosenMove, track)
    outMove = stringify(chosenMove)
    newRemark = remark()
    global moveCount
    moveCount += 1
    depth += 1

    return [[outMove, outState], newRemark]



MAP_ROW = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
MAP_COL = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}


def stringify(m):
    # [piece, (r,c), (temp_r,temp_c)] as m - one piece of movesList
    r = m[1][0]
    c = m[1][1]
    rf = m[2][0]
    cf = m[2][1]
    return ((r, c), (rf, cf))  # formatted as ((a,b),(aa,bb))


# [piece, (r,c), (temp_r,temp_c)] as m - one piece of movesList
# [piece, (r,c), (temp_r,temp_c), cap] as m - one piece of captureList
# cap could be [(3,4),(5,6),(2,5)]
# takes the state as the parameter
# returns a moved state
def statify(state, m, track):
    newState = BC.BC_state(state.board)
    r = m[1][0]
    c = m[1][1]
    rf = m[2][0]
    cf = m[2][1]
    piece = m[0]
    newState.board[r][c] = 0
    newState.board[rf][cf] = piece
    newState.whose_move = 1 - track
    length = 3
    try:
        if len(m) == 4:
            length = 4
    except:
        dummy = None

    if length == 4:
        for i in m[3]:
            rCap = i[0]
            cCap = i[1]
            newState.board[rCap][cCap] = 0

    return newState


def successors(currentState):
    global movesList
    global captureList
    movesList = []
    captureList = []
    generateStates(currentState)

    random.shuffle(movesList)
    random.shuffle(captureList)

    fullList = []
    for moves in captureList:
        fullList.append(moves)
    for moves in movesList:
        fullList.append(moves)
    # print("successors here")
    # print (len(fullList))
    return fullList


def generateStates(currentState):
    if currentState.whose_move == 1:
        track = 1
    else:
        track = 0


    global opponent
    opponent = [3 - track, 5 - track, 7 - track, 9 - track, 11 - track, 13 - track, 15 - track]

    global friendly
    friendly = [2 + track, 4 + track, 6 + track, 8 + track, 10 + track, 12 + track, 14 + track]

    frozenPieces = []
    kingR = 0
    kingC = 0
    cordR = 0
    cordC = 0
    board = currentState.board

    for i in range(8):
        for j in range(8):
            item = board[i][j]
            if item == (15 - track):
                # the enemy freezer; map all your frozen pieces
                movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
                for k in movedirection:
                    if i + k[0] in range(8) and j + k[1] in range(8):
                        if board[i + k[0]][j + k[1]] in friendly:
                            frozenPieces.append(board[i + k[0]][j + k[1]])

            if item == (14 + track):
                # My freezer to check whether it has an imitator next to it
                movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
                Freezerfreeze = False
                imiR = 0
                imiC = 0

                for k in movedirection:
                    if i + k[0] in range(8) and j + k[1] in range(8):
                        # found freezer
                        if board[i + k[0]][j + k[1]] == (9 - track):
                            Freezerfreeze = True
                            imiR = i + k[0]
                            imiC = j + k[1]

                if Freezerfreeze:
                    for k in movedirection:
                        if imiR + k[0] in range(8) and imiC + k[1] in range(8):
                            if board[imiR + k[0]][imiC + k[1]] in friendly:
                                frozenPieces.append(board[imiR + k[0]][imiC + k[1]])

            if item == (12 + track):
                # My army's king
                kingR = i
                kingC = j

            if item == (4 + track):
                # My army's coordinator
                cordR = i
                cordC = j

    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece not in frozenPieces and piece in friendly:
                if piece == 2 or piece == 3:  # Pincer - Done
                    pincerMoves(board, i, j, piece)
                elif piece == 4 or piece == 5:  # Coordinator - Done
                    coordinatorMoves(board, i, j, kingR, kingC, piece)
                elif piece == 6 or piece == 7:  # Leaper - Done
                    leaperMoves(board, i, j, piece)
                elif piece == 8 or piece == 9:  # Imitator - Done
                    imitatorMoves(board, i, j, kingR, kingC, piece, track)
                elif piece == 10 or piece == 11:  # Withdrawer - Done
                    withdrawerMoves(board, i, j, piece)
                elif piece == 12 or piece == 13:  # King - Done
                    kingMoves(board, i, j, cordR, cordC, piece)
                elif piece == 14 or piece == 15:  # Freezer - Done
                    freezerMoves(board, i, j, piece)


def pincerMoves(board, r, c, piece):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0]]

    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]
        while temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
            new_k = [-k[0],-k[1]]
            neighbour = [dir for dir in movedirection if dir != new_k]
            cap = []
            capture = False
            for n in neighbour:
                nR = temp_r + n[0]
                nC = temp_c + n[1]
                if nR in range(8) and nC in range(8) and board[nR][nC] in opponent:
                    if nR + n[0] in range(8) and nC + n[1] in range(8) and board[nR + n[0]][nC + n[1]] in friendly:
                        cap.append((nR, nC))
                        capture = True
            if capture:
                # pincer capture moves
                captureList.append([piece, (r, c), (temp_r, temp_c), cap])
            else:
                # pincer non-capture moves
                movesList.append([piece, (r, c), (temp_r, temp_c)])
            temp_r += k[0]
            temp_c += k[1]


def withdrawerMoves(board, r, c, piece):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
    captureMoves = []

    # withdrawer capture moves
    for k in movedirection:
        temp_r = r
        temp_c = c

        if temp_r + k[0] in range(8) and temp_c + k[1] in range(8):
            if board[temp_r + k[0]][temp_c + k[1]] in opponent:
                capture = False
                temp_r -= k[0]
                temp_c -= k[1]
                while temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
                    captureList.append([piece, (r, c), (temp_r, temp_c), [(r + k[0], c + k[1])]])
                    capture = True
                    temp_r -= k[0]
                    temp_c -= k[1]

                if capture:
                    captureMoves.append([k[0], k[1]])
                    captureMoves.append([-k[0], -k[1]])

    # withdrawer non-capture moves
    noncaptureMoves = [k for k in movedirection if k not in captureMoves]

    for k in noncaptureMoves:
        final = move(board, r, c, k, piece)


def leaperMoves(board, r, c, piece):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        # leaper non-capture moves
        final = move(board, r, c, k, piece)

        # leaper Capture moves
        if final:
            temp_r = final[0] + k[0]
            temp_c = final[1] + k[1]
            if temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] in opponent:
                if (temp_r + k[0]) in range(8) and (temp_c + k[1]) in range(8):
                    if board[temp_r + k[0]][temp_c + k[1]] == 0:
                        captureList.append([piece, (r, c), (temp_r + k[0], temp_c + k[1]), [(temp_r, temp_c)]])


def coordinatorMoves(board, r, c, rk, ck, piece):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]
        while temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
            if temp_r == rk or temp_c == ck:
                movesList.append([piece, (r, c), (temp_r, temp_c)])
            else:
                cap = []
                capture = False
                if board[temp_r][ck] in opponent:
                    cap.append((temp_r, ck))
                    capture = True
                if board[rk][temp_c] in opponent:
                    cap.append((rk, temp_c))
                    capture = True

                if capture:
                    captureList.append([piece, (r, c), (temp_r, temp_c), cap])
                else:
                    movesList.append([piece, (r, c), (temp_r, temp_c)])
            temp_r += k[0]
            temp_c += k[1]


def kingMoves(board, r, c, rcord, ccord, piece):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]
        if temp_r in range(8) and temp_c in range(8):
            if board[temp_r][temp_c] in opponent:
                captureList.append([piece, (r, c), (temp_r, temp_c)])


def freezerMoves(board, r, c, piece):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        final = move(board, r, c, k, piece)


def imitatorMoves(board, r, c, rk, ck, piece, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
    capture = False
    captureMoves = []


    # Stationary analysis
    for k in movedirection:
        if r + k[0] in range(8) and c + k[1] in range(8) and board[r + k[0]][c + k[1]] in opponent:
            enemy = board[r + k[0]][c + k[1]]
            # King capture
            if enemy == (13 - track):
                captureList.append([piece, (r, c), (r + k[0], c + k[1])])

            # Withdrawer capture
            if enemy == (11 - track):
                temp_r = r - k[0]
                temp_c = c - k[1]
                while temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
                    captureList.append([piece, (r, c), (temp_r, temp_c), [(r + k[0], c + k[1])]])
                    capture = True
                    temp_r -= k[0]
                    temp_c -= k[1]
                if capture:
                    captureMoves.append([k[0], k[1]])
                    captureMoves.append([-k[0], -k[1]])

            # Coordinator capture
            if enemy == (5 - track):
                enemy_r = r + k[0]
                enemy_c = c + k[1]
                if enemy_r == rk:
                    for h in movedirection:
                        temp_r = r + h[0]
                        temp_c = c + h[1]
                        if temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
                            if temp_c == enemy_c:
                                captureList.append([piece, (r, c), (temp_r, temp_c), [(enemy_r, enemy_c)]])

                if enemy_c == ck:
                    for h in movedirection:
                        temp_r = r + h[0]
                        temp_c = c + h[1]
                        if temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
                            if temp_r == enemy_r:
                                captureList.append([piece, (r, c), (temp_r, temp_c), [(enemy_r, enemy_c)]])

            # Leaper capture
            if enemy == (7 - track):
                temp_r = r + k[0] + k[0]
                temp_c = c + k[1] + k[1]
                if temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
                    captureList.append([piece, (r, c), (temp_r, temp_c), [(r + k[0], c + k[1])]])


    other_dir = [k for k in movedirection if k not in captureMoves]

    # Dynamic analysis
    for k in other_dir:
        temp_r = r + k[0]
        temp_c = c + k[1]
        while temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
            cap = imitatorDEval(board, temp_r, temp_c, rk, ck, track, k)
            if len(cap) == 0:
                movesList.append([piece, (r, c), (temp_r, temp_c)])
            else:
                captureList.append([piece, (r, c), (temp_r, temp_c), cap])
            temp_r += k[0]
            temp_c += k[1]

        # Leaper capture
        if temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == (7 - track):
            if temp_r + k[0] in range(8) and temp_c + k[1] in range(8) and board[temp_r + k[0]][temp_c + k[1]] == 0:
                captureList.append([piece, (r, c), (temp_r + k[0], temp_c + k[1]), [(temp_r, temp_c)]])


def imitatorDEval(board, r, c, rk, ck, track, dir):
    # r,c are the moved coordinates of imitator
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
    cList = []

    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]
        if temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] in opponent:
            enemy = board[temp_r][temp_c]
            # Pincer capture
            if enemy == (3 - track) and k in movedirection[:4] and dir in movedirection[:4]:
                if temp_r + k[0] in range(8) and temp_c + k[1] in range(8) and board[temp_r + k[0]][temp_c + k[1]] in friendly:
                    cList.append((temp_r, temp_c))

            # Coordinate capture
            if enemy == (5 - track) and (r != rk or c != ck):
                if (temp_r, temp_c) in [(r, ck), (rk, c)]:
                    cList.append((temp_r, temp_c))
    return cList


def move(board, r, c, k, item):
    temp_r = r + k[0]
    temp_c = c + k[1]
    while temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
        movesList.append([item, (r, c), (temp_r, temp_c)])
        temp_r += k[0]
        temp_c += k[1]
    if (temp_r - k[0]) in range(8) and (temp_c - k[1]) in range(8):
        return [temp_r - k[0], temp_c - k[1]]
    else:
        return None


def kingCheckAttack(board, r, c, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]
        if temp_r in range(8) and temp_c in range(8):
            adj = board[temp_r][temp_c]
            if adj == (9 - track):  # Imitator
                return k
            if adj == (11 - track):  # Withdrawer
                return k
            if adj == (3 - track):  # Pincer
                return k

        # COMMENTED OUT because of this the there is a constact kingAttack move
        # temp_tempr = r + k[0]
        # temp_tempc = c + k[1]
        # while temp_tempr in range(8) and temp_tempc in range(8):
        #     adj = board[temp_tempr][temp_tempc]
        #     if adj == (13 - track) or adj == (5 - track): # King-Coordinator
        #         return k
        #     temp_tempr += k[0]
        #     temp_tempc += k[1]

        while temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
            temp_r += k[0]
            temp_c += k[1]

        if temp_r in range(8) and temp_c in range(8):
            adj = board[temp_r][temp_c]
            if adj == (7 - track):  # Leaper
                if r-k[0] in range(8) and c-k[1] in range(8) and board[r-k[0]][c-k[1]] == 0:
                    return k
            if adj == (3 - track) and k in movedirection[:4]:  # Pincer
                if r-k[0] in range(8) and c-k[1] in range(8) and board[r-k[0]][c-k[1]] in opponent:
                    return k
            if adj == (15 - track):  # Freezer
                return k
    return None


def kingAttackMove(board, r, c, piece, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    frozen = FREEZERcheck(board, track)
    if piece in frozen:
        return None

    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]

        if temp_r in range(8) and temp_c in range(8):
            adj = board[temp_r][temp_c]
            if adj == 0 or adj in opponent:
                if not kingCheckAttack(board, temp_r, temp_c, track):
                    return [piece, (r, c), (temp_r, temp_c)]
    return None


def kingMinionMove(board, r, c, KK, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0]]
    closures = []
    frozen = FREEZERcheck(board, track)

    for i in range(3):
        temp_r = r + (KK[0] * (i + 1))
        temp_c = c + (KK[1] * (i + 1))
        if temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
            closures.append((temp_r, temp_c))

    if closures:
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece in friendly and piece != 12+track and piece not in frozen:  # all my pieces except king
                    move = tryMove(board, i, j, closures, piece, track)
                    if move: return move


def FREEZERcheck(board, track):
    frozenPieces = []
    for i in range(8):
        for j in range(8):
            item = board[i][j]
            if item == (15 - track):
                # the enemy freezer; map all your frozen pieces
                movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
                for k in movedirection:
                    if i + k[0] in range(8) and j + k[1] in range(8):
                        if board[i + k[0]][j + k[1]] in friendly:
                            frozenPieces.append(board[i + k[0]][j + k[1]])

            if item == (14 + track):
                # My freezer to check whether it has an imitator next to it
                movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
                Freezerfreeze = False
                imiR = 0
                imiC = 0

                for k in movedirection:
                    if i + k[0] in range(8) and j + k[1] in range(8):
                        # found freezer
                        if board[i + k[0]][j + k[1]] == (9 - track):
                            Freezerfreeze = True
                            imiR = i + k[0]
                            imiC = j + k[1]

                if Freezerfreeze:
                    for k in movedirection:
                        if imiR + k[0] in range(8) and imiC + k[1] in range(8):
                            if board[imiR + k[0]][imiC + k[1]] in friendly:
                                frozenPieces.append(board[imiR + k[0]][imiC + k[1]])
    return frozenPieces


def tryMove(board, r, c, possibilities, piece, track):
    # r,c are the coordinates of the unmoved friendly pieces
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        temp_r = r+k[0]
        temp_c = c+k[1]
        while temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
            for p in possibilities:
                if temp_r == p[0] and temp_c == p[1]:
                    if piece == 2+track and k in movedirection[:4]:
                        return [piece, (r, c), (temp_r, temp_c)]
                    elif piece != 2+track:
                        return [piece, (r, c), (temp_r, temp_c)]
            temp_r += k[0]
            temp_c += k[1]
    return None


def nickname():
    return "Brew"

def introduce():
    return "I'm Brew, and I am an aspiring Baroque Chess player."


# NEW STUFF START________________________________________________________________________________________
def prepare(player2Nickname):
    global colourtrack
    global captureList
    global movesList
    global moveCount
    global chosenMove
    global inputtime
    global ZOBTAB
    global ZOBHASH
    global W
    global check
    global episodes
    episodes += 1
    moveCount = 0

    ZOBTAB = numpy.zeros((65, 13))
    ZOBHASH = {}
    W =[1, 1, 1, 1, 1, 1]
    check = [0, 0, 0, 0, 0, 0]
    Zobrist()

    print("Hey ", player2Nickname,"! *cracks knuckles* Let's get started.")

# NEW STUFF END


def basicStaticEval(state):
    totalEval = 0

    for i in range(8):
        for j in range(8):
            # Coordinator, Leaper, Imitator, Withdrawer, Freezer
            if state.board[i][j] in [4, 6, 8, 10, 14]:
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
    remarks = ["Your turn!", "Take that!", "Try to beat that!", "Think well before you move", "Best is yet to come!",
               "Come on!", "Lets get moving,", "Don't think too much, just play!",
                           "Here you go!", "Don't "]
    return random.choice(remarks)


# NEW STUFF START________________________________________________________________________________________
def featureRL(state):
    global W
    global check
    returnval = 0
    board = state.board

    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] in [2, 3]: # pincer
                check[0] = W[0]*(pincerMobility(board, (i, j)) + pincerKill(board, (i, j)))
                returnval += check[0]
            elif board[i][j] in [4, 5]: # Coordinator
                check[1] = W[1]*coordinatorKill(board, (i, j))
                returnval += check[1]
            elif board[i][j] in [6, 7]: # Leaper
                check[2] = W[2]*leaperKill(board, (i, j))
                returnval += check[2]
            elif board[i][j] in [10, 11]: # Withdrawer
                check[3] = W[3]*withdrawerKill(board, (i, j))
                returnval += check[3]
            elif board[i][j] in [12, 13]: # King
                check[4] = W[4]*kingCheck(board, (i, j))
                returnval += check[4]
            elif board[i][j] in [14, 15]: # Freezer
                check[5] = W[5]*freezerKill(board, (i, j)) /2
                returnval += check[5]
    return returnval

# NEW STUFF END


def pincerMobility(board, k):
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    count = 0
    for s in movedirection:
        if (k[0] + s[0]) in range(0, 8) and (k[1] + s[1]) in range(0, 8):
            if board[k[0] + s[0]][k[1] + s[1]] == 0:
                count += pieceValue.get(board[k[0]][k[1]])/abs(pieceValue.get(board[k[0]][k[1]]))

    return count * 5


def pincerKill(board, k):
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    if board[k[0]][k[1]] in [2, 4, 6, 8, 10, 12, 14]:
        opponentPieces = [3, 5, 7, 9, 11, 13, 15]
    else:
        opponentPieces = [2, 4, 6, 8, 10, 12, 14]
    count = 0
    networth = 0

    for s in movedirection:
        t = [k[0], k[1]]

        t[0] += s[0]
        t[1] += s[1]
        while t[0] in range(0, 8) and t[1] in range(0, 8) and board[t[0]][t[1]] == 0:
            t[0] += s[0]
            t[1] += s[1]

        if t[0] in range(0, 8) and t[1] in range(0, 8):
            if board[t[0]][t[1]] in opponentPieces:
                t[0] += s[0]
                t[1] += s[1]
                if t[0] in range(0, 8) and t[1] in range(0, 8):
                    if board[t[0]][t[1]] not in opponentPieces and board[t[0]][t[1]] != 0:
                        t[0] -= s[0]
                        t[1] -= s[1]
                        networth += pieceValue.get(board[t[0]][t[1]])
                        count += 1
    return networth * count


def freezerKill(board, k):
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]

    if board[k[0]][k[1]] in [2, 4, 6, 8, 10, 12, 14]:
        opponentPieces = [3, 5, 7, 9, 11, 13, 15]
    else:
        opponentPieces = [2, 4, 6, 8, 10, 12, 14]

    count = 0
    networth = 0

    for s in movedirection:
        t = [k[0], k[1]]
        t[0] += s[0]
        t[1] += s[1]
        if (t[0] in range(0, 8) and t[1] in range(0, 8) and board[t[0]][t[1]] != 0):
            if board[t[0]][t[1]] in opponentPieces:
                networth += pieceValue.get(board[t[0]][t[1]])
                count += 1
    return (networth * count)/2


def kingCheck(board, k):
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]

    if board[k[0]][k[1]] in [2, 4, 6, 8, 10, 12, 14]:
        opponentPieces = [3, 5, 7, 9, 11, 13, 15]
    else:
        opponentPieces = [2, 4, 6, 8, 10, 12, 14]

    count = 0

    for s in movedirection:
        t = [k[0], k[1]]

        for loop in range(1, 2):
            # print("Loop: ", loop)
            t[0] += s[0] * loop
            t[1] += s[1] * loop

            if t[0] in range(0, 8) and t[1] in range(0, 8):
                if (board[t[0]][t[1]] < 0 and board[k[0]][k[1]] < 0) or (board[t[0]][t[1]] > 0 and board[k[0]][k[1]] > 0):
                    sameSide = True
                else:
                    sameSide = False
                if t[0] in range(0, 8) and t[1] in range(0, 8) and board[t[0]][t[1]] != 0:
                    if pieceValue.get(board[k[0]][k[1]]) < 0 and sameSide:
                        count += 100
                    else:
                        count -= 100
                if t[0] in range(0, 8) and t[1] in range(0, 8) and board[t[0]][t[1]] == 0 and loop == 1:
                    temp = [0, 0]
                    temp[0] = k[0] # + s[0]
                    temp[1] = k[1] # + s[1]
                    temp[0] -= s[0]
                    temp[1] -= s[1]
                    while (temp[0] in range(0, 8) and temp[1] in range(0, 8)):
                        if (board[temp[0]][temp[1]] in [6, 7] and board[temp[0]][temp[1]] in opponentPieces):
                            count -= pieceValue.get(board[k[0]][k[1]])
                        temp[0] -= s[0]
                        temp[1] -= s[1]

    opp = []
    for i in range(0, 8):
        for j in range(0, 8):
            if (((board[i][j] == 4 or board[i][j] == 5) and board[i][j] in opponentPieces) or
                    ((board[i][j] == 12 or board[i][j] == 13) and board[i][j] in opponentPieces)):
                opp.append([i, j])

    #(i, j) and (a, b)
    if (len(opp) == 2):
        t1 = opp.__getitem__(0)
        t2 = opp.__getitem__(1)
        if (board[t1[0]][t2[1]] == board[k[0]][k[1]] or board[t1[1]][t2[0]] == board[k[0]][k[1]]):
            count -= pieceValue.get(board[k[0]][k[1]])
    return count


def leaperKill(board, k):
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    if board[k[0]][k[1]] in [2, 4, 6, 8, 10, 12, 14]:
        opponentPieces = [3, 5, 7, 9, 11, 13, 15]
    else:
        opponentPieces = [2, 4, 6, 8, 10, 12, 14]
    count = 0
    networth = 0

    for s in movedirection:
        t = [k[0], k[1]]
        while (t[0] in range(0, 8) and t[1] in range(0, 8) and board[t[0]][t[1]] == 0):
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
    return networth * count


def withdrawerKill(board, k):
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]

    count = 0

    if board[k[0]][k[1]] in [2, 4, 6, 8, 10, 12, 14]:
        opponentPieces = [3, 5, 7, 9, 11, 13, 15]
    else:
        opponentPieces = [2, 4, 6, 8, 10, 12, 14]

    for s in movedirection:
        t = [k[0], k[1]]
        t[0] += s[0]
        t[1] += s[1]
        if t[0] in range(0, 8) and t[1] in range(0, 8):

            if board[t[0]][t[1]] in opponentPieces:
                if (t[0] + s[0]) in range(0, 8) and (t[1] + s[1]) in range(0, 8):
                    if board[t[0] + s[0]][t[1] + s[1]]:
                        count += pieceValue.get(board[t[0]][t[1]])

    return count


def coordinatorKill(board, k):
    # board = state.board
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
