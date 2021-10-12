# this function can be used to export the fitted data. but not as parameters but evaluated.
# params = pars_cl_{} with {} = element_number
from plots_scripts.Analysis_ana import get_params_fkt
from plots_scripts.Analysis_plotting import param_into_pars_and_sorting, spectra_and_and_model_generator
from plots_scripts.Plotting_functions import model_separator_eval_fkt
import yaml
import matplotlib.pyplot as plt
import numpy as np


def export_fitted_eval_data_main_fkt(Inputs):

    element_number = Inputs["element_number"]
    nr_of_spectra = Inputs["number_of_spectra"]
    nr_of_peaks = Inputs["el{}_number_of_peaks".format(element_number)]

    pars_cl, df_a_sum, df_a_1_sum, df_c_sum = get_params_fkt(Inputs, element_number)

    pars_s_d = param_into_pars_and_sorting(pars_cl)
    d, x, y_d, mod_d, peak_func = spectra_and_and_model_generator(Inputs, element_number)
    mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_eval = model_separator_eval_fkt(pars_s_d, mod_d, peak_func, x,
                                                                              nr_of_spectra, nr_of_peaks)

    label_list = Inputs["label_list"]
    print("now the results of the analysis (area calc) will be printed out.")
    print("total area : ")
    print(df_a_sum[0])
    print("area of {}: ".format(label_list[0]))
    print(df_a_sum[1])
    print("area of {}: ".format(label_list[1]))
    print(df_a_sum[2])
    print("area of {}: ".format(label_list[2]))
    print(df_a_sum[3])

    printout_loop = False
    while printout_loop is False:
        spectra_to_plot = int(input("please enter the spectra nr (0 to n-1) you want to extract"))
        export_eval_data_fkt(Inputs, element_number, spectra_to_plot, x, mod_w_sBG_peaks_eval, shirley_BG_d,
                                mod_d_eval)

        export_plot_fkt(x, y_d, mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_eval, Inputs, element_number, spectra_to_plot)

        printout_loop_check = input("do you want to extract other spectra as well? if yes please type 'y' or 'yes'. "
                                     "Else any key.")
        if not printout_loop_check.lower() == "y" or printout_loop_check.lower() == "yes":
            printout_loop = True

#        else:
#            continue
    return


def export_plot_fkt(x, y_d, mod_d_eval, shirley_BG_d, mod_w_sBG_peaks_eval, Inputs, element_number, spectra_to_plot):

    number_of_peaks = Inputs["el{}_number_of_peaks".format(element_number)]
    color_list = Inputs["color_list"]   # ["g", "b", "darkorange", "lightgreen", "cornflowerblue", "orange"]
    label_list = Inputs["label_list"]   # ["oxid_1$_{3/2}$", "oxid_2$_{3/2}$", "oxid_3$_{3/2}$", "oxid_1$_{1/2}$",
                                        # "oxid_2$_{1/2}$", "oxid_3$_{1/2}$"]
    oxid_sorting = Inputs["el{}_oxid_and_corelvl_sorting".format(element_number)]

    fig, axs = plt.subplots()
    axs.plot(x, y_d[spectra_to_plot], 'black', label='data_{}'.format(element_number))
    axs.plot(x, mod_d_eval[spectra_to_plot], 'r', label='fit')

    label_check = [True, True, True, True, True, True]
    for idx in range(int(number_of_peaks)):
        if label_check[oxid_sorting[idx]]:
            axs.plot(x, mod_w_sBG_peaks_eval[f'spectra_{spectra_to_plot}'][f'p_{idx}'],
                     label=label_list[oxid_sorting[idx] % 6], color=color_list[oxid_sorting[idx]])
        else:
            axs.plot(x, mod_w_sBG_peaks_eval[f'spectra_{spectra_to_plot}'][f'p_{idx}'],
                     color=color_list[oxid_sorting[idx]])
        label_check[oxid_sorting[idx]] = False

    axs.plot(x, shirley_BG_d[f"spectra_{spectra_to_plot}"], color='grey', linestyle='dashed', label='shirley')

    plt.xlim([max(x), min(x)])
    plt.legend(axs.lines[:5], label_list)
    plt.legend(loc='best')
    plt.show()
    return


def export_eval_data_fkt(Inputs, element_number, spectra_to_plot, x, mod_w_sBG_peaks_eval, shirley_BG_d,
                                mod_d_eval):

    path = Inputs["result_file_path"] + "eval_spec_{}_{}.txt".format(Inputs["el{}_name".format(element_number)],
                                                                     spectra_to_plot)
    file = open(path, "a")
    len_col = len(x)
    spectra_i = "spectra_" + str(spectra_to_plot)

    file.write("Spectra ")
    file.write(str(spectra_to_plot))
    file.write("\n")

    file.write("E")
    file.write(",\t")
    for i in range(Inputs["el{}_number_of_peaks".format(element_number)]):
        p_i = "p_" + str(i)
        file.write(p_i)
        file.write(",\t")
    file.write("shirley")
    file.write(",\t")
    file.write("fit")
    file.write("\n")

    for j in range(len_col):
        file.write(str(x[j]))
        file.write("\t")
        for i in range(Inputs["el{}_number_of_peaks".format(element_number)]):
            p_i = "p_" + str(i)
            file.write(str(mod_w_sBG_peaks_eval[spectra_i][p_i][j]))
            file.write("\t")
        file.write(str(shirley_BG_d[spectra_i][j]))
        file.write("\t")
        file.write(str(mod_d_eval[spectra_to_plot][j]))
        file.write("\t")
        file.write("\n")

    file.close()


param_file_path = input("please enter the file path + name of the Inputs-extraction file:\n")#"D:\\Profile\\ogd\\Eigene Dateien\\GitHub\\Fitting_at_HZB\\tests\\"
param_file_type_str = "yaml"
param_file_type = yaml

Inputs = param_file_type.load(open(param_file_path + "." + param_file_type_str), Loader=param_file_type.FullLoader)

export_fitted_eval_data_main_fkt(Inputs)
