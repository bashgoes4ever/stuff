from itertools import groupby

def dbl_linear(n):
	sequence = [1]
	prev1 = 0
	prev2 = 0
	for i, x in enumerate(sequence):
		y = 2*x+1
		z = 3*x+1
		if prev1 != y and prev2 != y:
			sequence.append(y)
		if prev1 != z and prev2 != z:
			sequence.append(z)
		prev1, prev2 = y, z
		sequence.sort()
		if 50000 < i:
			break

	return sequence[n]



print(dbl_linear(50))