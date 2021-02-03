#####################################################################################################################
#																													#
# in this file you can enter the starting parameters in the folllowing example pattern 								#
#																													#
#	pars["peakTypeSpectraNr_peakNr_parameter"].set(values=startingValue, min=lowerBoundary, max=upperBoundary,      #
#							vary=changableDuringIteration(Ture/False), expr="formula") 								#
#																													#
#	Important:																										#
# 		when fitting more than 1 spectra at a time:																	#
#		always enter the + center_peak[nr of spectra to fit ('vX_')] to it. since the spectra merger in the main 	#
#		script will add it to the basic energy. therefore if you do not to that, all peaks are packed in the 1st 	#
#		one and will not fit the others as well																		#
#																													#
#	example 1: 																										#
#		pars['v1_5_center'].set(value=854.4, min=853, max=856)														#
#		voigt_peak, spectra nr 2, peaknr 6, peakcenter at 853< 854.4 <856											#
#																													#	
#	example 2:																										#
#		it is also possible to add worn parameters 																	#
#					name 				value 			not changeable 												#
#		pars.add('peak_2_height_multi',value = 1.415, vary = False) 												#
#																													#
#		to use for later calculations 																				#
#		pars['v0_2_amplitude'].set(expr="v0_0_amplitude*peak_2_height_multi", vary= False)							#
#																													#
# you can find further examples/parameters for each peak type at 													#
# https://lmfit.github.io/lmfit-py/builtin_models.html 																#
#																													#
#####################################################################################################################	


def parameter_file(pars, number_of_spectra):
	for i in range(int(number_of_spectra)):
		pars.add('center_peak_'+str(i),value = i*10000, vary = False)

	pars['v0_0_amplitude'].set(value=50000,min=0)
	pars['v0_0_center'].set(value=854.4, min=853, max=856)
	pars['v0_0_sigma'].set(value=0.74, min=0, max=5)
	pars['v0_0_gamma'].set(value=0.000092, min=0, max=5)
	
	pars.add('peak_1_height_multi',value = 0.2985, vary = False)
	pars.add('peak_1_center_split',value = 17.27, vary = False)
	pars['v0_1_amplitude'].set(expr="v0_0_amplitude*peak_1_height_multi", vary = False)
	pars['v0_1_center'].set(expr="v0_0_center+peak_1_center_split", vary = False)
	pars['v0_1_sigma'].set(value=0.985, min=0, max=5)
	pars['v0_1_gamma'].set(value=0.00006, min=0, max=5)
	
	pars.add('peak_2_height_multi',value = 1.415, vary = False)
	pars.add('peak_2_center_split',value = 1.6711, vary = False)
	pars['v0_2_amplitude'].set(expr="v0_0_amplitude*peak_2_height_multi", vary= False)
	pars['v0_2_center'].set(expr="v0_0_center+peak_2_center_split", vary = False)
	pars['v0_2_sigma'].set(value=1.91, min=0, max=5)
	pars['v0_2_gamma'].set(value=0.16, min=0, max=5)
	#...
	#...
	#...
	
	pars['v1_0_amplitude'].set(value=260,min=0)
	pars['v1_0_center'].set(expr="v0_0_center+center_peak_1", vary = False)
	pars['v1_0_sigma'].set(expr="v1_0_sigma", vary = False)
	pars['v1_0_gamma'].set(expr="v1_0_gamma", vary = False)
	
	pars['v1_1_amplitude'].set(value=180, vary = False)
	pars['v1_1_center'].set(expr="v0_0_center+center_peak_1", vary = False)
	pars['v1_1_sigma'].set(expr="v0_1_sigma", min=0, max=5)
	pars['v1_1_gamma'].set(expr="v0_1_gamma", min=0, max=5)
	
	pars['v1_2_amplitude'].set(value=80, vary= False)
	pars['v1_2_center'].set(expr="v0_0_center+center_peak_1", vary = False)
	pars['v1_2_sigma'].set(value=1.91, min=0, max=5)
	pars['v1_2_gamma'].set(value=0.16, min=0, max=5)
	# ...
	# ...
	# ...
	# ...

	return pars
