#!//anaconda/bin/python
from astropy.io import fits
import numpy as np
import scipy as sp
import itertools
import argparse

__author__ = "Abigail Stevens"
__author_email__ = "A.L.Stevens@uva.nl"
__year__ = "2013-2015"

"""
		tools.py

This has not been rigorously tested.
There is no 'main' to this program, only helper methods to import and be called.

To assign the returned value to a variable in a bash script (in the directory 
containing tools.py, or with that directory added to PYTHONPATH) (where 'fun' 
is the function name and 'vars' are the variables to be passed in):
var=$(python -c "from tools import fun; print fun('$vars')")
Alternatively: python -c "from tools import fun; fun(vars)" >> a_file

Written in Python 2.7.

"""

###############################################################################
def get_key_val(fits_file, ext, keyword):
	"""
			get_key_val
	
	Gets the value of a keyword from a FITS header. Keyword does not seem to be 
	case-sensitive.

	Passed: fits_file - str - The full path of the FITS file.
			ext - int - The FITS extension in which to search for the given 
				keyword.
			keyword - str - The keyword for which you want the associated value.
			
	Returns: key_value - any - Value of the given keyword.
	
	"""
	
	ext = np.int8(ext)
	assert (ext >= 0 and ext <= 2)
	keyword = str(keyword)
	
	try:
		hdulist = fits.open(fits_file)
	except IOError:
		print "\tERROR: File does not exist: %s" % fits_file
		exit()
		
	key_value = hdulist[ext].header[keyword]
# 	print key_value
	hdulist.close()
	
	return key_value
## End of function 'get_key_val'


###############################################################################
def check_mode(file_list, datamode_key):
	"""
			check_mode
	"""
	input_files = [line.strip() for line in open(file_list)]
	good_files = []
	for file in input_files:
		if datamode_key in get_key_val(file, 1, 'DATAMODE'):
			good_files.append(file)
			print file
	return good_files
	
## End of 'check mode'


###############################################################################
def compute_obs_time(file_list):
	"""
			compute_obs_time
		
	Computes the total observation time of a list of observation FITS files, in
	seconds.
	
	Passed: file_list - str - Name of file with list of fits files of the 
				observations.
	
	Returns: total_time - float - The total observation time.
	
	"""

	input_files = [line.strip() for line in open(file_list)]
	total_time = 0
	
	for file in input_files:
		time = float(get_key_val(file, 1, 'ONTIME'))
		total_time += time

	return total_time # in seconds
	## but can double check units of times in FITS header
## End of function 'compute_obs_time'

	
###############################################################################
def read_obs_time(in_file):
	"""
		
		read_obs_time
		
	Read the total observation time from the header of a text file.
	
	Passed: in_file - str - Name of (ASCII/txt/dat) input file with exposure 
				time in the header.
		
	Returns: nothing
	
	"""
	
	with open(in_file, 'r') as f:
		for line in f:
			if line[0].strip() == "#":
				if "xposure" in line.strip():
					line = line.strip().split()
# 					print line
					obs_time = float(line[-2])
					return obs_time
			else:
				return 0.0
## End of function 'read_obs_time'


###############################################################################
def power_of_two(num):
	"""
			power_of_two
			
	Checks if an input is a power of 2 (1 <= num < 2147483648).
	
	Passed: num - int - The number in question.
	
	Returns: bool - 'True' if 'num' is a power of two, 'False' if 'num' is not.
	
	"""
	n = int(num)
	x = 2
	assert n > 0, "ERROR: Number must be positive."
	
	if n == 1:
		return True
	else: 
		while x < n and x < 2147483648:
			x *= 2
		return n == x
## End of function 'power_of_two'


###############################################################################
def type_power_of_two(num):
	"""
			type_power_of_two
			
	Checks if an input is a power of 2 (1 <= num < 2147483648), as an argparse 
	type.
	
	Passed: num - The number in question.
	
	Returns: n if it's a power of two, ArgumentTypeError if it isn't.
	
	"""
	n = int(num)
	x = 2
	assert n > 0

	if n == 1:
		return n
	else: 
		while x <= n and x < 2147483648:
			if n == x:
				return n
			x *= 2

	message = "%d is not a power of two." % n
# 	print message
	raise argparse.ArgumentTypeError(message)
## End of function 'type_power_of_two'


###############################################################################
def type_positive_float(num):
	"""
			type_positive_float
			
	Checks if an input is a positive float, as an argparse type.
	
	Passed: num - The number in question.
	
	Returns: n if it's a positive float, Argument Type Error if it isn't.
	
	"""
	n = float(num)
	if n >= 0:
		return n
	else:
		message = "%d is not a positive float." % n
		raise argparse.ArgumentTypeError(message)
