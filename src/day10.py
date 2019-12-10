import math

def solvepart1():
	chart = []
	with open('inputs/day10.txt') as f:
		for line in f:
			chart.append(list(line.strip()))
	#chart[y][x]=='#' means asteroid at (x,y)

	best_mapscore = 0
	for y in range(len(chart)):
		for x in range(len(chart[y])):
			if chart[y][x] == '#':
				mapscore = get_mapscore(chart, x, y)
				#print("mapscore for ("+str(x)+","+str(y)+") is "+str(mapscore))
				if mapscore > best_mapscore:
					best_mapscore = mapscore
	return best_mapscore


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

def solvepart2():
	pass
		


if __name__=='__main__':
	print(solvepart1())
	print(solvepart2())

