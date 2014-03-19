import argparse
from astropy.io import fits 

"""
		get_keyword.py
	
Gets the a keyword value from a FITS header.

Use this in a bash script like so:
variable=$(python "$script_dir"/get_keyword.py "$filter_file" 1 KEY)
This finds the value of 'KEY' in the first ('1') extension of 'filter_file' and assigns 
it to 'variable'. Keyword does not seem to be case-sensitive.

Written in Python 2.7 by A.L. Stevens, A.L.Stevens@uva.nl, 2014

Passed: fits_file - str - The full path of the FITS file.
		ext - int - The FITS extension in which to search for the given keyword.
		keyword - str - The keyword for which you want the associated value.

Returns: nothing, but prints the keyword value

"""

def main(fits_file, ext, keyword):
	pass
	assert (ext >= 0 and ext <= 3)

	hdulist = fits.open(fits_file)

	print hdulist[ext].header[keyword]
	
	## End of function 'main'

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument('fits_file', help="The full path of the FITS file.")
	parser.add_argument('ext', type=int, help="The FITS extension in which to search for the given keyword.")
	parser.add_argument('keyword', help="The keyword for which you want the associated value.")
	args = parser.parse_args()

	main(args.fits_file, args.ext, args.keyword)

## End of program 'get_keyword.py'