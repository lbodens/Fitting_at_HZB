import lmfit.models
import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np

from plots_scripts.Param_updater import param_per_spectra_sorting_fkt
from plots_scripts.Data_loader import dat_merger_single_file_fkt, dat_merger_multiple_files_fkt
from plots_scripts.Fitting_functions import y_for_fit
from plots_scripts.Shirley_fkt_build import peak_model_build_main_fkt
from plots_scripts.Plotting_functions import model_separator_eval_fkt


def param_into_pars_and_sorting(params):
    """
    This function takes the pre-cleaned param values and put them into the right type (p{i}_{idx}_name: { value: int})
    and then sorts it into the right type (after spectra)
    """
    # make from the cleaned params (only value int) into dict with p.._name : {value: int}
    param_val = {}
    for name in params:
        if param_val.get(name) is None:
            param_val[name] = {}
        param_val[name]["value"] = params[name]

    # creates the pars
    pars = lmfit.Parameters()
    for name, rest in param_val.items():
        pars.add(lmfit.Parameter(name=name, **rest))

    # and sorts them into the spectra style for the eval&fitting later
    result = param_per_spectra_sorting_fkt(pars)
    return result


def spectra_and_and_model_generator(Inputs, element_number):
    file_type = Inputs["el{}_folder_or_file".format(element_number)]
    skip_rows = Inputs["el{}_skip_rows".format(element_number)]
    txt = Inputs["el{}_txt_or_dat".format(element_number)]
    number_of_spectra = Inputs["number_of_spectra".format(element_number)]
    number_of_peaks = Inputs["el{}_number_of_peaks".format(element_number)]
    if file_type == "file":
        path = Inputs["el{}_file_path".format(element_number)]
        d = dat_merger_single_file_fkt(path, txt, Inputs, int(skip_rows), int(number_of_spectra))
    if file_type == "folder":
        path = Inputs["el{}_folder_path".format(element_number)]
        counting_start = Inputs["el{}_file_counting_start".format(element_number)]
        column_nr = Inputs["el{}_column_nr".format(element_number)]
        d = dat_merger_multiple_files_fkt(path, txt, Inputs, int(skip_rows), counting_start, column_nr, int(number_of_spectra))

    x = d[f'dat_0']["E"].to_numpy()
    y_d, resid = y_for_fit(d, x, number_of_spectra, number_of_peaks)
    mod_d, number_of_peaks, peak_func = peak_model_build_main_fkt(d, Inputs, element_number)

    return d, x, y_d, mod_d, peak_func


def other_spectra_loader(Inputs):
    txt = ".dat"
    skip_rows = 0
    number_of_spectra = 13
    d = {}
    for i in range(13):
        path = "D:\\Profile\\ogd\\Eigene Dateien\\GitHub\\Fitting_at_HZB\\tests\\Ni2p_data_shirley_Row_{}".format(i + 1)
        d["row_{}".format(i)] = dat_merger_single_file_fkt(path, txt, Inputs, int(skip_rows), int(number_of_spectra))
    print(d)
    return d


