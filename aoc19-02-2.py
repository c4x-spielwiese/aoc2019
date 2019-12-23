import string, sys, math

def findIntcode(input, search):
	m = list(map(int, input.split(',')))
	
	for noun in range(0, 100):
		for verb in range(0, 100):
			m2 = m.copy()
			m2[1] = noun
			m2[2] = verb
			result = intcode(m2)
			if result == search:
				print("found! noun=%i verb=%i = %i" % (noun, verb, result))
				return
			else:
				print(":-( noun=%i verb=%i = %i" % (noun, verb, result))


def intcode(m):	
	print(m)
	#m = list(map(int, input.split(',')))
	try:
		i = 0
		while True:
			if m[i] == 99:
				#return ','.join(map(str, m))
				return m[0]
			else:
				if(m[i] == 1):
					m[m[i+3]] = m[m[i+1]] + m[m[i+2]]
				elif(m[i] == 2):				
					m[m[i+3]] = m[m[i+1]] * m[m[i+2]]
				else: 
					print("ERR!")
			i += 4			
	except:
		return -1


if len(sys.argv) > 1 and sys.argv[1] == "test":
	print("test mode:")
	#tests = [
	#			"1,0,0,0,99", "2,0,0,0,99",
	#			"2,3,0,3,99", "2,3,0,6,99",
	#			"2,4,4,5,99,0", "2,4,4,5,99,9801",
	#			"1,1,1,4,99,5,6,0,99", "30,1,1,4,2,5,6,0,99"				
	#		]
	#i = 0
	#while i < len(tests):
	#	res = intcode(tests[i])
	#	print("%s => %s ?? %s || %s" % (tests[i], tests[i+1], res, "OK" if res == tests[i+1] else "ERR!"))
	#	i += 2

if len(sys.argv) > 1:
	print("find %s:" % sys.argv[1])
	with open(__file__.replace('.py', '.input.txt'), 'r') as f:
		input = f.readlines()
		findIntcode(input[0], int(sys.argv[1]))
	