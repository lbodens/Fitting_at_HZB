"""
sub-file with all the functions put together who have something to do with data output/saving From the analysis scripts
"""

import numpy as np
from plots_scripts.Analysis_plotting import plot_2D_map, save_2D_map


"""----------------Analysis_data_exporting-------------"""


def export_area_fkt(df_a_sum, df_a_1_sum, element_nr, nr_of_spectra, Inputs):
    """
    This function will save the areas of the different peaks (according to the list of oxid_and_corelcalc sorting and
    the naming list) in a file
    """

    path = Inputs["result_file_path"] + "areas_" + Inputs["el{}_name".format(element_nr)] + ".txt"
    label_list = Inputs["label_list"]
    list_length = len(label_list)
    list_mid = int(list_length / 2)
    file = open(path, "a")

    file.write("The following areas are corresponding to the label list: " + str(label_list))
    file.write("\n\n")
    file.write("Spectra")
    file.write("\t")
    file.write("'tot area of 1st 5'")
    file.write("\t")
    for i in range(list_mid):
        file.write("'{}'".format(label_list[i]))
        file.write("\t")
    file.write("'tot area of last 5'")
    file.write("\t")
    for i in range(list_mid, list_length):
        file.write("'{}'".format(label_list[i]))
        file.write("\t")
    file.write("\n")
    for s in range(nr_of_spectra):
        spectra_s = "spectra_" + str(s)
        file.write("S" + str(s))
        file.write("\t")
        for i in range(list_mid + 1):
            file.write(str(df_a_sum[i][spectra_s]))
            file.write("\t")
        for i in range(list_mid + 1):
            file.write(str(df_a_1_sum[i][spectra_s]))
            file.write("\t")
        file.write("\n")
    file.close()


def export_center_fkt(df_c_sum_0, df_c_sum_1, element_nr, nr_of_spectra, Inputs):
    """
    This function will save the areas of the different peaks (according to the list of oxid_and_corelcalc sorting and
    the naming list) in a file
    """

    path = Inputs["result_file_path"] + "center_" + Inputs["el{}_name".format(element_nr)] + ".txt"
    label_list = Inputs["label_list"]
    file = open(path, "a")

    file.write("The following center are from the 1st (main) peak of the first 5 corresponding to the label list: " +
               str(label_list) + "\nThe following investigated peaks are selected by the 'nr_per_oxid_state_#', "
                                 "which will be skipped, with respect to the naming pi_#_center")
    file.write("\n\n")
    file.write("Spectra")
    file.write("\t")
    for i in range(len(label_list)):
        file.write("'{}' ".format(label_list[i]))
        file.write("\t")
    file.write("\n")

    for s in range(nr_of_spectra):
        spectra_s = "spectra_" + str(s)
        file.write("S" + str(s))
        file.write("\t")
        for i in range(len(df_c_sum_0)):
            file.write(str(df_c_sum_0[i][spectra_s]))
            file.write("\t")
        for i in range(len(df_c_sum_1)):
            file.write(str(df_c_sum_1[i][spectra_s]))
            file.write("\t")
        file.write("\n")
    file.close()


def export_eval_data_fkt(Inputs, element_number, spectra_to_plot, x, mod_w_sBG_peaks_eval, shirley_BG_d,
                         mod_d_eval):
    """
    this fkt exports the evaluated peaks into a file with:
     - all the peaks + shirley
     - shirly itself
     - the sum of all peaks + shirley (fit)
    """
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


"""---------ratio_calc_ana exporting----------------"""


