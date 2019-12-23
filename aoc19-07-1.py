import string, sys, math

def intcode(inputStr, extInputs = []):	
	m = list(map(int, inputStr.split(',')))

	i = 0
	while True:
		opstr = str(m[i])
		opcode = int(opstr[-2:]) # last two digits
		modeC = int(opstr[-3:-2] or 0) # mode p1
		modeB = int(opstr[-4:-3] or 0) # mode p2
		modeA = int(opstr[-5:-4] or 0) # mode p3
		
		assert (opcode >= 1 and opcode <= 8) or opcode == 99, "unknown opcode=%i" % opcode
		assert (modeA >= 0 and modeA <= 1), "unkown modeA=%i" % modeA
		assert (modeB >= 0 and modeB <= 1), "unkown modeB=%i" % modeB
		assert (modeC >= 0 and modeC <= 1), "unkown modeC=%i" % modeC

		if opcode == 99:
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
				v = extInputs.pop(0) if len(extInputs) > 0 else int(input('< '))
				m[m[i+1]] = v
				i += 2
			elif(opcode == 4):								# output
				p1 = m[m[i+1]] if modeC == 0 else m[i+1]
				return p1
				i += 2
			elif(opcode == 5):								# jump-if-true
				p1 = m[m[i+1]] if modeC == 0 else m[i+1]
				p2 = m[m[i+2]] if modeB == 0 else m[i+2]
				if p1 != 0:
					i = p2				
				else:
					i += 3
			elif(opcode == 6):								# jump-if-false
				p1 = m[m[i+1]] if modeC == 0 else m[i+1]
				p2 = m[m[i+2]] if modeB == 0 else m[i+2]
				if p1 == 0:
					i = p2				
				else:
					i += 3					
			elif(opcode == 7):								# less-than
				p1 = m[m[i+1]] if modeC == 0 else m[i+1]
				p2 = m[m[i+2]] if modeB == 0 else m[i+2]
				m[m[i+3]] = 1 if p1 < p2 else 0
				i += 4
			elif(opcode == 8):								# equals
				p1 = m[m[i+1]] if modeC == 0 else m[i+1]
				p2 = m[m[i+2]] if modeB == 0 else m[i+2]
				m[m[i+3]] = 1 if p1 == p2 else 0
				i += 4				
			else: 
				print("ERR! [%i]" % m[i])	

def ampController(intCode, phaseSeq):
	r = 0
	for i in range(0, 5):	
		r = intcode(intCode, [phaseSeq[i], r])
	return r

def findMaxAmp(intCode):
	results = []
	phaseSeq = [0, 0, 0, 0, 0]
    
	for a in range(0, 5):
		for b in range(0, 5):
			for c in range(0, 5):
				for d in range(0, 5):
					for e in range(0, 5):
						if a == b or a == c or a == d or a == e or \
						   b == c or b == d or b == e or \
						   c == d or c == e or \
						   d == e:
							continue
						phaseSeq[0] = a
						phaseSeq[1] = b
						phaseSeq[2] = c
						phaseSeq[3] = d
						phaseSeq[4] = e

						res = ampController(intCode, phaseSeq)
						print("test %s  --> %d" % (phaseSeq, res))
						results.append(res)
	return max(results)




if len(sys.argv) > 1 and sys.argv[1] == "test":
	print("test mode:")
	tests = [
				"3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0", "4,3,2,1,0", 43210,
				#"3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0", "0,1,2,3,4", 54321, 
				#"3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0", "1,0,4,3,2", 65210, 
			]
	i = 0
	while i < len(tests):
		print("test: %s phaseSeq=%s" % (tests[i], tests[i+1]))
		res = ampController(tests[i], list(map(int, tests[i+1].split(','))))
		maxSignal = findMaxAmp(tests[i])
		print("%d == %d == %d -> %s" % (tests[i+2], res, maxSignal, "OK" if res == tests[i+2] and res == maxSignal else "ERR!"))

		#print("res2 = ", ampController(tests[i], [0,0,0,0,0]))

		i += 3

if len(sys.argv) == 1:
	with open(__file__.replace('.py', '.input.txt'), 'r') as f:
		lines = f.readlines()
		print("result= ", findMaxAmp(lines[0]))
	