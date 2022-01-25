import yaml, json
import pandas as pd
import numpy as np


"""---------------for Analysis_data_exporting------------------"""


def get_params_fkt(Inputs, element_number):
    """
    function, which loads a fit result and saves it into a df. Then cleans it and sorts it after area and center.
    Which one is loaded depends on the 'element_number'

    """
    param_file_type = Inputs["el{}_param_file_type".format(element_number)]
    param_file_name = Inputs["el{}_param_file_name".format(element_number)]

    pars = result_param_reader(param_file_type, param_file_name)
    pars_cl = param_cleaning_fkt(pars)

    pars_area = param_area_sorting_fkt(pars_cl, Inputs, element_number)
    pars_center = param_center_sorting_fkt(pars_cl, Inputs, element_number)

    df_a = oxid_state_area_sort_fkt(pars_area, Inputs, element_number)
    df_c = oxid_state_center_sort_fkt(pars_center, Inputs, element_number)

    return pars_cl, df_a, df_c


def result_param_reader(param_file_type, param_file_name):
    """
    fkt to set the right param-file type
    """
    if param_file_type == "yaml":
        param_file_type = yaml
        param_file_type_str = "yaml"
    if param_file_type == "json":
        param_file_type = json
        param_file_type_str = "json"
    params = param_file_type.load(open(str(param_file_name) + '.' + param_file_type_str), Loader=param_file_type.FullLoader)
    return params


def param_cleaning_fkt(pars):
    """
    this function cleans the parms, so that only the real values (ints and floats) are left.
    before that, there are a lot ov other str parts, which are not used for calculations
    """
    result_pars = {}
    for name in pars:
        pos_val_start = pars[name].index("=")
        pos_val_end = pars[name].index(", bound")
        if " (fixed)" in pars[name]:
            pos_val_end = pars[name].index(" (fixed)")

        pars_value = ""
        for k in range(pos_val_start+1, pos_val_end):
            pars_value = pars_value + pars[name][k]
        pars_value = float(pars_value)
        result_pars[name] = pars_value
    return result_pars


def param_area_sorting_fkt(pars, Inputs, element_number):
    """
    This function sorts all params by the amplidude values and save them into a
    df["spectra_{i}"]["p{i}_{idx}_amplitude"] style (with each peak as a single value)
    """
    number_of_spectra = Inputs["number_of_spectra"]
    number_of_peaks = Inputs["el{}_number_of_peaks".format(element_number)]

    pars_area_di = {}
    for i in range(int(number_of_spectra)):
        pars_area_di["spectra_" + str(i)] = {}
    for idx in range(int(number_of_peaks)):
        for i in range(int(number_of_spectra)):
            for name in pars:
                if 'p{}_{}_amplitude'.format(i, idx) in name:
                    pars_area_di["spectra_" + str(i)][f"{name}"] = pars[name]

    return pars_area_di


def get_werte(werte_list, begin, end):
    return werte_list[begin:end]


def sum_list(list):
    sum=0
    for i in range(len(list)):
        sum += list[i]
    return sum