def writing_ratio_to_file(Inputs, ratio_tot, ratio_perc, el_nr_1, el_nr_2=None, oxid_1=None, oxid_2=None):
    """
    This function will save the total and percentage ratio of the chosen type into a file with the name/folder of the
    1st selected element
    """
    el_list = Inputs["el_list"]
    el_path = el_list[el_nr_1] + "_file_path"
    path = Inputs[el_path] + "Ratio_results_" + str(el_list[el_nr_1]) + ".txt"

    file = open(path, "a")
    if el_nr_2 is not None:
        file.write("The ratios of the total area of the main/dominant spin orbit of " + str(el_list[el_nr_1]) + " and "
                   + str(el_list[el_nr_2]) + " are now saved. With the tot-ratio (el1/el2) and %-ratio (el1/(el1+el2))."
                    "\n the sigma were: " + str(el_list[el_nr_1])+": "+str(Inputs[el_list[el_nr_1]+"_sigma"][0])+" & "
                    + str(el_list[el_nr_2]) + ": " + str(Inputs[el_list[el_nr_2]+"_sigma"][0]))
    if el_nr_2 is None:
        file.write("The ratios of " + str(el_list[el_nr_1]) + "´s oxid_state " + str(oxid_1) + " and " + str(oxid_2) +
                   " according to the area_" + str(el_list[el_nr_1]) + " file")
    file.write("\n")
    file.write("Spectra")
    file.write("\t")
    file.write("Ratio_perc")
    file.write("\t")
    file.write("Ratio_tot")
    file.write("\n")
    for s in range(len(ratio_tot)):
        file.write("S" + str(s))
        file.write("\t")
        file.write(str(float(format(ratio_perc[s], '.2f'))))
        file.write("\t")
        file.write(str(float(format(ratio_tot[s], '.2f'))))
        file.write("\n")
    file.write("\n")
    file.close()
    return


def matrix_creation(df, Inputs):
    """
    changes the given df into a matrix style function
    """
    nr_of_columns = int(np.sqrt(len(df)))
    nr_of_rows = int(np.sqrt(len(df)))

    array_d = []
    for name, rest in df.items():
        array_d.append(rest)
    array = np.array(array_d)

    A = array.reshape(nr_of_columns, nr_of_rows)
    return A


def mat_writing_to_file(A, el_nr, oxid, Inputs):
    """
    This function will save the areas of the different peaks (according to the list of oxid_and_core calc sorting and the
    naming list) in a file
    """
    element = Inputs["el_list"][el_nr]
#    path = Inputs["result_path"] + "matrix_" + str(element) + "_oxid_" + str(oxid) + ".txt"
#    file = open(path, "a")

    el_list = Inputs["el_list"]
    el_path = el_list[el_nr] + "_file_path"
    path = Inputs[el_path] + "Ratio_results_" + str(el_list[el_nr]) + ".txt"

    file = open(path, "a")


    file.write("Matrix is " + str(element) + " with oxid_state " + str(oxid) + " according to the area_" + str(element)
               + " file")
    file.write("\n")
    file.write("Spectra")
    file.write("\t")
    for i in range(len(A)):
        file.write("S" + str(i))
        file.write("\t")
    file.write("\n")
    for s in range(len(A)):
        file.write("S" + str(s))
        file.write("\t")
        for i in range(len(A)):
            file.write(str(A[s][i]))
            file.write("\t")
        file.write("\n")
    file.write("\n")
    file.close()
    return


def writing_center_to_file(Inputs, center_shift, el_nr, oxid_1, oxid_2=None):
    """
    This function will save the center shifts of the chosen element, oxid state and  type into a file with the
    name/folder of the 1st selected element
    """
    el_list = Inputs["el_list"]
    el_path = el_list[el_nr] + "_file_path"
    path = Inputs[el_path] + "Ratio_results_" + str(el_list[el_nr]) + ".txt"

    file = open(path, "a")
    if oxid_2 is None:
        file.write("The shift of the main/dominant peak of the " + str(Inputs[el_list[el_nr]+"_label_list"][oxid_1]) +
                    " set is now saved. In dependence to the first peak")
    if oxid_2 is not None:
        file.write("The shift of the main/dominant peak between " + str(Inputs[el_list[el_nr]+"_label_list"][oxid_1]) +
                   " and " + str(Inputs[el_list[el_nr]+"_label_list"][oxid_2]) + " is saved. ")
    file.write("\n")
    file.write("Spectra")
    file.write("\t")
    file.write("el shift /eV")
    file.write("\n")
    for s in range(len(center_shift)):
        file.write("S" + str(s))
        file.write("\t")
        file.write(str(float(format(center_shift[s], '.2f'))))
        file.write("\n")
    file.write("\n")
    file.close()
    return



