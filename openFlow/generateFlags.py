import random

def generateFlags(flags):
	sum = 0

	for i in flags:
		sum += i * random.randint(0, 1)

	return sum