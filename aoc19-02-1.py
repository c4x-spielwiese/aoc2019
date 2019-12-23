import string, sys, math


def intcode(input):	
	m = list(map(int, input.split(',')))
	i = 0
	while True:
		if m[i] == 99:
			return ','.join(map(str, m))
		else:
			if(m[i] == 1):
				m[m[i+3]] = m[m[i+1]] + m[m[i+2]]
			elif(m[i] == 2):				
				m[m[i+3]] = m[m[i+1]] * m[m[i+2]]
			else: 
				print("ERR!")
		i += 4
			


if len(sys.argv) > 1 and sys.argv[1] == "test":
	print("test mode:")
	tests = [
				"1,0,0,0,99", "2,0,0,0,99",
				"2,3,0,3,99", "2,3,0,6,99",
				"2,4,4,5,99,0", "2,4,4,5,99,9801",
				"1,1,1,4,99,5,6,0,99", "30,1,1,4,2,5,6,0,99"				
			]
	i = 0
	while i < len(tests):
		res = intcode(tests[i])
		print("%s => %s ?? %s || %s" % (tests[i], tests[i+1], res, "OK" if res == tests[i+1] else "ERR!"))
		i += 2

		
else:
	with open(__file__.replace('.py', '.input.txt'), 'r') as f:
		input = f.readlines()
		print(intcode(input[0]))