# Optimal usage:
# Open python terminal
# Enter: 'from TestMoves import *'
# This will allow access to all methods here (just call the name)
#   and methods in BC_state_etc (call with BC.method_name())
# A state (BC.BC_state()) is available in var state

import BC_state_etc as BC
import itertools

state = BC.BC_state()

def find_piece(state, piece, n=0):
    """
    Finds the piece in the board.
    :param state: a BC_state
    :param piece: either a string or number representing a piece
    :param n: if there are duplicates of the piece on the board (i.e. pincers),
        Find the (n-1)th piece. 0 finds the first, 1 finds the second, etc.
    :return: coordinate (x, y). Returns None if the piece is not found
    """

    # Transform piece into an int so that the board lookup can take place
    if type(piece) == str:
        piece = BC.INIT_TO_CODE[piece]

    # Loop through the entire board
    for x in range(0, 8):
        for y in range(0, 8):

            # If the piece is found
            if state.board[x][y] == piece:

                # If there are duplicates, check if the right duplicate is found
                # If not, decrement n
                # Otherwise, return the current coordinates in a tuple
                if n > 0:
                    n -= 1
                else:
                    return (x, y)
    # Piece was not fonud, so return None
    return None

def find_moves(state, piece, n=0, p=True):
    """
    Creates a Dict of the moves (x, y) and boolean
    :param state: BC_state
    :param piece: string or int representation of a piece
    :param n: if there are duplicates of the piece on the board (i.e. pincers),
        Find the (n-1)th piece. 0 finds the first, 1 finds the second, etc.
    :param p: (boolean), if True, prints out some information. The same information
        can be printed out by calling map_summary on the returned Dict.
    :return: Dict of moves to validity of moves:
        (x, y): True (valid move)
        (a, b): False (invalid move)
    """
    start = find_piece(state, piece, n)
    moves = {}
    for x in range(0, 8):
        for y in range(0, 8):
            moves[(x, y)] = BC.can_move(state, start, (x, y))
    if p:
        map_summary(moves)
    return moves

def find_valid_moves_by_coord(state, start):
    """
    Finds the valid moves for the piece at start.
    :param state: Game state.
    :param start: Tuple (x,y) starting coordinates.
    :return: list of moves.
    """
    moves = []
    if state.board[start[0]][start[1]] != 0:
        for x in range(0, 8):
            for y in range(0, 8):
                if BC.can_move(state, start, (x, y)):
                    moves.append((x, y))
    return moves

def find_valid_moves(state, piece, n=0):
    """
    Returns a list of the coordinates that the piece can validly move to.
    :param state: BC_state
    :param piece: string or int representation of a piece
    :param n: if there are duplicates of the piece on the board (i.e. pincers),
        Find the (n-1)th piece. 0 finds the first, 1 finds the second, etc.
    :return: list of coordinates [(x, y), (a, b) ... ]
    """
    piece = find_piece(state, piece, n)
    moves = []
    for x in range(0, 8):
        for y in range(0, 8):
            if BC.can_move(state, piece, (x, y)):
                moves.append((x, y))
    return moves

def map_summary(dict):
    """
    Prints out a summary of the Dict. The values must be singular.
    :param dict:
    """
    print([(k, len(list(v))) for k, v in itertools.groupby(sorted(dict.values()))])

def translate_from_location(state, x, y):
    """
    Translates the piece at (x, y) on the board to it's letter.
    :param state: BC_state
    :param x: x-coordinate
    :param y: y-coordinate
    :return: string representing a piece
    """
    return translate(state.board[x][y])

def translate(piece):
    """
    Translates a pieces number representation to letter, or vice versa
    :param piece: piece representation to translate
    :return: string or number representing the piece
    """
    if type(piece) == str:
        return BC.INIT_TO_CODE[piece]
    return BC.CODE_TO_INIT[piece]

def translate_board(board):
    """
    Translates an entire board, keeping the same structure.
    :param board: Game board.
    :return: List of lists
    """
    translated = []
    for x in range(0, 8):
        translated.append(translate_all(board[x]))
    return translated

