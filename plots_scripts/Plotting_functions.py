########################################################################################################################
#                                                                                                                      #
#               in this file all plots are generated.                                                                  #
#               The peak parameter [spectra_{i}] are sorted to [p{i}_{idx}] and the models get evaluated               #
#               (with and w/o the shirley, which then gets subtracted to get the single shirley as well                #
#                                                                                                                      #
#               There are the 3 plot functions written as well. The subplots are for after fitting                     #
#               for better overview. Note: the other functions are used in the script before!                          #
#                                                                                                                      #
########################################################################################################################


import numpy as np
import pandas as pd
# import tkinter
# import matplotlib as mpl
import matplotlib.pyplot as plt
# matplotlib.use('TkAgg')
import re
from plots_scripts.Fitting_functions import model_eval_fitted_fkt
# from plots_scripts.Param_check_via_plotting import choose_spectra_to_plot


def matches_str(key, pattern):
    return pattern.search(key)


def param_per_peak_from_spec_sorting_fkt(p4fit, number_of_spectra, number_of_peaks):
    p4fit_out_p_d = {}
    for i in range(int(number_of_spectra)):
        for idx in range(int(number_of_peaks)):
            pattern = re.compile(f"p{i}_{idx}.*")
            for k, v in p4fit[f'spectra_{i}'].items():
                if matches_str(k, pattern):
                    p4fit_out_p_d[k] = v

    p4fit_p_p_d = {}
    for i in range(int(number_of_spectra)):
        for idx in range(int(number_of_peaks)):
            p4fit_p_p_d[f'p{i}_{idx}'] = {}
            for name in p4fit_out_p_d:
                if f'p{i}_{idx}_' in name:
                    p4fit_p_p_d[f'p{i}_{idx}'][f"{name}"] = p4fit_out_p_d[name]
    return p4fit_p_p_d


def model_w_only_peaks_p_spec_d(peak_func, number_of_spectra, number_of_peaks):
    mod_w_only_peaks_p_spec_d = {}
    for i in range(int(number_of_spectra)):
        mod_p_p_i = peak_func(prefix=f'p{i}_0_')
        for idx in range(1, int(number_of_peaks)):
            mod_p_p_i = mod_p_p_i + peak_func(prefix=f'p{i}_{idx}_')
        mod_w_only_peaks_p_spec_d[f'spectra_{i}'] = mod_p_p_i
    return mod_w_only_peaks_p_spec_d


def model_w_only_peaks_p_spec_eval_d(mod_w_only_peaks_p_spec_d, out_params, x, number_of_spectra, number_of_peaks):
    mod_w_only_peaks_p_spec_d_eval = {}
    for i in range(int(number_of_spectra)):
        for idx in range(int(number_of_peaks)):
            mod_w_only_peaks_p_spec_d_eval[f"spectra_{i}"] = pd.DataFrame()

    for i in range(int(number_of_spectra)):
        mod_w_only_peaks_p_spec_d_eval[f'spectra_{i}'] = mod_w_only_peaks_p_spec_d[f'spectra_{i}'].eval(x=np.array(x),
                                                                                                        params=
                                                                                                        out_params[
                                                                                                            f"spectra_{i}"])
    return mod_w_only_peaks_p_spec_d_eval


def shirley_BG_only_eval_fkt(model_d, mod_w_only_peaks_p_spec_d_eval, number_of_spectra):
    shirley_BG_d = {}
    for i in range(int(number_of_spectra)):
        shirley_BG_d[f"spectra_{i}"] = model_d[i] - mod_w_only_peaks_p_spec_d_eval[f'spectra_{i}']
    return shirley_BG_d


def model_w_only_peaks_fkt(peak_func, number_of_spectra, number_of_peaks):
    mod_w_only_peaks_p_p_d = {}
    for i in range(int(number_of_spectra)):
        for idx in range(int(number_of_peaks)):
            mod_w_only_peaks_p_p_d[f'p{i}_{idx}'] = peak_func(prefix=f'p{i}_{idx}_')
    return mod_w_only_peaks_p_p_d


def model_w_only_peaks_eval_fkt(mod_w_only_peaks_p_p_d, p4fit_p_p_d, x, number_of_spectra, number_of_peaks):
    mod_w_only_peaks_p_p_d_eval = {}
    for i in range(int(number_of_spectra)):
        model_eval_df = pd.DataFrame()
        for idx in range(int(number_of_peaks)):
            model_eval_df[f"p_{idx}"] = []
        mod_w_only_peaks_p_p_d_eval[f"spectra_{i}"] = model_eval_df

    for i in range(int(number_of_spectra)):
        for idx in range(int(number_of_peaks)):
            mod_w_only_peaks_p_p_d_eval[f'spectra_{i}'][f'p_{idx}'] = mod_w_only_peaks_p_p_d[f'p{i}_{idx}'].eval(
                x=np.array(x), params=p4fit_p_p_d[f'p{i}_{idx}'])

    return mod_w_only_peaks_p_p_d_eval


def model_w_sBG_plus_peaks_p_p_eval_d(shirley_BG_d, mod_w_only_peaks_p_p_d_eval, number_of_spectra, number_of_peaks):
    mod_w_sBG_peaks_p_p_d_eval = {}
    for i in range(int(number_of_spectra)):
        mod_w_sBG_peaks_p_p_d_eval[f'spectra_{i}'] = {}
        for idx in range(int(number_of_peaks)):
            mod_w_sBG_peaks_p_p_d_eval[f'spectra_{i}'][f'p_{idx}'] = shirley_BG_d[f"spectra_{i}"] + \
                                                                     mod_w_only_peaks_p_p_d_eval[f'spectra_{i}'][
                                                                         f'p_{idx}']
    return mod_w_sBG_peaks_p_p_d_eval


