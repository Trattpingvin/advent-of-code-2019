def solvepart1():
	fuel = 0
	with open('inputs/day1.txt') as f:
		for i in f:
			fuel += get_fuel_requirement(int(i))
	return fuel

def get_fuel_requirement(mass):
	return max(0, mass//3-2)

def get_fuel_requirement_rocket_tyranny(mass):
	fuel = 0
	while mass>0:
		added = get_fuel_requirement(mass)
		fuel += added
		mass = added
	return fuel

def solvepart2():
	fuel = 0
	with open('inputs/day1.txt') as f:
		for i in f:
			mass = int(i)
			fuel += get_fuel_requirement_rocket_tyranny(mass)
	return fuel

if __name__=='__main__':
	print("Fuel requiement for mass {0} is {1} for part one and {2} for part two".format(2000, get_fuel_requirement(2000),get_fuel_requirement_rocket_tyranny(2000)))
	print(solvepart1())
	print(solvepart2())

