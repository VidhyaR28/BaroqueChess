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
              11: 500, 12: 10000, 13: -10000, 14: -500, 15: 500}

WHITE = 1
BLACK = 0

global statesExpanded
global numberEvals
global cutoff
global chosenMove
global finaltime
global inputtime

def parameterized_minimax(currentState, alphaBeta=False, ply=3, useBasicStaticEval=True, useZobristHashing=False):
    global statesExpanded
    global numberEvals
    global cutoff
    global chosenMove
    global inputtime
    statesExpanded = 0
    numberEvals = 0
    cutoff = 0

    chosen = miniMax(currentState, ply, -100000, 100000) # , 0.9*inputtime)

    # [piece, (r,c), (temp_r,temp_c)] is the format for chosenMove
    chosenMove = chosen[1]
    dict = {'CURRENT_STATE_STATIC_VAL': chosen[0], 'N_STATES_EXPANDED': statesExpanded, 'N_STATIC_EVALS': numberEvals, 'N_CUTOFFS': cutoff}
    return dict


#the input is just a [state]
#the outout is formated as [staticValue, move]
def miniMax(state, depth, a, b): # , inputtime):
    global statesExpanded
    global numberEvals
    global cutoff
    global finaltime

    if depth == 0 or inputtime <= 0.75:
        numberEvals += 1
        static = staticEval(state)
        return [static, None]

    # makeMove sends in with a starttime, endtime
    # if time < 1

    moves = successors(state)
    # successors produce a list of moves and not states
    track = state.whose_move
    if track == 1:
        val = -100000
        Bstate = None #[moves]
        for child in moves:
            statesExpanded += 1
            function = miniMax(statify(state,child,track), depth-1, a, b) # , 0.9*inputtime)
            if function[0] > val:
                Bstate = child
                val = function[0]
            if val > b:
                cutoff += 1
                break
            if val > a:
                a = val
        return [val, Bstate]
    else:
        val = 1000000
        Bstate = None
        for child in moves:
            statesExpanded += 1
            function = miniMax(statify(state,child,track), depth-1, a, b) # , inputtime)
            if function[0] < val:
                Bstate = child
                val = function[0]
            if val < a:
                cutoff += 1
                break
            if val < b:
                b = val
        return [val, Bstate]



def makeMove(currentState, currentRemark, timelimit=10):
    start_time = time.time()
    global finaltime
    global inputtime
    # we have a start time, time limit, and elapsed time.
    # elapsed time too close to timelimit, stop.
    # make move has to send in a function with time.
    # first time, I send in nothing? First time I send in time.time
    # everytime I send in a time limit. I'm gonna do time.time and find out what the time left is.

    finaltime = timelimit + start_time

    track = 0
    if currentState.whose_move == 1:
        track = 1
    else: track = 0
    board = currentState.board

    global opponent
    opponent = [3-track, 5-track, 7-track, 9-track, 11-track, 13-track, 15-track]

    global friendly
    friendly = [2+track, 4+track, 6+track, 8+track, 10+track, 12+track, 14+track]

    king_r = 0
    king_c = 0
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece == (12+track):
                king_r = i
                king_c = j


    attackDir = kingCheckAttack(board, king_r, king_c, track)
    if attackDir:
        attackMove = kingAttackMove(board, king_r, king_c, 12+track, track)
        # attackMove in the format [piece, (r,c), (temp_r,temp_c)]
        if attackMove:
            newState = statify(currentState,attackMove,track)
            strMove = stringify(attackMove)
            return [[strMove,newState],"Phew! Close save!"]

        finalSave = kingMinionMove(board, king_r, king_c, attackDir, track)
        # finalSave in the format [piece, (r,c), (temp_r,temp_c)]
        if finalSave:
            newState = statify(currentState,finalSave,track)
            strMove = stringify(finalSave)
            return [[strMove,newState],"Phew! Close save!"]


    #IDDFS
    for depth in range(15):
        inputtime = start_time + timelimit - time.time() # this will give us the time left.
        parameterized_minimax(currentState, True, depth, False, False)

        if depth == 2: # REPLACE THIS - keep track of the timer to timeout here keep 0.02 secconds to compute the following

            global chosenMove
            outState = statify(currentState,chosenMove,track)
            outMove = stringify(chosenMove)
            newRemark = remark()

            print("OutState: ", currentState)
            print("Chosen move: ", chosenMove)

            global moveCount
            moveCount += 1
            return [[outMove, outState], newRemark]


