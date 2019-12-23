import string, sys, math

def calcFuel(mass):
	fuel = math.floor(mass / 3) - 2
	if fuel > 0:
		return fuel
	else:
		return 0


with open(__file__.replace('.py', '.input.txt'), 'r') as f:
	input = f.readlines()

print("calc total fuell\n")

sum = 0
for line in input:
	#print("%i => %i" % (int(line), calcFuel(int(line))))
	f = int(line)
	while (f > 0):
		x = calcFuel(f)
		sum += x
		f = x
		
print("sum: %i" % sum)