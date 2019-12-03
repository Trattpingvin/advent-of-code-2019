def manhattan(coord):
	return abs(coord[0])+abs(coord[1])

def solvepart1():
	wires = [[],[]]
	with open('inputs/day3.txt') as f:
		wire = -1
		for line in f:
			x = 0
			y = 0
			wire += 1
			dirs = line.split(',')

			for d in dirs:
				xdelta = 0
				ydelta = 0
				length = int(d[1:])
				if d[0] == "R":
					xdelta = 1
				elif d[0] == "D":
					ydelta = 1
				elif d[0] == "L":
					xdelta = -1
				elif d[0] == "U":
					ydelta = -1
				else:
					raise "shouldn't happen"
				for _ in range(length):
					wires[wire].append((x, y))
					y += ydelta
					x += xdelta

	for i in range(2):
		wires[i].remove((0,0))
		print("found "+str(len(wires[i]))+" wire segments from wire "+str(i))
		wires[i].sort(key=manhattan)
	i = 0
	while True:
		i += 1
		temp_wires = (set(), set())
		for w in range(2):
			while manhattan(wires[w][0]) == i:
				temp_wires[w].add(wires[w].pop(0))
		for w1 in temp_wires[0]:
			if w1 in temp_wires[1]:
				return manhattan(w1)

	return False

def solvepart2():
	wires = [[],[]]
	with open('inputs/day3.txt') as f:
		wire = -1
		for line in f:
			x = 0
			y = 0
			wire_length = 0
			wire += 1
			dirs = line.split(',')

			for d in dirs:
				xdelta = 0
				ydelta = 0
				length = int(d[1:])
				if d[0] == "R":
					xdelta = 1
				elif d[0] == "D":
					ydelta = 1
				elif d[0] == "L":
					xdelta = -1
				elif d[0] == "U":
					ydelta = -1
				else:
					raise "shouldn't happen"
				for _ in range(length):
					wires[wire].append(((x, y), wire_length))
					wire_length += 1
					y += ydelta
					x += xdelta

	for i in range(2):
		wires[i].remove(((0,0),0))
		print("found "+str(len(wires[i]))+" wire segments from wire "+str(i))
		wires[i].sort(key=lambda x: x[1])
		print(wires[i][len(wires[i])-1])

	i = 0
	w0 = set()
	intersections = []
	for w in wires[0]:
		w0.add(w[0])
	for w1 in wires[1]:
		if w1[0] in w0:
			intersections.append(w1)

	shortest_intersection = 9999999
	for i in intersections:
		for w0 in wires[0]:
			if w0[0]==i[0]:
				current_dist = i[1] + w0[1]
				if current_dist < shortest_intersection:
					shortest_intersection = current_dist
				break
	return shortest_intersection	
	

if __name__=='__main__':
	#print(solvepart1())
	print(solvepart2())