MAP_ROW = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
MAP_COL = {0:'8', 1:'7', 2:'6', 3:'5', 4:'4', 5:'3', 6:'2', 7:'1'}
#[[move, newState], newRemark] and moves as (fr, new_fr) where fr is e2, e is column and 2 is row
# def stringify(m):
#     # [piece, (r,c), (temp_r,temp_c)] as m - one piece of movesList
#     r = MAP_COL[m[1][0]] #number str
#     c = MAP_ROW[m[1][1]] #alphabet str
#     fromStr = c+r
#     rf = MAP_COL[m[2][0]]
#     cf = MAP_ROW[m[2][1]]
#     toStr = cf+rf
#     return (fromStr,toStr) #formatted as (fr, new_fr)


def stringify(m):
    # [piece, (r,c), (temp_r,temp_c)] as m - one piece of movesList
    r = m[1][0]
    c = m[1][1]
    rf = m[2][0]
    cf = m[2][1]
    return ((r,c),(rf,cf)) #formatted as ((a,b),(aa,bb))


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
    try:
        for i in m[3]:
            rCap = i[0]
            cCap = i[1]
            newState.board[rCap][cCap] = 0
    except:
        dummy = None
    newState.board[r][c] = 0
    newState.board[rf][cf] = piece
    newState.whose_move = 1-track
    return newState


def successors(currentState):
    global movesList
    global captureList
    movesList = []
    captureList = []
    generateStates(currentState)
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
    else: track = 0

    frozenPieces = []
    kingR = 0
    kingC = 0
    cordR = 0
    cordC = 0
    board = currentState.board


    for i in range(8):
        for j in range(8):
            item = board[i][j]
            if item == (15-track):
                # the enemy freezer; map all your frozen pieces
                movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
                for k in movedirection:
                    if i+k[0] in range(8) and j+k[1] in range(8):
                        if board[i+k[0]][j+k[1]] in friendly:
                            frozenPieces.append(board[i+k[0]][j+k[1]])

            if item == (14+track):
                # My freezer to check whether it has an imitator next to it
                movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
                Freezerfreeze = False
                imiR = 0
                imiC = 0

                for k in movedirection:
                    if i+k[0] in range(8) and j+k[1] in range(8):
                        # found freezer
                        if board[i+k[0]][j+k[1]] == (9-track):
                            Freezerfreeze = True
                            imiR = i+k[0]
                            imiC = j+k[1]

                if Freezerfreeze:
                    for k in movedirection:
                        if imiR+k[0] in range(8) and imiC+k[1] in range(8):
                            if board[imiR+k[0]][imiC+k[1]] in friendly:
                                frozenPieces.append(board[imiR+k[0]][imiC+k[1]])

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
            piece = board[i][j]
            if piece not in frozenPieces and piece in friendly:
                if piece == 2 or piece == 3: #Pincer - Done
                    pincerMoves(board, i, j, piece)
                elif piece == 4 or piece == 5: #Coordinator - Done
                    coordinatorMoves(board, i, j, kingR, kingC, piece)
                elif piece == 6 or piece == 7: #Leaper - Done
                    leaperMoves(board, i, j, piece)
                elif piece == 8 or piece == 9: #Imitator - Done
                    imitatorMoves(board, i, j, kingR, kingC, piece, track)
                elif piece == 10 or piece == 11: #Withdrawer - Done
                    withdrawerMoves(board, i, j, piece)
                elif piece == 12 or piece == 13: #King - Done
                    kingMoves(board, i, j, cordR, cordC, piece)
                elif piece == 14 or piece == 15: #Freezer - Done
                    freezerMoves(board, i, j, piece)

