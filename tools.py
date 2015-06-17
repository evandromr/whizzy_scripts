#!//anaconda/bin/python
from astropy.io import fits
import numpy as np
import scipy as sp
import itertools
import argparse
import os
import subprocess
import warnings

__author__ = "Abigail Stevens, A.L.Stevens at uva.nl"

"""
This has not been rigorously tested.
There is no 'main' to this program, only helper methods to import and be called.

To assign the returned value to a variable in a bash script (in the directory 
containing tools.py, or with that directory added to PYTHONPATH) (where 'fun' 
is the function name and 'vars' are the variables to be passed in):
var=$(python -c "from tools import fun; print fun('$vars')")
Alternatively: python -c "from tools import fun; fun(vars)" >> a_file

Abigail Stevens, A.L.Stevens at uva.nl, 2013-2015

"""

################################################################################
def get_key_val(fits_file, ext, keyword):
	"""
	Gets the value of a keyword from a FITS header. Keyword does not seem to be 
	case-sensitive.

	Parameters
	----------
	fits_file : str
		The full path of the FITS file.
	
	ext : int
		The FITS extension in which to search for the given keyword.
	
	keyword : str
		The keyword for which you want the associated value.
			
	Returns
	-------
	any type
		Value of the given keyword.
	
	Raises
	------
	IOError if the input file isn't actually a FITS file.
	
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
	hdulist.close()
	
	return key_value


################################################################################
def get_fits_tab_val(fits_file, ext, row, col):
	"""
	Gets one value from a fits data table.
	
	Parameters
	----------
	fits_file : str
		The full path of the FITS file.
		
	ext : int
		The FITS extension from which to get the data.
		
	row : int 
		The row of the data table.
			
	col : int
		The column of the data table.
	
	Returns
	-------
	any type
		Value at data[row][col].
	
	Raises
	------
	IOError if the input file isn't actually a FITS file. 
	
	"""
	ext=np.int8(ext)
	row=np.int(row)
	col=np.int(col)
	try:
		hdulist = fits.open(fits_file)
	except IOError:
		print "\tERROR: File does not exist: %s" % fits_file
		exit()
	tab_value = hdulist[ext].data[row][col]
	hdulist.close()
	
	return tab_value


################################################################################
def check_mode(file_list, datamode_key):
	"""
	Checks that the data mode of each file in file_list matches datamode_key.
	Designed for RXTE FITS files.
	
	Parameters
	----------
	file_list : string
		List of files of which to check the data mode. 
	
	datamode_key : string
		The name of the data mode, as a FITS header keyword.
	
	Returns
	-------
	list of strings
		List of files from file_list that are in datamode_key.
	
	Raises
	------
	Exception if the file list doesn't exist.
	
	Exception if the list is empty.
	
	"""
	if not os.path.isfile(file_list):
		raise Exception("ERROR: File list does not exist.")
		
	input_files = [line.strip() for line in open(file_list)]
	
	if not files:  ## If it's an empty list
		raise Exception("ERROR: No files in the list %s" % file_list)
		
	good_files = []
	for file in input_files:
		if datamode_key in get_key_val(file, 1, 'DATAMODE'):
			good_files.append(file)
			print file
	return good_files


################################################################################
def compute_obs_time(file_list):
	"""
	Computes the total observation time of a list of observation FITS files, in
	seconds.
	
	Parameters
	----------
	file_list : str
		Name of file with list of fits files of the observations.
	
	Returns
	-------
	float
		The total observation time.
		
	Raises
	------
	Exception if the file list doesn't exist.
	
	Exception if the list is empty.
	
	"""

	if not os.path.isfile(file_list):
		raise Exception("ERROR: File list does not exist.")
		
	input_files = [line.strip() for line in open(file_list)]
	
	if not files:  ## If it's an empty list
		raise Exception("ERROR: No files in the list %s" % file_list)
		
	total_time = 0
	
	for file in input_files:
		time = float(get_key_val(file, 1, 'ONTIME'))
		total_time += time

	return total_time  ## in seconds
			## should double check units of times in FITS header

	
################################################################################
def read_obs_time(in_file):
	"""
	Read the total observation time from the header of a text file.
	
	Parameters
	----------
	in_file : str
		Name of (ASCII/txt/dat) input file with exposure time in the header.
		
	Returns
	-------
	float
		The exposure time of the observation.
	
	Raises
	------
	Exception if the input file doesn't exist.
	
	"""
	if not os.path.isfile(in_file):
		raise Exception("ERROR: File does not exist for tools.read_obs_time.")
		
	with open(in_file, 'r') as f:
		for line in f:
			if line[0].strip() == "#":
				if "xposure" in line.strip():
					line = line.strip().split()
					obs_time = float(line[-2])
					return obs_time
			else:
				return 0.0


################################################################################
def power_of_two(num):
	"""
	Checks if a positive integer is a power of 2 (1 <= num < 2147483648).
	
	Parameters
	----------
	num : int
		The number in question.
	
	Returns
	-------
	bool
		True if 'num' is a power of two, False if 'num' is not.
	
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


