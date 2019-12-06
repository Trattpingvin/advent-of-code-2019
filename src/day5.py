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
		self.input = elf_input
		self.reset()

	def reset(self):
		self.PC = 0
		self.running = False

	def read_from_file(self, file, delimiter=','):
		self.memory = []
		with open(file) as f:
			self.memory.extend([x.strip() for x in f.read().split(',')])

	def run(self):
		self.running = True
		while self.running:
			if self.PC<len(self.memory):
				mode = self.memory[self.PC][:-2]
				op = int(self.memory[self.PC][-2:])
				self.OPCODES[op](mode)
			else:
				print("Ran through entire memory")
				return

	def pad_mode(self, mode, goal):
		while len(mode) < goal:
			mode = "0" + mode
		mode = mode[::-1]
		return mode

	def get_value(self, mode, value):
		# mode==1 is immediate mode, mode==0 is position mode
		if mode=="1":
			return value
		return self.memory[int(value)]

	def get_input(self):
		return self.input

	def send_output(self, out):
		print(out)

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
		operand0 = int(self.memory[self.PC+1])
		self.memory[operand0] = self.get_input()
		self.PC += 2

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

def solvepart1():
	cpu = Computer("1")
	cpu.read_from_file('inputs/day5.txt')
	cpu.run()


def solvepart2():
	#5578375 too low
	cpu = Computer("5")
	cpu.read_from_file('inputs/day5.txt')
	cpu.run()

if __name__=='__main__':
	print(solvepart1())
	print(solvepart2())

