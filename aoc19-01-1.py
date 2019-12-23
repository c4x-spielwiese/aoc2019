import string, sys, math

def calcFuel(mass):
    return math.floor(mass / 3) - 2


with open(__file__.replace('.py', '.input.txt'), 'r') as f:
    input = f.readlines()

print("calc Mass\n")

sum = 0
for line in input:
    print("%i => %i" % (int(line), calcFuel(int(line))))
    sum += calcFuel(int(line))
print("sum: %i" % sum)


