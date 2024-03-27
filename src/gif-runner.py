#!/bin/python3

import time,struct
#INJECT
b=[]
for c in a:
 d = []
 for e in c[1]:
  f = ""
  e = [e[g:g+4] for g in range(0,len(e),4)]
  for h in e:
   *j, k = struct.unpack("BBBc", h)
   f += "\x1b[38;2;%i;%i;%im%s\x1b[0m" % (*j, k.decode())
  d.append(f)
 d = "\n".join(d)
 b.append([c[0], "\x1B[2J\x1B[H"+d])
del a,c,e
while True:
 for i in b:
  print(i[1])
  time.sleep(i[0])
