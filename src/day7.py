class Computer():
	def __init__(self, elf_input):
		self.OPCODES = {
			1: self.ADD,
			2: self.MUL,
			3: self.WRITE,
			4: self.READ,
			5: self.JNZ,
			6: self.JEZ,
			7: self.LT,
			8: self.EQ,
			99: self.EXIT
		}
		self.input = []
		try: #if elf input is iterable then we extend input with it, otherwise we just add it
			for ei in elf_input:
				self.input.append(ei)
		except TypeError:
			self.input.append(elf_input)
		self.output = None
		self.input_index = 0
		self.PC = 0
		self.running = False
		self.output_targets = []

	def read_from_file(self, file, delimiter=','):
		self.memory = []
		with open(file) as f:
			self.memory.extend([x.strip() for x in f.read().split(',')])

	def run(self):
		self.running = True
		while self.running:
			if self.PC<len(self.memory):
				self.step()

	def step(self):
		if self.running:
			if self.PC<len(self.memory):
				mode = self.memory[self.PC][:-2]
				op = int(self.memory[self.PC][-2:])
				self.OPCODES[op](mode)
			else:
				print("Ran through entire memory")
				return True

	def add_output_target(self, f):
		self.output_targets.append(f)

	def pad_mode(self, mode, goal):
		while len(mode) < goal:
			mode = "0" + mode
		mode = mode[::-1]
		return mode

	def get_value(self, mode, value):
		# mode==1 is immediate mode, mode==0 is position mode
		if not mode or mode=="0":
			return self.memory[int(value)]
		elif mode=="1":
			return value
		print("ERROR: Got mode unsupported mode: "+str(mode))
		return False

	def add_input(self, i):
		self.input.append(i)
		

	def send_output(self, out):
		for f in self.output_targets:
			f(out)

	def ADD(self, mode):
		mode = self.pad_mode(mode, 3)
		operand0 = self.get_value(mode[0], self.memory[self.PC+1])
		operand1 = self.get_value(mode[1], self.memory[self.PC+2])
		operand2 = int(self.memory[self.PC+3])
		self.memory[operand2] = str(int(operand0) + int(operand1))
		self.PC += 4

	def MUL(self, mode):
		mode = self.pad_mode(mode, 3)
		operand0 = self.get_value(mode[0], self.memory[self.PC+1])
		operand1 = self.get_value(mode[1], self.memory[self.PC+2])
		operand2 = int(self.memory[self.PC+3])
		self.memory[operand2] = str(int(operand0) * int(operand1))
		self.PC += 4

	def WRITE(self, mode):
		if len(self.input) > self.input_index:
			operand0 = int(self.memory[self.PC+1])
			self.memory[operand0] = self.input[self.input_index]
			self.input_index += 1
			self.PC += 2
		else:
			return False

	def READ(self, mode):
		operand0 = self.get_value(mode, self.memory[self.PC+1])
		self.send_output(operand0)
		self.PC += 2

	def JNZ(self, mode):
		mode = self.pad_mode(mode, 2)
		operand0 = int(self.get_value(mode[0], self.memory[self.PC+1]))
		operand1 = int(self.get_value(mode[1], self.memory[self.PC+2]))
		if operand0 == 0:
			self.PC += 3
		else:
			self.PC = operand1
		

	def JEZ(self, mode):
		mode = self.pad_mode(mode, 2)
		operand0 = int(self.get_value(mode[0], self.memory[self.PC+1]))
		operand1 = int(self.get_value(mode[1], self.memory[self.PC+2]))
		if operand0 == 0:
			self.PC = operand1
		else:
			self.PC += 3
			

	def LT(self, mode):
		mode = self.pad_mode(mode, 3)
		operand0 = int(self.get_value(mode[0], self.memory[self.PC+1]))
		operand1 = int(self.get_value(mode[1], self.memory[self.PC+2]))
		operand2 = int(self.memory[self.PC+3])
		if operand0 < operand1:
			self.memory[operand2] = 1
		else:
			self.memory[operand2] = 0
		self.PC += 4

	def EQ(self, mode):
		mode = self.pad_mode(mode, 3)
		operand0 = int(self.get_value(mode[0], self.memory[self.PC+1]))
		operand1 = int(self.get_value(mode[1], self.memory[self.PC+2]))
		operand2 = int(self.memory[self.PC+3])
		if operand0 == operand1:
			self.memory[operand2] = 1
		else:
			self.memory[operand2] = 0
		self.PC += 4

	def EXIT(self, mode):
		self.running = False
		self.PC += 1
		return True

class ResultComparer():
	def __init__(self):
		self.best = 0
	def check(self, thrust):
		thrust = int(thrust)
		if thrust > self.best:
			self.best = thrust
	def get_best(self):
		return self.best

def solvepart1():
	import itertools
	rc = ResultComparer()
	num_computers = 5
	for p in itertools.permutations(range(num_computers)):
		cpus = []
		for index, phase in enumerate(p):
			if index==0:
				cpus.append(Computer((str(phase), "0")))
			else:
				cpus.append(Computer(str(phase)))
		for i in range(num_computers-1):
			cpus[i].add_output_target(cpus[i+1].add_input)
		cpus[num_computers-1].add_output_target(rc.check)
		for cpu in cpus:
			cpu.read_from_file('inputs/day7.txt')
			cpu.run()
	return rc.get_best()


def solvepart2():
	pass

if __name__=='__main__':
	print(solvepart1())
	#print(solvepart2())

