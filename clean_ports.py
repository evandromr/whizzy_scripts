import os

"""
		clean_ports.py
	
Selfupdates macports, checks for inactive ports, and uninstalls inactive ports. 

Written in Python 2.7 by A.L. Stevens, A.L.Stevens@uva.nl, 2014

Passed: nothing

Returns: nothing

"""

def main():
	ports_to_uninstall = []

	os.system("sudo port selfupdate") # Since we're using sudo, you'll have to type in your password

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
		print "Finished uninstalling inactive ports."
	else:
		print "All installed ports are active."
	
	## End of function 'main'
	
if __name__ == "__main__":

	main()
	
# End of program 'clean_ports.py'