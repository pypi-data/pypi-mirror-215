from hak.string.print_and_return_false import f as pf

f = lambda x: int(x/abs(x) if x else 0)

def t_negative():
  x = -123
  y = -1
  z = f(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])

def t_zero():
  x = 0
  y = 0
  z = f(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])

def t_positive():
  x = 123
  y = 1
  z = f(x)
  return y == z or pf([f'x: {x}', f'y: {y}', f'z: {z}'])

def t():
  if not t_negative(): return pf('!t_negative')
  if not t_zero(): return pf('!t_zero')
  if not t_positive(): return pf('!t_positive')
  return True