"""--------------------result_analysis_ pars (old)-------------------"""
def matrix_and_plot_creation_and_save(df, message, plot_name ,Inputs):
    A = matrix_creation(df, Inputs)
    plot_2D_map(A, plot_name, Inputs)
    write_to_file(A, message, Inputs)
    save_2D_map(A, plot_name, Inputs)
    return

def matrix_creation_and_save(df, message, Inputs):
    A = matrix_creation(df, Inputs)
    write_to_file(A, message, Inputs)
    return

def matrix_creation(df, Inputs):
    """
    changes the given df into a matrix style function
    """
    nr_of_columns = Inputs["number_of_columns"]
    nr_of_rows = Inputs["number_of_rows"]

    array_d = []
    for name, rest in df.items():
        array_d.append(rest)
    array = np.array(array_d)

    A = array.reshape(nr_of_columns, nr_of_rows)
    return A


def write_to_file(A, message, Inputs):
    file = open(Inputs["result_file_path"], "a")

    content = str(A)
    file.write(message)
    file.write("\n")
    file.write("\n")
    file.write(content)
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.close()


def save_to_file_main_fkt(Inputs, df_a_1, df_a_2, df_a_tot, df_c_shift_bw_oxid, df_c_shift_el1, df_c_shift_el2):
    df_ratio_perc_1, df_ratio_abs_1 = df_a_1
    df_ratio_perc_2, df_ratio_abs_2 = df_a_2
    df_ratio_perc_tot, df_ratio_abs_tot = df_a_tot


    matrix_and_plot_creation_and_save(df_ratio_perc_1, "Percentage ratio of oxid state 1 to 2 of {}:".format(Inputs["el1_name"]),
                             "perc_oxid_{}:".format(Inputs["el1_name"]), Inputs)
    matrix_creation_and_save(df_ratio_abs_1, "Absolute ratio of oxid state 1 to 2 of {}:".format(Inputs["el1_name"]),
                             Inputs)
    matrix_and_plot_creation_and_save(df_ratio_perc_2, "Percentage ratio of oxid state 1 to 2 of {}:".format(Inputs["el2_name"]),
                             "perc_oxid_{}:".format(Inputs["el2_name"]),Inputs)
    matrix_creation_and_save(df_ratio_abs_2, "Absolute ratio of oxid state 1 to 2 of {}:".format(Inputs["el2_name"]),
                             Inputs)
    matrix_and_plot_creation_and_save(df_ratio_perc_tot,
                             "Percentage ratio of {} to {}:".format(Inputs["el1_name"], Inputs["el2_name"]),
                             "perc_oxid_{}_to_{}:".format(Inputs["el1_name"], Inputs["el2_name"]), Inputs)
    matrix_creation_and_save(df_ratio_abs_tot,
                             "Absolute ratio of {} to {}:".format(Inputs["el1_name"], Inputs["el2_name"]), Inputs)

    matrix_creation_and_save(df_c_shift_bw_oxid, "Energy shift of main peak between oxid state 1 & 2", Inputs)
    matrix_creation_and_save(df_c_shift_el1,
                             "Energy shift of the main peak over the sample in dependence of the 1st main peaks position of {}:".format(
                                 Inputs["el1_name"]), Inputs)
    matrix_creation_and_save(df_c_shift_el2,
                             "Energy shift of the main peak over the sample in dependence of the 1st main peaks position of {}:".format(
                                 Inputs["el2_name"]), Inputs)
    return



