import argparse

if __name__ == '__main__':
	pass
	parser = argparse.ArgumentParser()
	parser.add_argument('x', type=int, help="The integer to take 2 to the power of (i.e. 2 ^ x).")
	args = parser.parse_args()
	print 2 ** args.x