def pincerMoves(board, r, c, piece):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0]]

    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]
        while temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
            neighbour = [dir for dir in movedirection if dir != k]
            cap = []
            capture = False
            for n in neighbour:
                nR = temp_r + n[0]
                nC = temp_c + n[1]
                if nR in range(8) and nC in range(8) and board[nR][nC] in opponent:
                    if nR+n[0] in range(8) and nC+n[1] in range(8) and board[nR+n[0]][nC+n[1]] in friendly:
                        cap.append((temp_r, temp_c))
                        capture = True
            if capture:
                # pincer capture moves
                captureList.append([piece, (r,c), (temp_r,temp_c), cap])
            else:
                # pincer non-capture moves
                movesList.append([piece, (r,c), (temp_r,temp_c)])
            temp_r += k[0]
            temp_c += k[1]


def withdrawerMoves(board, r, c, piece):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
    captureMoves = []

    # withdrawer capture moves
    for k in movedirection:
        temp_r = r
        temp_c = c

        if temp_r+k[0] in range(8) and temp_c+k[1] in range(8):
            if board[temp_r+k[0]][temp_c+k[1]] in opponent:
                capture = False
                temp_r -= k[0]
                temp_c -= k[1]
                while temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
                    captureList.append([piece, (r,c),(temp_r,temp_c),(r+k[0],c+k[1])])
                    capture = True
                    temp_c -= k[1]
                    temp_r -= k[0]

                if capture:
                    captureMoves.append([k[0], k[1]])
                    captureMoves.append([-k[0],-k[1]])

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
            temp_r = final[0]+k[0]
            temp_c = final[1]+k[1]
            if temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] in opponent:
                if temp_r+k[0] in range(8) and temp_c+k[1] in range(8):
                    if board[temp_r + k[0]][temp_c + k[1]] == 0:
                        captureList.append([piece, (r,c), (temp_r+k[0],temp_c+k[1]), (temp_r,temp_c)])


def coordinatorMoves(board, r, c, rk, ck, piece):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]
        while temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
            if temp_r == rk or temp_c == ck:
                movesList.append([piece, (r,c), (temp_r,temp_c)])
            else:
                cap = []
                capture = False
                if board[temp_r][ck] in opponent:
                    cap.append((temp_r,ck))
                    capture = True
                if board[rk][temp_c] in opponent:
                    cap.append((rk, temp_c))
                    capture = True

                if capture:
                    captureList.append([piece, (r, c), (temp_r, temp_c), cap])
                else:
                    movesList.append([piece, (r,c), (temp_r,temp_c)])
            temp_r += k[0]
            temp_c += k[1]


def kingMoves(board, r, c, rcord, ccord, piece):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        temp_r = r +k[0]
        temp_c = c +k[1]
        if temp_r in range(8) and temp_c in range(8):
            if board[temp_r][temp_c] in opponent:
                captureList.append([piece, (r,c), (temp_r,temp_c)])
            elif board[temp_r][temp_c] == 0:
                #captures with coordinator
                cap = []
                capture = False
                if board[temp_r][ccord] in opponent:
                    cap.append((temp_r,ccord))
                    capture = True
                if board[rcord][temp_c] in opponent:
                    cap.append((rcord,temp_c))
                    capture = True

                if capture:
                    captureList.append([piece, (r,c), (temp_r,temp_c), cap])
                else:
                    movesList.append([piece, (r,c), (temp_r,temp_c)])


def freezerMoves(board, r, c, piece):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        final = move(board, r, c, k, piece)


