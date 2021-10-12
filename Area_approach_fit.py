import matplotlib as mpl
import sys
import pandas as pd
import yaml

from plots_scripts.Analysis_area_calculation import calc_path_main_fkt
from plots_scripts.Analysis_area_loader import *
from plots_scripts.Analysis_area_plotting import plotting_path_main_fkt

"""-----------------here all the functions from the other files are called and executed-----------------------"""


def choice_fkt(choice_input, Inputs, df):
    e_bound_container = None

    if choice_input == "yes" or choice_input == "y":
        plot_or_calculation, fit_E_low, i_low_fit, fit_E_up, i_up_fit, int_E_low, i_low_int, int_E_up, i_up_int = plotting_path_main_fkt(df, Inputs)
        #b_container_test = fit_E_low, i_low_fit, fit_E_up, i_up_fit, int_E_low, i_low_int, int_E_up, i_up_int

        """
        plot_or_calculation, bounds_container = plotting_path_main_fkt(df, Inputs)

        fit_low_container, fit_up_container, int_low_container, int_up_container = bounds_container
        lower_fit_bound, fit_E_low, i_low_fit = fit_low_container
        upper_fit_bound, fit_E_up, i_up_fit = fit_up_container
        lower_int_bound, int_E_low, i_low_int = int_low_container
        upper_int_bound, int_E_up, i_up_int = int_up_container
        """
        e_bound_container = fit_E_low, i_low_fit, fit_E_up, i_up_fit, int_E_low, i_low_int, int_E_up, i_up_int

    if choice_input == "no" or choice_input == "n" or plot_or_calculation == "no":
        df, df2, df3, df4, df5, df6, e_bound_container = calc_path_main_fkt(df, Inputs, e_bound_container)

    else:
        print("\nError, please type in 'yes' or 'no'\n")
        plot_matrix_choice = False
        return plot_matrix_choice

    save_output_fkt(Inputs, e_bound_container, df, df2, df3, df4, df5, df6)

"""---------------------------------------- main code part ----------------------------------------------------------"""

input_param_file_type_str = "yaml"
input_param_file_type = yaml
inputs_file_name = input("please enter the name/path of the fit input file (normally Input_fit):\n")
Inputs = input_param_file_type.load(open(inputs_file_name + "." + input_param_file_type_str),
                                    Loader=input_param_file_type.FullLoader)

# load the data into a df
number_of_spectra = Inputs["number_of_spectra"]
df = load_data_main_fkt(Inputs)

# choose, if you want to do the plotting or matrix stuff directly
plot_matrix_choice = False
while not plot_matrix_choice:
    plot_or_calculation = input("Do you want to show the plots & select the ranges for calculations type: 'yes'. \n"
                                "If not and you want to create the measurement matrix type: 'no'. \n")
    plot_matrix_choice = choice_fkt(plot_or_calculation, Inputs, df)
