import string, sys, math

s = 372037
e = 905157

def valid(x):
    sX = str(x)
    if sX[0] != sX[1] and sX[1] != sX[2] and sX[2] != sX[3] and sX[3] != sX[4] and sX[4] != sX[5]:
       return False
    min = 0
    for i in range(0, 6):
        t = int(sX[i])
        if t > min:
            min = t
        if t < min:
            return False
    return True

c = 0
for x in range(s, e + 1):
    if valid(x):
        c += 1

print(c)