import get_keyword
import argparse

"""
		total_obs_time

Arguments:
file_list - str - Name of (ASCII/txt) file with list of FITS observation files. 
	One file per line.

Written in Python 2.7 by A.L. Stevens, A.L.Stevens@uva.nl, 2014

get_keyword is available in my Git repository 'whizzy_scripts'
			
"""

##########################	
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('file_list', \
		help="Name of file with list of fits files of the observations.")
	args = parser.parse_args()

	input_files = [line.strip() for line in open(args.file_list)]
	
	total_time = 0
	for file in input_files:
		start_time = float(get_keyword.main(file, 0, 'TSTART'))
		stop_time = float(get_keyword.main(file, 0, 'TSTOP'))
		time = stop_time - start_time
		total_time += time
	
	print total_time # in seconds


## End of function 'total_obs_time'