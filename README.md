# Fitting_at_HZB

#This code is writen by MvdM and LBD with great help of Will and Flo!

# the main files are the 
#	- Fitting_testung_MvdM_LBD.py and 
# 	- test_param.json/yaml
#
# The goal of this fitting script is, that you can fit multiple spectra at once with an active(!) shirely BG. 
#  --> One shirley BG per peak each, which changes with the change of the peak during fitting aswell. 
# The code is written the way, that noone needs to touch it! Everything necessary is asked from the code and the only input is via cmd. So you do not ruin it by accident. ;)
# You can choose:
# 	- what type of peak you want to fit (Voigt, Gauss, etc) as long they are in the lmfit package (might need to include them into the mainscript once, or just talk to me and i´ll do it)
# 	- how many spectra you want to fit
#	- what kind of files you want to use
#		- a single file with all spectra inside it in diff columns
#		- multiple (all!) files in one folder
# 	- if you are using BE or KE as the energy. If KE: the code asks you for the exertation energy and claculates the BE automatically 
#
#	- also you can pre-set parameters (like before with the excel sheet). done in test_param.json/.yaml
#		- It  doesn´t matter if you use the yaml or json file/type. What ever style you preffer. 
#
# furthermore gives the code you the opportunity to check your previous param input for the spectra you want. If you are unhappy with them, change them in the test_param file
# and the new params will be updated.  
