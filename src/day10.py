import math

def solvepart1():
	chart = []
	with open('inputs/day10.txt') as f:
		for line in f:
			chart.append(list(line.strip()))
	#chart[y][x]=='#' means asteroid at (x,y)

	best_mapscore = 0
	best_x, best_y = 0,0
	for y in range(len(chart)):
		for x in range(len(chart[y])):
			if chart[y][x] == '#':
				mapscore = get_mapscore(chart, x, y)
				#print("mapscore for ("+str(x)+","+str(y)+") is "+str(mapscore))
				if mapscore > best_mapscore:
					best_mapscore = mapscore
					best_x, best_y = x, y
	return ((best_x, best_y), best_mapscore)


def get_mapscore(chart, start_x, start_y):
	lines = set()
	for y in range(len(chart)):
		for x in range(len(chart[y])):
			if y==start_y and x==start_x:
				continue
			if chart[y][x] == '#':
				line = (start_x-x, start_y-y)
				gcd = math.gcd(line[0], line[1])
				line = (line[0]//gcd, line[1]//gcd)
				#if (-line[0], -line[1]) not in lines:
				lines.add(line)
	return len(lines)

class Polar():
	def __init__(self, x, y):
		self.r = math.sqrt(x*x + y*y)
		self.phi = (math.atan2(y, x) - math.pi/2) % (2 * math.pi)

	def __repr__(self):
		return "("+str(self.r)+", "+str(self.phi)+"°)"

def solvepart2(base_coord):
	#421 too low
	#2426 too high
	chart = []
	polar_to_cartesian = {}
	with open('inputs/day10.txt') as f:
		for y, line in enumerate(f):
			for x, char in enumerate(line.strip()):
				if char == '#':
					polar = Polar(base_coord[0] - int(x), base_coord[1] - int(y))
					chart.append(polar)
					polar_to_cartesian[polar] = (x, y)

	chart.sort(key=lambda x: x.r)
	chart.sort(key=lambda x: x.phi)
	prev_phi = math.inf
	
	removed = 0
	i = 0
	while True:
		index = i%len(chart)
		current = chart[index]
		if current.phi != prev_phi:
			removed += 1
			if removed == 200:
				return polar_to_cartesian[current]
#			print("Removed "+str(polar_to_cartesian[current]))
			chart.remove(current)
		else:
			i += 1
		prev_phi = current.phi
		


if __name__=='__main__':
	coord, score = solvepart1()
	print(score)
	print(solvepart2(coord))

