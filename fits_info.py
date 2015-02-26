#!//anaconda/bin/python
import argparse
from astropy.io import fits 

__author__ = "Abigail Stevens"
__author_email__ = "A.L.Stevens@uva.nl"
__year__ = "2014-2015"

"""
		fits_info.py
	
Prints HDU information, header keywords, column names, and some data. Easily 
modifiable to print whatever you want!

Written in Python 2.7.
	
"""
################################################################################
if __name__ == "__main__":
	
	###########################
	## Parsing input arguments
	###########################
	
	parser = argparse.ArgumentParser(usage="python fits_info.py fits_file", \
description="Prints information about the specified fits file. Recommended for \
tables not images.")

	parser.add_argument('fits_file', help="The full path of the FITS file.")
	
	args = parser.parse_args()
	
	###############################################################
	## Opening the fits file using the Astropy library 'fits.open'
	###############################################################
	
	try:
		file_hdu = fits.open(args.fits_file)
	except IOError:
		print "\tERROR: File does not exist: %s" % args.fits_file
		exit()
	
	#########################################################
	## Printing out the basic info on structure of FITS file
	#########################################################
	
	print "\n", file_hdu.info()
	
	########################################################
	## Printing header keywords and column names
	## .header.keys outputs much cleaner than just .header
	########################################################
	
	print file_hdu[0].header.keys
	print "\n", file_hdu[1].header.keys
	print "\n", file_hdu[2].header.keys
	print "\nColumns of data table in ext 1:", file_hdu[1].columns.names
	print "\n"
	
	##########################################
	## Other things you may want to print out
	##########################################
	
# 	print file_hdu[1].data[0]
	print file_hdu[1].data.field(0)
# 	print file_hdu[1].data[-1]
# 	print "%.13f" % file_hdu[1].data[0].field(0)
# 	print file_hdu[1].data
# 	print file_hdu[2].columns.names
# 	print file_hdu[2].data	
# 	for col_name in file_hdu[1].columns.names:
# 		if 'Pcu2' in col_name and 'Spec' in col_name:
# 			print col_name
	
	#########################
	## Closing the fits file
	#########################
	
	file_hdu.close()
	
## End of program 'fits_info.py'

################################################################################
