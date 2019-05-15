'''PlayerSkeletonA.py

A Baroque Chess Agent by Lexi Loessberg-Zahl and Bryden Robertson.

'''

import BC_state_etc as BC
import BaroqueMemes_BC_module_helper
import time, math, random

# if True:
#     from selenium import webdriver
#     import TestMoves as TM
#     global driver
#     driver = webdriver.Chrome("./chromedriver-Darwin")
#     driver.get("http://xanthippe.cs.washington.edu/bc/BC-GUI-for-move-validation.html")

run_webdriver = False

STATES_EXPANDED = 0
NUM_EVALS = 0
NUM_CUTOFFS = 0
BEST_MOVE = None
BEST_STATE = None
END_TIME = None

# def validate_moves(old_state, new_state, move_from):
#     global driver
#     start_box = driver.find_element_by_id("start_entry")
#     end_box = driver.find_element_by_id("end_entry")
#     start_square = driver.find_element_by_id("start_square")
#     start_box.clear()
#     start_box.send_keys(TM.board_to_string(old_state.board))
#     end_box.clear()
#     end_box.send_keys(TM.board_to_string(new_state.board))
#     start_square.clear()
#     coords = move_from.name
#     base = ord('a')
#     letter = chr(base + coords[0])
#     start_square.send_keys(letter + str(coords[1]))
#     driver.find_element_by_id("validate").click()
#     response = driver.find_element_by_id("validation_result").text
#     if 'False' in response:
#         return False
#     return True


def parameterized_minimax(currentState, alphaBeta=False, ply=3,\
    useBasicStaticEval=True, useZobristHashing=False):
  '''Implement this testing function for your agent's basic
  capabilities here.'''

  # set up values to be returned later
  global STATES_EXPANDED 
  STATES_EXPANDED = 0
  global NUM_EVALS
  NUM_EVALS = 0
  global NUM_CUTOFFS
  NUM_CUTOFFS = 0
  eval_fn = basicStaticEval
  if not useBasicStaticEval: eval_fn = staticEval
  
  # run minimax
  alpha = -1 * math.inf
  beta = math.inf
  value = recursive_minimax(currentState, ply, ply, eval_fn, alphaBeta, alpha, beta) 
  return {'CURRENT_STATE_STATIC_VAL': value, 'N_STATES_EXPANDED': STATES_EXPANDED,
          'N_STATIC_EVALS': NUM_EVALS, 'N_CUTOFFS': NUM_CUTOFFS}


def recursive_minimax(state, plyLeft, initial_ply, eval_fn, alphabeta, alpha, beta, timed=False):
  '''Returns the minimax value associated with state and updates BEST_MOVE and
  its associated BEST_STATE on the highest level of the traversal

  state: current state
  plyLeft: how many more levels to be expanded
  initial_ply: highest level (where we are choosing the move)
  eval_fn: static eval function being used
  alphabeta: if True, implements alpha beta pruning
  alpha: current alpha value
  beta: current beta value
  timed: True if the current search is timed'''
  #print("RUNNING RECURSIVE MINIMAX, plyLeft:", plyLeft)
  global STATES_EXPANDED
  global NUM_EVALS
  global NUM_CUTOFFS
  global BEST_MOVE
  global BEST_STATE
  global END_TIME

  # Base case:
  if plyLeft == 0: 
    NUM_EVALS += 1
    # return the static state eval value
    score = eval_fn(state)
    # print('Base case value:', score)
    return score
  
  # Recursive case:
  # print('Reached recursive case, ply left =', plyLeft)
  provisional = math.inf # positive infinity
  if state.whose_move == BC.WHITE:
      provisional = -1 * math.inf # negative infinity

  # Expand the state: try all operators
  STATES_EXPANDED += 1
  op_count = 0
  # used_op = -1
  for op in BC.OPERATORS:
    # Check the time and stop if necessary
    if timed and END_TIME - time.time() < 0.08:
      return
    # For valid operators, recurse to find the minimax value for this node
    if op.precond(state):
      # print('Move', str(op.name), 'is good')
      new_state = op.state_transf(state)

      if BEST_MOVE is None:
        # print("UPDATING BEST STATE BY DEFAULT")
        BEST_MOVE = op 
        BEST_STATE = new_state
      newVal = recursive_minimax(new_state, plyLeft-1, initial_ply, eval_fn, alphabeta, alpha, beta, timed)
      # newVal is only None if we are running out of time, so just return
      if newVal is None:
        return
      # If the value returned is better than the current value, replace
      if ((state.whose_move == BC.WHITE and newVal > provisional)
          or (state.whose_move == BC.BLACK and newVal < provisional)):
        provisional = newVal
        # Update the appropriate alpha/beta value if necessary
        if state.whose_move == BC.BLACK and provisional < beta:
          beta = newVal
        elif state.whose_move == BC.WHITE and provisional > alpha: 
          alpha = newVal
        # update globals - only update on the highest level of tree
        if plyLeft == initial_ply:
          # print("UPDATING BEST STATE")
          BEST_MOVE = op
          # used_op = op_count
          BEST_STATE = new_state
    op_count += 1
    # If we have reached a cutoff, do not explore any more successors
    if alphabeta and alpha >= beta: 
      # print('Alpha beta cutoff reached')
      NUM_CUTOFFS += 1
      break
  #print("Used operator at:", used_op)
  return provisional

