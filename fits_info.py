#!//anaconda/bin/python
import argparse
from astropy.io import fits 

"""
		fits_info.py
	
Prints HDU information, header keywords, column names, and some data. Easily 
modifiable

Arguments:
fits_file - The full path of the FITS file in question.

Written in Python 2.7 by A.L. Stevens, A.L.Stevens@uva.nl, 2014-2015
	
"""
################################################################################
if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('fits_file', help="The full path of the FITS file.")
	args = parser.parse_args()
	
	## Opens the fits file using the Astropy library 'fits.open'.
	file_hdu = fits.open(args.fits_file)
	
	## Print out the basic info on structure of FITS file.
	print "\n", file_hdu.info()
	
	# .header.keys outputs much cleaner than just .header
	print file_hdu[0].header.keys
	print "\n", file_hdu[1].header.keys
	print "\n", file_hdu[2].header.keys
	print "\nColumns of data table in ext 1:", file_hdu[1].columns.names
# 	print "\n", file_hdu[2].header.keys
	print "\n"
# 	print file_hdu[1].data[0]
	print file_hdu[1].data.field(0)
# 	print file_hdu[1].data[-1]
# 	print "%.13f" % file_hdu[1].data[0].field(0)
# 	print file_hdu[1].data
# 	print "%.21f" % file_hdu[1].data[0].field(0)
# 	print "%.21f" % file_hdu[1].data[-1].field(0)
	
# 	for col_name in file_hdu[1].columns.names:
# 		if 'Pcu2' in col_name and 'Spec' in col_name:
# 			print col_name

	
# 	print file_hdu[2].header.keys
	print file_hdu[2].columns.names
	print file_hdu[2].data

	file_hdu.close()
	
## End of program 'fits_info.py'

################################################################################
