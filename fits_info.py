import argparse
from astropy.io import fits 

"""
		fits_info.py
	
Prints HDU information, extension 1 header keywords, and extension 1 column names for a 
given FITS file. Using extension 1 here for RXTE event-mode data.

Arguments:
fits_file - str - The full path of the FITS file in question.

Written in Python 2.7 by A.L. Stevens, A.L.Stevens@uva.nl, 2014

All scientific modules imported above, as well as python 2.7, can be downloaded in the 
Anaconda package, https://store.continuum.io/cshop/anaconda/
I don't think argparse came with Anaconda, but I don't remember installing anything 
special to get it.
	
"""

def main(fits_file):
	pass
	## Opens the fits file using the Astropy library 'fits.open'.
	file_hdu = fits.open(fits_file)
	## Print out the basic info on structure of FITS file.
	print "\n", file_hdu.info()

	print file_hdu[0].header.keys
	# print file_hdu[0].header.keys
	# print file_hdu[1].header
	print "\n", file_hdu[1].header.keys
	print "\nColumns of data table in ext 1:", file_hdu[1].columns.names
	print ""

# 	table = file_hdu[1].data
# 	segment_rate = table[0:128].field(1).astype(int)
# 	print segment_rate
	
	print file_hdu[1].data
	
	file_hdu.close()
	
	## End of function 'main'

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument('fits_file', help="The full path of the FITS file in question.")
	args = parser.parse_args()

	main(args.fits_file)

## End of program 'fits_info.py'