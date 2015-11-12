# whizzy_scripts

Whizzy little scripts I write for fun, mostly to help with research, in 
Python 2.7. 

Scientific modules imported in the scripts, as well as python 2.7, can be 
downloaded in the Anaconda package, https://store.continuum.io/cshop/anaconda/


## Contents

### 2x.py
Take 2 to the power of x. Just because I can.

### clean_ports.py
Selfupdates macports, checks for inactive ports, and uninstalls inactive ports. 
Note that this program assumes that macports is installed. I don't know what 
would happen if you tried to run this without having macports installed.

### dump_columns.py
Dumps two columns from a FITS file into an ASCII/txt/dat file. You shouldn't
actually use this, since you will lose float precision when switching from a 
binary file format to an ASCII file format.

### fits_info.py
Prints HDU information, extension 1 header keywords, and extension 1 column 
names for a given FITS file. Using extension 1 here for RXTE event-mode data.

### get_keyword.py
Gets the value of a keyword from a FITS header.

### obs_epoch_rxte.py
Determines the observational epoch of a specific RXTE observation. Be careful 
with this one, it's barely tested.

### total_obs_time.py
Computes the total observation time for a list of FITS observation files.

### tools.py
Centralized helper methods to import and call within another function:

* get_key_val can get the value of a keyword from a FITS header; 
* compute_obs_time computes the total observation time in seconds of a list of 
	observation FITS files; 
* read_obs_time reads the observation time from the text header; 
* power_of_two checks is an integer is a power of two; 
* pairwise allows you to get the next two items of an iterable; 
* replace_key_val replaces the value of a keyword in a FITS header; 
* time_ordered_list takes a list of files and prints them in order of ascending 
	start time (from the FITS header keyword TSTART);
* obs_epoch_rxte determines which RXTE calibration epoch an observation was taken 
	during;
* type_positive_float is an argparse type that checks if the input is a positive 
	float;
* type_power_of_two is an argparse type that checks if the input is an integer 
	power of two.


## Authors and License
* Abigail Stevens (UvA API)

Pull requests are welcome!

All code is Copyright 2013-2015 The Authors, and is distributed under the MIT 
Licence. See LICENSE for details. If you are interested in the further 
development of whizzy_scripts, please [get in touch via the issues]
(https://github.com/abigailstev/whizzy_scripts/issues)!


[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)]
(http://www.astropy.org/) 