################################################################################
def type_power_of_two(num):
	"""
	Checks if an input is a power of 2 (1 <= num < 2147483648), as an argparse 
	type.
	
	Parameters
	----------
	num : int
		The number in question.
	
	Returns
	-------
	int
		n, if it's a power of two 
	
	Raises
	------
	ArgumentTypeError if n isn't a power of two.
	
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
	raise argparse.ArgumentTypeError(message)


################################################################################
def type_positive_float(num):
	"""
	Checks if an input is a positive float, as an argparse type.
	
	Parameters
	----------
	num : int, long, float, or double
		The number in question.
	
	Returns
	-------
	float
		n, if it's a positive float
	
	Raises
	------
	ArgumentTypeError if n isn't a real number or a positive float.
	
	"""
	try:
		n = float(num)
	except ValueError or TypeError:
		message = "%d is not a real number." % n
		raise argparse.ArgumentTypeError(message)
		
	if n >= 0:
		return n
	else:
		message = "%d is not a positive float." % n
		raise argparse.ArgumentTypeError(message)


################################################################################
def type_positive_int(num):
	"""
	Checks if an input is a positive integer, as an argparse type.
	
	Parameters
	----------
	num : int, long, float, or double
		The number in question.
	
	Returns
	-------
	int
		n, if it's a positive integer
	
	Raises
	------
	ArgumentTypeError if n isn't a real number or a positive integer.
	
	"""
	try:
		n = int(num)
	except ValueError or TypeError:
		message = "%d is not a real number." % n
		raise argparse.ArgumentTypeError(message)
		
	if n >= 0:
		return n
	else:
		message = "%d is not a positive integer." % n
		raise argparse.ArgumentTypeError(message)

	
################################################################################
def pairwise(iterable):
	"""
	s -> (s0,s1), (s1,s2), (s2, s3), ...
	From https://docs.python.org/2/library/itertools.html#recipes
	Used when reading lines in the file so I can peek at the next line.
	
	Parameters
	----------
	an iterable, like a list or an open file
	
	Returns
	-------
	The next two items in an iterable, like in the example a few lines above.
	
	"""
	a, b = itertools.tee(iterable)
	next(b, None)
	return itertools.izip(a, b)
	
	
################################################################################
def replace_key_val(fits_file, ext, keyword, value):
	"""
	Replaces the value of a keyword in a FITS header with a given value.
	
	Parameters
	----------
	fits_file : str
		The full path of the FITS file.
		
	ext : int
		The FITS extension in which you want to replace the keyword value.
				
	keyword : str
		The header keyword of the value you want to replace.
			
	value : any type
		The new value for the header keyword.
	
	Returns
	-------
	nothing
	
	Raises
	------
	IOError if the input file isn't a FITS file.
	
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


################################################################################
def time_ordered_list(file_list):
	"""
	Takes an input file containing a list of fits files, gets the start time of 
	each file, sorts the files based on listed start time (from keyword TSTART),
	applies the same sort to the file names, and prints the sorted file names.
	
	Parameters
	----------
	file_list : str
		Name of a text file that is a list of FITS files, with one FITS file 
		per line. 
	
	Returns
	-------
	nothing
	
	Raises
	------
	Exception if the file list doesn't exist.
	
	Exception if the list is empty.
	
	"""
	if not os.path.isfile(file_list):
		raise Exception("ERROR: File list does not exist.")
    	
	files = [line.strip() for line in open(file_list)]
	if not files:  ## If it's an empty list
		raise Exception("ERROR: No files in the list %s" % file_list)
		
	times = [float(get_key_val(fits_file, 1, 'TSTART')) for fits_file in files]
	sorted_files = [x for y,x in sorted(zip(times,files))]
	for filename in sorted_files: print filename
		
	