## End of function 'type_positive_float'

	
###############################################################################
def pairwise(iterable):
	"""
			pairwise
	
	s -> (s0,s1), (s1,s2), (s2, s3), ...
	From https://docs.python.org/2/library/itertools.html#recipes
	Used when reading lines in the file so I can peek at the next line.
	
	Passed: an iterable, like a list or an open file
	
	Returns: the next two items in an iterable, like in the example a few lines
				above.
	
	"""
	a, b = itertools.tee(iterable)
	next(b, None)
	return itertools.izip(a, b)
## End of function 'pairwise'
	
	
###############################################################################
def replace_key_val(fits_file, ext, keyword, value):
	"""
			replace_key_val
			
	Replaces the value of a keyword in a FITS header with a given value.
	
	Passed: fits_file - str - Name of a FITS file.
			ext - int - The FITS extension in which you want to replace the 
				keyword value.
			keyword - str - The keyword of the value you want to replace.
			value - any - The new value for the FITS header keyword.
	
	Returns: nothing
	
	"""
	ext = np.int8(ext)
	assert (ext >= 0 and ext <= 2)
	keyword = str(keyword)
	
	try:
		hdu = fits.open(fits_file, mode='update')
	except IOError:
		print "\tERROR: File does not exist: %s" % fits_file
		exit()
	
	hdu[ext].header[keyword] = value
	hdu.flush()
	hdu.close()
	return
## End of function 'replace_key_val'


###############################################################################
def time_ordered_list(file_list):
	"""
			time_ordered_list
			
	Takes an input file containing a list of fits files, gets the start time of 
	each file, sorts the files based on listed start time (from keyword TSTART),
	applies the same sort to the file names, and prints the sorted file names.
	
	Passed: file_list - str - Name of a list of FITS files.
	
	Returns: nothing, but prints
	
	"""
	files = [line.strip() for line in open(file_list)]
	times = [float(get_key_val(fits_file, 1, 'TSTART')) for fits_file in files]
# 	for (time, filename) in zip(times, files): print time," ",filename
	sorted_files = [x for y,x in sorted(zip(times,files))]
# 	for time in sorted(times): print time
	for filename in sorted_files: print filename
	return
## End of function 'time_ordered_list'
	
	
###############################################################################
def obs_epoch_rxte(fits_file):
	"""
			obs_epoch_rxte
			
	Determines the epoch of an RXTE observation. Returns 0 if an error occurred.
	Future update: use MJD.

	WARNING:
	1. This has not been rigorously tested (barely tested, really) and is not 
		guaranteed.
	2. It can only understand and parse 'DATE-OBS' keyword values with length 8
		or length 19.
	3. I'm interpreting the 'stop time' listed as the start time of the next 
		epoch.
	
	Passed: fits_file - str - Name of an RXTE observation FITS file.
	
	Returns: epoch - int - The RXTE observation epoch of the FITS observation 
				file.
	
	"""
	
	obs_time = get_key_val(fits_file, 0, 'DATE-OBS')
# 	print "DATE-OBS =", obs_time
# 	print "Length of DATE-OBS =", len(obs_time)
	year = -1
	month = -1
	day = -1
	hour = -1
	minute = -1
	
	if len(obs_time) == 19:
		year = int(obs_time[0:4])
		month = int(obs_time[5:7])
		day = int(obs_time[8:10])
		hour = int(obs_time[11:13])
		minute = int(obs_time[14:16])
# 		print "Year =", year
# 		print "Month =", month
# 		print "Day =", day
# 		print "Hour =", hour
# 		print "Minute =", minute
		
	elif len(obs_time) == 8:
		day = int(obs_time[0:2])
		month = int(obs_time[3:5])
		year = obs_time[6:8]
		if year[0] == '9': year = int("19"+year)
		else: year = int("20"+year)
