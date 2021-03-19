########################################################################################################################
#                                                                                                                      #
#               in this file plots with fitted parameters are generated.                                               #
#               For this the peak parameter are sorted, and the Models are evaluated                                   #
#               (with and w/o the shirley, which then gets subtracted to get the single shirley as well                #
#               Also can one choose if he wants to see multiple spectra at the same time (and how many)                #
#                                                                                                                      #
########################################################################################################################


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re




def matches_str(key,pattern):
    return pattern.search(key)

def param_per_peak_from_spec_sorting_fkt(p4fit, number_of_spectra, number_of_peaks):
    p4fit_out_p_d = {}
    for i in range(int(number_of_spectra)):
        for idx in range(int(number_of_peaks)):
            pattern = re.compile(f"p{i}_{idx}.*")
            for k, v in p4fit[f'spectra_{i}'].items():
                if matches_str(k,pattern):
                    p4fit_out_p_d[k] = v

    p4fit_p_p_d={}
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
                params=out_params[f"spectra_{i}"])
    return mod_w_only_peaks_p_spec_d_eval

def shirley_BG_only_eval_fkt(model_d,mod_w_only_peaks_p_spec_d_eval, number_of_spectra):
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

def model_w_only_peaks_eval_fkt(mod_w_only_peaks_p_p_d, p4fit_p_p_d,x, number_of_spectra, number_of_peaks):
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

def model_w_sBG_plus_peaks_p_p_eval_d(shirley_BG_d,mod_w_only_peaks_p_p_d_eval, number_of_spectra, number_of_peaks):
    mod_w_sBG_peaks_p_p_d_eval={}
    for i in range(int(number_of_spectra)):
        mod_w_sBG_peaks_p_p_d_eval[f'spectra_{i}']={}
        for idx in range(int(number_of_peaks)):
            mod_w_sBG_peaks_p_p_d_eval[f'spectra_{i}'][f'p_{idx}'] = shirley_BG_d[f"spectra_{i}"]+mod_w_only_peaks_p_p_d_eval[f'spectra_{i}'][f'p_{idx}']
    return mod_w_sBG_peaks_p_p_d_eval


def model_eval_after_fitting_fkt(out_params, model_d_fitted, peak_func, x, number_of_spectra, number_of_peaks):
    p4fit_p_p_d=param_per_peak_from_spec_sorting_fkt(out_params, number_of_spectra, number_of_peaks)
    mod_w_only_peaks_p_spec_d = model_w_only_peaks_p_spec_d(peak_func, number_of_spectra, number_of_peaks)
    mod_w_only_peaks_p_spec_d_eval = model_w_only_peaks_p_spec_eval_d(mod_w_only_peaks_p_spec_d, out_params,x, number_of_spectra, number_of_peaks)
    shirley_BG_d = shirley_BG_only_eval_fkt(model_d_fitted, mod_w_only_peaks_p_spec_d_eval, number_of_spectra)

    mod_w_only_peaks_p_p_d = model_w_only_peaks_fkt(peak_func, number_of_spectra, number_of_peaks)
    mod_w_only_peaks_p_p_d_eval = model_w_only_peaks_eval_fkt(mod_w_only_peaks_p_p_d, p4fit_p_p_d,x, number_of_spectra, number_of_peaks)
    mod_w_sBG_peaks_p_p_d_eval = model_w_sBG_plus_peaks_p_p_eval_d(shirley_BG_d, mod_w_only_peaks_p_p_d_eval, number_of_spectra, number_of_peaks)
    return shirley_BG_d, mod_w_sBG_peaks_p_p_d_eval



def plotting_after_fit_subplots(x, y_d, model_d_fitted, shirley_BG_d, mod_w_sBG_peaks_p_p_d_eval,number_of_peaks, x_nr_of_subplt, y_nr_of_subplt):
    fig, axs = plt.subplots(y_nr_of_subplt, x_nr_of_subplt, figsize=(15, 8), sharex=True, sharey=True)
    for i, axes in enumerate(axs.flat):
        axes.plot(x, y_d[i], 'black', label='data')
        axes.plot(x, model_d_fitted[i], 'r', label='fit')  # envelope of fitted peaks
        for idx in range(int(number_of_peaks)):
            axes.plot(x, mod_w_sBG_peaks_p_p_d_eval[f'spectra_{i}'][f'p_{idx}'],
                      label=f"peak_{idx}")  # every fitted peak + shirley sum
        axes.plot(x, shirley_BG_d[f"spectra_{i}"], 'grey--', label='shirley')  # shirley of fitted peaks
    plt.legend(loc='best')
    plt.show()


def plotting_after_fitting_main_fkt(x, out_params, model_d_fitted, y_d, peak_func, d, number_of_spectra, number_of_peaks):
    shirley_BG_d, mod_w_sBG_peaks_p_p_d_eval= model_eval_after_fitting_fkt(out_params, model_d_fitted, peak_func,x, number_of_spectra, number_of_peaks)

    x_nr_of_subplt = int(input("please enter the number of plots you want to see in x-direction"))
    y_nr_of_subplt = int(input("please enter the number of plots you want to see in y-direction"))
    plotting_after_fit_subplots(x, y_d, model_d_fitted, shirley_BG_d, mod_w_sBG_peaks_p_p_d_eval, number_of_peaks,
                                x_nr_of_subplt, y_nr_of_subplt)





