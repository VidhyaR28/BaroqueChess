from BC_state_etc import *
from DilutedCoffee_BC_Player import *



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
new = BC_state(i)

k = staticEval(new)
print(k)