import argparse
from astropy.io import fits 

"""
		get_keyword.py
	
Gets the value of a keyword from a FITS header.

Use this in a bash script like so:
variable=$(python "$script_dir"/get_keyword.py "$filter_file" 1 KEYNAME 1)
This finds the value of 'KEY' in the first ('1') extension of 'filter_file' and assigns 
it to 'variable'. Keyword does not seem to be case-sensitive.

Both prints and returns the value, for use in bash scripts like example above or 
importing and calling in a python script. For calling in a python script, set print_it 
to False.

Arguments:
fits_file - str - The full path of the FITS file.
ext - int - The FITS extension in which to search for the given keyword.
keyword - str - The keyword for which you want the associated value.
print_it - int - 1 if you want to print the value (like with a bash script), 0 if 
	you don't want to print the value (like with a python script).


Written in Python 2.7 by A.L. Stevens, A.L.Stevens@uva.nl, 2014

All scientific modules imported above, as well as python 2.7, can be downloaded in the 
Anaconda package, https://store.continuum.io/cshop/anaconda/

"""

##################################
def main(fits_file, ext, keyword):
	pass
	assert (ext >= 0 and ext <= 3)
	hdulist = fits.open(fits_file)
	key_value = hdulist[ext].header[keyword]
	hdulist.close()
	return key_value
	## End of function 'main'

##########################
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument('fits_file', help="The full path of the FITS file.")
	parser.add_argument('ext', type=int, help="The FITS extension in which to search for the given keyword.")
	parser.add_argument('keyword', help="The keyword for which you want the associated value.")
	parser.add_argument('print_it', type=int, help="1 if you want to print the value, 0 if you don't.")
	args = parser.parse_args()
	assert (args.print_it == 1 or args.print_it == 0)
	
	val = main(args.fits_file, args.ext, args.keyword)
	
	if args.print_it == 1:
		print val

## End of program 'get_keyword.py'