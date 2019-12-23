import itertools
import math

class Computer():
	def __init__(self, phase = None):
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
		if phase:
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
		

	def _send_output(self, out):
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
			return -1

	def READ(self, mode):
		operand0 = self._get_value(mode, self.memory[self.PC+1])
		self._send_output(operand0)
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

class Day11():
	def __init__(self):
		self.cpu = Computer()
		self.cpu.add_output_target(self.handle_output)
		self.cpu.read_from_file('inputs/day11.txt')
		self.current_pos = (0, 0)
		self.current_dir = (0, 1)
		self.paints = {}
		self.outputs = 0
		self.ROTLEFT = {
			(0, 1) : (-1, 0),
			(-1, 0) : (0, -1),
			(0, -1) : (1, 0),
			(1, 0) : (0, 1)
		}
		self.ROTRIGHT = {
			(0, 1) : (1, 0),
			(1, 0) : (0, -1),
			(0, -1) : (-1, 0),
			(-1, 0) : (0, 1)
		}
		
	def solvepart1(self):
		while self.cpu.running:
			self.cpu.add_input(self.get_paint(*self.current_pos))
			self.cpu.run()
		return len(self.paints)

	def solvepart2(self):
		self.paints[(0, 0)] = 1
		while self.cpu.running:
			self.cpu.add_input(self.get_paint(*self.current_pos))
			self.cpu.run()
		

		lowx, lowy, highx, highy = 0,0,0,0
		for coord in self.paints:
			x = coord[0]
			y = coord[1]
			if x < lowx:
				lowx = x
			if x > highx:
				highx = x
			if y < lowy:
				lowy = y
			if y > highy:
				highy = y
		
		import cv2
		import numpy
		shape = [abs(highx-lowx)+1, abs(highy-lowy)+1, 3]
		img = numpy.zeros(shape)
		for coord in self.paints:
			x = coord[0]
			y = abs(coord[1])
			if self.paints[coord] == 1:
				img[x,y,0] = 255
				img[x,y,1] = 255
				img[x,y,2] = 255
		cv2.imshow("registration number", img.transpose([1,0,2]))
		cv2.waitKey()



	def handle_output(self, o):
		o = int(o)
		if self.outputs % 2 == 0:
			self.paints[self.current_pos] = o
		else:
			if o == 0:
				self.current_dir = self.ROTLEFT[self.current_dir]
			elif o == 1:
				self.current_dir = self.ROTRIGHT[self.current_dir]
			else:
				raise ("ERROR bad direction")
			prevpos = self.current_pos
			self.current_pos = (self.current_pos[0] + self.current_dir[0], self.current_pos[1] + self.current_dir[1])
			# print("Started at {0}. Moved in direction {1}. Ended at {2} ".format(str(prevpos), str(self.current_dir), self.current_pos))
		self.outputs += 1

	def get_paint(self, x, y):
		if (x, y) not in self.paints:
			self.paints[(x, y)] = 0
		return self.paints[(x, y)]

def solvepart1():
	day11 = Day11()
	return day11.solvepart1()

def solvepart2():
	day11 = Day11()
	return day11.solvepart2()


if __name__=='__main__':
	#print(solvepart1())
	print(solvepart2())

