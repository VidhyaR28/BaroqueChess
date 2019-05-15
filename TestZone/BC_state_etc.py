'''BC_state_etc.py
S. Tanimoto, October 30, 2017

This file includes functions to support building agents
that play Baroque Chess.  It should be imported by
Python files that implement move generation,
static evaluation, holding matches between players,
etc.

We use 2 alternative representations of states:
 R1. ASCII, for display and initialization.
 R2. A class BC_state that contains a representation of the
     board consisting of an array (implemented as alist of lists).

 To go from R1 to R2, use function: parse to get a board array,
    and then we construct an instance of BC_state.
 To go from R2 to R1, use function: __repr__ (or cast to str).

Within R1, pieces are represented using initials; e.g., 'c', 'C', 'p', etc.
Within R2, pieces are represented using integers 1 through 14.

We are following these rules:

  No leaper double jumps.
      SOME PEOPLE CONSIDER IT DETRIMENTAL TO THE GAME TO ALLOW A LEAPER
      TO MAKE MORE THAN ONE JUMP IN ONE TURN, AND IT INCREASES THE
      BRANCHING FACTOR IN THE GAME TREE, WHICH IS ALREADY LARGE.

  No altering the initial symmetries of the board, although Wikipedia suggests this is allowed.

  No "suicide" moves allowed.

  Pincers can pinch using any friendly piece as their partners, not just other pincers.

  An imitator can imitate at most one piece during a move.

'''
import math
BLACK = 0
WHITE = 1
NORTH = 0; SOUTH = 1; WEST = 2; EAST = 3; NW = 4; NE = 5; SW = 6; SE = 7

# Used in parsing the initial state and in testing:

INIT_TO_CODE = {'p':2, 'P':3, 'c':4, 'C':5, 'l':6, 'L':7, 'i':8, 'I':9,
  'w':10, 'W':11, 'k':12, 'K':13, 'f':14, 'F':15, '-':0}

# Used in printing out states:

CODE_TO_INIT = {0:'-',2:'p',3:'P',4:'c',5:'C',6:'l',7:'L',8:'i',9:'I',
  10:'w',11:'W',12:'k',13:'K',14:'f',15:'F'}

# Global variables representing the various types of pieces on the board:

EMPTY             = 0

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

# TODO Remove DEBUG_MODE for final product
DEBUG_MODE = False

leaper_move = False

def who(piece): return piece % 2  # BLACK's pieces are even; WHITE's are odd.

def parse(bs): # bs is board string
  '''Translate a board string into the list of lists representation.'''
  b = [[0,0,0,0,0,0,0,0] for r in range(8)]
  rs9 = bs.split("\n")
  rs8 = rs9[1:] # eliminate the empty first item.
  for iy in range(8):
    rss = rs8[iy].split(' ')
    for jx in range(8):
      b[iy][jx] = INIT_TO_CODE[rss[jx]]
  return b

