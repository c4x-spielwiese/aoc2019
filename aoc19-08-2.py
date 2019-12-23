import string, sys, math

class SpaceImg:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.layers = []

	def printLayer(self, layerNo):
		for row in range(0, self.height):
			for cell in range(0, self.width):
				idx = (row * self.width) + cell
				sys.stdout.write(self.layers[int(layerNo)][idx : idx+1])
			sys.stdout.write('\n')

	def printLayers(self):
		for i in range(len(self.layers)):
			print("Layer ", i)
			self.printLayer(i)

	def decode(self, inputStr):		
		layerCount = math.floor(len(inputStr) / (self.width * self.height))
		s = 0
		e = self.width * self.height
		for i in range(0, layerCount):
			self.layers.append(inputStr[s : e])
			s = e
			e += self.width * self.height

	def render(self):
		self.renderedImg = []
		for row in range(0, self.height):
			for cell in range(0, self.width):
				idx = (row * self.width) + cell
				c = self.getColor(0, idx)
				sys.stdout.write(c if c != '0' else ' ')
			sys.stdout.write('\n')										
		

	def getColor(self, layerNo, idx):
		c = self.layers[layerNo][idx : idx+1]
		if c == '0' or c == '1':
			return c
		else:
			return self.getColor(layerNo + 1, idx)

	def calcChecksum(self):
		c = -1
		minZeros = -1
		for i in range(len(self.layers)):
			zeros = self.layers[i].count('0')
			if zeros < c or c == -1:
				c = zeros
				minZeros = i
		return self.layers[minZeros].count('1') * self.layers[minZeros].count('2')	



if len(sys.argv) > 1 and sys.argv[1] == "test":
	print("test mode:")
	tests = [
				"0222112222120000", 1,
			]
	i = 0
	while i < len(tests):
		print("test: %s" % tests[i])
		
		s = SpaceImg(2, 2)
		s.decode(tests[i])
		s.printLayers()
		res = s.calcChecksum()
		s.render()
		
		print("%d == %d -> %s" % (tests[i+1], res, "OK" if res == tests[i+1] else "ERR!"))
		i += 2

if len(sys.argv) == 1:
	with open(__file__.replace('.py', '.input.txt'), 'r') as f:
		lines = f.readlines()
		s = SpaceImg(25, 6)
		s.decode(lines[0])
		#s.printLayers()
		#res = s.calcChecksum()
		#print("checksum=", res)
		s.render()