# this is where all the magic appends and the models are called etc
def model_separator_eval_fkt(params_s_d, mod_d, peak_func, x, number_of_spectra, number_of_peaks):
    # this calculates the single parts for the plotting. 1st: sorts the out params in right order
    params_p_d = param_per_peak_from_spec_sorting_fkt(params_s_d, number_of_spectra, number_of_peaks)
    mod_d_eval = model_eval_fitted_fkt(params_s_d, mod_d, x, number_of_spectra, number_of_peaks)
    # 2nd generates a model of all peaks per spectra w/o the shirley BG, so that when it is subtracted from the total
    # spectra only the shirley is left
    mod_w_only_peaks_p_spec_d = model_w_only_peaks_p_spec_d(peak_func, number_of_spectra, number_of_peaks)
    mod_w_only_peaks_p_spec_d_eval = model_w_only_peaks_p_spec_eval_d(mod_w_only_peaks_p_spec_d, params_s_d, x,
                                                                      number_of_spectra, number_of_peaks)
    shirley_BG_d = shirley_BG_only_eval_fkt(mod_d_eval, mod_w_only_peaks_p_spec_d_eval, number_of_spectra)

    # creates model with only single peaks, where then the shirley is added ontop
    mod_w_only_peaks_p_p_d = model_w_only_peaks_fkt(peak_func, number_of_spectra, number_of_peaks)
    mod_w_only_peaks_p_p_d_eval = model_w_only_peaks_eval_fkt(mod_w_only_peaks_p_p_d, params_p_d, x, number_of_spectra,
                                                              number_of_peaks)
    mod_w_sBG_peaks_p_p_d_eval = model_w_sBG_plus_peaks_p_p_eval_d(shirley_BG_d, mod_w_only_peaks_p_p_d_eval,
                                                                   number_of_spectra, number_of_peaks)
    return mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_p_p_d_eval


'''----------------------here all 3 plot functions are written-->change here to make them more pretty--------------'''


def plot_1st_spectra_for_overview(d):
    fig, axes = plt.subplots()
    axes.plot(d["dat_0"]["E"], d["dat_0"]["Spectra"], 'b')
    plt.xlim([min(d["dat_0"]["E"]), max(d["dat_0"]["E"])])
    print("Now a plot of the 1st spectra is shown, that you can quickly look if you want to change some pre set "
          "parameters. Close it to continue")
    plt.xlim([max(d["dat_0"]["E"]), min(d["dat_0"]["E"])])
    plt.show()


def plotting_fit_subplots(x, y_d, model_d_fitted, shirley_BG_d, mod_w_sBG_peaks_p_p_d_eval, number_of_peaks,
                          x_nr_of_subplt, y_nr_of_subplt):
    fig, axs = plt.subplots(y_nr_of_subplt, x_nr_of_subplt, figsize=(15, 8), sharex=True, sharey=True)
    for i, axes in enumerate(axs.flat):
        if i >= len(y_d):  # to not break, if the number of plots is e.g. uneven
            break
        axes.plot(x, y_d[i], 'black', label='data')
        axes.plot(x, model_d_fitted[i], 'r', label='fit')  # envelope of fitted peaks
        for idx in range(int(number_of_peaks)):
            axes.plot(x, mod_w_sBG_peaks_p_p_d_eval[f'spectra_{i}'][f'p_{idx}'],
                      label=f"peak_{idx}")  # every fitted peak + shirley sum
        axes.plot(x, shirley_BG_d[f"spectra_{i}"], color='grey', linestyle='dashed',
                  label='shirley')  # shirley of fitted peaks
    plt.xlim([max(x), min(x)])
    plt.legend(loc='best')
    plt.show()


def plotting_fit_single_plot_fkt(x, y_d, mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_p_p_d_eval, number_of_peaks,
                                 spectra_to_plot):
    fig, axs = plt.subplots()
    axs.plot(x, y_d[spectra_to_plot], 'black', label=f'data S{spectra_to_plot}')
    axs.plot(x, mod_d_eval[spectra_to_plot], 'r', label='fit')  # envelope of fitted peaks
    for idx in range(int(number_of_peaks)):
        axs.plot(x, mod_w_sBG_peaks_p_p_d_eval[f'spectra_{spectra_to_plot}'][f'p_{idx}'],
                 label=f"peak_{idx}")  # every fitted peak + shirley sum
    axs.plot(x, shirley_BG_d[f"spectra_{spectra_to_plot}"], color='grey', linestyle='dashed',
             label='shirley')  # shirley of fitted peaks
    plt.xlim([max(x), min(x)])
    plt.legend(loc='best')
    plt.show()


def plotting_subplots_main_fkt(x, pAfit_s_d, mod_d, y_d, peak_func, number_of_spectra, number_of_peaks):
    mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_p_p_d_eval = model_separator_eval_fkt(pAfit_s_d, mod_d, peak_func, x,
                                                                                    number_of_spectra, number_of_peaks)

    x_nr_of_subplt = int(input("please enter the number of plots you want to see in x-direction"))
    y_nr_of_subplt = int(input("please enter the number of plots you want to see in y-direction"))
    if y_nr_of_subplt * x_nr_of_subplt == 1:
        spectra_to_plot = int(input("Please enter the spectra nr (0 to n-1) which you want to look at:\n"))
        plotting_fit_single_plot_fkt(x, y_d, mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_p_p_d_eval, number_of_peaks,
                                     spectra_to_plot)
    else:
        plotting_fit_subplots(x, y_d, mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_p_p_d_eval, number_of_peaks,
                              x_nr_of_subplt, y_nr_of_subplt)
