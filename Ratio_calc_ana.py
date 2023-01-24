"""
This script is to use the 'areas_' and 'center_' files created by 'Analysis_data-exporting.py', to calculate different
ratios/shifts of the main peaks.
For this it uses the 'Inputs_ana_ratios.yaml' in the way as written in the example.

Output:
 - chosen ratio between elements. Either:
    - the ratio of different oxid states 'within'(0) a specific element,
    - the ratio of an elements specific oxid state to other 'samples'(1) same oxid state
    - 'between'(2) different elements \
    - or a 'gradient' (3) between between two elements (list of IMFP´s needed)
 - ratio between oxid states of chosen element. Either
    - the shift of an oxid state compared to 'itself'(0) along the sample
    - the shift 'between'(1) different oxid states (1st main peak used)
"""

import yaml
import pandas as pd
import numpy as np
from plots_scripts.Analysis_ana import ratio_calc_choice, oxid_ratio_clac_fkt, el_ratio_calc_fkt, el_ratio_3_el_calc_fkt
from plots_scripts.Analysis_ana import el_gradient_ratio_calc_fkt, el_within_calc_fkt, el_gradient_error_calc_fkt
from plots_scripts.Analysis_ana import center_shift_fkt_choice, center_shift_self_fkt, center_shift_bewteen_fkt
from plots_scripts.Analysis_save_output import writing_ratio_to_file, matrix_creation, mat_writing_to_file, \
    writing_center_to_file, writing_ratio_3_el_to_file


def data_load_fkt(Inputs, area_or_center):
    """
    fkt to load al the wanted file into a df, which then will be used later
    either its using the center or the area part of the exportet stuff from the ana_data_exporting
    """
    skip_rows = Inputs["skip_rows"]
    txt = Inputs["txt"]
    file_name = Inputs["file_name_" + str(area_or_center)]
    el_list = Inputs["el_list"]
    nr_of_elements = len(el_list)
    path_list = {}
    for i in range(nr_of_elements):
        path = el_list[i] + "_file_path"
        path_list[i] = Inputs[path] + file_name + el_list[i] + txt

    df_data = {}
    if area_or_center == "area":
        for i in range(nr_of_elements):
            df_data[el_list[i]] = pd.read_csv(path_list[i], skiprows=skip_rows, delim_whitespace=True, header=None)
    if area_or_center == "center":
        for i in range(nr_of_elements):
            skip_rows_center = skip_rows + 1
            df_data[el_list[i]] = pd.read_csv(path_list[i], skiprows=skip_rows_center, delim_whitespace=True, header=None)
    return df_data