def oxid_state_area_sort_fkt(pars_df, Inputs, element_number):
    """
    This function adds all the peaks per oxidation state and spin-orbit-splitting into a df each (and the sum of all)
    These are saved in containers which will have the first 3 and last 3 of the naming list [a:3/2_1, b:3/2_2, c:3/2_3,
    d:1/2_1, e:1/2_2, f:1/2_3] put together. Corresponding to the oxid_and_corelvl_sorting list
    --> container1: all 3/2 (a-c), container2: all 1/2 (d-f)
    """
    number_of_spectra = Inputs["number_of_spectra"]
    number_of_peaks = Inputs["el{}_number_of_peaks".format(element_number)]
    oxid_core_lvl_list = Inputs["el{}_oxid_and_corelvl_sorting".format(element_number)]
    list_of_peaks_per_el = Inputs["el{}_number_of_peaks_per_el".format(element_number)]
    nr_of_oxid_states = Inputs["el{}_number_of_total_oxid_state".format(element_number)]
    nr_of_elements = len(list_of_peaks_per_el)
    half_list_len = int(nr_of_elements/2)
    nr_peaks_1_half = sum(list_of_peaks_per_el[0:half_list_len])
    nr_peaks_2_half = sum(list_of_peaks_per_el[half_list_len: len(list_of_peaks_per_el)])

    # creation of df where all sum's of the spin-orbit splitting, elements/oxid states (who belong togther) and each
    # oxid sates separately area included with: [0:sum of tot, 1: sum(el1), 2: el1[i], 3: sum(el2) el2[i], ...]
    df_o = {}

    for i in range(nr_of_oxid_states * 2 + nr_of_elements + 2):
        df_o[i] = {}

    for i in range(int(number_of_spectra)):
        spectra_i = "spectra_" + str(i)
        # creation of list for the input for the df,
        df_list = []
        area = [0] * (nr_of_oxid_states * 2)

        # add areas which belong together together (according to oxid_cre_lvl_list)
        for name in pars_df[spectra_i]:
            for idx in range(number_of_peaks):
                if f'p{i}_{idx}_' in name:
                    area[oxid_core_lvl_list[idx]] = area[oxid_core_lvl_list[idx]] + pars_df[spectra_i][name]

        # "insert" the sums at the right places in new df (first (e.g. 2p3/2) half)
        begin_idx = 0
        df_list.append(sum_list(area[0:nr_peaks_1_half]))
        for j in range(half_list_len):
            value = get_werte(area, begin_idx, begin_idx + list_of_peaks_per_el[j])
            sum_of_list = sum_list(value)
            df_list.append(sum_of_list)
            df_list.extend(value)
            begin_idx += list_of_peaks_per_el[j]

        # 2nd half (e.g. 2p1/2)
        df_list.append(sum_list(area[nr_peaks_1_half:nr_peaks_2_half]))
        for j in range(half_list_len):
            value = get_werte(area, begin_idx, begin_idx + list_of_peaks_per_el[j])
            sum_of_list = sum_list(value)
            df_list.append(sum_of_list)
            df_list.extend(value)
            begin_idx += list_of_peaks_per_el[j]

        # putting all into big df with all spectra in one
        for o in range(nr_of_oxid_states * 2 + nr_of_elements + 2):
            df_o[o][spectra_i] = df_list[o]

    return df_o


def param_center_sorting_fkt(pars, Inputs, element_number):
    """
    This function sorts all params by the center values and save them into a df["spectra_{i}"]["p{i}_{idx}_center"] style (with each peak as a single value)
    """
    number_of_spectra = Inputs["number_of_spectra"]
    number_of_peaks = Inputs["el{}_number_of_peaks".format(element_number)]

    pars_center_di = {}
    for i in range(int(number_of_spectra)):
        pars_center_di[f"spectra_{i}"] = {}
    for idx in range(int(number_of_peaks)):
        for i in range(int(number_of_spectra)):
            for name in pars:
                if f'p{i}_{idx}_center' in name:
                    pars_center_di[f'spectra_{i}'][f"{name}"] = pars[name]
    return pars_center_di


def oxid_state_center_sort_fkt(pars_df, Inputs, element_number):
    """
    fkt to sort all the centers of the peaks according to the 'oxid_and_corelvl_sorting'-list and the corresponding
    spin-orbit-splitting and put them into a container
    """
    number_of_spectra = Inputs["number_of_spectra"]
    number_of_peaks = Inputs["el{}_number_of_peaks".format(element_number)]
    oxid_core_lvl_list = Inputs["el{}_oxid_and_corelvl_sorting".format(element_number)]
    nr_of_oxid_states = Inputs["el{}_number_of_total_oxid_state".format(element_number)]

    df_c = {}
    for i in range(nr_of_oxid_states):
        df_c[i] = {}

    for i in range(int(number_of_spectra)):
        spectra_i = "spectra_" + str(i)

        # setting the area to 0 at the beginning for each spectra
        center = [0] * (nr_of_oxid_states * 2)

        for name in pars_df[spectra_i]:
            for idx in range(number_of_peaks):
                if f'p{i}_{idx}_' in name and center[oxid_core_lvl_list[idx]] == 0:
                    center[oxid_core_lvl_list[idx]] = center[oxid_core_lvl_list[idx]] + pars_df[spectra_i][name]

        for o in range(nr_of_oxid_states):
            df_c[o][spectra_i] = center[o]

    return df_c


