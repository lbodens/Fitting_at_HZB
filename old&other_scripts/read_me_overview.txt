#In the followig a short overview over every script is given and the name of its creator so that possible questions can reach him/her

#Here only the general function/result are described. A more detailed description of the functions (should be) are at the beginnign of each file itself


#####################################################################################################################
# automated_area_approach_fitting - Lucas																			# 
# 	for fittinga linear BG of spectra with selecting the boundaries for the fit and intgration						# 
#																													# 
# inputs																											# 
# 	file : input file																								# 
#																													# 
# output																											# 
# 	plot of plot																									#
# 	matrix with all integrated values																				# 
# 	file with lin BG 																								#	
#																													# 
# possible change in future: 																						#
# 	right now its still in a single longstripe output.a structured output can/will be added later					#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                                                   #
#                                               IMPORTANT                                                           #
#                                                                                                                   #
# what you need: the file has to be in the following style                                                          #
# (with 'E' as the Energy (doesnt matter if KE or BE) name and the single spectra with the names 'S00' etc.):       #
#                                                                                                                   #
#   E        S00       S01       S02       S03       S04       ...                                                  #
# 969.95  1391.5362 1664.0262 1719.9869 1670.4967 1687.8547    ...                                                  #
# 969.85  1398.9735 1677.9272 1708.2657 1678.4641 1654.1115    ...                                                  #
#####################################################################################################################



#####################################################################################################################
# automated_Al_K-beta_subtraction - Lucas																			#
#	this skript is written for the case, that you ever have the problem, that an Al K-beta line is sitting under 	#
#	your other spectra. For this you need 3 files. 																	#
#																													#
# Inputs:																											#
#   1st Spectra (which is the source of the peak)   (BE in x.05, x.15, x.25 ... steps)								#
#   2nd spectra (from which the peak should be subtracted) (BE in x.05, x.15, x.25 ... steps))						#
#   K_beta peak spexctra (use file 'Al_K_beta_satellite_fit' in this folder). I´ll also include the peak parameters #
#	for Origin ('AlKa_satellites_K-beta_peak'), that one can calculate the peak them self, if they have different 	#
# 	step sizes.																										#
# 	If its a singulet or doublet. IF the latter: get a point inbetween the doublets to get the peak max of both for #
#	calculations 																									#
#																													#
# output:																											#
# K_beta spectra for each spectra/column 																			#
# 2nd spectra - k_beta Spectra 																						#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                                                   #
#                                               IMPORTANT                                                           #
#                                                                                                                   #
# Right now i only tested it once for my Ni spectra. and it was a hell of work to get the right shifting end energy #
# positioning going. If you have different energy step sizes etx, everything could stop working.. But then I´m happy#
# to sit down with you and try to figure out how and why. If you, for what ever reason use another K_beta line 		#	 
# (should in theory also work for the Mg Kß) make sure, they have only 2 decimal digits for the Energy scale and  	#
# are the same step size!			                                                          						#		
#####################################################################################################################



#####################################################################################################################
# automated_power_BE_Intensity - Lucas																				# 
# 	this script is just a short one to be able to extract and make a fast plotting of a time dependent measurement. #
# 	It then creates the files to plot the intensity or BE over power of the source * time  							#
#	An example of this is: you want to do a beamdamage test of a sample with different powers of the source over 	# 
# 	times/loopes (can easely be create with the 'automated_spectra_merger_into_one_file.py') plotting time over  	#
# 	power over BE 																									#	 
#																													#
# input:																											#
# 	sheet with all spectra summed up																				#
#																													#
# output:																											#
# 	file with peak BE position & height over Power/time 															#	
#																													# 
# possible change in future: 																						#
# 	including normalisation options for the spectra etc. 															#
#####################################################################################################################



#####################################################################################################################
# automated_spectra_merger_into_one_file - Lucas																	# 
# 	This script is written to combine a designated column from single files in one file for up to 6 diferent 		#
#	elements in the style of E, S00, S01, S02... 																	#
# 	There it doesn´t matter if they are from a looped measruement at EMIL or just files 							#
#																													#
# Input 																											#			
# 	single files with data columns 																					#
# 	different parameters which ara all asked one-by-one																#
#																													#
# output 																											#
# 	single file with all columns according to their "position" with naming of: S00, S01, S02.... 					#
#	THe naming of these files are though an input in the skript														#	
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                                                   #
#                                               IMPORTANT                                                           #
#                                                                                                                   #
# The file names for the EMIL files it can be an increasing one at the normal position, but for the other files the #
# digit needs to be at the end of the file name like Name_1, Name_2, Name_3 etc. The underline before the digit is 	# 
# important! 																										#
# Also do they need a headder for the column, which you want to use for combination									#
#####################################################################################################################



