import sys, math
from pprint import pprint

def parseInput(input):
	r = {}
	for line in input.split('\n'):
		inp, out = line.strip().split(' => ')
		inpMap = {}
		for t in inp.split(','):
			num, name = t.strip().split(' ')
			inpMap[name.strip()] = int(num.strip())
		num, name = out.split(' ')
		r[name.strip()] = {'num': int(num.strip()), 'inpMap': inpMap}
	#pprint(r)
	return r

def solve(r, name, num, heap, level=0):	
	#print((level * ' ') + "solve: name=", name, "num=", num, "heap=", heap)

	resolved = 0
	i=0
	for el in r[name]['inpMap']:
		i += 1
		#print((level * ' '), "check cond ", i, "/", len(r[name]['inpMap']), " for ", r[name]['inpMap'][el], el)

		if el not in heap:
			heap[el] = 0

		if heap[el] >= r[name]['inpMap'][el]:
			#print((level * ' '), "sufficient ", el, "found, reduce by ", r[name]['inpMap'][el])
			heap[el] -= r[name]['inpMap'][el]
			resolved += 1
		
		elif el == 'ORE':
			#print((level * ' '), "add", r[name]['inpMap'][el], " ORE to heap")
			heap['ORE_TOTAL'] += r[name]['inpMap'][el]
			resolved += 1
		
		elif el not in r:
			continue
		else:	
			#print((level * ' '), "insufficient", el, ", resolve... ")
			while True:
				cnt_before = heap[el]
				solve(r, el, r[name]['inpMap'][el], heap, level + 1)
				cnt_after = heap[el]
				#print((level * ' '), "before:", cnt_before, "afer:", cnt_after)
				if cnt_before == cnt_after:
					break
				if heap[el] >= r[name]['inpMap'][el]:
					#print((level * ' '), "sufficient ", el, "found, reduce by ", r[name]['inpMap'][el])
					heap[el] -= r[name]['inpMap'][el]
					resolved += 1
					break			

	if resolved == len(r[name]['inpMap']):
		#print((level * ' '), "all resolved, add ", r[name]['num'], " to ", name)
		if name not in heap:
			heap[name] = 0
		heap[name] += r[name]['num']
	else:
		print((level * ' '), "failed to resolve all")

def calcOre(input):
	r = parseInput(input)
	h = {'ORE_TOTAL': 0}
	solve(r, 'FUEL', 1, h)
	print(h)
	return h['ORE_TOTAL']


	
if len(sys.argv) > 1 and sys.argv[1] == "test":
	print("test mode:")
	tests = [
				 """10 ORE => 10 A
					1 ORE => 1 B
					7 A, 1 B => 1 C
					7 A, 1 C => 1 D
					7 A, 1 D => 1 E
					7 A, 1 E => 1 FUEL""", 31,
				 """9 ORE => 2 A
					8 ORE => 3 B
					7 ORE => 5 C
					3 A, 4 B => 1 AB
					5 B, 7 C => 1 BC
					4 C, 1 A => 1 CA
					2 AB, 3 BC, 4 CA => 1 FUEL""", 165,
				 """157 ORE => 5 NZVS
					165 ORE => 6 DCFZ
					44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
					12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
					179 ORE => 7 PSHF
					177 ORE => 5 HKGWZ
					7 DCFZ, 7 PSHF => 2 XJWVT
					165 ORE => 2 GPVTF
					3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT""", 13312,
				 """171 ORE => 8 CNZTR
					7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
					114 ORE => 4 BHXH
					14 VRPVC => 6 BMBT
					6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
					6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
					15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
					13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
					5 BMBT => 4 WPTQ
					189 ORE => 9 KTJDG
					1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
					12 VRPVC, 27 CNZTR => 2 XDBXC
					15 KTJDG, 12 BHXH => 5 XCVML
					3 BHXH, 2 VRPVC => 7 MZWV
					121 ORE => 7 VRPVC
					7 XCVML => 6 RJRHP
					5 BHXH, 4 VRPVC => 5 LTCX""", 2210736,
			]
	i = 0
	while i < len(tests):
		res = calcOre(tests[i])
		print("res=%i, test=%s" % (res, "OK" if res == tests[i+1] else "ERR!"))
		i += 2

else:
	with open(__file__.replace('.py', '.input.txt'), 'r') as f:
		contents = f.read()
		print(calcOre(contents))