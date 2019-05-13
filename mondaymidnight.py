#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Diluted Coffee is a Baroque Chess Player made by Vidhya Rajendran and Krishna Teja

"""

import BC_state_etc as BC

pieceValue = {0: 0, 2: -100, 3: 100, 4: -500, 5: 500, 6: 500, 7: -500, 8: -900, 9: 900, 10: -500,
              11: 500, 12: 100000, 13: -100000, 14: -500, 15: 500}

WHITE = 1


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
                returnval += freezerKill(state, [i, j]) / 2

    return returnval


def pincerMobility(state, k):
    board = state.board
    movedirection = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    count = 0
    for s in movedirection:
        if board[k[0] + s[0]][k[1] + s[1]] == 0:
            count += 1
    return count * 5


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
    return networth * count


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
    return (networth * count + threatworth * threatcount) / 4


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
                if pieceValue.get(board[t[0]][t[1]]) < 0:
                    count -= 800
                else:
                    count += 800
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














