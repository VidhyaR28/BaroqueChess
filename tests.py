from BC_state_etc import *
from Brew_BC_Player import *
import numpy
import random

i = parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P P
F L I W K I L C
''')

# i = parse('''
# - - - k - - - -
# - - - - - - - -
# - - - - - p - -
# - - - - - - - -
# - - - - - - - -
# - - - - - L - -
# - - - - - - - -
# - - - K - - - -
# ''')

new = BC_state(i)



k = staticEval(new)
print(k)


def Zobrist():
    # We need to loop through every item on board, give every piece a randomly generated value,
    # XOR stuff? and then, get a "has" . This hash should point to a dictionary, K (Zob hash) -> Value (tuple of data)
    # UPDATE MINIMAX WITH ZOBRIST STUFF
    # ZOBTAB = [[0 for i in range(0, 65)] for j in range(2, 16)]
    ZOBTAB = numpy.zeros((65, 13))
    # ZOBTAB = numpy.zeros((2, 13))
    # matrix = [[0] * 5 for i in range(5)]
    # print(matrix)
    print(ZOBTAB)
    # init = [[4, 6, 8, 10, 12, 8, 6, 14], [2, 2, 2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 3, 3, 3, 3, 3], [15, 7, 9, 11, 13, 9, 7, 5]]
    for i in range (0, 65):
        print("I ", i)
        for j in range (0, 13):
            # insert a random value
            ZOBTAB[i][j] = random.getrandbits(24)
    return


Zobrist()