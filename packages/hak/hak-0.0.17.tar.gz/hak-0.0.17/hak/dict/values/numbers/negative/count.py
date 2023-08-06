from hak.string.print_and_return_false import f as pf
from hak.bools.count_true import f as count_true

# negatives
f = lambda x: count_true([_ < 0 for _ in [x[k] for k in x]]) if x else 0

def t():
  x = {'a': 1, 'b': 0, 'c': -1, 'd': 2, 'e': -2, 'f': -3}
  y = 3
  z = f(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])