def imitatorMoves(board, r, c, rk, ck, piece, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    # Stationary analysis
    for k in movedirection:
        if r+k[0] in range(8) and c+k[1] in range(8) and board[r+k[0]][c+k[1]] in opponent:
            enemy = board[r+k[0]][c+k[1]]
            # King capture
            if enemy == (13 - track):
                captureList.append([piece, (r,c), (r+k[0],c+k[1])])

            # Withdrawer capture
            if enemy == (11-track):
                temp_r = r-k[0]
                temp_c = r-k[1]
                while temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
                    captureList.append([piece, (r,c), (temp_r,temp_c), (r+k[0],c+k[1])])
                    temp_r -= k[0]
                    temp_c -= k[1]

            # Coordinator capture
            if enemy == (5-track):
                if r+k[0] == rk and rk != r:
                    if board[r][c+k[1]] == 0:
                        captureList.append([piece, (r,c), (r,c+k[1]), (r+k[0],c+k[1])])

                elif r+k[0] == rk and c+k[1] == c:
                    if r+1 in range(8):
                        if board[r+1][c] == 0:
                            captureList.append([piece, (r,c), (r+1,c), (r+k[0],c+k[1])])
                    elif r-1 in range(8):
                        if board[r-1][c] == 0:
                            captureList.append([piece, (r,c), (r-1,c), (r+k[0],c+k[1])])

                elif c+k[0] == ck and ck != c:
                    if board[r+k[0]][c] == 0:
                        captureList.append([piece, (r,c), (r+k[0],c), (r+k[0],c+k[1])])

                elif c+k[0] == ck and r+k[0] == r:
                    if c+1 in range(8):
                        if board[r][c+1] == 0:
                            captureList.append([piece, (r,c), (r,c+1), (r+k[0],c+k[1])])
                    elif c-1 in range(8):
                        if board[r][c-1] == 0:
                            captureList.append([piece, (r,c), (r,c-1), (r+k[0],c+k[1])])

            # Leaper capture
            if enemy == (7 - track):
                temp_r = r+k[0]+k[0]
                temp_c= c+k[1]+k[1]
                if temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
                    captureList.append([piece, (r,c), (temp_r,temp_c), (r+k[0],c+k[1])])


    # Dynamic analysis
    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]
        while temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
            cap = imitatorDEval(board, temp_r, temp_c, rk, ck, track)
            if len(cap) == 0:
                movesList.append([piece, (r,c), (temp_r,temp_c)])
            else:
                captureList.append([piece, (r,c), (temp_r,temp_c), cap])
            temp_r += k[0]
            temp_c += k[1]

        # Leaper capture
        if temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == (7 - track):
            if temp_r+k[0] in range(8) and temp_c+k[1] in range(8) and board[temp_r+k[0]][temp_c+k[1]] == 0:
                captureList.append([piece, (r, c), (temp_r+k[0],temp_c+k[1]), (temp_r,temp_c)])


def imitatorDEval(board, r, c, rk, ck, track):
    # r,c are the moved coordinates of imitator
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]
    cList = []

    for k in movedirection:
        temp_r = r+k[0]
        temp_c = c+k[1]
        if temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] in opponent:
            enemy = board[temp_r][temp_c]
            # Pincer capture
            if enemy == (3-track) and k in movedirection[:4]:
                if temp_r+k[0] in range(8) and temp_c+k[1] in range(8) and board[temp_r+k[0]][temp_c+k[1]] in friendly:
                    cList.append((temp_r,temp_c))

            # Coordinate capture
            if enemy == (5-track) and (r != rk or c != ck):
                if (r+k[0],c+k[1]) in [(r,ck),(rk,c)]:
                    cList.append((r+k[0],c+k[1]))
    return cList


def move(board, r, c, k, item):
    temp_r = r+k[0]
    temp_c = c+k[1]
    while temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
        movesList.append([item, (r,c), (temp_r,temp_c)])
        temp_r += k[0]
        temp_c += k[1]
    if temp_r in range(8) and temp_c in range(8):
        return [temp_r-k[0],temp_c-k[1]]
    else: return None


def kingCheckAttack(board, r, c, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        temp_r = r + k[0]
        temp_c = c + k[1]
        if temp_r in range(8) and temp_c in range(8):
            adj = board[temp_r][temp_c]
            if adj == (9-track): #Imitator
                return k
            if adj == (11-track): #Withdrawer
                return k
            if adj == (3-track): #Pincer
                return k

        while temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
            temp_r += k[0]
            temp_c += k[1]

        if temp_r in range(8) and temp_c in range(8):
            adj = board[temp_r][temp_c]
            if adj == (7-track): #Leaper
                return k
            if adj == (3-track) and k in movedirection[:4]: #Pincer
                return k
            if adj == (13-track) or adj == (5-track): #King-Coordinator
                return k
            if adj == (15-track): #Freezer
                return k
    return None


def kingAttackMove(board, r, c, piece, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0], [-1, 1], [-1, -1], [1, -1], [1, 1]]

    for k in movedirection:
        temp_r = r+k[0]
        temp_c = c+k[1]

        if temp_r in range(8) and temp_c in range(8):
            adj = board[temp_r][temp_c]
            if adj == 0 or adj in opponent:
                newBoard = board
                newBoard[r][c] = 0
                newBoard[temp_r][temp_c] = piece
                if not kingCheckAttack(board,temp_r,temp_c, track):
                    return [piece, (r,c), (temp_r,temp_c)]
    return None


