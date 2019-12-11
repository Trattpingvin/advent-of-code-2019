import pygame
import sys

def make_chart():
	chart = []
	with open("inputs/day10order.txt") as f:
		for line in f:
			chart.append(list(line.strip().split(',')))
	return chart


class Visualizer():
	def __init__(self):
		self.target_fps = 60
		self.chart = make_chart()
		self.base = (26, 36)
		self.size = self.width, self.height = 960, 720
		self.MARGIN = 20
		self.tile_size = (self.height - self.MARGIN)  // len(self.chart)
		self.FIRE_TIME = 100  # miliseconds per shot
		self.SHOOT_DURATION = 35


	def get_asteroid_location(self, x, y):
		return (((self.width-self.height)//2) + self.MARGIN + x * self.tile_size, self.MARGIN + y * self.tile_size)

	def elapsed(self, since):
		return pygame.time.get_ticks() - since

	def coords_for_target(self, target):
		for y in range(len(self.chart)):
				for x in range(len(self.chart[0])):
					if self.chart[y][x] == str(target):
						return x, y
		raise "couldn't find target"

	def run(self):
		pygame.init()
		screen = pygame.display.set_mode(self.size)
		previous_shot = pygame.time.get_ticks()
		shooting = False
		shoot_target = 0
		shoot_start = None
		ASTEROID_SIZE = self.tile_size // 2 - 1
		while True:
			start = pygame.time.get_ticks()
			if shoot_target == 200:
				return
			screen.fill((0,0,0))
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()
			for y in range(len(self.chart)):
				for x in range(len(self.chart[0])):
					if self.chart[y][x] == '#' or self.chart[y][x].isdigit():
						pygame.draw.circle(screen, (146, 133, 125), self.get_asteroid_location(x, y), ASTEROID_SIZE)

			pygame.draw.circle(screen, (20, 240, 50), self.get_asteroid_location(*self.base), ASTEROID_SIZE)

			if self.elapsed(previous_shot) > self.FIRE_TIME:
				shooting = True
				shoot_start = pygame.time.get_ticks()
				previous_shot = pygame.time.get_ticks()
				shoot_target += 1
				trgt = self.coords_for_target(shoot_target)
			if shooting:
				if self.elapsed(shoot_start) > self.SHOOT_DURATION:
					self.chart[trgt[1]][trgt[0]] = "."
					shooting = False
				pygame.draw.circle(screen, (220, 20, 20), self.get_asteroid_location(*trgt), ASTEROID_SIZE)
				pygame.draw.line(screen, (220, 20, 20), self.get_asteroid_location(*self.base), self.get_asteroid_location(*trgt))

			pygame.display.flip()
			end = pygame.time.get_ticks()
			pygame.time.wait(int((1.0 / self.target_fps) - (end - start)) * 1000)

if __name__ == "__main__":
	v = Visualizer()
	v.run()