def plotting_fit_single_plot_fkt(x, y_d, shir_d, mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_p_p_d_eval, Inputs,
                                 element_number, spectra_to_plot):
    number_of_peaks = Inputs["el{}_number_of_peaks".format(element_number)]
    """
    range_of_1st_state = Inputs["el{}_number_per_oxid_state_0".format(element_number)]
    range_of_2nd_state = range_of_1st_state + Inputs["el{}_number_per_oxid_state_1".format(element_number)]
    range_of_3rd_state = range_of_2nd_state + Inputs["el{}_number_per_oxid_state_2".format(element_number)]
    """
    fig, axs = plt.subplots()
    axs.plot(x, y_d[spectra_to_plot], 'black', label='data_{}'.format(element_number))
    axs.plot(x, mod_d_eval[spectra_to_plot], 'r', label='fit')  # envelope of fitted peaks
    """
    for idx in range(int(number_of_peaks)):
        if idx < range_of_1st_state:
            axs.plot(x, mod_w_sBG_peaks_p_p_d_eval[f'spectra_{spectra_to_plot}'][f'p_{idx}'],
                     label="oxid_1", color='g')  # every fitted peak + shirley sum
        if range_of_1st_state <= idx < range_of_2nd_state:
            axs.plot(x, mod_w_sBG_peaks_p_p_d_eval[f'spectra_{spectra_to_plot}'][f'p_{idx}'],
                     label="oxid_2", color='b')  # every fitted peak + shirley sum
        if idx >= range_of_2nd_state:
            axs.plot(x, mod_w_sBG_peaks_p_p_d_eval[f'spectra_{spectra_to_plot}'][f'p_{idx}'],
                     label="BG_peaks", color='orange')  # every fitted peak + shirley sum
    """
    color_list = Inputs["color_list"]
    label_list = Inputs["label_list"]
    check_list = [0]*len(label_list)
    for idx in range(int(number_of_peaks)):
        if check_list[idx] == 0:
            axs.plot(x, mod_w_sBG_peaks_p_p_d_eval[f'spectra_{spectra_to_plot}'][f'p_{idx}'], label=label_list[idx],
                     color=color_list[idx])
            check_list[idx] = 1
        if check_list == 1:
            axs.plot(x, mod_w_sBG_peaks_p_p_d_eval[f'spectra_{spectra_to_plot}'][f'p_{idx}'], color=color_list[idx])

    axs.plot(x, shirley_BG_d[f"spectra_{spectra_to_plot}"], color='grey', linestyle='dashed',
             label='shirley')  # shirley of fitted peaks

    # old shirley
    shir_row_nr = spectra_to_plot % 13
    shir_nr = int(spectra_to_plot / 13)

    s_d = shir_d[f"row_{shir_row_nr}"]['dat_{}'.format(shir_nr)]
    shir_d_min = min(s_d["Spectra"])
    spec_min = min(shirley_BG_d[f"spectra_{spectra_to_plot}"])

    axs.plot(s_d["E"], s_d["Spectra"] - shir_d_min + spec_min, color='purple', linestyle='dashed', label='shirley_old')

    plt.xlim([max(x), min(x)])
    plt.legend(loc='best')
    plt.show()
    return


def plot_2D_map(df, title, Inputs):
    x = np.linspace(1, Inputs["number_of_columns"], Inputs["number_of_columns"])
    x = np.linspace(1, Inputs["number_of_rows"], Inputs["number_of_rows"])
    z = np.array(df)

    # fig, map = plt.subplots()
    Z = z.reshape(Inputs["number_of_columns"], Inputs["number_of_rows"])
    cmap = col.LinearSegmentedColormap.from_list("", ["green", "yellow", "red", "violet", "blue"])
    plt.suptitle(title)
    plt.imshow(Z, cmap=cmap, interpolation="bilinear")
    plt.colorbar()
    plt.show()
    return


def save_2D_map(df, plot_name, Inputs):
    x = np.linspace(1, Inputs["number_of_columns"], Inputs["number_of_columns"])
    x = np.linspace(1, Inputs["number_of_rows"], Inputs["number_of_rows"])
    z = np.array(df)
    Z = z.reshape(Inputs["number_of_columns"], Inputs["number_of_rows"])
    plt.imshow(Z, interpolation="bilinear")
    plt.savefig(Inputs["result_plot_path"] + plot_name + Inputs["result_plot_path_end"])
    return


def plotting_ana_main_fkt(params, Inputs, element_number):
    nr_of_spectra = Inputs["number_of_spectra"]
    number_of_peaks = Inputs["el{}_number_of_peaks".format(element_number)]

    pars_s_d = param_into_pars_and_sorting(params)
    d, x, y_d, mod_d, peak_func = spectra_and_and_model_generator(Inputs, element_number)
    mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_eval = model_separator_eval_fkt(pars_s_d, mod_d, peak_func, x,
                                                                              nr_of_spectra, number_of_peaks)

    shir_d = other_spectra_loader(Inputs)
    plotting_loop = True
    while plotting_loop:
        spectra_to_plot = int(input("which spectra do you want to plot [0:n-1]?\n"))

        plotting_fit_single_plot_fkt(x, y_d, shir_d, mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_eval, Inputs,
                                     element_number, spectra_to_plot)

        continue_loop = input("do you want to plot other spectra as well? please enter 'y' or 'n':\n")
        if continue_loop == 'n':
            break
    return