def kingMinionMove(board, r, c, KK, track):
    movedirection = [[0, 1], [-1, 0], [0, -1], [1, 0]]
    closures = []
    for i in range(3):
        temp_r = r+(KK[0]*(i+1))
        temp_c = c+(KK[1]*(i+1))
        if temp_r in range(8) and temp_c in range(8) and board[temp_r][temp_c] == 0:
            closures.append((r+(KK[0]*(i+1)),c+(KK[1]*(i+1))))

    if closures:
        for i in range(8):
            for j in range(8):
                piece = board[i][j]
                if piece == (2+track) and KK in movedirection: # pincer
                    move = tryMove(board,i,j,closures,piece)
                    if move: return move
                if piece in friendly[1:]: # all other pieces
                    move = tryMove(board,i,j,closures, piece)
                    if move: return move


def tryMove(board, r, c, possibilities, piece):
    for p in possibilities:
        if r == p[0]:
            val = abs(c-p[1])-1
            occupied = False
            minVal = min(c,p[1])
            while val > 0:
                minVal += 1
                if board[r][minVal] != 0:
                    occupied = True
                val -= 1
            if not occupied:
                return [piece, (r,c), (r,p[1])]

        if c == p[1]:
            val = abs(r - p[0]) - 1
            occupied = False
            minVal = min(r, p[0])
            while val > 0:
                minVal += 1
                if board[minVal][c] != 0:
                    occupied = True
                val -= 1
            if not occupied:
                newState = BC.BC_state(board)
                newState.board[r][c] = 0
                newState.board[p[0]][c] = piece
                return [piece, (r,c), (p[0],c)]
    return None



def nickname():
    return "Brew"


def introduce():
    return "I'm Diluted Coffee, and I am an aspiring Baroque Chess player."


def prepare(player2Nickname, playWhite = False):
    global colourtrack
    global captureList
    global movesList
    global moveCount
    global chosenMove
    global inputtime
    captureList = []
    movesList = []
    moveCount = 0
    chosenMove = [0,0,0,0]


    if (playWhite == True):
        colourtrack = 1
    else:
        colourtrack = 0
    print("Hey ", player2Nickname,"! *cracks knuckles* Let's get started.")


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


    returnval = 0
    board = state.board

    for i in range(0, 8):
        for j in range(0, 8):
            #print("Piece location: (", i, ", ", j,") Piece value:",  state.board[i][j])
            if board[i][j] in [2, 3]:
                # Pincer
                # print("Enter Pincer")
                check1 = pincerMobility(board, (i, j)) + pincerKill(board, (i, j))
                print("Pincer mobility + kill", check1)
                returnval += check1
                # print("Pincer done")
            elif board[i][j] in [4, 5]:
                # Coordinator
                # print("Enter Coordinator")
                check2 = coordinatorKill(board, (i, j))
                print("Coordinator Kill ", check2)
                returnval += check2
                # print("Coordinator done")

            elif board[i][j] in [6, 7]:
                # Leaper
                # print("Enter Leaper")
                check3 = leaperKill(board, (i, j))
                print("Leaper Kill: ", check3)

                returnval += check3
                # print("Leaper done")
            elif board[i][j] in [10, 11]:
                # Withdrawer
                # print("Enter Withdrawer")
                check4 = withdrawerKill(board, (i, j))
                print("Withdrawer Kill: ", check4)
                returnval += check4
                # print("Withdrawer done")
            elif board[i][j] in [12, 13]:
                # King
                # print("Enter King")
                check5 = kingCheck(board, (i, j))
                print("King Check: ", check5)
                returnval += check5
                # print("King done")
            elif board[i][j] in [14, 15]:
                # Freezer
                # print("Enter Freezer")
                check6 = freezerKill(board, (i, j)) /2
                print("Freezer Kill: ", check6)
                returnval += check6
                # print("Freezer done")
    # print("Board is: ")
    # print(state.board)
    # print("Stativ Eval: ", returnval)
    return returnval


