from hak.string.print_and_return_false import f as pf

f = lambda obj, keys: {k: obj[k] for k in [k for k in keys if k in obj]}

def t():
  x = {
    'obj': {'a': 'AAA', 'b': 'BBB', 'c': "CCC", 'd': "DDD"},
    'keys': ['a', 'c', 'e']
  }
  y = {'a': 'AAA', 'c': "CCC"}
  z = f(**x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])
