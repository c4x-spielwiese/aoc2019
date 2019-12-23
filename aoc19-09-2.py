import sys, math

def intcode(inputStr, extInputs = [], startPointer=0):	
	m = list(map(int, inputStr.split(',')))

	for i in range(0, 1024): # add some memory
		m.append(0)

	i = startPointer
	relBase = 0
	outputs = []
	while True:
		opstr = str(m[i])
		opcode = int(opstr[-2:]) # last two digits
		modeC = int(opstr[-3:-2] or 0) # mode p1
		modeB = int(opstr[-4:-3] or 0) # mode p2
		modeA = int(opstr[-5:-4] or 0) # mode p3
		
		assert (opcode >= 1 and opcode <= 9) or opcode == 99, "unknown opcode=%i" % opcode
		assert (modeA >= 0 and modeA <= 2), "unkown modeA=%i" % modeA
		assert (modeB >= 0 and modeB <= 2), "unkown modeB=%i" % modeB
		assert (modeC >= 0 and modeC <= 2), "unkown modeC=%i" % modeC

		if opcode == 99:
			return outputs
		else:
			p1 = m[i+1] if modeC == 0 else (i+1 if modeC == 1 else relBase + m[i+1])
			p2 = m[i+2] if modeB == 0 else (i+2 if modeB == 1 else relBase + m[i+2])
			p3 = m[i+3] if modeA == 0 else (i+3 if modeA == 1 else relBase + m[i+3])

			if(opcode == 1):								# add p1 and p2 store in p3
				m[p3] = m[p1] + m[p2]
				i += 4
			elif(opcode == 2):								# mul p1 and p2 store in p3
				m[p3] = m[p1] * m[p2]
				i += 4
			elif(opcode == 3):								# input            
				if len(extInputs) > 0:
					v = extInputs.pop(0)
					m[p1] = v
					i += 2
				else:				
					raise Exception("no input on stack")
			elif(opcode == 4):								# output
				outputs.append(m[p1])
				i += 2
			elif(opcode == 5):								# jump-if-true				
				if m[p1] != 0:
					i = m[p2]				
				else:					
					i += 3
			elif(opcode == 6):								# jump-if-false
				if m[p1] == 0:
					i = m[p2]				
				else:
					i += 3					
			elif(opcode == 7):								# less-than
				m[p3] = 1 if m[p1] < m[p2] else 0
				i += 4
			elif(opcode == 8):								# equals
				m[p3] = 1 if m[p1] == m[p2] else 0
				i += 4				
			elif(opcode == 9):								# set relBase
				relBase += m[p1]
				i += 2			
			else:
				raise Exception('opcode error i=', i, 'm[i]=', m[i]) 


if len(sys.argv) > 1 and sys.argv[1] == "test":
	print("test mode:")
	tests = [
				# "output whatever is input", "3,0,4,0,99", [23], [23],
				# "just halt", "1101,100,-1,4,0", [], [],
                # "eq 8 (pm)?", "3,9,8,9,10,9,4,9,99,-1,8", [8], [1],
				# "eq 8 (pm)?", "3,9,8,9,10,9,4,9,99,-1,8", [7], [0],
                # "lt 8 (pm)?", "3,9,7,9,10,9,4,9,99,-1,8", [7], [1],
				# "lt 8 (pm)?", "3,9,7,9,10,9,4,9,99,-1,8", [8], [0],
                # "eq 8 (im)?", "3,3,1108,-1,8,3,4,3,99", [8], [1],
				# "eq 8 (im)?", "3,3,1108,-1,8,3,4,3,99", [7], [0],
                # "lt 8 (im)?", "3,3,1107,-1,8,3,4,3,99", [7], [1],
				# "lt 8 (im)?", "3,3,1107,-1,8,3,4,3,99", [8], [0],
                # "non-zero?", "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [1], [1],
				# "non-zero?", "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [0], [0],
                # "non-zero?", "3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [1], [1],
				# "non-zero?", "3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [0], [0],
                # "lt(999), eq(1000), gt(1001) 8?", "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", [7], [999],
				# "lt(999), eq(1000), gt(1001) 8?", "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", [8], [1000],
				# "lt(999), eq(1000), gt(1001) 8?", "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99", [9], [1001],
				"output self", "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99", [], [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99],
				"output 16-digit", "1102,34915192,34915192,7,4,7,99,0", [], [1219070632396864],
				"long int", "104,1125899906842624,99", [], [1125899906842624] 
			]
	i = 0
	while i < len(tests):
		print("runtest: ", tests[i])
		res = intcode(tests[i+1], tests[i+2])
		resStr = ','.join(str(x) for x in res)
		tstStr = ','.join(str(x) for x in tests[i+3])
		print("OK" if resStr == tstStr  else "ERR", "out=", resStr)
		i += 4

if len(sys.argv) == 1:
	with open(__file__.replace('.py', '.input.txt'), 'r') as f:
		lines = f.readlines()
		res = intcode(lines[0], [2])
		print(res)