"""------------all fkt´s for Ratio_calc_ana - Area part ---------------------"""


def ratio_calc_choice():
    """
    fkt to chose which area calculation should be done:
    - the ratio of different oxid states 'within'(0) a specific element,
    - the ratio of an elements specific oxid state to other 'samples'(1) same oxid state
    - 'between'(2) different elements
    - a 'gradient' (3) between between two elements (list of IMFP´s needed)
    - or the 'error' (4) of a gradient between between two elements (list of IMFP´s & error´s needed!!!)
    """
    ratio_choice_bool = False
    while not ratio_choice_bool:
        ratio_choice = input(
            "Please choose if you want to calc: \n"
            "- the ratio of different oxid states 'within'(0) a specific element,\n"
            "- the ratio of an elements specific oxid state to other 'samples'(1) same oxid state \n"
            "- 'between'(2) different elements \n"
            "- a 'gradient' (3) between between two elements (list of IMFP´s needed)\n"
            "- or the 'error' (4) of a gradient between between two elements (list of IMFP´s & error´s needed!!!)\n"
            "please enter either the words or number\n")
        if (ratio_choice.lower() == "within") or ratio_choice == "0":
            ratio_choice = 0
            return ratio_choice
        elif (ratio_choice.lower() == "sample") or ratio_choice == "1":
            ratio_choice = 1
            return ratio_choice
        elif (ratio_choice.lower() == "between") or ratio_choice == "2":
            ratio_choice = 2
            return ratio_choice
        elif (ratio_choice.lower() == "gradient") or ratio_choice == "3":
            ratio_choice = 3
            return ratio_choice
        elif (ratio_choice.lower() == "error") or ratio_choice == "4":
            ratio_choice = 4
            return ratio_choice
        else:
            ratio_choice_bool = False


def if_sweep_list_fkt(Inputs,area, el_chosen):
    if Inputs[str(el_chosen) + "_sweep_list"] is True:
        el_sweep = pd.read_csv(Inputs[str(el_chosen) + "_sweep_list_path"], skiprows=Inputs["skip_rows"],
                                 delim_whitespace=True, header=None)
    else:
        el_sweep = pd.DataFrame(data=np.zeros((len(area), 2)))
        for i in range(len(area)):
            el_sweep.loc[i, 0] = "S" + str(i)
            el_sweep.loc[i, 1] = Inputs[str(el_chosen) + "_sweep"]
    return el_sweep


def if_IMFP_list_fkt(Inputs,area, el_chosen, oxid):
    if Inputs[str(el_chosen) + "_IMFP_list"] is True:
        el_IMFP = pd.read_csv(Inputs[str(el_chosen) + "_IMFP_list_path"], skiprows=Inputs["skip_rows"],
                                 delim_whitespace=True, header=None)
    else:
        el_IMFP = pd.DataFrame(data=np.zeros((len(area), 2)))
        for i in range(len(area)):
            el_IMFP.loc[i, 0] = "S" + str(i)
            el_IMFP.loc[i, 1] = Inputs[str(el_chosen) + "_IMFP"][oxid]
    return el_IMFP


def if_error_list_fkt(Inputs,area, el_chosen):
    if Inputs[str(el_chosen) + "_error_list"] is True:
        el_error = pd.read_csv(Inputs[str(el_chosen) + "_error_list_path"], skiprows=Inputs["skip_rows"],
                                 delim_whitespace=True, header=None)
    else:
        el_error = pd.DataFrame(data=np.zeros((len(area), 2)))
        for i in range(len(area)):
            el_error.loc[i, 0] = "S" + str(i)
            el_error.loc[i, 1] = Inputs[str(el_chosen) + "_error"]
    return el_error


