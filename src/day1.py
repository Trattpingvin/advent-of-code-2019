def solvepart1():
	fuel = 0
	with open('inputs/day1.txt') as f:
		for i in f:
			fuel += get_fuel_requirement(int(i))
	return fuel

def get_fuel_requirement(mass):
	return max(0, mass//3-2)

def solvepart2():
	fuel = 0
	with open('inputs/day1.txt') as f:
		for i in f:
			mass = int(i)
			while mass>0:
				added = get_fuel_requirement(mass)
				fuel += added
				mass = added
	return fuel

if __name__=='__main__':
	print(solvepart1())
	print(solvepart2())

