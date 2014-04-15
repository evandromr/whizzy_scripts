import argparse
from astropy.io import fits 
from astropy.io import ascii
import numpy as np

"""
		dump_columns.py

Dumps two columns from a FITS file into an ASCII/txt/dat file.

Arguments:
fits_file - str - Name of input FITS file (full path).
ext - int - FITS extension of the data.
col1 - str - Column header of first column of data.
col2 - str - Column header of second column of data.
out_file - str - Name of output ASCII/txt/dat file.

Written in Python 2.7 by A.L. Stevens, A.L.Stevens@uva.nl, 2014

All scientific modules imported above, as well as python 2.7, can be downloaded in the 
Anaconda package, https://store.continuum.io/cshop/anaconda/
I don't think argparse came with Anaconda, but I don't remember installing anything 
special to get it.

"""

def main(fits_file, ext, col1, col2, out_file):
	pass
	
	assert (ext >= 0 and ext <= 3) # RXTE FITS files shouldn't have more than 3 exensions
	
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
	hdulist.close()

	print fits_data[1].field(col1)
	print fits_data[1].field(col2)

	assert len(fits_data.field(col1)) == len(fits_data.field(col2))

# 	table = np.column_stack((fits_data.field(col1), fits_data.field(col2)))
	print "Going to output"
# ## Writing the columns of fits data to an table
# 	out = open(out_file, 'w')
# 	for i in range(len(fits_data.field(col1))):
# 		out.write("%r\t%r\n" % (fits_data[i].field(col1), fits_data[i].field(col2)))
# 		if i % 1000 == 0:
# 			print "i = ", i
# 	out.write(table)
# 	out.close()
	
	ascii.write(fits_data, output=out_file, include_names=[col1, col2], formats='no_header')

	
	## End of function 'main'

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument('fits_file', help="The full path of the FITS file.")
	parser.add_argument('ext', type=int, help="The FITS extension of the data to dump.")
	parser.add_argument('col1', help="Column header for first column to dump.")
	parser.add_argument('col2', help="Column header for second column to dump.")
	parser.add_argument('out_file', help="The full path of the ASCII/txt/dat file to dump to.")
	args = parser.parse_args()

	main(args.fits_file, args.ext, args.col1, args.col2, args.out_file)
	
## End of program 'dump_columns.py'