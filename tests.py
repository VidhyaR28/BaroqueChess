from BC_state_etc import *
from Brew_BC_Player import *



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