def oxid_ratio_clac_fkt(Inputs, df):
    """
    fkt which calculates the ratio between the desired oxid sates of the chosen element
    """
    el_list = Inputs["el_list"]
    el_to_calc = int(input("please enter the nr of the el according to " + str(el_list) + " in the type of [0,1,2...]"))
    print("Please enter the oxid state you want to calc [1-3].\nIf you want to have the ratio of an element in "
          "regards to the total area type '0' for that element ([tot, ox_1, ox_2, ox_3] in the type of [0,1,"
          "2...])\n They will be calculated by 'ox_1/ox_2' & 'ox_1/(ox1_ox2)'")
    oxid_1 = int(input("please enter the 1st oxid state you want to calc"))
    oxid_2 = int(input("please enter the 2nd oxid state you want to calc"))
    el_chosen = el_list[el_to_calc]

    area_1 = df[el_chosen][oxid_1 + 1]          # the +1 is necessary, since the 0th column is S00 etc
    area_2 = df[el_chosen][oxid_2 + 1]
    # check if there is a list of sweeps, if yes load it, if not create a df with the static sweep written into it
    el_sweep = if_sweep_list_fkt(Inputs, area_1, el_chosen)
    el_1_IMFP = if_IMFP_list_fkt(Inputs, area_1, el_chosen, oxid_1)
    el_2_IMFP = if_IMFP_list_fkt(Inputs, area_2, el_chosen, oxid_2)

    ox_factor = pd.DataFrame(data=np.zeros((len(area_1), len(Inputs[str(el_chosen) + "_sigma"]))))
    for i in range(len(area_1)):
        ox_factor.loc[i, 0] = "S" + str(i)
        ox_factor.loc[i, oxid_1] = (Inputs[str(el_chosen) + "_sigma"][oxid_1] * Inputs[str(el_chosen) + "_TF"] *
                   el_1_IMFP[1][0] * el_sweep[1][i])
        ox_factor.loc[i, oxid_2] = (Inputs[str(el_chosen) + "_sigma"][oxid_2] * Inputs[str(el_chosen) + "_TF"] *
                   el_2_IMFP[1][0] * el_sweep[1][i])

    ratio_tot = [0]*len(area_2)
    ratio_perc = [0]*len(area_2)
    for i in range(len(area_1)):
        ratio_tot[i] = ((area_1[i] / ox_factor.loc[i, oxid_1]) / (area_2[i] / ox_factor.loc[i, oxid_2]))
        ratio_perc[i] = (area_1[i] / ox_factor.loc[i, oxid_1]) / ((area_1[i] / ox_factor.loc[i, oxid_1])
                                                               + (area_2[i] / ox_factor.loc[i, oxid_2]))
    return ratio_tot, ratio_perc, el_to_calc, oxid_1, oxid_2


def el_within_calc_fkt(Inputs, df):
    """
    fkt which calculates the ratio between samples itsef, of a desired oxid sates of the chosen element
    """
    el_list = Inputs["el_list"]
    el_to_calc = int(input("please enter the nr of el according to " + str(el_list) + " in the type of [0,1,2...]"))
    print("Please enter the oxid state you want to analyze the ratio within the chosen element [1-3].\n"
          "If you want to have the ratio of the the total areas type '0' for that element ([tot, ox_1, ox_2, ox_3] in "
          "the type of [0,1,2...])\n")
    oxid = int(input("Please enter the oxid state you want to calc"))

    el_chosen = el_list[el_to_calc]
    area = df[el_chosen][int(oxid)+1]
    df_len = len(df[el_chosen])
    df_mat = {}
    for i in range(df_len):
        for j in range(df_len):
            df_mat[j + (df_len * i)] = area[i] / area[j]
    return df_mat, el_to_calc, oxid


