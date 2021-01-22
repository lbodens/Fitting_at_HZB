#####################################################################################################################
#																													#
# in this file you can enter the starting parameters in the folllowing example pattern 								#
#																													#
#	pars["peakTypeSpectraNr_peakNr_parameter"].set(values=startingValue, min=lowerBoundary, max=upperBoundary,      #
#							vary=changableDuringIteration(Ture/False), expr="formula") 								#
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
#																													#
# you can find further examples/parameters for each peak type at 													#
# https://lmfit.github.io/lmfit-py/builtin_models.html 																#
#																													#
#####################################################################################################################	

from Fitting_test_2 import pars

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

pars.add('peak_3_height_multi',value = 0.59876, vary = False)
pars.add('peak_3_center_split',value = 17.27, vary = False)
pars['v0_3_amplitude'].set(expr="v0_0_amplitude*peak_3_height_multi", vary = False)
pars['v0_3_center'].set(expr="v0_2_center+peak_3_center_split", vary = False)
pars['v0_3_sigma'].set(value=1.943, min=0, max=5)
pars['v0_3_gamma'].set(value=2.317, min=0, max=5)

pars.add('peak_4_height_multi',value = 0.9743, vary = False)
pars.add('peak_4_center_split',value = 7.25, vary = False)
pars['v0_4_amplitude'].set(expr="v0_0_amplitude*peak_4_height_multi", vary = False)
pars['v0_4_center'].set(expr="v0_0_center+peak_4_center_split", vary = False)
pars['v0_4_sigma'].set(value=2.29, min=0, max=5)
pars['v0_4_gamma'].set(value=0.18, min=0, max=5)

pars.add('peak_5_height_multi',value = 0.16, vary = False)
pars.add('peak_5_center_split',value = 10.1994, vary = False)
pars['v0_5_amplitude'].set(expr="v0_0_amplitude*peak_5_height_multi", vary = False)
pars['v0_5_center'].set(expr="v0_0_center+peak_5_center_split", vary = False)
pars['v0_5_sigma'].set(value=1.054, min=0, max=5)
pars['v0_5_gamma'].set(value=0.2167, min=0, max=5)

pars.add('peak_6_height_multi',value = 0.1869, vary = False)
pars.add('peak_6_center_split',value = 12.5, vary = False)
pars['v0_6_amplitude'].set(expr="v0_0_amplitude*peak_6_height_multi", vary = False)
pars['v0_6_center'].set(expr="v0_0_center+peak_6_center_split", vary = False)
pars['v0_6_sigma'].set(value=1.934, min=0, max=5)
pars['v0_6_gamma'].set(value=0.00017, min=0, max=5)

pars.add('peak_7_height_multi',value = 0.29881, vary = False)
pars.add('peak_7_center_split',value = 22.2676, vary = False)
pars['v0_7_amplitude'].set(expr="v0_0_amplitude*peak_7_height_multi", vary = False)
pars['v0_7_center'].set(expr="v0_0_center+peak_7_center_split", vary = False)
pars['v0_7_sigma'].set(value=3.75, min=0, max=5)
pars['v0_7_gamma'].set(value=0.0000307, min=0, max=5)

pars.add('peak_8_height_multi',value = 0.5513, vary = False)
pars.add('peak_8_center_split',value = 26.367, vary = False)
pars['v0_8_amplitude'].set(expr="v0_0_amplitude*peak_8_height_multi", vary = False)
pars['v0_8_center'].set(expr="v0_0_center+peak_8_center_split", vary = False)
pars['v0_8_sigma'].set(value=3.06, min=0, max=5)
pars['v0_8_gamma'].set(value=0.322, min=0, max=5)

pars['v1_0_amplitude'].set(value=50000,min=0)
pars['v1_0_center'].set(value=v0_0_center, vary = False)
pars['v1_0_sigma'].set(value=v1_0_sigma, vary = False)
pars['v1_0_gamma'].set(value=v1_0_gamma, vary = False)

# ...
# ...
# ...
# ...
