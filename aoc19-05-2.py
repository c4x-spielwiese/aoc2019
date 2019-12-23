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
				m[m[i+1]] = int(input('< '))
				i += 2
			elif(opcode == 4):								# output
				p1 = m[m[i+1]] if modeC == 0 else m[i+1]
				print('>', p1)
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


if len(sys.argv) > 1 and sys.argv[1] == "test":
	print("test mode:")
	tests = [
				#"output whatever is input", "3,0,4,0,99",
				#"just halt", "1101,100,-1,4,0",
                #"eq 8 (pm)?", "3,9,8,9,10,9,4,9,99,-1,8",
                #"lt 8 (pm)?", "3,9,7,9,10,9,4,9,99,-1,8",
                #"eq 8 (im)?", "3,3,1108,-1,8,3,4,3,99",
                #"lt 8 (im)?", "3,3,1107,-1,8,3,4,3,99",
                #"non-zero?", "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9",
                #"non-zero?", "3,3,1105,-1,9,1101,0,0,12,4,12,99,1",
                "lt(999), eq(1000), gt(1001) 8?", "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
			]
	i = 0
	while i < len(tests):
		print("test: ", tests[i])
		res = intcode(tests[i+1])
		#print("%s => %s ?? %s || %s" % (tests[i], tests[i+1], res, "OK" if res == tests[i+1] else "ERR!"))
		i += 2

if len(sys.argv) == 1:
	with open(__file__.replace('.py', '.input.txt'), 'r') as f:
		lines = f.readlines()
		print("result= ", intcode(lines[0]))
	