def el_ratio_calc_fkt(Inputs, df):
    """
    this function calculates the ratio between 2 chosen elements taking the area_tot of the first spin-orbit splitting
    one can choose an element from the list written in the ratio-calc.yaml file. then  it takes the needed parameters
    from it.
    If one has different sweeps for different measurement one can put it into a file and this will be called then.
    it then calc the ratio and percentage ratio of the chosen element
    """
    el_list = Inputs["el_list"]
    element_1 = int(input("please enter the nr of the 1st element according to " + str(el_list) +
                          " in the type of [0,1,2...]"))
    element_2 = int(input("please enter the nr of the 2nd element according to " + str(el_list) +
                          " in the type of [0,1,2...]"))
    el_chosen_1 = el_list[element_1]
    el_chosen_2 = el_list[element_2]
    area_1 = df[el_list[element_1]][1]
    area_2 = df[el_list[element_2]][1]

    # check if there is a list of sweeps, if yes load it, if not create a df with the static sweep written into it
    el_1_sweep = if_sweep_list_fkt(Inputs, area_1, el_chosen_1)
    el_2_sweep = if_sweep_list_fkt(Inputs, area_2, el_chosen_2)
    el_1_IMFP = if_IMFP_list_fkt(Inputs, area_1, el_chosen_1, 0)
    el_2_IMFP = if_IMFP_list_fkt(Inputs, area_2, el_chosen_2, 0)

    el_1_factor = pd.DataFrame(data=np.zeros((len(area_1), 2)))
    for i in range(len(area_1)):
        el_1_factor.loc[i, 0] = "S" + str(i)
        el_1_factor.loc[i, 1] = (Inputs[str(el_chosen_1) + "_sigma"][0] * Inputs[str(el_chosen_1) + "_TF"] *
                   el_1_IMFP[1][0] * el_1_sweep[1][i])

    el_2_factor = pd.DataFrame(data=np.zeros((len(area_2), 2)))
    for i in range(len(area_1)):
        el_2_factor.loc[i, 0] = "S" + str(i)
        el_2_factor.loc[i, 1] = (Inputs[str(el_chosen_2) + "_sigma"][0] * Inputs[str(el_chosen_2) + "_TF"] *
                   el_2_IMFP[1][0] * el_2_sweep[1][i])


    ratio_tot = [0]*len(area_2)
    ratio_perc = [0]*len(area_2)
    for i in range(len(area_1)):
        ratio_tot[i] = ((area_1[i] / el_1_factor.loc[i, 1]) / (area_2[i] / el_2_factor.loc[i, 1]))
        ratio_perc[i] = (area_1[i] / el_1_factor.loc[i, 1]) / ((area_1[i] / el_1_factor.loc[i, 1])
                                                               + (area_2[i] / el_2_factor.loc[i, 1]))

    return ratio_tot, ratio_perc, element_1, element_2


