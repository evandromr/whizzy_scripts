import argparse
from astropy.io import fits 
from astropy.io import ascii
# import numpy as np
"""
		dump_columns.py

Dumps two columns from a FITS file into an ASCII file.

Written in Python 2.7 by A.L. Stevens, A.L.Stevens@uva.nl, 2014

"""

def main(fits_file, ext, col1, col2, ascii_file):
	pass
	
	assert (ext >= 0 and ext <= 3) # RXTE FITS files shouldn't have more than 3 exensions
	
	# np.set_printoptions(threshold='nan') # to print out the whole array

	## Opens the fits file using the Astropy library 'fits.open'.
	hdulist = fits.open(fits_file)
	## Print out the basic info on structure of FITS file.
	# print hdulist.info()

	# print hdulist[0].header
	# print hdulist[1].header
	# print hdulist[2].header
	fits_data = hdulist[ext].data
	# print table
	cols = hdulist[ext].columns
	# print "Column names:", cols.names

	# print fits_data.field(col1)
	# print fits_data.field(col2)

	assert len(fits_data.field(col1)) == len(fits_data.field(col2))

	# table = np.column_stack((fits_data.field(col1), fits_data.field(col2)))

	ascii.write(fits_data, output=ascii_file, include_names=[col1, col2], formats='no_header', fill_include_names="")

	# ## Writing the columns of fits data to an ascii table
	# out = open(ascii_file, 'w')
	# out.write(table)
	# out.close()
	
	## End of function 'main'

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument('fits_file', help="The full path of the FITS file.")
	parser.add_argument('ext', type=int, help="The FITS extension of the data to dump.")
	parser.add_argument('col1', help="Column header for first column to dump.")
	parser.add_argument('col2', help="Column header for second column to dump.")
	parser.add_argument('ascii_file', help="The full path of the ASCII file to dump to.")
	args = parser.parse_args()

	main(args.fits_file, args.ext, args.col1, args.col2, args.ascii_file)
	
## End of program 'dump_columns.py'