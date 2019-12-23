import string, sys, math

def intcode(inputStr, extInputs = [], startPointer=0):	
	m = list(map(int, inputStr.split(',')))

	i = startPointer
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

		outputs = []

		if opcode == 99:
			return {'code': 0, 'val': m[0], 'pointer': i, 'intcode': ','.join(str(x) for x in m)}
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
				if len(extInputs) > 0:
					v = extInputs.pop(0)
					m[m[i+1]] = v
					i += 2
				else:				
					return {'code': 1, 'pointer': i, 'intcode': ','.join(str(x) for x in m)}				
			elif(opcode == 4):								# output
				p1 = m[m[i+1]] if modeC == 0 else m[i+1]				
				i += 2
				return {'code': 2, 'val': p1, 'pointer': i, 'intcode': ','.join(str(x) for x in m)}								
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

def recAmpController(intCode, phaseSeq):
	limit = 100
	limitC = 0

	amps = [
		{'intcode': intCode, 'pointer': -1, 'initialCall': True},
		{'intcode': intCode, 'pointer': -1, 'initialCall': True},
		{'intcode': intCode, 'pointer': -1, 'initialCall': True},
		{'intcode': intCode, 'pointer': -1, 'initialCall': True},
		{'intcode': intCode, 'pointer': -1, 'initialCall': True}
	]

	def callAmp(ampNo, val):		
		if amps[ampNo]['pointer'] == -1:					# first call, hand in the phaseSeq
			inpData = [phaseSeq[ampNo], val]
			amps[ampNo]['pointer'] = 0
		else:			
			inpData = [val]

		amps[ampNo] = intcode(amps[ampNo]['intcode'], inpData, amps[ampNo]['pointer'])
		if amps[ampNo]['code'] == 2:
			callAmp((ampNo + 1) % 5, amps[ampNo]['val'])
		elif amps[ampNo]['code'] == 1:
			print("halted ampNo=", ampNo)
	
	callAmp(0, 0)
	return amps[4]['val']

# def ampController(intCode, phaseSeq): #TODO: fixme :) 
# 	prevVal = 0
# 	returnCode = 1
# 	limit = 100
# 	c = 0
# 	amps = []
# 	while returnCode == 1 and c < limit:			
# 		i = c % 5
# 		print("# startIntCode # i=", i)
# 		if len(amps) <= i:
# 			print("vorheri", intCode)
# 			amps.append(intcode(intCode, [phaseSeq[i], 0], 0)) # init
# 			print("nachher: ", amps[i])
# 		else:
# 			print("vorhere", amps[i]['intcode'])
# 			amps[i] = intcode(amps[i]['intcode'], [prevVal], amps[i]['pointer'])
# 			print("nachher: ", amps[i])
# 		print("code=", amps[i]['code'], ", prevVal=", amps[i]['val'], "-- i=", i, "-- phase=", phaseSeq[i], ", c=", c)
# 		if amps[i]['code'] == 0: # wait till one returns w/ 99
# 			return amps[i]['val'] 
# 		else:
# 			prevVal = amps[i]['val'] # carry over result
# 		c += 1		
# 	raise Exception('program not ended properly')

def findMaxAmp(intCode, feedbackLoopMode = False):
	results = []
	phaseSeq = [0, 0, 0, 0, 0]
	start = 0 if feedbackLoopMode == False else 5
	end = 5 if feedbackLoopMode == False else 10

	for a in range(start, end):
		for b in range(start, end):
			for c in range(start, end):
				for d in range(start, end):
					for e in range(start, end):
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

						res = recAmpController(intCode, phaseSeq)
						print("test %s  --> %d" % (phaseSeq, res))
						results.append(res)
	return max(results)




if len(sys.argv) > 1 and sys.argv[1] == "test":
	print("test mode:")
	tests = [
				#"3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5", "9,8,7,6,5", 139629729,
				"3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10", "9,7,8,5,6", 18216
			]
	i = 0
	while i < len(tests):
		print("test: %s phaseSeq=%s" % (tests[i], tests[i+1]))
		#res = ampController(tests[i], list(map(int, tests[i+1].split(','))))
		res = recAmpController(tests[i], list(map(int, tests[i+1].split(','))))
		maxSignal = findMaxAmp(tests[i], True)
		print("%d == %d == %d -> %s" % (tests[i+2], res, maxSignal, "OK" if res == tests[i+2] and res == maxSignal else "ERR!"))

		#print("res2 = ", ampController(tests[i], [0,0,0,0,0]))

		i += 3

if len(sys.argv) == 1:
	with open(__file__.replace('.py', '.input.txt'), 'r') as f:
		lines = f.readlines()
		print("result= ", findMaxAmp(lines[0], True))