def el_gradient_ratio_calc_fkt(Inputs, df):
    """
    This function calculates the gradiental ratio between 2 chosen elements (with the changing IMFP´s for each ratio)
    You can choose an element from the list written in the ratio-calc.yaml file. then  it takes the needed parameters
    from it.
    If one has different sweeps for different measurement one can put it into a file and this will be called then.
    it then calc the ratio and percentage ratio of the chosen element.
    """
    el_list = Inputs["el_list"]
    element_1 = int(input("please enter the nr of the 1st element according to " + str(el_list) +
                          " in the type of [0,1,2...]"))
    element_2 = int(input("please enter the nr of the 2nd element according to " + str(el_list) +
                          " in the type of [0,1,2...]"))
    el_chosen_1 = el_list[element_1]
    el_chosen_2 = el_list[element_2]
    area_1 = df[el_list[element_1]][1]
    area_2 = df[el_list[element_2]][1]

    # check if there is a list of sweeps, if yes load it, if not create a df with the static sweep written into it
    el_1_sweep = if_sweep_list_fkt(Inputs, area_1, el_chosen_1)
    el_2_sweep = if_sweep_list_fkt(Inputs, area_2, el_chosen_2)
    el_1_IMFP = if_IMFP_list_fkt(Inputs, area_1, el_chosen_1, 0)
    el_2_IMFP = if_IMFP_list_fkt(Inputs, area_2, el_chosen_2, 0)

    el_1_factor = pd.DataFrame(data=np.zeros((len(area_1), 2)))
    for i in range(len(area_1)):
        el_1_factor.loc[i, 0] = "S" + str(i)
        el_1_factor.loc[i, 1] = (Inputs[str(el_chosen_1) + "_sigma"][0] * Inputs[str(el_chosen_1) + "_TF"] *
                   el_1_IMFP[1][0] * el_1_sweep[1][i])

    el_2_factor = pd.DataFrame(data=np.zeros((len(area_2), 2)))
    for i in range(len(area_1)):
        el_2_factor.loc[i, 0] = "S" + str(i)
        el_2_factor.loc[i, 1] = (Inputs[str(el_chosen_2) + "_sigma"][0] * Inputs[str(el_chosen_2) + "_TF"] *
                   el_2_IMFP[1][0] * el_2_sweep[1][i])

    ratio_tot = [0]*len(area_2)
    ratio_perc = [0]*len(area_2)
    for i in range(len(area_1)):
        ratio_tot[i] = ((area_1[i] / el_1_factor.loc[i, 1]) / (area_2[i] / el_2_factor.loc[i, 1]))
        ratio_perc[i] = (area_1[i] / el_1_factor.loc[i, 1]) / ((area_1[i] / el_1_factor.loc[i, 1])
                                                               + (area_2[i] / el_2_factor.loc[i, 1]))

    for n in range(5000):
        for i in range(len(area_1)):

            # calc of the correct IMFP vaule for each sectra_i
            ratio_lower_limit = 1000  # necessary since floats have to big errors when substracted
            while ratio_perc[i] * 1000 < ratio_lower_limit:
                ratio_lower_limit -= 25
            ratio_lower_limit = ratio_lower_limit / 1000

            for j in range(len(el_1_IMFP)):
                if el_1_IMFP[0][j] == ratio_lower_limit:
                    el_1_IMFP_j = el_1_IMFP[1][j]
                    el_2_IMFP_j = el_2_IMFP[1][j]


            # calc the new ratio with the new IMFP
            el_1_factor.loc[i, 1] = (Inputs[str(el_chosen_1) + "_sigma"][0] * Inputs[str(el_chosen_1) + "_TF"] *
                                         el_1_IMFP_j * el_1_sweep[1][i])
            el_2_factor.loc[i, 1] = (Inputs[str(el_chosen_2) + "_sigma"][0] * Inputs[str(el_chosen_2) + "_TF"] *
                                     el_2_IMFP_j * el_2_sweep[1][i])

            ratio_tot[i] = float(format(((area_1[i] / el_1_factor.loc[i, 1]) / (area_2[i] / el_2_factor.loc[i, 1]))
                                        , '.2f'))
            ratio_perc[i] = float(format(((area_1[i] / el_1_factor.loc[i, 1]) / ((area_1[i] / el_1_factor.loc[i, 1])
                                                                   + (area_2[i] / el_2_factor.loc[i, 1]))), '.2f'))

    return ratio_tot, ratio_perc, element_1, element_2, el_1_factor, el_2_factor


