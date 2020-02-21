import itertools
import math
import pygame

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

class Tile():
	def __init__(self):
		self.x = -1
		self.y = -1
		self.id = -1

class Day13():
	def __init__(self):
		self.cpu = Computer()
		self.cpu.add_output_target(self.handle_output)
		self.cpu.read_from_file('inputs/day13.txt')
		self.gametiles = {}
		self.outputs = 0
		self.score = 0
		
	def solvepart1(self):
		self.cpu.run()
		ans = 0
		for tile in self.gametiles:
			if tile.id == 2:
				ans += 1
		return ans

	def solvepart2(self):
		import random
		i = 0
		self.setup_game()
		self.cpu.memory[0] = "2"
		while True:
			i += 1
			self.cpu.run()
			ans = 0
			for tile in self.gametiles:
				if self.gametiles[tile].id == 2:
					ans += 1
			if ans==0:
				return self.score
			self.drawboard()
			print()
			print("tiles left: "+str(ans))
			print("score: "+str(self.score))
			self.handle_input()
			

	def setup_game(self):
		pygame.init()
		self.screen = pygame.display.set_mode((1000, 1000))

	def handle_input(self):
		"""
		while True:
			ev = pygame.event.poll()
			if ev.type == pygame.KEYDOWN:
				if ev.key == pygame.K_RIGHT:
					playerinput = 1
				elif ev.key == pygame.K_LEFT:
					playerinput = -1
				else:
					playerinput = 0
				break
			elif ev.type == pygame.QUIT:
				import sys
				sys.exit()
"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				import sys
				sys.exit()
		playerinput = 0
		if playerinput == 0:
			for tile in self.gametiles:
				tile = self.gametiles[tile]
				if tile.id == 3:
					paddlex = tile.x
				elif tile.id == 4:
					ballx = tile.x

			if abs(paddlex-ballx)>0:
				if ballx > paddlex:
					playerinput = 1
				else:
					playerinput = -1
		self.cpu.add_input(playerinput)	

	def drawrect(self, tile):
		colors = {0 : (0 ,0, 0),
		1 : (193, 169, 169),
		2 : (74, 92, 179),
		3 : (166, 163, 37),
		4 : (118, 17, 75),
		}
		if tile.id > 0:
			pygame.draw.rect(self.screen, colors[tile.id], (20*tile.x, 20*tile.y, 20, 20))

	def drawboard(self):
		self.screen.fill((0,0,0))
		for tile in self.gametiles:
			self.drawrect(self.gametiles[tile])
		pygame.display.flip()


	def handle_output(self, o):
		o = int(o)
		if self.outputs % 3 == 0:
			self.current_tile = Tile()
			self.current_tile.x = o
		elif self.outputs % 3 == 1:
			self.current_tile.y = o
		elif self.outputs % 3 == 2:
			self.current_tile.id = o
			if self.current_tile.x == -1 and self.current_tile.y == 0:
				self.score = o
			else:
				self.gametiles[(self.current_tile.x, self.current_tile.y)] = self.current_tile
		self.outputs += 1


def solvepart1():
	day13 = Day13()
	return day13.solvepart1()

def solvepart2():
	day13 = Day13()
	return day13.solvepart2()


if __name__=='__main__':
	#print(solvepart1())
	print(solvepart2())

