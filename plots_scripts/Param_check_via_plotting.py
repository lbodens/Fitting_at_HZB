########################################################################################################################
#                                                                                                                      #
#                   in this file the preselected parameter are checked.                                                #
#                   If one wants to change them, bc they don´t look good enough, then they can                         #
#                   update them and look at the plot again. You can choose the spectra to plot aswell                  #
#                                                                                                                      #
########################################################################################################################


import matplotlib.pyplot as plt
from plots_scripts.Param_updater import param_updater_main_fkt
from plots_scripts.Plotting_functions import model_separator_eval_fkt, plotting_fit_single_plot_fkt



def choose_spectra_to_plot():
    spectra_to_plot = int(input("Please enter the spectra nr (0 to n-1) which you want to look at:\n"))
    return spectra_to_plot



def check_if_peak_inport_is_good():
    check_shown_peak_input = input("Are these init parameters good enough? please enter 'yes'/'y' or 'no'/'n':\n")
    if check_shown_peak_input.lower() == "yes" or check_shown_peak_input.lower() == "y":
        check_shown_peak_input = True
        return check_shown_peak_input
    else:
        check_shown_peak_input = False
        return check_shown_peak_input


def params_via_plot_checking(x,d, y_d, mod_d,peak_func, param_file_type, param_file_name,number_of_spectra, number_of_peaks) :
    spectra_to_plot_bool = False
    are_pre_params_good_bool = False
    spectra_to_plot = choose_spectra_to_plot()
    while spectra_to_plot_bool == False and are_pre_params_good_bool == False:
        while are_pre_params_good_bool == False:

            p4fit, p4fit_s_d, p4fit_p_d = param_updater_main_fkt(d,param_file_type, param_file_name, number_of_spectra, number_of_peaks)
            mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_p_p_d_eval= model_separator_eval_fkt(p4fit_s_d, mod_d, d, peak_func, x, number_of_spectra, number_of_peaks)
            plotting_fit_single_plot_fkt(x, y_d, mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_p_p_d_eval,number_of_peaks, spectra_to_plot)

            are_pre_params_good_bool = check_if_peak_inport_is_good()
            if are_pre_params_good_bool == True:
                plt.close()
                continue
            if are_pre_params_good_bool == False:
                plt.close()
                print("Please change the paramter to the desired one\n")
                continue
        while spectra_to_plot_bool == False:
            other_spectra_check = input("do you want to check other spectra as well?\n")
            if other_spectra_check.lower() == "yes" or other_spectra_check.lower() == "y":
                spectra_to_plot = choose_spectra_to_plot()
                spectra_to_plot_bool = False
                are_pre_params_good_bool = False
                break
            if other_spectra_check.lower() == "no" or other_spectra_check.lower() == "n":
                spectra_to_plot_bool = True
                continue


