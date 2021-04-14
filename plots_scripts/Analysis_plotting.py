import lmfit.models
import matplotlib.pyplot as plt

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
    param_val={}
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
    path = Inputs["el{}_file_path".format(element_number)]
    skip_rows = Inputs["el{}_skip_rows".format(element_number)]
    txt = Inputs["el{}_txt_or_dat".format(element_number)]
    number_of_spectra = Inputs["number_of_spectra".format(element_number)]
    number_of_peaks = Inputs["el{}_number_of_peaks".format(element_number)]
    if file_type == "file":
        d = dat_merger_single_file_fkt(path, txt, Inputs, int(skip_rows), int(number_of_spectra))
    if file_type == "folder":
        d = dat_merger_multiple_files_fkt(path, txt, Inputs, int(skip_rows), int(number_of_spectra))

    x = d[f'dat_0']["E"].to_numpy()
    y_d, resid = y_for_fit(d, x, number_of_spectra, number_of_peaks)
    mod_d, number_of_peaks, peak_func = peak_model_build_main_fkt(d, Inputs, element_number)

    return d, x, y_d, mod_d, peak_func


"""def plotting_fit_single_plot_fkt_2(x, y_d, mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_p_p_d_eval, Inputs, element_number, spectra_to_plot):
    number_of_peaks = Inputs["el{}_number_of_peaks".format(element_number)]
    number_per_oxid_state_0 = Inputs["el{}_number_per_oxid_state_0".format(element_number)]
    number_per_oxid_state_1 = Inputs["el{}_number_per_oxid_state_1".format(element_number)]
    number_per_oxid_state_2 = Inputs["el{}_number_per_oxid_state_2".format(element_number)]

    range_of_1st_state = Inputs["el{}_number_per_oxid_state_0".format(element_number)]
    range_of_2nd_state = range_of_1st_state + Inputs["el{}_number_per_oxid_state_1".format(element_number)]
    range_of_3rd_state = range_of_2nd_state + Inputs["el{}_number_per_oxid_state_2".format(element_number)]

    from cycler import cycler
    my_cycler = cycler('color', ['g', 'b', 'orange']) * cycler('linewidth', [1., 1.5, 2.])
    actual_cycler = my_cycler()

    fig, axes = plt.subplots(2, 3)
    for ax in axes.flat:
        ax.plot((0, 1), (0, 1), **next(actual_cycler))
    return


def plotting_fit_single_plot_fkt_1(x, y_d, mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_p_p_d_eval, Inputs,
                                     element_number, spectra_to_plot):
    names = ['oxid_0', 'Oxid_3', 'BG']  # sample labels
    color = ['g', 'b', 'orange']
    fig = plt.figure()  # save your figure in a variable for later access
    for i in range(5):
        plt.plot([0, 1], [i, i], label=names[i])

    plt.legend()  # still wrong legend for comparison purpose

    ax = fig.gca()  # get the current axis

    for i, p in enumerate(ax.get_lines()):  # this is the loop to change Labels and colors
        if p.get_label() in names[:i]:  # check for Name already exists
            idx = names.index(p.get_label())  # find ist index
            p.set_c(ax.get_lines()[idx].get_c())  # set color
            p.set_label('_' + p.get_label())  # hide label in auto-legend
    plt.legend(loc='center')  # correct legend
    return
"""


def plotting_fit_single_plot_fkt(x, y_d, mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_p_p_d_eval, Inputs, element_number, spectra_to_plot):
    number_of_peaks = Inputs["el{}_number_of_peaks".format(element_number)]
    range_of_1st_state = Inputs["el{}_number_per_oxid_state_0".format(element_number)]
    range_of_2nd_state = range_of_1st_state + Inputs["el{}_number_per_oxid_state_1".format(element_number)]
    range_of_3rd_state = range_of_2nd_state + Inputs["el{}_number_per_oxid_state_2".format(element_number)]
    fig, axs = plt.subplots()
    axs.plot(x, y_d[spectra_to_plot], 'black', label='data_{}'.format(element_number))
    axs.plot(x, mod_d_eval[spectra_to_plot], 'r', label='fit')  # envelope of fitted peaks
    for idx in range(int(number_of_peaks)):
        if idx < range_of_1st_state:
            axs.plot(x, mod_w_sBG_peaks_p_p_d_eval[f'spectra_{spectra_to_plot}'][f'p_{idx}'],
                      label=f"peak_{idx}", color='g')  # every fitted peak + shirley sum
        if range_of_1st_state <= idx < range_of_2nd_state:
            axs.plot(x, mod_w_sBG_peaks_p_p_d_eval[f'spectra_{spectra_to_plot}'][f'p_{idx}'],
                      label=f"peak_{idx}", color='b')  # every fitted peak + shirley sum
        if idx >= range_of_2nd_state:
            axs.plot(x, mod_w_sBG_peaks_p_p_d_eval[f'spectra_{spectra_to_plot}'][f'p_{idx}'],
                      label=f"peak_{idx}", color='orange')  # every fitted peak + shirley sum
    axs.plot(x, shirley_BG_d[f"spectra_{spectra_to_plot}"], color = 'grey', linestyle='dashed', label='shirley')  # shirley of fitted peaks
    plt.xlim([max(x), min(x)])
    plt.legend(loc='best')
    plt.show()
    return


def plotting_ana_main_fkt(params, Inputs, element_number):
    #print(Inputs)
    nr_of_spectra = Inputs["number_of_spectra"]
    number_of_peaks = Inputs["el{}_number_of_peaks".format(element_number)]

    pars_s_d = param_into_pars_and_sorting(params)
    d, x, y_d, mod_d, peak_func = spectra_and_and_model_generator(Inputs, element_number)
    mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_eval = model_separator_eval_fkt(pars_s_d, mod_d, peak_func, x, nr_of_spectra, number_of_peaks)

    plotting_loop = True
    while plotting_loop:
        spectra_to_plot = int(input("which spectra do you want to plot [0:n-1]?\n"))

        plotting_fit_single_plot_fkt(x, y_d, mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_eval, Inputs, element_number, spectra_to_plot)

        continue_loop = input("do you want to plot other spectra aswell? please enter 'y' or 'n':\n")
        if continue_loop == 'n':
            break
    return