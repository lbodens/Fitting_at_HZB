"""
This script exports the fitted peak params center & area (amplitude) using the 'Inputs_ana_element.yaml' file
It also sorts the params belonging together (according tho the 'oxid_and_corelvl_sorting' list)
"""

import yaml
import matplotlib.pyplot as plt
from pathlib import Path
from plots_scripts.Analysis_ana import get_params_fkt
from plots_scripts.Analysis_plotting import param_into_pars_and_sorting, spectra_and_and_model_generator, export_plot_fkt
from plots_scripts.Plotting_functions import model_separator_eval_fkt
from plots_scripts. Analysis_save_output import export_area_fkt,  export_center_fkt, export_eval_data_fkt


def export_eval_peaks_fkt(Inputs, element_nr, nr_of_spectra, nr_of_peaks, pars_cl):
    """
    This fkt calls the evaluation, plot & output_save functions for the wanted peaks according to the result_path
    """
    pars_s_d = param_into_pars_and_sorting(pars_cl)
    d, x, y_d, mod_d, peak_func = spectra_and_and_model_generator(Inputs, element_nr)
    mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_eval = model_separator_eval_fkt(pars_s_d, mod_d, peak_func, x,
                                                                              nr_of_spectra, nr_of_peaks)

    spectra_to_plot = int(input("please enter the spectra nr (0 to n-1) you want to extract"))
    printout_loop = False
    while printout_loop is False:
        export_eval_data_fkt(Inputs, element_nr, spectra_to_plot, x, mod_w_sBG_peaks_eval, shirley_BG_d,
                             mod_d_eval)
        export_plot_fkt(x, y_d, mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_eval, Inputs, element_nr, spectra_to_plot)

        printout_loop_check = input("Do you want to extract other spectra as well? if yes please type 'y' or 'yes' or "
                                    "directly the number. Else any key.")
        if not printout_loop_check.lower() == "y" or printout_loop_check.lower() == "yes":
            try:  # to catch if someone accidently types in the nr directly
                int(printout_loop_check)
                spectra_to_plot = int(printout_loop_check)
            except ValueError:
                printout_loop = True
        else:
            spectra_to_plot = int(input("please enter the spectra nr (0 to n-1) you want to extract"))
    return


def export_fitted_eval_data_main_fkt(Inputs):
    """
    This fkt sorts the params after area & center, and saves it into a file each
    First it checks if the 'areas_' & 'center_' file already exists, if not it creats it and saves the stuff inside it
    Also it gives the opportunity to plot the fitted data and saves the evaluated peaks into a file each
    """
    element_nr = Inputs["element_number"]
    nr_of_spectra = Inputs["number_of_spectra"]
    nr_of_peaks = Inputs["el{}_number_of_peaks".format(element_nr)]

    pars_cl, df_a, df_c = get_params_fkt(Inputs, element_nr)

    my_file_area = Path(Inputs["result_file_path"] + "areas_" + Inputs["el1_name"] + ".txt")
    try:
        file_a = open(my_file_area)  # .is_file():
        print(
            "The save file exists already and will not be created/written. If you want to have it updated, delete it first"
            " and restart the program\n")
        file_a.close()
    except:
        print("And will be saved in:" + Inputs["result_file_path"] + "areas_" + Inputs["el1_name"] + ".txt \n")
        export_area_fkt(df_a, element_nr, nr_of_spectra, Inputs)


    my_file_center = Path(Inputs["result_file_path"] + "center_" + Inputs["el1_name"] + ".txt")
    try:
        file_c = open(my_file_center)  # .is_file():
        print("The file exists already and will not be created/written. If you want to have it updated, delete it first"
              " and restart the program")
        file_c.colse()
    except:
        print("An overview of the main peak centers will be saved in:" + Inputs["result_file_path"] + "center_" +
              Inputs["el1_name"] + ".txt\n")
        export_center_fkt(df_c, element_nr, nr_of_spectra, Inputs)


    export_eval_peaks_fkt(Inputs, element_nr, nr_of_spectra, nr_of_peaks, pars_cl)

    return


# -------------------------------------------------------------------------------------------------------------------

param_file_path = input(
    "please enter the file path + name of the Inputs-extraction file:\n")
param_file_type_str = "yaml"
param_file_type = yaml

Inputs = param_file_type.load(open(param_file_path + "." + param_file_type_str), Loader=param_file_type.FullLoader)

export_fitted_eval_data_main_fkt(Inputs)