def makeMove(currentState, currentRemark, timelimit=10):
    # Compute the new state for a move.
    # You should implement an anytime algorithm based on IDDFS.

    move = None
    global BEST_MOVE
    global BEST_STATE
    global END_TIME
    # reset globals
    BEST_MOVE = None
    BEST_STATE = None
    # IDDFS
    ply = 1
    
    END_TIME = time.time() + timelimit
    # prev_state = BEST_STATE
    # curr_state = BEST_STATE
    # prev_best = BEST_MOVE
    # curr_best = BEST_MOVE

    while END_TIME - time.time() > 0.08:
      # prev_best = curr_best
      # no relevant returns - updates the global variables BEST_STATE and BEST_MOVE
      val = recursive_minimax(currentState, ply, ply, staticEval, True, -1 * math.inf, math.inf, True)
      #print('Searched (at least partially) to depth', ply)
      # if ply > 1 and val is None:
      #   curr_best = prev_best
      #   curr_state = prev_state
      # else:
      #   curr_best = BEST_MOVE
      #   curr_state = BEST_STATE
      ply += 1


    newState = BEST_STATE
    move = BEST_MOVE

    print("Move from", move.name)


    # global run_webdriver
    # if run_webdriver:
    #     if not validate_moves(currentState, newState, move):
    #         print("Move is not valid")

    # Make up a new remark
    old_score = basicStaticEval(currentState)
    new_score = basicStaticEval(newState)
    if (currentState.whose_move == BC.WHITE and new_score > old_score) or \
       (currentState.whose_move == BC.BLACK and new_score < old_score):
        # when a piece was captured
        choose = random.randint(0, len(CAPTURE_REMARKS)-1)
        newRemark = CAPTURE_REMARKS[choose]
    else:
        # when a piece wasn't captured
        choose = random.randint(0, len(NEUTRAL_REMARKS)-1)
        newRemark = NEUTRAL_REMARKS[choose]

    #move.name = ((move.name[0][0] - 1, move.name[0][1]), move.name[1])
    #result = [[move.name, newState], newRemark]
    #print('Returning =', str(result))
    return [[move.name, newState], newRemark]

def nickname():
    return "BaroqueMemes"

def introduce():
    return '''I'm BaroqueMemes, a Baroque Chess player created by Bryden 
              Robertson and Lexi Loessberg-Zahl. All my remarks are sourced 
              from memes or Baroque related puns. 
              
              If it ain't Baroque, don't fix it!'''

P2_NAME = None
CAPTURE_REMARKS = []
NEUTRAL_REMARKS = []

