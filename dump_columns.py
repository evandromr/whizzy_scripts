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

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument('fits_file', help="The full path of the FITS file.")
	parser.add_argument('ext', type=int, help="The FITS extension of the data to dump.")
	parser.add_argument('col1', help="Column header for first column to dump.")
	parser.add_argument('col2', help="Column header for second column to dump.")
	parser.add_argument('out_file', help="The full path of the ASCII/txt/dat file to dump to.")
	args = parser.parse_args()

	assert (args.ext >= 0 and args.ext <= 3) # RXTE FITS files shouldn't have more than 3 exensions
	
	fits_hdu = fits.open(args.fits_file)
	# print fits_hdu.info()

	# print fits_hdu[0].header
	# print fits_hdu[1].header
	# print fits_hdu[2].header
	fits_data = fits_hdu[args.ext].data
	cols = fits_hdu[args.ext].columns
	# print "Column names:", cols.names
	fits_hdu.close()

# 	print fits_data[1].field(args.col1)
# 	print fits_data[1].field(args.col2)

	assert len(fits_data.field(args.col1)) == len(fits_data.field(args.col2))

# 	table = np.column_stack((fits_data.field(args.col1), fits_data.field(args.col2)))
# 	print "Going to output"
# ## Writing the columns of fits data to an table
# 	out = open(args.out_file, 'w')
# 	for i in range(len(fits_data.field(args.col1))):
# 		out.write("%r\t%r\n" % (fits_data[i].field(args.col1), fits_data[i].field(args.col2)))
# 	out.write(table)
# 	out.close()
	
	ascii.write(fits_data, output=args.out_file, include_names=[args.col1, args.col2], formats='no_header')
	
## End of program 'dump_columns.py'