import argparse
from astropy.io import fits 

"""
		fits_info.py
	
Prints HDU information, extension 1 header keywords, and extension 1 column names for a 
given FITS file. Using extension 1 here for RXTE event-mode data.

Arguments:
fits_file - The full path of the FITS file in question.

Written in Python 2.7 by A.L. Stevens, A.L.Stevens@uva.nl, 2014

All scientific modules imported above, as well as python 2.7, can be downloaded in the 
Anaconda package, https://store.continuum.io/cshop/anaconda/
	
"""

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('fits_file', help="The full path of the FITS file in question.")
	args = parser.parse_args()
	
	## Opens the fits file using the Astropy library 'fits.open'.
	file_hdu = fits.open(args.fits_file)
	
	## Print out the basic info on structure of FITS file.
	print "\n", file_hdu.info()
	
	# .header.keys outputs much cleaner than just .header
	print file_hdu[0].header.keys
	print "\n", file_hdu[1].header.keys
	print "\nColumns of data table in ext 1:", file_hdu[1].columns.names
	print ""
	
# 	print file_hdu[1].data[0]
# 	print "%.13f" % file_hdu[1].data[0].field(0)
# 	print file_hdu[1].data[1]
# 	print "%.13f" % file_hdu[1].data[1].field(0)
	
# 	print file_hdu[2].header.keys
# 	print file_hdu[2].data
	
# 	cols=file_hdu[1].columns.names
# 	for col in cols:
# 		if "pcu2" in col.lower():
# 			print col
# 			
# 	table = file_hdu[1].data
# 	segment_rate = table[0:128].field(1).astype(int)
# 	print segment_rate

# 	for i in range(0,10):
# 		print file_hdu[1].data[i].field(0)
	
	num_points=len(file_hdu[1].data.field(1))
# 	print file_hdu[1].data[num_points-1].field(0)

	file_hdu.close()
## End of program 'fits_info.py'