def prepare(player2Nickname):
    ''' Here the game master will give your agent the nickname of
    the opponent agent, in case your agent can use it in some of
    the dialog responses.  Other than that, this function can be
    used for initializing data structures, if needed.'''
    global P2_NAME
    global NEUTRAL_REMARKS
    global CAPTURE_REMARKS

    # set the name of the opponent
    P2_NAME = player2Nickname

    NEUTRAL_REMARKS = ['Outstanding move.',
                    'This is fine.',
                    'You just can\'t Handel it.',
                    'Too hot to Handel.',
                    'If this were a betting game, you\'d be Baroque.',
                    'While you were partying, I studied Baroque Chess.']

    CAPTURE_REMARKS = ['I have the high ground, ' + P2_NAME, 
                   'Congratulations, you played yourself.',
                   'One does not simply beat the Meme-bot.',
                   'That\'s a strike Bach.',
                   '*Sips tea*']


def basicStaticEval(state):
    '''Use the simple method for state evaluation described in the spec.
    This is typically used in parameterized_minimax calls to verify
    that minimax and alpha-beta pruning work correctly.'''
    score = 0
    for r in range(8):
      for c in range(8):
        
        curr_piece = state.board[r][c]
        if curr_piece == BC.WHITE_KING:
          # print('Found white king')
          score += 100
        elif curr_piece == BC.BLACK_KING:
          # print('Found black king')
          score -= 100
        elif curr_piece == BC.WHITE_PINCER:
          # print('Found white pincer')
          score += 1
        elif curr_piece == BC.BLACK_PINCER:
          # print('Found black pincer')
          score -= 1
        elif curr_piece % 2 == 1:
          # print('Found white piece (not king or pincer)')
          score += 2
        elif curr_piece != 0:
          # print('Found black piece (not king or pincer)')
          score -= 2
    return score
          
         
def staticEval(state):
    '''Compute a more thorough static evaluation of the given state.
    This is intended for normal competitive play.  How you design this
    function could have a significant impact on your player's ability
    to win games.'''
    score = 0
    other_team = BC.BLACK
    if state.whose_move == BC.BLACK:
      other_team = BC.WHITE
    other_state = BC.BC_state(state.board, other_team)
    for r in range(8):
      for c in range(8):
        my_moves = len(BaroqueMemes_BC_module_helper.find_valid_moves_by_coord(state, (r,c)))
        other_moves = len(BaroqueMemes_BC_module_helper.find_valid_moves_by_coord(other_state, (r,c)))
        
        #print('Moves:', my_moves)
        curr_piece = state.board[r][c]
        if curr_piece%2 == BC.WHITE:
          if curr_piece == BC.WHITE_PINCER:
            score += my_moves//2
            score += other_moves//2
          else:
            score += my_moves
            score += other_moves
        else:
          if curr_piece == BC.BLACK_PINCER:
            score -= my_moves//2
            score -= other_moves//2
          else:
            score -= my_moves
            score -= other_moves

        if curr_piece == BC.WHITE_KING:
          #print('Found white king')
          score += 100
        elif curr_piece == BC.BLACK_KING:
          #print('Found black king')
          score -= 100
        elif curr_piece == BC.WHITE_PINCER:
          #print('Found white pincer')
          score += 1
        elif curr_piece == BC.BLACK_PINCER:
          #print('Found black pincer')
          score -= 1
        elif curr_piece % 2 == 1:
          #print('Found white piece (not king or pincer)')
          score += 2
        elif curr_piece != 0:
          #print('Found black piece (not king or pincer)')
          score -= 2
    return score
    
    #IDEAS:
    #   incorporate basic static eval, which already takes captures into account
    #   something based on how many turns there have been?
    #   can something be captured in the next turn?
    #   are certain positions bad/good for particular pieces?
    #   
    #   if we keep track of where each of our pieces are, 
    #   we can determine if certain pieces are in danger/in advantageous positions
    #
    #   maybe just check if anything can capture the king on the next turn