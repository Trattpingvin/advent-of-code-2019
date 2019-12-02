class Computer():
	def __init__(self):
		self.OPCODES = {
			1: self.ADD,
			2: self.MUL,
			99: self.EXIT
		}
		self.reset()

	def reset(self):
		self.PC = 0
		self.running = False

	def read_from_file(self, file):
		with open(file) as f:
			self.memory = [int(x) for x in f.readline().split(',')]

	def run(self):
		self.running = True
		while self.running:
			self.OPCODES[self.memory[self.PC]]()

	def ADD(self):
		operand1 = self.memory[self.PC+1]
		operand2 = self.memory[self.PC+2]
		store_addr = self.memory[self.PC+3]
		self.memory[store_addr] = self.memory[operand1] + self.memory[operand2]
		self.PC += 4

	def MUL(self):
		operand1 = self.memory[self.PC+1]
		operand2 = self.memory[self.PC+2]
		store_addr = self.memory[self.PC+3]
		self.memory[store_addr] = self.memory[operand1] * self.memory[operand2]
		self.PC += 4

	def EXIT(self):
		self.running = False
		self.PC += 1

def solvepart1():
	cpu = Computer()
	cpu.read_from_file('inputs/day2.txt')
	cpu.memory[1] = 12
	cpu.memory[2] = 2
	cpu.run()
	return cpu.memory[0]

def solvepart2():
	cpu = Computer()
	for noun in range(100):
		for verb in range(100):
			cpu.reset()
			cpu.read_from_file('inputs/day2.txt')
			cpu.memory[1] = noun
			cpu.memory[2] = verb
			cpu.run()
			if cpu.memory[0] == 19690720:
				return 100 * noun + verb

if __name__=='__main__':
	print(solvepart1())
	print(solvepart2())

