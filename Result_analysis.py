#################################################################################################################################
#                                                                                                                               #
# This Program is written to use the fitted data and plot/analyzes it.                                                          #
# Therefore it first loads the fitted data (via get params) for the two elements, which you want to plot/analyze/compare        #
#                                                                                                                               #
#################################################################################################################################

import yaml
import numpy as np

from plots_scripts.Analysis_plotting import *
from plots_scripts.Analysis_ana import *
from plots_scripts.Analysis_save_output import *


"""-------------creating matrix style output and save it into a file----------------------"""


def result_ana_main_fkt(Inputs):

    print("Importing 1st dataset")
    pars_cl_1, df_1_a_sum, df_1_a_1_sum, df_1_c_sum = get_params_fkt(Inputs, 1)
    print("Importing 2nd dataset")
    pars_cl_2, df_2_a_sum, df_2_a_1_sum, df_2_c_sum = get_params_fkt(Inputs, 2)
    
    plot_or_ana_check = True
    while plot_or_ana_check:
        plot_or_ana = input("do you want to 'plot' or 'analyze'? Please enter '0' or '1'. If not just type any key:\n")

        if plot_or_ana == "0" or plot_or_ana == "plot":
            element_number = input("which element do you want to plot? please enter 1 or 2:\n")
            if element_number == "1":
                plotting_ana_main_fkt(pars_cl_1, Inputs, 1)
            if element_number == "2":
                plotting_ana_main_fkt(pars_cl_2, Inputs, 2)

            continue_PoA = input("do you want to continue with fitting? Please enter 'y' or 'n':\n")
            if continue_PoA == "y":
                continue
            if continue_PoA == "n":
                break

        if plot_or_ana == '1' or plot_or_ana == "analyze":
    
            df_a_1, df_a_2, df_a_tot = area_calculations_fkt(df_1_a_sum, df_2_a_sum, Inputs)
            df_c_shift_bw_oxid, df_c_shift_el1, df_c_shift_el2 = center_calculations_fkt(df_1_c_sum, df_2_c_sum, Inputs)

            save_to_file_main_fkt(Inputs, df_a_1, df_a_2, df_a_tot, df_c_shift_bw_oxid, df_c_shift_el1, df_c_shift_el2)
            print("Analysis is done.")
            continue_PoA = input("Do you want to continue the analysis or plot? Please enter 'y' or 'n':\n")
            if continue_PoA == 'y':
                continue
            if continue_PoA == "n":
                plot_or_ana_check = False
                break
        else:
            plot_or_ana_check = False

    return
    

"""--------------------------------'main' code---------------------------------------"""
    
input_param_file_type_str = "yaml"
input_param_file_type = yaml
inputs_file_name = input("please enter the name/path of the fit input file (normally Input_fit):\n")
Inputs = input_param_file_type.load(open(inputs_file_name + "." + input_param_file_type_str),
                                    Loader=input_param_file_type.FullLoader)
number_of_spectra = Inputs["number_of_spectra"]

result_ana_main_fkt(Inputs)


