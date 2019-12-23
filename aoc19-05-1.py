import string, sys, math

def intcode(inputStr):	
	m = list(map(int, inputStr.split(',')))

	i = 0
	while True:
		opstr = str(m[i])
		
		opcode = int(opstr[-2:]) # last two digits
		
		modeC = int(opstr[-3:-2] or 0) # mode p1
		modeB = int(opstr[-4:-3] or 0) # mode p2
		modeA = int(opstr[-5:-4] or 0) # mode p3
		
		assert (opcode >= 1 and opcode <= 4) or opcode == 99, "unknown opcode=%i" % opcode
		assert (modeA >= 0 and modeA <= 1), "unkown modeA=%i" % modeA
		assert (modeB >= 0 and modeB <= 1), "unkown modeB=%i" % modeB
		assert (modeC >= 0 and modeC <= 1), "unkown modeC=%i" % modeC

		if opcode == 99:
			print("stop --> ", m)
			return m[0]
		else:
			if(opcode == 1):								# add p1 and p2 store in p3
				p1 = m[m[i+1]] if modeC == 0 else m[i+1]
				p2 = m[m[i+2]] if modeB == 0 else m[i+2]
				m[m[i+3]] = p1 + p2
				i += 4
			elif(opcode == 2):								# mul p1 and p2 store in p3
				p1 = m[m[i+1]] if modeC == 0 else m[i+1]
				p2 = m[m[i+2]] if modeB == 0 else m[i+2]
				m[m[i+3]] = p1 * p2
				i += 4
			elif(opcode == 3):								# input
				m[m[i+1]] = int(input('< '))
				i += 2
			elif(opcode == 4):								# output
				print('>', m[m[i+1]])
				i += 2
			else: 
				print("ERR! [%i]" % m[i])	


if len(sys.argv) > 1 and sys.argv[1] == "test":
	print("test mode:")
	tests = [
				#"3,0,4,0,99",
				"1101,100,-1,4,0"
			]
	i = 0
	while i < len(tests):
		print("test: ", tests[i])
		res = intcode(tests[i])
		#print("%s => %s ?? %s || %s" % (tests[i], tests[i+1], res, "OK" if res == tests[i+1] else "ERR!"))
		i += 1

if len(sys.argv) == 1:
	with open(__file__.replace('.py', '.input.txt'), 'r') as f:
		lines = f.readlines()
		print("result= ", intcode(lines[0]))
	