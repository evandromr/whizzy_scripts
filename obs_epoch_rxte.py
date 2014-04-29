import argparse
from astropy.io import fits

import get_keyword

"""
		obs_epoch_rxte.py


MANY WARNINGS:
1. This has not been rigorously tested (barely tested, really) and is not guaranteed.
2. It can only understand and parse 'DATE-OBS' keyword values with length 8 or length 19.
3. The times of crossover dates are not yet understood.
4. Returning '0' for the epoch means that something broke.
5. It currently cannot categorize 'crossover' dates

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
	obs_time = get_keyword.main(fits_file, 0, 'DATE-OBS')
	print obs_time
	print len(obs_time)
	year = -1
	month = -1
	day = -1
	if len(obs_time) == 8:
		day = int(obs_time[0:2])
		print day
		month = int(obs_time[3:5])
		print month
		year = obs_time[6:8]
		if year[0] == '9':
			year = int("19"+year)
		else:
			year = int("20"+year)
		print year
	elif len(obs_time) == 19:
		year = int(obs_time[0:4])
		print year
		month = int(obs_time[5:7])
		print month
		day = int(obs_time[8:10])
		print day
	else:
		print "\tERROR: Format of date is not understood."
		return 0
		
	assert (year >= 1995 and year <= 2012) ## Making sure that the date is actually when 
										   ##  RXTE was operational
	
	## Determining which epoch the date falls in
	
	if year = -1 or month = -1 or day = -1:
		print "\tERROR: Month, date, or year not properly assigned."
		return 0
	
	## This will be easier if I just use MJD...
	##  but need to convert TT to MJD which is too big a headache for now...
	
	if year == 1995: 
		return 1
		
	elif year == 1996:
		if month < 3:
			return 1
		elif month == 3:
			if day < 3: return 1
			elif day == 3: return 0 ## Need to check times
			else: return 2
		elif month == 4:
			if day < 15: return 2
			elif day == 15: return 0 ## Need to check times
			else: return 3
		else:
			return 3
		
	elif year == 1997 or year == 1998:
		return 3
	
	elif year == 1999:
		if month < 3:
			return 3
		elif month == 3:
			if day < 22: return 3
			elif day == 22: return 0 ## Need to check times
			else: return 4
		else: 
			return 4
		
	elif year == 2000:
		if month < 5:
			return 4
		elif month == 5:
			if day < 13: return 4
			elif day == 13: return 0 ## Need to check times
			else: return 5
		else:
			return 5
		
	else:
		return 5

	## End of function 'main'
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('fits_file', help="The full path of the FITS file.")
	args = parser.parse_args()

	epoch = main(args.fits_file)
	print "Epoch of observation: %d" % epoch
	
## End of program 'obs_epoch_rxte.py'