INITIAL = parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P P
F L I W K I L C
''')


def find_frozen_spaces(coords):
    freeze = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            if (x, y) != (0, 0):
                freeze.append((coords[0] + x, coords[1] + y))
    return freeze


class BC_state:
    def __init__(self, old_board=INITIAL, whose_move=WHITE):
        new_board = [r[:] for r in old_board]  # Deeply copy the board.
        self.board = new_board
        self.whose_move = whose_move

        # if old_board == INITIAL:
        self.FROZEN_BLACK = [(0, 5), (1, 6), (1, 7)]
        self.FROZEN_WHITE = [(7, 0), (6, 0), (6, 1)]
        self.FREEZER_FROZEN = [False, False]
        # else:
        #     self.FROZEN_BLACK = []
        #     self.FROZEN_WHITE = []
        #     self.FREEZER_FROZEN = [False, False]
        #     new_board = [r[:] for r in old_board]  # Deeply copy the board.
        #     bi = (-1, -1)
        #     wi = (-1, -1)
        #     for x in range(0, 8):
        #         for y in range(0, 8):
        #             if new_board[x][y] == WHITE_FREEZER:
        #                 self.FROZEN_WHITE = find_frozen_spaces((x, y))
        #             elif new_board[x][y] == BLACK_FREEZER:
        #                 self.FROZEN_WHITE = find_frozen_spaces((x, y))
        #             elif new_board[x][y] == BLACK_IMITATOR:
        #                 bi = (x, y)
        #             elif new_board[x][y] == WHITE_IMITATOR:
        #                 wi = (x, y)
        #
        #     for x in range(-1, 2):
        #         for y in range(-1, 2):
        #             if -1 < wi[0] + x < 8 and -1 < wi[1] + y < 8:
        #                 if new_board[wi[0] + x][wi[1] + y] == BLACK_FREEZER:
        #                     self.FREEZER_FROZEN[BLACK] = True
        #             if -1 < bi[0] + x < 8 and -1 < bi[1] + y < 8:
        #                 if new_board[bi[0] + x][bi[1] + y] == WHITE_FREEZER:
        #                     self.FREEZER_FROZEN[WHITE] = True

    def __repr__(self): # Produce an ASCII display of the state.
        s = ''
        for r in range(8):
            for c in range(8):
                s += CODE_TO_INIT[self.board[r][c]] + " "
            s += "\n"
        if self.whose_move==WHITE: s += "WHITE's move"
        else: s += "BLACK's move"
        s += "\n"
        return s

    def __eq__(self, other):
      if not (type(other)==type(self)): return False
      if self.whose_move != other.whose_move: return False
      try:
        b1 = self.board
        b2 = other.board
        for i in range(8):
          for j in range(8):
            if b1[i][j] != b2[i][j]: return False
        return True
      except Exception as e:
        return False

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

# get all the letter number combinations, one for each space on the board
spaces = [(c, r) for c in [0, 1, 2, 3, 4, 5, 6, 7]
        for r in [7, 6, 5, 4, 3, 2, 1, 0]]

# get every combination of spaces
space_combinations = [(p, q) for p in spaces for q in spaces]

OPERATORS = [Operator((p, q),
                    lambda s, p1=p, q1=q: can_move(s, p1, q1),
                    # The default value construct is needed
                    # here to capture the values of p&q separately
                    # in each iteration of the list comp. iteration.
                    lambda s, p1=p, q1=q: move(s, p1, q1))
           for (p, q) in space_combinations]

def move(state, p1, q1):
    """
    Handle moving a piece, and any relevant captures.
    :param state: Current game state.
    :param p1: Tuple (x, y) starting coordinates of the move.
    :param q1: Tuple (x, y) ending coordinates of the move.
    :return:
    """

    # Create the next state
    copy = BC_state(old_board=state.board, whose_move=state.whose_move)
    copy.FREEZER_FROZEN = state.FREEZER_FROZEN
    copy.FROZEN_WHITE = state.FROZEN_WHITE
    copy.FROZEN_BLACK = state.FROZEN_BLACK

    # Move the piece, and set the space it moved from to empty
    piece = copy.board[p1[0]][p1[1]]
    copy.board[q1[0]][q1[1]] = piece
    copy.board[p1[0]][p1[1]] = EMPTY

    # Handle captures
    if piece == BLACK_PINCER or piece == WHITE_PINCER:
        pincer_capture(copy, q1)
    elif piece == BLACK_WITHDRAWER or piece == WHITE_WITHDRAWER:
        withdrawer_capture(copy, p1, q1)
    elif piece == BLACK_COORDINATOR or piece == WHITE_COORDINATOR:
        coordinator_capture(copy, q1)
    elif piece == BLACK_IMITATOR or piece == WHITE_IMITATOR:
        imitator_capture(copy, p1, q1)
    elif piece == BLACK_FREEZER or piece == WHITE_FREEZER:
        freeze_pieces(copy, q1)
    elif piece == BLACK_LEAPER or piece == WHITE_LEAPER:
        leaper_capture(copy, p1, q1)

    # Handle pincer capture after move
    # if piece != BLACK_PINCER or piece != WHITE_PINCER:
    #     pincer_capture(copy, q1, True)

    if copy.whose_move == WHITE:
        copy.whose_move = BLACK
    else:
        copy.whose_move = WHITE
    return copy

def capture_enemy(state, coords, required_piece=False):
    """
    If an enemy is located at coords, remove it.
    :param state: Current game state.
    :param coords: Tuple (x,y)
    """
    if enemy_on_space(state, coords):
        if required_piece:
            if state.board[coords[0]][coords[1]] == required_piece:
                capture_at(state, coords)
        else:
            capture_at(state, coords)

def piece_on_space(state, coords):
    """
    Checks if a piece is located at coords.
    :param state: Current game state.
    :param coords: Tuple (x,y)
    :return: True if a piece is at coords, False otherwise.
    """
    return space_in_bounds(coords[0], coords[1]) and not check_space_is_empty(state, coords)

def enemy_on_space(state, coords):
    """
    Checks if an enemy piece is located at coords.
    :param state: Current game state.
    :param coords: Tuple (x,y)
    :return: True if an ally piece is at coords, False otherwise.
    """
    return piece_on_space(state, coords) and state.board[coords[0]][coords[1]] % 2 != state.whose_move

def ally_on_space(state, coords):
    """
    Checks if an ally piece is located at coords.
    :param state: Current game state.
    :param coords: Tuple (x,y)
    :return: True if an ally piece is at coords, False otherwise.
    """
    return piece_on_space(state, coords) and state.board[coords[0]][coords[1]] % 2 == state.whose_move

def capture_at(state, coords):
    """
    Captures the enemy at coords.
    :param state: Current game state.
    :param coords: Tuple (x,y)
    """
    if state.board[coords[0]][coords[1]] == BLACK_IMITATOR:
        state.FREEZER_FROZEN[WHITE] = False
    elif state.board[coords[0]][coords[1]] == WHITE_IMITATOR:
        state.FREEZER_FROZEN[BLACK] = False
    elif state.board[coords[0]][coords[1]] == WHITE_FREEZER:
        state.FROZEN_WHITE = []
    elif state.board[coords[0]][coords[1]] == BLACK_FREEZER:
        state.FROZEN_BLACK = []
    state.board[coords[0]][coords[1]] = EMPTY


def imitator_capture(state, start, end):
    """
    Handles checking if a leaper can capture, and then potentially capturing.
    :param state: Current game state.
    :param start: Tuple (x,y), the start coordinates of the move.
    :param end: Tuple (x,y), the end coordinates of the move.
    """

    global leaper_move
    # state_copy = BC_state(state.board, turn)
    if leaper_move:
        leaper_capture(state, start, end, imitate=True)

    # Handle withdrawer capture
    withdrawer_capture(state, start, end, imitate=True)

    # Handle coordinator capture
    coordinator_capture(state, end, imitate=True)

    # Handle pincer capture
    if start[0] == end[0] or start[1] == end[1]:
        pincer_capture(state, end, imitate=True)

    # Handle freezing
    for x in range(-1, 2):
        for y in range(-1, 2):
            freeze_x = end[0] + x
            freeze_y = end[1] + y
            if (x, y) != (0, 0) and space_in_bounds(freeze_x, freeze_y):
                freeze_piece = BLACK_FREEZER
                if state.whose_move == BLACK:
                    freeze_piece = WHITE_FREEZER
                if state.board[freeze_x][freeze_y] == freeze_piece:
                    state.FREEZER_FROZEN[freeze_piece % 2] = True

    # Handle King capture uniquely, as there is no explicit king capture method
    # Check if the move was a single tile
    if math.sqrt(math.pow(abs(start[0] - end[0]), 2) + math.pow(abs(start[1] - end[1]), 2)) < 2:

        # If any of the 8 tiles around the end space are the enemy king, capture it
        for x in range(-1, 1):
            for y in range(-1, 1):
                if space_in_bounds(x, y):
                    king_piece = BLACK_KING
                    if state.whose_move == BLACK:
                        king_piece = WHITE_KING
                    if state.board[x][y] == king_piece:
                        state.board[x][y] = 0


def leaper_capture(state, start, end, imitate=False):
    """
    Handles checking if a leaper can capture, and then potentially capturing.
    :param state: Current game state.
    :param start: Tuple (x,y), the start coordinates of the move.
    :param end: Tuple (x,y), the end coordinates of the move.
    """
    step = define_step(start, end)
    target = (end[0] - step[0], end[1] - step[1])
    if -1 < target[0] and target[0] < 8:
        if -1 < target[1] and target[1] < 8:
            if imitate:
                imitate = BLACK_LEAPER
                if state.whose_move == BLACK:
                    imitate = WHITE_LEAPER
            capture_enemy(state, target, imitate)

def bad_freeze(state, coords, piece):
    if piece != BLACK_FREEZER and piece != WHITE_FREEZER:
        print("Freeze coordinates not centered for", coords)
        print("Actually moving", CODE_TO_INIT[piece])
        print("Actually moving", CODE_TO_INIT[state.board[coords[0]][coords[1]]])
        import sys
        sys.exit()

def freeze_pieces(state, coords):
    """
    Updates the frozen pieces matrix.
    :param state: Current game state.
    :param coords: Tuple (x, y) end coordinates for the freezer move.
    """
    freeze = []
    # bad_freeze(state, coords, state.board[coords[0]][coords[1]])
    for x in range(-1, 2):
        for y in range(-1, 2):
            freeze_space = (coords[0] + x, coords[1] + y)
            if (x, y) != (0, 0):
                freeze.append(freeze_space)
            # else:
            #     bad_freeze(state, coords, state.board[freeze_space[0]][freeze_space[1]])
    if state.whose_move == BLACK:
        state.FROZEN_BLACK = freeze
    else:
        state.FROZEN_WHITE = freeze

def coordinator_capture(state, coords, imitate=False):
    """
    Handles checking if a coordinator can capture, and then potentially capturing.
    :param state: Current game state.
    :param coords: Tuple (x,y), the end coordinates of the move.
    """
    king_space = (-1, -1)
    king_piece = BLACK_KING
    if state.whose_move == WHITE:
        king_piece = WHITE_KING
    for x in range(0, 8):
        for y in range(0, 8):
            if state.board[x][y] == king_piece:
                king_space = (x, y)
                break
    if king_space[0] != -1 and king_space[1] != -1:
        if imitate:
            imitate = WHITE_COORDINATOR
            if state.whose_move == BLACK:
                imitate = BLACK_COORDINATOR
        if state.board[coords[0]][king_space[1]] != EMPTY:
            capture_enemy(state, (coords[0], king_space[1]), imitate)
        if state.board[king_space[0]][coords[1]] != EMPTY:
            capture_enemy(state, (king_space[0], coords[1]), imitate)


def withdrawer_capture(state, start, end, imitate=False):
    """
    Handles checking if a withdrawer can capture, and then potentially capturing.
    :param state: Current game state.
    :param start: Tuple (x,y), the start coordinates of the move.
    :param end: Tuple (x,y), the end coordinates of the move.
    """
    step = define_step(start, end)
    if imitate:
        imitate = BLACK_WITHDRAWER
        if state.whose_move == BLACK:
            imitate = WHITE_WITHDRAWER
    capture_enemy(state, (start[0] - step[0], start[1] - step[1]), imitate)


def at(state, coords):
    return piece_on_space(state, coords) and state.board[coords[0]][coords[1]] % 2 == state.whose_move


# def test(raw):
#     aa = BC.parse(raw)
#     state = BC.BC_state(aa)
#     pincer_capture(state, (2, 5))
#     print(state)

"""
from BaroqueMemes_BC_module_helper import *
raw = '''
c - - w k - l f 
p p - p - p i p 
- P - l - P p - 
- i - P - - - P 
- - - W p I - - 
- - p - - - - - 
P - P - P - P - 
F L I - K - L C'''
start = (3, 2)
end = (3, 1)
state = BC.BC_state(BC.parse(raw))
state.whose_move = BC.BLACK
origin = BC.BC_state(state.board, state.whose_move)
BC.pincer_capture(state, end, True)
"""

def pincer_capture(state, coords, imitate=False):
    """
    Handles checking if a pincer can capture, and then potentially capturing.
    :param state: Current game state.
    :param coords: The end coordinates of the move.
    """
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            if abs(x) != abs(y):
                target_coords = (coords[0] + x, coords[1] + y)
                if target_coords != coords:
                    if enemy_on_space(state, target_coords):
                        ally_coords = (target_coords[0] + x, target_coords[1] + y)
                        if ally_on_space(state, ally_coords):
                            if imitate:
                                piece = BLACK_PINCER
                                ally = WHITE_PINCER
                                if state.whose_move == BLACK:
                                    piece = WHITE_PINCER
                                    ally = BLACK_PINCER
                                if state.board[ally_coords[0]][ally_coords[1]] == ally:
                                    if state.board[target_coords[0]][target_coords[1]] == piece:
                                        capture_at(state, target_coords)
                            else:
                                capture_at(state, target_coords)

def space_in_bounds(x, y):
    """
    Checks if the space represented by (x, y) is on the board.
    :param x: x-coordinate
    :param y: y-coordinate
    :return: True if the space is on the board, False otherwise.
    """
    return -1 < x < 8 and -1 < y < 8


def check_direction(state, start, step_x, end, step_y, team):
    """
    Checks if a piece can move from the space at (start_x, start_y) to (end_x, end_y) in
    moves of (step_x, step_y). Primarily the check is to ensure that no pieces are in the
    way, with the exception of when the Leaper is moving.
    When the Leaper is moving, use in_way and case to allow one piece of the opposing team
    to be in the way (i.e. it is capturing a piece)
    :param state: the current state of the game. Use state.board to get the board.
    :param start: the starting (x, y) coordinates of the piece
    :param step_x: the amount to move in the x-direction each cycle, which should be -1, 0 or 1
    :param end: the ending (x, y) coordinates of the piece
    :param step_y: the amount to move in the y-direction each cycle, which should be -1, 0 or 1
    :param team: the team of the currently moving piece
    :return: True if the movement is valid, False otherwise.
    """

    global DEBUG_MODE, leaper_move

    # Init spaces
    count = (start[0] + step_x, start[1] + step_y)
    start_piece = state.board[start[0]][start[1]]

    # Move through the valid spaces
    while count[0] != end[0] or count[1] != end[1]:

        # If there is a piece at the target space (not the end space)
        if not check_space_is_empty(state, count):

            # If the current move is for a leaper, and the piece it
            if leaper_move:

                # If the space after the piece is not blank, return False
                landing = (count[0] + step_x, count[1] + step_y)
                if landing == end:

                    # If the tile that is being jumped has a piece on the opposing team,
                    tile = state.board[count[0]][count[1]]
                    if tile % 2 != state.whose_move:

                        # Assume the move is of a Leaper (either color)
                        piece = True

                        # If the move is an imitator, check that it is jumping a leaper
                        if start_piece == BLACK_IMITATOR:
                            piece = tile == WHITE_LEAPER
                        elif start_piece == WHITE_IMITATOR:
                            piece = tile == BLACK_LEAPER
                        return piece and check_space_is_empty(state, landing)
            return False

        # Move to next space
        count = (count[0] + step_x, count[1] + step_y)

    # The final space (end[0], end[1]) MUST be empty, except for Kings (which don't use this method).
    return check_space_is_empty(state, end)


def check_space_is_empty(state, space):
    """
    Checks that the tile located at (x, y) is empty.
    :param state: The current state of the game.
    :param space: A tuple of the (x, y) coordinates of the sp[ace
    :return: True if the space is empty, False otheriwise.
    """
    return state.board[space[0]][space[1]] == 0


def define_step(start, end):
    """
    Defines the step size for a piece going from start to end
    :param start: Tuple (x, y) of the starting location.
    :param end: Tuple (x, y) of the ending location.
    :return: Tupel of of: ([1, 0, -1], [1, 0, -1]) depending on if the start value is
    less than, equal to, or greater than the end value.
    """
    if start[0] == end[0]:
        if start[1] < end[1]:
            return (0, 1)
        return (0, -1)
    if start[1] == end[1]:
        if start[0] < end[0]:
            return (1, 0)
        return (-1, 0)
    if abs(start[0] - end[0]) == abs(start[1] - end[1]):
        x = 1
        y = 1
        if start[0] > end[0]:
            x = -1
        if start[1] > end[1]:
            y = -1
        return (x, y)
    return None


def can_move(state, start, end):
    """
    Determines if the piece located at start can move to end in the current state.
    :param state: The current state of the game.
    :param start: The location of the piece at the start. Must have a piece.
    :param end: The location of the piece at the end.
    :return: True if the movement is valid, False otherwise
    """

    # Useful for debugging reasons why moves are not valid
    global DEBUG_MODE

    # Check that the start and end spaces are in bounds, and that they are not the same space
    if not space_in_bounds(start[0], start[1]) or not space_in_bounds(end[0], end[1]) or start == end:
        return False

    # Check that the start space has a piece
    if check_space_is_empty(state, start):
        return False

    # Get the piece to move
    piece = state.board[start[0]][start[1]]

    # Check for correct turn
    if state.whose_move != piece % 2:
        return False

    # Check frozen pieces
    freeze = state.FROZEN_WHITE
    if state.whose_move == WHITE:
        freeze = state.FROZEN_BLACK

    if start in freeze:
        if DEBUG_MODE:
            print("Piece at:", start, "is frozen.")
        return False

    # if piece == BLACK_IMITATOR or piece == WHITE_IMITATOR:
    #     return False

    if piece == BLACK_FREEZER or piece == WHITE_FREEZER:
        if state.FREEZER_FROZEN[state.whose_move]:
            return False

    # Check for king movement
    if piece == WHITE_KING or piece == BLACK_KING:

        # Check that the end space does not have a piece on the same team
        end_value = state.board[end[0]][end[1]]
        if end_value != EMPTY and (end_value % 2 == state.whose_move):
            return False

        # Ensure that the distance between squares is less than 2
        # This is based on the Pythagorean theorem (a^2 + b^2 = c^2) (similar to Manhattan Distance)
        # This restricts the difference of the x/y coordinates to be 1 or 0.
        # As an equation: square_root(|start_x - end_x|^2 + |start_y - end_y|^2) must be less than 2
        # sqrt(2^2, 0) < 2 => 2 < 2, which is false.
        # sqrt(1^2 + 1^2) < 2 => ~1.14 < 2
        # sqrt(1^2 + 0^2) < 1 => 1 < 2
        return math.sqrt(math.pow(abs(start[0] - end[0]), 2) + math.pow(abs(start[1] - end[1]), 2)) < 2
    else:
        # Handle all other pieces

        # Check for pincer movement
        if piece == BLACK_PINCER or piece == WHITE_PINCER:
            if start[0] != end[0] and start[1] != end[1]:
                return False

        # Define the step distance for x and y
        steps = define_step(start, end)
        if steps is None:
            return False

        step_x = steps[0]
        step_y = steps[1]

        # Leaper can have one piece in the way from the opposing team
        global leaper_move, imitator_move
        leaper_move = (piece == WHITE_LEAPER or piece == BLACK_LEAPER or piece == BLACK_IMITATOR or piece == WHITE_IMITATOR)
        team = state.whose_move

        return check_direction(state, start, step_x, end, step_y, team)

def test_starting_board():
  init_state = BC_state(INITIAL, WHITE)
  print(init_state)


if __name__ == "__main__":
  test_starting_board()