def pincerMobility(board, k):
    #print("Pincer Mobility")
    # board = state.board
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    count = 0
    for s in movedirection:
        if (k[0] + s[0]) in range(0, 8) and (k[1] + s[1]) in range(0, 8):
            if board[k[0] + s[0]][k[1] + s[1]] == 0:
                count += pieceValue.get(board[k[0]][k[1]])/abs(pieceValue.get(board[k[0]][k[1]]))

    return count * 5


def pincerKill(board, k):
    # board = state.board
    # go north, south, east, west. Hit a block. Check if it's the other colour. If yes, go one step ahead and see if we
    # have a piece there. If yes, more points.
    count = 0
    #print("Pincer Kill")
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    if board[k[0]][k[1]] in [2, 4, 6, 8, 10, 12, 14]:
        opponentPieces = [3, 5, 7, 9, 11, 13, 15]
    else:
        opponentPieces = [2, 4, 6, 8, 10, 12, 14]
    count = 0
    networth = 0

    for s in movedirection:
        t = [k[0], k[1]]

        # checks in a direction. Loops through blank spaces, checks if it's an opponent. If true, checks if our
        # our piece exists right after.
        # checking for blank spaces
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
                    if board[t[0]][t[1]] not in opponentPieces and board[t[0]][t[1]] != 0:
                        t[0] -= s[0]
                        t[1] -= s[1]
                        networth += pieceValue.get(board[t[0]][t[1]])
                        count += 1
    # print("Pincer Kill end")
    return networth * count


def freezerKill(board, k):
    # board = state.board
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]

    if board[k[0]][k[1]] in [2, 4, 6, 8, 10, 12, 14]:
        opponentPieces = [3, 5, 7, 9, 11, 13, 15]
    else:
        opponentPieces = [2, 4, 6, 8, 10, 12, 14]

    count = 0
    networth = 0
    # threatworth = 0
    # threatcount = 0

    for s in movedirection:
        t = [k[0], k[1]]
        t[0] += s[0]
        t[1] += s[1]
        if (t[0] in range(0, 8) and t[1] in range(0, 8) and board[t[0]][t[1]] != 0):
            if board[t[0]][t[1]] in opponentPieces:
                # do something
                networth += pieceValue.get(board[t[0]][t[1]])
                count += 1
            # else:
            #
            #     threatworth = pieceValue.get(board[t[0]][t[1]])
            #     threatcount += 1
    # the more things we freeze, the better off we are
    return (networth * count) / 4


def kingCheck(board, k):
    # If king is around  a couple of different folks,
    # board = state.board
    print("Original Input: ", board[k[0]][k[1]])
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]

    if board[k[0]][k[1]] in [2, 4, 6, 8, 10, 12, 14]:
        opponentPieces = [3, 5, 7, 9, 11, 13, 15]
    else:
        opponentPieces = [2, 4, 6, 8, 10, 12, 14]

    count = 0

    for s in movedirection:
        t = [k[0], k[1]]

        for loop in range(1, 3):
            print("Loop: ", loop)

            t[0] += s[0] * loop
            t[1] += s[1] * loop

            if t[0] in range(0, 8) and t[1] in range(0, 8):
                if (board[t[0]][t[1]] < 0 and board[k[0]][k[1]] < 0) or (board[t[0]][t[1]] > 0 and board[k[0]][k[1]] > 0):
                    sameSide = True
                else:
                    sameSide = False
                print("Same Side: ", sameSide, "King: ",board[k[0]][k[1]], "Other: ", board[t[0]][t[1]])
                if t[0] in range(0, 8) and t[1] in range(0, 8) and board[t[0]][t[1]] != 0:
                    if pieceValue.get(board[k[0]][k[1]]) < 0 and sameSide:
                        count += 800
                    else:
                        count -= 800
                    print("Count: ", count)

    print("Final count ", count)
    return count


def leaperKill(board, k):
    # board = state.board
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
        t = [k[0], k[1]]

        # checks in a direction. Loops through blank spaces, checks if it's an opponent. If true, checks if our
        # our piece exists right after.
        # checking for blank spaces
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
    # if we have an item of opposite colour and on opposite side we have a blank, then we add value.
    # board = state.board
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