def board_to_string(board):
    """
    Creates a string representation of the board.
    :param board: Game board.
    :return: str
    """
    translated = board
    if type(board[0][0]) != str:
        translated = translate_board(board)
    ret = ""
    for x in range(0, 8):
        for y in range(0, 8):
            ret += translated[x][y] + " "
        ret += "\n"
    ret = ret[0:len(ret) - 2]
    return ret


def translate_all(list):
    """
    Translates all piece representations in list from letter to number, or vice verse
    :param list: list of piece representations
    :return: list of translated representations
    """
    translated = []
    for item in list:
        translated.append(translate(item))
    return translated

def find_num_all_moves(state):
    """
    Finds the number of moves for each piece in the initial state.
    Not super useful
    :param state:
    :return:
    """
    cols = [0, 1, 6, 7]
    total_moves = {}
    for col in cols:
        for row in range(0, 8):
            total_moves[translate_from_location(state, col, row)] = find_moves(state, state.board[col][row], p=False)
    return total_moves

def piece_at(state, x, y):
    """
    Gets the letter representation of the piece located at (x, y)
    :param state: BC_state
    :param x: x-coordiante
    :param y: y-coordinate
    :return: string
    """
    print(BC.CODE_TO_INIT[state.board[x][y]])


def test_open_moves(piece, expected=27):
    """
    Tests the moves of piece on an open game board.
    :param piece: The string representation of the piece to test.
    :param expected: The expected number of moves. Set to 27 by default, which
    covers most pieces: withdrawer, imitator, leaper, coordinator, freezer.
    Pincers have 14, and kings have 8.
    """

    # Define a board, and put the piece in the middle
    b = BC.parse('''
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - 1 - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
'''.replace('1', piece))
    state = BC.BC_state(b)
    num_moves = find_valid_moves(state, piece)
    print("Found", len(num_moves), "for", piece, "expected", expected)


def test_open_king_moves():
    """
        Tests the king moves on a blank board.
        """
    test_open_moves('k', 8)

def test_open_pincer_moves():
    """
    Tests the pincer moves on a blank board.
    """
    test_open_moves('p', 14)

def test_all_open_moves():
    """
    Tests the number of moves for a piece in the middle of a blank board
    """
    pieces = ['c', 'l', 'i', 'w', 'f']
    for piece in pieces:
        test_open_moves(piece)
    test_open_king_moves()
    test_open_pincer_moves()


def test_initial_moves_helper(state, piece):
    """
    Helper method for test_initial_moves
    :param state: Initial state
    :param piece: piece to test
    :return: Boolean, True if the number of moves found mathces the expected,
    False otherwise
    """
    num_moves = find_valid_moves(state, piece[0], piece[1])
    # Set the expected number of moves. Pincers have 4 moves, all others have 0
    expected = 0
    if piece[0] == 'p' or piece[0] == 'P':
        expected = 4
    if len(num_moves) != expected:
        print("Found", len(num_moves), "for", piece, "expected", expected)
        return False
    return True

def test_initial_moves():
    """
    Checks if BC.can_move works correctly for the initial state.
    :return: None
    """

    # Get a clean state
    s = BC.BC_state()
    success = True

    # Define pieces by (letter, duplicate)
    black_pieces = [('c', 0), ('l', 0), ('i', 0), ('w', 0), ('k', 0), ('i', 1), ('l', 1), ('f', 0)]
    white_pieces = [('C', 0), ('L', 0), ('I', 0), ('W', 0), ('K', 0), ('I', 1), ('L', 1), ('F', 0)]
    for pincer in range(0, 7):
        black_pieces.append(('p', pincer))
        white_pieces.append(('P', pincer))

    # Check each pieces movement,
    for index in range(0, len(white_pieces)):
        state.whose_move = BC.WHITE
        white_success = test_initial_moves_helper(state, white_pieces[index])
        state.whose_move = BC.BLACK
        black_success = test_initial_moves_helper(state, black_pieces[index])
        success = success and white_success and black_success

    if success:
        print("Success!")

# test_all_open_moves()
# test_initial_moves()
# lm = find_valid_moves(state, 'k')
# print("Found", len(lm), "moves")
# print(lm)