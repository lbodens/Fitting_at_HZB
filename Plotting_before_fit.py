########################################################################################################################
#                                                                                                                      #
#                   in this file plots with the pre-set parameters from Param_updater are                              #
#                   fitted. You can choose the spectra to plot aswell (TODO)                                           #
#                                                                                                                      #
########################################################################################################################


import matplotlib.pyplot as plt
from Param_updater import *



def choose_spectra_to_plot():
    spectra_to_plot = int(input("please enter the spectra which you want to be shown\n"))
    return spectra_to_plot

def plot_1st_spectra_for_overview(d):
    fig, axes = plt.subplots()
    axes.plot(d["dat_0"]["E"], d["dat_0"]["Spectra"], 'b')
    plt.xlim([min(d["dat_0"]["E"]), max(d["dat_0"]["E"])])
    print(
        "Now a plot of the 1st spectra is shown, that you can quickly look if you want to change some pre set parameters. Close it to continue")
    plt.show()
    plt.close()

def check_if_peak_inport_is_good():
    check_shown_peak_input = input("Are these init parameters good enough? please enter 'yes'/'y' or 'no'/'n':\n")
    if check_shown_peak_input == "yes" or check_shown_peak_input == "y":
        check_shown_peak_input = True
        return check_shown_peak_input
    else:
        check_shown_peak_input = False
        return check_shown_peak_input

def peak_eval_fkt(param_file_type):
    pars = param_updater(param_file_type,param_file_name)
    mod, p4fit = shirley_param_calc(pars)
    init = mod.eval(x=x, params=p4fit)
    return pars, mod, p4fit, init

def plotting(x, spectra_to_plot,number_of_peaks):
    pars, mod, p4fit, init = peak_eval_fkt(param_file_type)
    fig, axes = plt.subplots()
    x = dat["E"].to_numpy()
    yraw = dat["Spectra"].to_numpy()
    axes.plot(x, yraw, 'b')
    axes.plot(x, init, 'k--', label='initial fit')
    plt.xlim([min(x) + (int(spectra_to_plot) - 1) * 10000, max(x) + (int(spectra_to_plot) - 1) * 10000])
    plt.show()

def plot_checking():
    spectra_to_plot_bool = False
    are_pre_params_good_bool = False
    spectra_to_plot = choose_spectra_to_plot()
    while spectra_to_plot_bool == False and are_pre_params_good_bool == False:
        while are_pre_params_good_bool == False:
            plotting(x, spectra_to_plot, number_of_peaks)
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
            if other_spectra_check == "yes" or other_spectra_check == "y":
                spectra_to_plot = choose_spectra_to_plot()
                spectra_to_plot_bool = False
                are_pre_params_good_bool = False
                break
            if other_spectra_check == "no" or other_spectra_check == "n":
                spectra_to_plot_bool = True
                continue