# 		print "Day =", day
# 		print "Month =", month
# 		print "Year =", year
		hour = 0
		minute = 0
	else:
		raise Exception("ERROR: Format of date is not understood.")
		return 0
		
	assert (year >= 1995 and year <= 2012) ## Making sure the date is actually 
										   ## when RXTE was operational
	if (year is -1) or \
		(month is -1) or \
		(day is -1) or \
		(hour is -1) or \
		(minute is -1):
		raise Exception("ERROR: Month, date, year, hour, or minute not properly assigned.")
		return 0
	
	## Determining in which epoch the date falls
	
	if year == 1995: 
		return 1
		
	elif year == 1996:
		if month < 3:
			return 1
		elif month == 3:
			if day < 3: return 1
			elif day > 3: return 2 
			else: 
				if hour < 18: return 1
				elif hour > 18: return 2
				else:
					print "\n\tWARNING: Down to the minute in determining obs epoch. May not be correct."
					if minute < 33: return 1
					else: return 2
		elif month == 4:
			if day < 15: return 2
			elif day > 15: return 3
			else: 
				if hour < 23: return 2
				elif hour > 23: return 3
				else:
					print "\n\tWARNING: Down to the minute in determining obs epoch. May not be correct."
					if minute < 5: return 2
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
			elif day > 22: return 4
			else:
				if hour < 17: return 3
				elif hour > 17: return 4
				else:
					print "\n\tWARNING: Down to the minute in determining obs epoch. May not be correct."
					if minute < 37: return 3
					else: return 4
		else: 
			return 4
		
	elif year == 2000:
		if month < 5:
			return 4
		elif month == 5:
			if day < 13: return 4
			elif day >= 13: return 5  # since it changes at 00:00
		else:
			return 5
		
	else:
		return 5
## End of function 'obs_epoch_rxte'


################################################################################
def make_lightcurve(time, energy, n_bins, dt, seg_start_time):
    """
            make_lightcurve

    Populates a segment of a light curve with photons from the event list.

    Passed: time - Times at which a photon is detected.
            energy - Energy channel in which the photon is detected.
            n_bins - Number of bins per segment of light curve.
            dt - Desired timestep between bins in n_bins, in seconds.
            seg_start_time - Starting time of the segment, in TIMEZERO-corrected
                RXTE clock time (or whatever it is).

    Returns: lightcurve_2d - The populated 2-dimensional light curve. This one
                has split up the light curves for each energy channel. In units 
                of count rate.
             lightcurve_1d - The populated 1-dimensional light curve. This one
                is "bolometric", ignoring energy bins. In units of count rate.

    """

    ## Ranges need to be amount+1 here, because of how 'historgram' and
    ## 'histogram2d' bin the values
    t_bin_seq = np.arange(n_bins + 1) * dt + seg_start_time
    e_bin_seq = np.arange(0, 65)

    lightcurve_2d, t_bin_edges, e_bin_edges = np.histogram2d(time, energy,
        bins=[t_bin_seq, e_bin_seq])
    lightcurve_1d, t_bin_edges = np.histogram(time, bins=t_bin_seq)

    lightcurve_2d /= dt  # Need /dt to have units of count rate
    lightcurve_1d /= dt  # Need /dt to have units of count rate

    lightcurve_2d = lightcurve_2d.astype(int)  # 1/dt is an int, so we can make
                                               # 'lightcurve_2d' be ints here.
    lightcurve_1d = lightcurve_1d.astype(int)  # 1/dt is an int, so we can make
                                               # 'lightcurve_1d' be ints here.

    ## lightcurve[time_bin][energy_channel]
    ## lightcurve[:,energy_channel]

    return lightcurve_2d, lightcurve_1d

## End of function 'make_lightcurve'


###############################################################################
def make_pulsation(n_bins, dt, freq, amp, mean, phase):
	"""
			make_pulsation
			
	Summary.
	
	Passed:
	
	Returns:
	
	"""
	binning = 10
	period = 1.0 / freq  # in seconds
	bins_per_period = period / dt
	tiny_bins = np.arange(0, n_bins, 1.0/binning)
	smooth_sine = amp * np.sin(2.0 * np.pi * tiny_bins / bins_per_period + phase) + mean
	time_series = np.mean(np.array_split(smooth_sine, n_bins), axis=1)
	
	return time_series
## End of function 'make_pulsation'


###############################################################################
def make_col_list(fits_file, ext, with_words, without_words):
	"""
			make_col_list
			
	"""
	
# 	with_words=with_words.strip().split()
# 	print with_words
# 	without_words=without_words.strip().split()
# 	print without_words
# 	
# 	file_hdu = fits.open(fits_file)
# 	all_cols = file_hdu[ext].columns.names
# 		
# 	for a in with_words:
# 		cols = filter(lambda x: a in x, all_cols)
# 	print cols
# 	for b in without_words:
# 		temp = filter(lambda x: b in x, cols)
# 		print temp
# # 		cols.remove(temp)
# 	print cols
# 	
# 	file_hdu.close()
	return
## End of function 'make_col_list'


###############################################################################
def no_duplicates(txt_file):
	"""
			no_duplicates
			
	"""
	items = [line.strip() for line in open(txt_file)]

	no_duplicate_items = list(set(items))
	with open(txt_file, 'w') as out:	
		for thing in no_duplicate_items: 
			out.write(thing+"\n")
	return
## End of function 'no_duplicates'


###############################################################################
if __name__ == '__main__':

	print "\n\t\t tools.py"
	print "There is no 'main' to this program, only helper methods to import and be called.\n"
	