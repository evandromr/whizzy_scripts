#########################################################
##		clean_ports.py
##	
##	Selfupdates macports
##  Checks for inactive ports
##  Uninstalls inactive ports
##
##  Written by A.L. Stevens (A.L.Stevens@uva.nl), 2014
##	
#########################################################

import os

ports_to_uninstall = []

os.system("sudo port selfupdate")

installed = os.popen("port installed")

for line in installed:
	if ("(active)" not in line) and ("The following ports are currently installed" not in line):
		print line
		ports_to_uninstall.append(line.rstrip())

# print ports_to_uninstall

if len(ports_to_uninstall) > 0:
	for element in ports_to_uninstall:
		cmd_str = "sudo port uninstall"+element
# 		print cmd_str
		os.system(cmd_str)
else:
	print "All installed ports are active."
	
print "Done!"

# End of program 'clean_ports.py'