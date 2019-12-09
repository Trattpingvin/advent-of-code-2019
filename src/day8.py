import math

def solvepart1():
	wide = 25
	tall = 6
	best_zeroes = math.inf
	best_layerscore = 0
	with open('inputs/day8.txt') as f:
		chunk = f.read(wide*tall)
		while chunk:
			zeroes = 0
			ones = 0
			twos = 0
			for char in chunk:
				if char == "0":
					zeroes += 1
				if char == "1":
					ones += 1
				if char == "2":
					twos += 1
			if zeroes < best_zeroes:
				best_zeroes = zeroes
				best_layerscore = ones * twos
			chunk = f.read(wide*tall)
	return best_layerscore

def solvepart2():
	wide = 25
	tall = 6
	image = [["2"]*25 for _ in range(tall)]
	with open('inputs/day8.txt') as f:
		chunk = f.read(wide*tall)
		while chunk:
			for i, char in enumerate(chunk):
				row = i//25
				col = i%25
				if image[row][col] == "2":
					image[row][col] = char
			chunk = f.read(wide*tall)
	for line in image:
		print(" ".join(line))
		


if __name__=='__main__':
	print(solvepart1())
	print(solvepart2())