################################################################################
def obs_epoch_rxte(fits_file):
	"""
	Determines the epoch of an RXTE observation. Returns 0 if an error occurred.
	Future update: use MJD.

	WARNING:
	1. This has not been rigorously tested (barely tested, really) and is not 
		guaranteed.
	2. It can only understand and parse 'DATE-OBS' keyword values with length 8
		or length 19.
	3. I'm interpreting the 'stop time' listed as the start time of the next 
		epoch.
	
	Parameters
	----------
	fits_file : str
		Name of an RXTE observation FITS file (full path).
	
	Returns
	-------
	int 
		The RXTE observation epoch of the FITS file.
	
	Raises
	------
	Exception if the 'DATE-OBS' keyword value isn't 8 or 19 characters in 
	length.
	
	Exception if it couldn't read the month, day, year, hour, or minute of the 
	'DATE-OBS' keyword value.
	
	UserWarning if it goes out to minute precision in determining the 
	observation epoch, since it may not be correct.
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
		raise Exception("ERROR: Month, day, year, hour, or minute not properly assigned.")
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
					warning.warn("Using minute precision to determine obs epoch. May not be correct.")
					if minute < 33: return 1
					else: return 2
		elif month == 4:
			if day < 15: return 2
			elif day > 15: return 3
			else: 
				if hour < 23: return 2
				elif hour > 23: return 3
				else:
					warning.warn("Using minute precision to determine obs epoch. May not be correct.")
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
					warning.warn("Using minute precision to determine obs epoch. May not be correct.")
					if minute < 37: return 3
					else: return 4
		else: 
			return 4
		
	elif year == 2000:
		if month < 5:
			return 4
		elif month == 5:
			if day < 13: return 4
			elif day >= 13: return 5  ## since it changes at 00:00
		else:
			return 5
		
	else:
		return 5


################################################################################
def make_2Dlightcurve(time, energy, n_bins, detchans, dt, seg_start_time):
    """
    Populates a segment of a light curve with photons from the event list.

    Parameters
    ----------
    time : np.array of floats
    	Times at which a photon is detected (in TIMEZERO-corrected RXTE clock 
    	time or whatever it is).
    
    energy : np.array of ints
    	Energy channel in which the photon is detected.
    
    n_bins : int
    	Number of bins per segment of light curve.
        
    detchans : int
    	Number of detector energy channels.
    
    dt : float
    	Desired timestep between bins in n_bins, in seconds.
    
    seg_start_time : float
    	Start time of the segment, in TIMEZERO-corrected RXTE clock time (or 
    	whatever it is).

    Returns
    -------
    2D np.array of ints
    	The populated 2-dimensional light curve, with time as one axis and 
    	energy channel as the other. In units of count rate.

    """

    ## Ranges need to be amount+1 here, because of how 'histogram2d' bins the 
    ## values
    t_bin_seq = np.arange(n_bins + 1) * dt + seg_start_time
    e_bin_seq = np.arange(detchans + 1)

    lightcurve_2d, t_bin_edges, e_bin_edges = np.histogram2d(time, energy,
        bins=[t_bin_seq, e_bin_seq])

    lightcurve_2d /= dt  ## Need /dt to have units of count rate

    lightcurve_2d = lightcurve_2d.astype(int)  ## 1/dt is an int, so we can make
                                               ## 'lightcurve_2d' be ints here.

    ## lightcurve[time_bin][energy_channel]
    ## lightcurve[:,energy_channel]

    return lightcurve_2d


################################################################################
def make_1Dlightcurve(time, n_bins, seg_start, seg_end):
    """
    Populates a segment of a light curve with photons from the event list.

    Parameters
    ----------
    time : np.array of floats
    	Times at which a photon is detected (in TIMEZERO-corrected RXTE clock 
    	time or whatever it is).
    
    n_bins : int
    	Number of bins per segment of light curve.
    
    dt : float
    	Desired timestep between bins in n_bins, in seconds.
    
    seg_start_time : float
    	Start time of the segment, in TIMEZERO-corrected RXTE clock time (or
    	whatever it is).
    
    seg_end_time : float
    	End time of the segment, in TIMEZERO-corrected RXTE clock time (or 
    	whatever it is).

    Returns
    -------
    1D np.array of ints
    	The populated 1-dimensional light curve, with time as the axis. This 
    	lightcurve is "bolometric", i.e. ignoring energy bins. In units of 
    	count rate.

    """

    ## Ranges need to be amount+1 here, because of how 'historgram' bins the 
    ## values
    t_bin_seq = np.linspace(seg_start, seg_end, num=n_bins+1)  ## defining time
    														   ## bin edges
    dt = t_bin_seq[1]-t_bin_seq[0]
    # print dt

    lightcurve_1d, t_bin_edges = np.histogram(time, bins=t_bin_seq)

    lightcurve_1d /= dt  ## Need /dt to have units of count rate

    lightcurve_1d = lightcurve_1d.astype(int)  ## 1/dt is an int, so we can make
                                               ## 'lightcurve_1d' be ints here.

    return lightcurve_1d


################################################################################
def make_pulsation(n_bins, dt, freq, amp, mean, phase):
	"""
	Make a simulated time series with a coherent pulsation.
	
	Parameters
	----------
	n_bins : int
		Number of time bins per segment of light curve.
	
	dt : float
		Desired timestep between bins (or per time bin), in seconds.
	
	freq : float
		Desired frequency of the pulsation, in Hz.
	
	amp : float
		Desired amplitude of pulsation.
		
	mean : float
		Desired mean value of pulsation.
		
	phase : float
		Desired phase offset of pulsation from a sine wave, in radians.
		
		
	Returns
	-------
	np.array of floats
		One segment of the pulsation light curve, with an amplitude per n_bin.
	
	"""
	binning = 10
	period = 1.0 / freq  ## in seconds
	bins_per_period = period / dt
	tiny_bins = np.arange(0, n_bins, 1.0/binning)
	smooth_sine = amp * np.sin(2.0 * np.pi * tiny_bins / bins_per_period + \
		phase) + mean
	time_series = np.mean(np.array_split(smooth_sine, n_bins), axis=1)
	
	return time_series


################################################################################
def make_col_list(fits_file, ext, with_words, without_words):
	"""
	Makes a list of column names with specific words or phases and without
	specific words or phrases.
	
	"""
	pass
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


################################################################################
def no_duplicates(txt_file):
	"""
	Reads in lines from a text file, removes duplicates (by using 'set'), and 
	prints the non-duplicate lines back to the same text file, overwriting the
	previous information.
	
	Parameters
	----------
	txt_file : str
		Name of the text file containing the list to check for duplicates; one 
		entry per line.
	
	Returns
	-------
	nothing
	
	Raises
	------
	Exception if the text file doesn't exist.
	
	Exception if the text file is empty.
	
	"""
	if not os.path.isfile(txt_file):
		raise Exception("ERROR: Duplicates file does not exist.")
		
	items = [line.strip() for line in open(txt_file)]
	
	if not items:  ## If it's an empty list
		raise Exception("ERROR: No items in the duplicate list.")
    	
	no_duplicate_items = list(set(items))
	with open(txt_file, 'w') as out:	
		for thing in no_duplicate_items: 
			out.write(thing+"\n")


################################################################################
def remove_obsIDs(totallist_file, removelist_file):
	"""
	Makes a copy of the original list file, removes elements of the list, and 
	prints back to the original 'total list' file (overwriting it).
	
	
	Or use the following bash commands with awk:
	
	for element in $( cat "$file1" ); do
		awk "!/$element/" $file2 > dump.txt && mv dump.txt $file2
	done
	
	Parameters
	----------
	totallist_file : str
		Name of file containing a list of all the obsIDs, one per line.
	
	removelist_file : str
		Name of file containing a list of the obsIDs to remove from the list, 
		one per line.
	
	Returns
	-------
	nothing
	
	Raises
	------
	Exception if the list of all obsIDs doesn't exist.
	
	Exception if the list of obsIDs to remove doesn't exist.
	
	Exception if list of all obsIDs is empty.
	
	Exception if list of obsIDs to remove is empty.
	
	"""
	if not os.path.isfile(totallist_file):
		raise Exception("ERROR: Total obsID list does not exist.")
	if not os.path.isfile(removelist_file):
		raise Exception("ERROR: List of obsIDs to remove does not exist.")
	
	cp_totallist = os.path.splitext(totallist_file)[0]+"_all.lst"
	subprocess.call(["cp", totallist_file, cp_totallist])
	
	good_obsIDs = [line.strip() for line in open(totallist_file)]
	bad_obsIDs = [line.strip() for line in open(removelist_file)]
	
	if not good_obsIDs:  ## If it's an empty list
		raise Exception("ERROR: No files in the eventlist list.")
	if not bad_obsIDs:  ## If it's an empty list
		raise Exception("ERROR: No files in the eventlist list.")
	
	for item in bad_obsIDs:
		good_obsIDs.remove(item)
	
	with open(totallist_file, 'w') as out:
		for thing in good_obsIDs: 
			out.write(thing+"\n")
	

################################################################################
if __name__ == '__main__':

	print "\n\t\t tools.py"
	print "There is no 'main' to this program, only helper methods to import "\
			"and be called.\n"

################################################################################
	