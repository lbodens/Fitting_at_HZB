# Fitting_at_HZB

#This code is writen by MvdM and LBD with great help of Will and Flo!

# the main files are the 
#	- Fitting_testung_MvdM_LBD.py and 
# 	- test_param.json/yaml
#
# the goal of this fitting script is, that you can fit multiple spectra at once with an active(!) shirely BG. you can choose, what type of peak you want to fit as well (Voigt, Gauss, etc) as long they are in the lmfit package (might need to include them into the mainscript once)
# Furthermore is it writte, so that you do not need to change the code!!!! every input will be asked and answered via command line/terminal. So you do not ruin it by accident.
# 
# in the test_param, you can input starting parameters of your fit in the example style. It  doesn´t matter if you use the yaml or json file/type. What ever you preffer. 