def el_gradient_error_calc_fkt(Inputs, df, el_1, el_2, ratio_perc,  el_1_factor, el_2_factor):
    """
    this function calculates the ratio between 2 chosen elements
    one can choose an element from the list written in the ratio-calc.yaml file. then  it takes the needed parameters
    from it.
    If one has different sweeps for different measurement one can put it into a file and this will be called then.
    it then calc the ratio and percentage ratio of the chosen element
    """
    el_list = Inputs["el_list"]
    el_chosen_1 = el_list[el_1]
    el_chosen_2 = el_list[el_2]
    area_1 = df[el_list[el_1]][1]
    area_2 = df[el_list[el_2]][1]

    # check if there is a list of sweeps, if yes load it, if not create a df with the static sweep written into it
    el_1_error = if_error_list_fkt(Inputs, area_1, el_chosen_1)
    el_2_error = if_error_list_fkt(Inputs, area_2, el_chosen_2)

    df_ratio_error_pos = {}
    df_ratio_error_neg = {}

    ratio_error_pos_diff = {}
    ratio_error_neg_diff = {}
    for i in range(len(area_1)):
        error_factor_min = 1.2 * 1.1 * 1.05
        error_factor_max = 0.8 * 0.9 * 0.95

        df_ratio_error_pos[i] = float(
            format((area_1[i] * el_1_factor * (1 - el_1_error[i] / error_factor_min)) / (
                    (area_1[i] * el_1_factor * (1 - el_1_error[i] / error_factor_min)) +
                    (area_2[i] * el_2_factor * (1 + el_2_error[i] / error_factor_max))), '.2f'))

        df_ratio_error_neg[i] = float(
            format((area_1[i] * el_1_factor * (1 + el_1_error[i] / error_factor_max)) / (
                    (area_1[i] * el_1_factor * (1 + el_1_error[i] / error_factor_max)) +
                    (area_2[i] * el_2_factor * (1 - el_2_error[i] / error_factor_min))), '.2f'))

        ratio_error_pos_diff[i] = (ratio_perc[i] * 1000 - df_ratio_error_pos[i] * 1000) / 1000
        ratio_error_neg_diff[i] = (ratio_perc[i] * 1000 - df_ratio_error_neg[i] * 1000) / 1000

    return ratio_error_pos_diff, ratio_error_neg_diff

"""------------all fkt´s for Ratio_calc_ana - center part ---------------------"""


def center_shift_fkt_choice():
    """
    fkt to chose which center calculation should be done:
    - the shift of an oxid state compared to 'itself'(0) along the sample
    - the shift 'between'(1) different oxid states (1st main peak used)
    """
    shift_choice_bool = False
    while not shift_choice_bool:
        shift_choice = input(
            "Please choose if you want to calc: \n"
            "- the shift of an oxid state compared to 'itself'(0) along the sample ,\n"
            "- the shift 'between'(1) different oxid states (1st main peak used) \n "
            "please enter either the words or number\n")
        if (shift_choice.lower() == "itself") or shift_choice == "0":
            ratio_choice = 0
            return ratio_choice
        elif (shift_choice.lower() == "between") or shift_choice == "1":
            ratio_choice = 1
            return ratio_choice
        else:
            shift_choice_bool = False


def center_shift_self_fkt(Inputs, df):
    """
    fkt to calc the shift of all samples of a chosen oxid state compared to the first
    """
    el_list = Inputs["el_list"]
    el_to_calc = int(input("please enter the nr of the el according to " + str(el_list) + " in the type of [0,1,2...]"))
    el_chosen = el_list[el_to_calc]
    oxid = int(input("Please enter the oxid state you want to calc according to " + str(Inputs[el_chosen+"_label_list"])
                     + "\n in the type of [0,1,2...]"))

    center = df[el_chosen][oxid + 1]  # the +1 is necessary, since the 0th column is S00 etc
    center_shift = center.copy()

    center_shift = center_shift - center[0]
    return center_shift, el_to_calc, oxid


def center_shift_bewteen_fkt(Inputs, df):
    """
    fkt to calc the shift between 2 chosen oxid states of the same sample (for all samples)
    """
    el_list = Inputs["el_list"]
    el_to_calc = int(input("please enter the nr of the el according to " + str(el_list) + " in the type of [0,1,2...]"))
    el_chosen = el_list[el_to_calc]
    print("Please enter the oxid states you want to calc according to " + str(Inputs[el_chosen+"_label_list"]) + "\n in"
          " the type of [0,1,2...].\n")
    oxid_1 = int(input("please enter the 1st oxid state you want to calc"))
    oxid_2 = int(input("please enter the 2nd oxid state you want to calc"))

    center_1 = center = df[el_chosen][oxid_1 + 1]
    center_2 = center = df[el_chosen][oxid_2 + 1]

    center_diff = center_1 - center_2
    return center_diff, el_to_calc, oxid_1, oxid_2

