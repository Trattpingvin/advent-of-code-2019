import math
import random
import copy

class Moon():
	calls = 1
	def __init__(self):
		self.name = str(Moon.calls)
		Moon.calls += 1
		self.x = 0
		self.y = 0
		self.z = 0
		self.vx = 0
		self.vy = 0
		self.vz = 0
		self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

	def pos(self):
		return (self.x, self.y, self.z)

	def vel(self):
		return (self.vx, self.vy, self.vz)

	def prepare_gravity(self, moon2):
		if moon2.x < self.x:
			self.vx += -1
		elif moon2.x > self.x:
			self.vx += 1
		if moon2.y < self.y:
			self.vy += -1
		elif moon2.y > self.y:
			self.vy += 1
		if moon2.z < self.z:
			self.vz += -1
		elif moon2.z > self.z:
			self.vz += 1

	def apply_gravity(self):
		self.x += self.vx
		self.y += self.vy
		self.z += self.vz

	def kinetic_energy(self):
		return sum(map(abs, (self.vx, self.vy, self.vz)))
	
	def potential_energy(self):
		return sum(map(abs, (self.x, self.y, self.z)))

	def state(self):
		return (self.pos(), self.vel())

	def __repr__(self):
		return "moon {} potential: {} kinetic: {} pos: {} vel: {}".format(self.name, self.potential_energy(), self.kinetic_energy(), self.pos(), self.vel())


def convert_to_2d(point=[0,0,0]):
    return [480 + 8*int(point[0]*(point[2]*.3)),360 + 8*int(point[1]*(point[2]*.3))]

def solvepart1(visualize=False):

	if visualize:
		import pygame
		pygame.init()
		screen = pygame.display.set_mode((960, 720))

	moons = []

	with open('inputs/day12.txt') as f:
		for line in f:
			moon = Moon()
			splits = line.strip().strip('>').split(',')
			moon.x = int(splits[0].split('=')[1])
			moon.y = int(splits[1].split('=')[1])
			moon.z = int(splits[2].split('=')[1])
			moons.append(moon)

	for _ in range(1000):
		iterate_gravity(moons)


		if visualize:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					import sys
					sys.exit()
			screen.fill((0,0,0))
			for moon in moons:
				pygame.draw.circle(screen, moon.color, convert_to_2d((moon.pos())), 12+moon.z)
			pygame.display.flip()
			pygame.time.wait(120)


	ans = 0
	for moon in moons:
		ans += moon.kinetic_energy() * moon.potential_energy()

	return ans


def iterate_gravity(moons):
	for moon1 in moons:
		for moon2 in moons:
			if moon1 is not moon2:
				moon1.prepare_gravity(moon2)
	for moon in moons:
		moon.apply_gravity()


def printmoons(moons):
	for moon in moons:
		print(moon)
	print()

def lcm(numbers):
	p1 = numbers[0]
	p2 = numbers[1]
	if len(numbers)>2:
		return lcm([lcm([p1, p2])]+(numbers[2:]))
	return p1*p2//math.gcd(p1, p2)


def solvepart2():
	moons = []
	with open('inputs/day12.txt') as f:
		for line in f:
			moon = Moon()
			splits = line.strip().strip('>').split(',')
			moon.x = int(splits[0].split('=')[1])
			moon.y = int(splits[1].split('=')[1])
			moon.z = int(splits[2].split('=')[1])
			moons.append(moon)

	dimension_states = []
	dimension_states.append(tuple((moon.x, moon.vx) for moon in moons))
	dimension_states.append(tuple((moon.y, moon.vy) for moon in moons))
	dimension_states.append(tuple((moon.z, moon.vz) for moon in moons))
	xperiod, yperiod, zperiod = 0,0,0
	i = 0
	while True:
		i += 1
		iterate_gravity(moons)
		if not xperiod:
			if tuple((moon.x, moon.vx) for moon in moons) == dimension_states[0]:
				xperiod = i
		if not yperiod:
			if tuple((moon.y, moon.vy) for moon in moons) == dimension_states[1]:
				yperiod = i
		if not zperiod:
			if tuple((moon.z, moon.vz) for moon in moons) == dimension_states[2]:
				zperiod = i
		if xperiod and yperiod and zperiod:
			break

	return lcm([xperiod, yperiod, zperiod])

if __name__=='__main__':
	print(solvepart2())
