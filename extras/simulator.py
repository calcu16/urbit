#!/usr/bin/env python3
from ast import literal_eval
from re import sub
from sys import stdin,stdout

def parse(line):
  line = line.strip().replace(".","")
  line = sub(r"([a-zA-Z?_][a-zA-Z0-9?_]*)",r"'\1'", line)
  line = sub(r"\s+",",",line)
  try:
    return literal_eval(line)
  except SyntaxError as se:
    if se.args[0] == 'unexpected EOF while parsing':
      return None
    raise

def flatten(nock):
  if type(nock) is list:
    nock = [flatten(item) for item in nock]
    if type(nock[-1]) is list:
      nock = nock[:-1] + nock[-1]
    if len(nock) == 1:
      nock = nock[0]
  return nock

def sell(nock):
  if type(nock) == list:
    return "[%s]" % " ".join(sell(n) for n in nock)
  if type(nock) == tuple:
    try:
      return "%s%s" % tuple(sell(n) for n in nock)
    except TypeError:
      print(nock)
      raise
  return str(nock)

sym = "*/?+=$"

def join(a, *b):
  if type(a) is tuple and len(a) == 1:
    a = a[0]
  if len(b) == 0:
    return a
  else:
    b = join(*b)
    if type(b) not in {list,tuple}: return [a,b]
    elif not len(b): return a
    elif type(b[0]) is str and b[0] in sym: return [a,b]
    else: return [a] + list(b)

def branch(n, l, r, *rs):
  if n < 1:
    raise KeyError
  r = join(r,rs)
  i = 1
  while i <= n:
    i <<= 1
  n -= i >> 1
  b = r if n & i >> 2 else l
  return (n | i >> 2, b)

def equal(a, b):
  if type(a) == list and type(b) == list:
    return len(a) == len(b) and all(equal(ai,bi) for (ai,bi) in zip(a,b))
  elif type(a) == str and type(b) == str:
    return a == b
  elif type(a) == int and type(b) == int:
    return a == b
  elif type(a) == tuple and type(b) == tuple and len(a) == len(b) and all(equal(ai,bi) for (ai,bi) in zip(a,b)):
    return True
  elif type(a) == tuple or type(b) == tuple:
    raise TypeError
  return False

def test(a):
  if a == 0:
    return True
  elif a == 1:
    return False
  else:
    raise TypeError
  

funs = {
  '*' : (lambda a, b, c, *d : join(eval('*',a,b),eval('*',a,c,d)) if type(b) is list else call(b, a, c, *d)),
  '/' : (lambda a, b, *c : join(b,c) if a == 1 else eval('/',*branch(a,b,*c))),
  '?' : (lambda *a : 0 if len(a) != 1 else 1),
  '+' : (lambda a : a + 1),
  '=' : (lambda a, b, *c : 0 if equal(a,join(b,c)) else 1),
  '$' : (lambda a, b, c, *d : b if test(a) else join(c,d)),
  0 : (lambda a, b : eval('/',b,a)),
  1 : (lambda a, b, *c : join(b,c)),
  2 : (lambda a, b, c, *d : eval('*',eval('*',a,b), eval('*',a,c,d))),
  3 : (lambda a, b, *c : eval('?', eval('*',a,b,c))),
  4 : (lambda a, b, *c : eval('+', eval('*',a,b,c))),
  5 : (lambda a, b, *c : eval('=', eval('*',a,b,c))),
  6 : (lambda a, b, c, d, *e : eval('*',a,eval('$',eval('*',a,b),c,d,e))),
  7 : (lambda a, b, c, *d : eval('*',eval('*',a,b),c,d)),
  8 : (lambda a, b, c, *d : eval('*',join(eval('*',a,b),a),c,d)),
  9 : (lambda a, b, c, *d : eval('*',eval('*',a,c,d),eval('/',b,eval('*',a,c,d)))),
}

def call(num, pay, *args):
  try:
    return funs[num](pay, *args)
  except (TypeError,KeyError) as e:
    print(e)
    return ('*', join(pay,num,args))

def eval(*nock):
  global EVAL
  if len(nock) == 1:
    nock = nock[0]
  else:
    nock = (nock[0], join(*nock[1:]))
  if type(nock) != tuple:
    return nock
  return nock
  func, arg = nock
  try:
    if type(arg) in {list,tuple}:
      return funs[func](*arg)
    else:
      return funs[func](arg)
  except (TypeError,KeyError) as e:
    print(e)
    return nock

def uneval(nock):
  if type(nock) is tuple:
    return True
  elif type(nock) is list:
    return any(uneval(item) for item in nock)
  else:
    return False

def step(nock):
  if type(nock) == tuple:
    func, arg = nock
    if uneval(arg):
      return eval(func,step(arg))
    try:
       if type(arg) in {list,tuple}:
         return funs[func](*join(*arg))
       else:
         return funs[func](arg)
    except (TypeError,KeyError) as e:
       return nock
  elif type(nock) == list:
    return list(step(item) for item in nock)
  else:
    return nock

def main():
  stepping = False
  while True:
    try:
      saved = "" 
      print("> *",end="")
      stdout.flush()
      for line in stdin:
        saved += line.strip()
        if saved and saved[0] == ":":
          if saved[1:] == "step":
            stepping = True
          elif saved[1:] == "nostep":
            stepping = False
        else:   
          nock = parse(saved)
          if nock is None:
            saved += line.strip()
            continue
          nock = flatten(nock)
          nock = eval('*',nock)
          prev = ""
          sold = sell(nock)
          while prev != sold:
            if stepping:
              print(sold)
            prev = sold
            nock = step(nock)
            sold = sell(nock)
          if not stepping:
            print(sold)
        saved = ""
        print("> *",end="")
        stdout.flush()
    except SyntaxError as se:
      print("Error: %s" % se.args[0])
    except KeyboardInterrupt:
      print()
    else:
      break

if __name__ == "__main__":
  main()
