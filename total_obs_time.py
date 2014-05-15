import get_keyword
import argparse

"""
		total_obs_time

Passed: file_list - str - List of FITS observation files. One file per line.

Returns: total_time - float - The total observational time of all observations in the 
			list.
			
"""
##########################	
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('file_list', \
		help="List of fits files with observations")
	args = parser.parse_args()

	input_files = [line.strip() for line in open(args.file_list)]
	
	total_time = 0
	for file in input_files:
		start_time = float(get_keyword.main(file, 0, 'TSTART', 0))
		stop_time = float(get_keyword.main(file, 0, 'TSTOP', 0))
		time = stop_time - start_time
		total_time += time
	print total_time
# 	return total_time
	## End of function 'total_obs_time'