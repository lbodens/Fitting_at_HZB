import matplotlib as mpl
import sys
from plots_scripts.Data_loader import *
from plots_scripts.Shirley_fkt_build import *
from plots_scripts.Param_updater import *
from plots_scripts.Param_check_via_plotting import *
from plots_scripts.Fitting_functions import *
from plots_scripts.Plotting_functions import *

namespace = sys._getframe(0).f_globals
plt.style.use('seaborn-ticks')
mpl.rcParams.update({'font.size': 16})

"""-----------------here all the functions from the other files are called and executed-----------------------"""
input_param_file_type_str = "yaml"
input_param_file_type = yaml
inputs_file_name = input("please enter the name/path of the fit input file (normally Input_fit):\n")
Inputs = input_param_file_type.load(open(inputs_file_name + "." + input_param_file_type_str),
                                    Loader=input_param_file_type.FullLoader)

# loading the data into a df d
d, number_of_spectra = df_creator_main_fkt(Inputs)

# just to plot once for an overview
# plot_1st_spectra_for_overview(d)

# building the Models (peak + shirley) and save it as df. The 0 is there, since we are using the Input_fit.file. with
# the ana file, the number will be changed there
mod_d, number_of_peaks, peak_func = peak_model_build_main_fkt(d, Inputs, 0)

# Importing previous parameter file and check inputs
param_file_type_str = Inputs["param_file_type_str"]
param_file_name = Inputs["param_file_name"]
p4fit, p4fit_s_d, p4fit_p_d, param_file_type, param_file_type_str = param_updater_main_fkt(d, param_file_type_str,
                                                                                           param_file_name,
                                                                                           number_of_spectra,
                                                                                           number_of_peaks)

# plot selected spectra with the selected starting parameters, which then can be updated
x = d[f'dat_0']["E"].to_numpy()
y_d, resid = y_for_fit(d, x, number_of_spectra, number_of_peaks)
pre_param_check = input("Now you can check the pre-set parameters. If you don´t want to do that, enter 'yes'/'y'?")
if pre_param_check.lower() == "yes" or pre_param_check.lower() == "y":
    params_via_plot_checking(x, d, y_d, mod_d, peak_func, param_file_type_str, param_file_name, number_of_spectra,
                             number_of_peaks)

"""--------------------------------------actual fitting fkt------------------------------------------------"""
nfev = Inputs["fit_iterations"]
out, out_params, y_d = fitting_function_main_fkt(d, p4fit, x, mod_d, number_of_spectra, number_of_peaks, nfev)

"""-------------plotting the fitted spectra------------------------------"""

fit_loop = False
while not fit_loop:
    plotting_subplots_main_fkt(x, out_params, mod_d, y_d, peak_func, number_of_spectra, number_of_peaks)
    replot_loop = False
    while not replot_loop:
        replot_loop_check = input("Do you want to look at other spectra/in another way? Please enter 'yes/y' or 'no/n'")
        if replot_loop_check.lower() == "yes" or replot_loop_check.lower() == "y":
            plotting_subplots_main_fkt(x, out_params, mod_d, y_d, peak_func, number_of_spectra, number_of_peaks)
        if replot_loop_check.lower() == "no" or replot_loop_check.lower() == "n":
            replot_loop = True
    fit_quality_test = input("Is the fit good enough? \nIf yes please enter 'yes'/'y'. if Not enter 'no'/'n':\n")
    if fit_quality_test.lower() == "yes" or fit_quality_test.lower() == "y":
        fit_loop = True
        break
    if fit_quality_test.lower() == "no" or fit_quality_test.lower() == "n":

        print("Now a small loop sections will run, where you can check all init parameters via plots again.")
        nfev = int(input("So please update the starting parameters. Furthermore: update the max iterations do you "
                         "want to use here:"))
        params_via_plot_checking(x, d, y_d, mod_d, peak_func, param_file_type_str, param_file_name, number_of_spectra,
                                 number_of_peaks)
        out, out_params, y_d = fitting_function_main_fkt(d, p4fit, x, mod_d, number_of_spectra, number_of_peaks, nfev)
    else:
        continue

"""-----------------------------------------Exporting Data-----------------------------------------------------------"""

result_file_path = Inputs["fit_result_file_path"]
params_to_file = {}
for idx in range(int(number_of_peaks)):
    for i in range(int(number_of_spectra)):
        for name in out.params:
            params_to_file[f"{name}"] = str(out.params[name])
param_file_type.dump(params_to_file, open(result_file_path + "." + param_file_type_str, "w"))
