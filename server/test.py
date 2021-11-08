a = 5
def incr():
  global a
  print(a+1)
  a = a+5

incr()
print(a)