def solvepart1():
	ans = 0
	for n in range(138307,654504):
		asc = True
		prev = -1
		dubb = False
		for c in str(n):
			c = int(c)
			if c < prev:
				asc = False
			if c == prev:
				dubb = True
			prev = c
		if asc and dubb:
			ans += 1
		
	return ans

		

def solvepart2():
	ans = 0
	for n in range(138307,654504):
		n =  str(n)
		asc = True
		prev = -1
		dubb = False
		for i, c in enumerate(n):
			c = int(c)
			if c < prev:
				asc = False
			if c == prev:
				if (i==1 or n[i-2] != str(prev)) and (i==5 or (n[i+1] != str(prev))):
					dubb = True
			prev = c
		if asc and dubb:
			ans += 1
		
	return ans

if __name__=='__main__':
	print(solvepart1())
	print(solvepart2())

