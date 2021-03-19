# Fitting_at_HZB

#This code is writen by MvdM and LBD with great help of Will and Flo!

# the main files are the 
#	- Fitting_testung_MvdM_LBD.py 		(Main file which then calls all the others)
#   - Data_loader.py 					(where the data is loaded into a df)
#   - Shirley_fkt_biuld.py 				(creates the peak + shirley model)
#   - Param_updater.py					(takes the preset parameter from the testparam.json/yaml and upüdates the parameter)
# 	- test_param.json/yaml
#   - Plotting_before_fit.py			
#   - Fitting_functions.py
# 	- Plotting_after_fitting.py
#
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
#
# 


# Adittionall files in the folder (right now):
#
# 20210223_112711 is a picture of the current code and how the functions are connected with eaych other and the parameters (needs to be updated/refined)
# the 'Fitting_test_2' is an example code, which works but does not includes all the stuff as in the main script. SO that someone can test it on its own PC and doesn´t have to run through all the stuff again
# the same foes for the 'Shirley_test_3' and 'fitstuff'
# 'Ni2p_Ni-Kbeta_subtr' is an test file with 169 diff Ni2p spectra inside and 'Ni2p_ref_sat_sub' is a reference of Ni2p