def area_calc_main_fkt(Inputs):
    """
    fkt to calc the different possible ratios/combinations of the area_file. Either:
    - the ratio of different oxid states 'within'(0) a specific element,
    - the ratio of an elements specific oxid state to other 'samples'(1) same oxid state
    - 'between'(2) different elements \
    - a 'gradient' (3) between between two elements (list of IMFP´s needed)
    - or the 'error' (4) of a gradient between between two elements (list of IMFP´s & error´s needed!!!)
    """

    df_area = data_load_fkt(Inputs, "area")

    calc_fin_bool = False
    while not calc_fin_bool:
        ratio_choice = ratio_calc_choice()
        if ratio_choice == 0:
            ratio_tot, ratio_perc, el_nr_1, oxid_1, oxid_2 = oxid_ratio_clac_fkt(Inputs, df_area)
            writing_ratio_to_file(Inputs, ratio_tot, ratio_perc, el_nr_1, None, oxid_1, oxid_2)

        if ratio_choice == 1:
            df_mat, el_nr, oxid = el_within_calc_fkt(Inputs, df_area)
            A = matrix_creation(df_mat, Inputs)
            mat_writing_to_file(A, el_nr, oxid, Inputs)

        if ratio_choice == 2:
            ratio_tot, ratio_perc, el_nr_1, el_nr_2 = el_ratio_calc_fkt(Inputs, df_area)
            writing_ratio_to_file(Inputs, ratio_tot, ratio_perc, el_nr_1, el_nr_2, None, None)

        if ratio_choice == 3:
            ratio_tot, ratio_perc, el_nr_1, el_nr_2, el_nr_3 = el_ratio_3_el_calc_fkt(Inputs, df_area)
            writing_ratio_3_el_to_file(Inputs, ratio_tot, ratio_perc, el_nr_1, el_nr_2, el_nr_3, None, None)

        if ratio_choice == 4:
            ratio_tot, ratio_perc, el_nr_1, el_nr_2,el_1_factor, el_2_factor = el_gradient_ratio_calc_fkt(Inputs, df_area)
            writing_ratio_to_file(Inputs, ratio_tot, ratio_perc, el_nr_1, el_nr_2, None, None)

        if ratio_choice == 5:
            ratio_tot, ratio_perc, el_nr_1, el_nr_2,el_1_factor, el_2_factor = el_gradient_ratio_calc_fkt(Inputs, df_area)
            ratio_error_pos_diff, ratio_error_neg_diff = el_gradient_error_calc_fkt(Inputs, df_area, el_nr_1, el_nr_2, ratio_perc, el_1_factor, el_2_factor)
            writing_ratio_to_file(Inputs, ratio_error_pos_diff, ratio_error_neg_diff, el_nr_1, el_nr_2, None, None)
        calc_fin_choice = input("do you want to calc other ratios as well?\n Please enter 'yes/y' or 'no/n'")
        if calc_fin_choice.lower() == "yes" or calc_fin_choice.lower() == "y":
            continue
        if calc_fin_choice.lower() == "no" or calc_fin_choice.lower() == "n":
            calc_fin_bool = True
    return


def center_calc_main_fkt(Inputs):
    """
    Calcs the shift of the peaks in dependence of each other. Either
    - the shift of an oxid state compared to 'itself'(0) along the sample
    - the shift 'between'(1) different oxid states (1st main peak used)
    """

    df_center = data_load_fkt(Inputs, "center")
    calc_cen_bool = False
    while not calc_cen_bool:
        center_choice = center_shift_fkt_choice()

        if center_choice == 0:
            center_shift, el_nr, oxid = center_shift_self_fkt(Inputs, df_center)
            writing_center_to_file(Inputs, center_shift, el_nr, oxid, None)
        if center_choice == 1:
            center_shift, el_nr, oxid_1, oxid_2 = center_shift_bewteen_fkt(Inputs, df_center)
            writing_center_to_file(Inputs, center_shift, el_nr, oxid_1, oxid_2)

        calc_cen_choice = input("do you want to calc other ratios as well?\n Please enter 'yes/y' or 'no/n'")
        if calc_cen_choice.lower() == "yes" or calc_cen_choice.lower() == "y":
            continue
        if calc_cen_choice.lower() == "no" or calc_cen_choice.lower() == "n":
            calc_cen_bool = True

    return


param_file_path = input(
    "please enter the file path + name of the Inputs-extraction file:\n")
param_file_type_str = "yaml"
param_file_type = yaml

Inputs = param_file_type.load(open(param_file_path + "." + param_file_type_str), Loader=param_file_type.FullLoader)

# choose which ratio one wants to calc:
area_or_center = False
while not area_or_center:
    area_or_center_choice = input("do you want to work with the 'area' (0) or 'center' (1) of the peaks?\n")

    if area_or_center_choice.lower() == "area" or area_or_center_choice == "0":
        area_calc_main_fkt(Inputs)

        cont = input("Do you want to 'continue'(0) with the center calcs or do you want to 'stop'(1)?\n")
        if cont == "continue" or cont == "0":
            area_or_center_choice = "1"
        else:
            area_or_center = True

    if area_or_center_choice.lower() == "center" or area_or_center_choice == "1":
        center_calc_main_fkt(Inputs)

        cont = input("Do you want to 'continue'(0) with the area calcs or do you want to 'stop'(1)?\n")
        if cont == "continue" or cont == "0":
            area_or_center_choice = "0"
        else:
            area_or_center = True