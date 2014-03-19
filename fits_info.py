import argparse
from astropy.io import fits 

"""
		fits_info.py
	
Prints HDU list information, extension 1 header keywords, and extension 1 column names 
for a given FITS file. Using extension 1 here for RXTE data.

Written in Python 2.7 by A.L. Stevens, A.L.Stevens@uva.nl, 2014

Passed: fits_file - str - The full path of the FITS file.

Returns: nothing, but prints lots of stuff
	
"""

def main(fits_file):
	pass
	## Opens the fits file using the Astropy library 'fits.open'.
	hdulist = fits.open(fits_file)
	## Print out the basic info on structure of FITS file.
	print "\n", hdulist.info()

	# print hdulist[0].header
	# print hdulist[0].header.keys
	# print hdulist[1].header
	print "\n", hdulist[1].header.keys
	print "\nColumns of data table:", hdulist[1].columns.names
	print ""

	# print hdulist[2].header

	# table = hdulist[1].data
	# print table.field('RATE')
	
	## End of function 'main'

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument('fits_file', help="The full path of the FITS file.")
	args = parser.parse_args()

	main(args.fits_file)

## End of program 'fits_info.py'