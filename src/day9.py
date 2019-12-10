import itertools
import math

class Computer():
	def __init__(self, phase):
		self.OPCODES = {
			1: self.ADD,
			2: self.MUL,
			3: self.WRITE,
			4: self.READ,
			5: self.JNZ,
			6: self.JEZ,
			7: self.LT,
			8: self.EQ,
			9: self.ARB,
			99: self.EXIT
		}
		self.input = []
		self.input.append(phase)
		self.phase = phase
		self.last_output = None
		self.input_index = 0
		self.PC = 0
		self.output_targets = []
		self.running = True
		self.RB = 0  # relative base


	def read_from_file(self, file, delimiter=','):
		self.memory = []
		with open(file) as f:
			self.memory.extend([x.strip() for x in f.read().split(',')])

	def run(self):
		while self.running:
			if self.PC<len(self.memory):
				if self.PC<len(self.memory):
					mode = self.memory[self.PC][:-2]
					op = int(self.memory[self.PC][-2:])
					result = self.OPCODES[op](mode)
					if result == -1:
						return False
			else:
				print("Ran through entire memory")
				self.running = False
				return True


	def add_output_target(self, f):
		self.output_targets.append(f)

	def pad_mode(self, mode, goal):
		while len(mode) < goal:
			mode = "0" + mode
		mode = mode[::-1]
		return mode

	def _memory_write(self, index, value):
		index = int(index)
		missing_length = index + 1 - len(self.memory)
		if missing_length > 0:
			self.memory.extend([0]*missing_length)
		self.memory[index] = value

	def _memory_read(self, index):
		index = int(index)
		missing_length = index + 1 - len(self.memory)
		if missing_length > 0:
			self.memory.extend([0]*missing_length)
		return self.memory[index]

	def _get_value(self, mode, value):
		# mode==1 is immediate mode, mode==0 is position mode
		if not mode or mode=="0":
			return self._memory_read(int(value))
		elif mode=="1":
			return value
		elif mode=="2":
			return self._memory_read(int(value) + self.RB)
		print("ERROR: Got unsupported mode: "+str(mode))
		return False

	def add_input(self, i):
		self.input.append(i)
		

	def send_output(self, out):
		self.last_output = out
		for f in self.output_targets:
			f(out)

	def _get_operands(self, num, mode):
		ans = []
		for n in range(num):
			ans.append(self._get_value(mode[n], self._memory_read(self.PC + n + 1)))
		if len(ans) == 1:
			return ans[0]
		return ans

	def _get_dest(self, params, mode):
		mode = mode[-1]
		if mode == "2":
			ans = int(self._memory_read(self.PC + params)) + self.RB
		else:
			ans = self._memory_read(self.PC + params)
		return int(ans)

	def ADD(self, mode):
		mode = self.pad_mode(mode, 3)
		operand0, operand1 = self._get_operands(2, mode)
		dest = self._get_dest(3, mode)
		self._memory_write(dest, str(int(operand0) + int(operand1)))
		self.PC += 4

	def MUL(self, mode):
		mode = self.pad_mode(mode, 3)
		operand0, operand1 = self._get_operands(2, mode)
		dest = self._get_dest(3, mode)
		self._memory_write(dest, str(int(operand0) * int(operand1)))
		self.PC += 4

	def WRITE(self, mode):
		if len(self.input) > self.input_index:
			mode = self.pad_mode(mode, 1)
			dest = self._get_dest(1, mode)
			self._memory_write(dest, self.input[self.input_index])
			self.input_index += 1
			self.PC += 2
		else:
			print("write didnt have input")
			return -1

	def READ(self, mode):
		operand0 = self._get_value(mode, self.memory[self.PC+1])
		self.send_output(operand0)
		self.PC += 2

	def JNZ(self, mode):
		mode = self.pad_mode(mode, 2)
		operand0, operand1 = self._get_operands(2, mode)
		if int(operand0) == 0:
			self.PC += 3
		else:
			self.PC = int(operand1)
		

	def JEZ(self, mode):
		mode = self.pad_mode(mode, 2)
		operand0, operand1 = self._get_operands(2, mode)
		if int(operand0) == 0:
			self.PC = int(operand1)
		else:
			self.PC += 3
			

	def LT(self, mode):
		mode = self.pad_mode(mode, 3)
		operand0, operand1 = self._get_operands(2, mode)
		dest = self._get_dest(3, mode)
		if int(operand0) < int(operand1):
			self.memory[dest] = 1
		else:
			self.memory[dest] = 0
		self.PC += 4

	def EQ(self, mode):
		mode = self.pad_mode(mode, 3)
		operand0, operand1 = self._get_operands(2, mode)
		dest = self._get_dest(3, mode)
		if int(operand0) == int(operand1):
			self.memory[dest] = 1
		else:
			self.memory[dest] = 0
		self.PC += 4

	def ARB(self, mode):
		mode = self.pad_mode(mode, 1)
		operand0 = self._get_operands(1, mode)
		self.RB += int(operand0)
		self.PC += 2

	def EXIT(self, mode):
		self.running = False
		self.PC += 1
		return True

	
	def __repr__(self):
		return "Computer "+str(self.phase)

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
	cpu = Computer("2")
	cpu.add_output_target(print)
	cpu.read_from_file('inputs/day9.txt')
	cpu.run()


def solvepart2():
	rc = ResultComparer()
	num_computers = 5
	for p in itertools.permutations(range(5, 5+num_computers)):
		cpus = []
		for index, phase in enumerate(p):
			if index==0:
				cpu = Computer(str(phase))
				cpu.add_input("0")
				cpus.append(cpu)
			else:
				cpus.append(Computer(str(phase)))
		for i in range(num_computers-1):
			cpus[i].add_output_target(cpus[i+1].add_input)
		cpus[num_computers-1].add_output_target(cpus[0].add_input)
		for cpu in cpus:
			cpu.read_from_file('inputs/day7.txt')
		while any([cpu.running for cpu in cpus]):
			for cpu in cpus:
				cpu.run()
		rc.check(cpus[num_computers-1].last_output)
	return rc.get_best()

if __name__=='__main__':
	print(solvepart1())
	#print(solvepart2())

