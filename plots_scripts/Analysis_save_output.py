"""
sub-file with all the functions put together who have something to do with data output/saving From the analysis scripts
"""

import numpy as np
from plots_scripts.Analysis_plotting import plot_2D_map, save_2D_map


"""----------------Analysis_data_exporting-------------"""


def export_area_fkt(df_a, element_nr, nr_of_spectra, Inputs):
    """
    This function will save the areas of the different peaks (according to the list of oxid_and_corelcalc sorting and
    the naming list) in a file
    """

    path = Inputs["result_file_path"] + "areas_" + Inputs["el{}_name".format(element_nr)] + ".txt"
    label_list = Inputs["label_list"]
    list_length = len(label_list)

    list_of_peaks_per_el = Inputs["el{}_number_of_peaks_per_el".format(element_nr)]
    nr_of_elements = len(list_of_peaks_per_el)
    half_list_len = int(nr_of_elements/2)
    counter = 0

    file = open(path, "a")

    file.write("The following areas are corresponding to the label list: " + str(label_list))
    file.write("\n\n")
    # writing header
    file.write("Spectra")
    file.write("\t")
    file.write("tot area of 1st half")
    file.write("\t")
    for i in range(half_list_len):
        file.write("sum of next '{}'".format(list_of_peaks_per_el[i]))
        file.write("\t")
        for j in range(list_of_peaks_per_el[i]):
            file.write("'{}'".format(label_list[counter + j]))
            file.write("\t")
        counter += list_of_peaks_per_el[i]
    file.write("tot area of last half")
    file.write("\t")
    for i in range(half_list_len, len(list_of_peaks_per_el)):
        file.write("sum of next '{}'".format(list_of_peaks_per_el[i]))
        file.write("\t")
        for j in range(list_of_peaks_per_el[i]):
            file.write("'{}'".format(label_list[counter + j]))
            file.write("\t")
        counter += list_of_peaks_per_el[i]
    file.write("\n")

    # writing areas
    for s in range(nr_of_spectra):
        spectra_s = "spectra_" + str(s)
        file.write("S" + str(s))
        file.write("\t")
        for i in range(len(df_a)):
            file.write(str(df_a[i][spectra_s]))
            file.write("\t")
        file.write("\n")
    file.close()


def export_center_fkt(df_c, element_nr, nr_of_spectra, Inputs):
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
        for i in range(len(df_c)):
            file.write(str(df_c[i][spectra_s]))
            file.write("\t")
        file.write("\n")
    file.close()


def export_eval_data_fkt(Inputs, element_number, spectra_to_plot, x, y_d, mod_w_sBG_peaks_eval, shirley_BG_d,
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
    file.write(",\t")
    file.write("data")
    file.write(",\t")
    file.write("residuum")
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
        file.write(str(y_d[spectra_to_plot][j]))
        file.write("\t")
        file.write(str(mod_d_eval[spectra_to_plot][j]-y_d[spectra_to_plot][j]))
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
    label_list = Inputs[el_list[el_nr_1] + "_label_list"]

    file = open(path, "a")
    if el_nr_2 is not None:
        file.write("The ratios of the total area of the main/dominant spin orbit of " + str(el_list[el_nr_1]) + " and "
                   + str(el_list[el_nr_2]) + " are now saved. With the tot-ratio (el1/el2) and %-ratio (el1/(el1+el2))."
                    "\n the sigma were: " + str(el_list[el_nr_1])+": "+str(Inputs[el_list[el_nr_1]+"_sigma"][0])+" & "
                    + str(el_list[el_nr_2]) + ": " + str(Inputs[el_list[el_nr_2]+"_sigma"][0]))
    if el_nr_2 is None:
        file.write("The ratios of " + str(el_list[el_nr_1]) + "´s oxid_state " + str(oxid_1) + " and " + str(oxid_2) +
                   " according to the area_" + str(el_list[el_nr_1]) + " file (" + str(label_list)+")")
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


def writing_ratio_3_el_to_file(Inputs, ratio_tot, ratio_perc, el_nr_1, el_nr_2=None, el_nr_3=None, oxid_1=None, oxid_2=None):
    """
    This function will save the total and percentage ratio of the chosen type into a file with the name/folder of the
    1st selected element
    """
    el_list = Inputs["el_list"]
    el_path = el_list[el_nr_1] + "_file_path"
    path = Inputs[el_path] + "Ratio_results_" + str(el_list[el_nr_1]) + ".txt"
    label_list = Inputs[el_list[el_nr_1] + "_label_list"]

    file = open(path, "a")
    if el_nr_2 is not None:
        file.write("The ratios of the total area of the main/dominant spin orbit of " + str(el_list[el_nr_1]) + ", "
                   + str(el_list[el_nr_2]) + " and " + str(el_list[el_nr_3]) + " are now saved. With the tot-ratio "
                   "(el1/(el2+el3)) and %-ratio (el1/(el1+el2+el3)).\nThe sigma were: "
                   + str(el_list[el_nr_1])+": " + str(Inputs[el_list[el_nr_1]+"_sigma"][0])+" & "
                   + str(el_list[el_nr_2]) + ": " + str(Inputs[el_list[el_nr_2] + "_sigma"][0]) + " & "
                   + str(el_list[el_nr_3]) + ": " + str(Inputs[el_list[el_nr_3]+"_sigma"][0]))
    if el_nr_2 is None:
        file.write("The ratios of " + str(el_list[el_nr_1]) + "´s oxid_state " + str(oxid_1) + " and " + str(oxid_2) +
                   " according to the area_" + str(el_list[el_nr_1]) + " file (" + str(label_list)+")")
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