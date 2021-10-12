import yaml, json


def result_param_reader(param_file_type, param_file_name):
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

    df_a_0, df_a_1 = oxid_state_area_sort_fkt(pars_area, Inputs, element_number)
    df_c = oxid_state_center_sort_fkt(pars_center, Inputs, element_number)

    return pars_cl, df_a_0, df_a_1, df_c


"""------------area calcs---------------------"""


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

    area = {}
    # creation of df for the oxid sates o_x within the core level _y [0: main peak e.g (2p3/2), 1: 2nd peak e.g. 2p1/2)]
    df_o_0_0 = {}
    df_o_1_0 = {}
    df_o_2_0 = {}
    df_o_tot_0 = {}
    df_o_0_1 = {}
    df_o_1_1 = {}
    df_o_2_1 = {}
    df_o_tot_1 = {}

    for i in range(int(number_of_spectra)):
        spectra_i = "spectra_" + str(i)

        # setting the area to 0 at the beginning for each spectra
        for o in range(6):  # IF you are changing the number of oxid states to greater than 2x3, then update here as well!
            area[o] = 0

        for name in pars_df[spectra_i]:
            for idx in range(number_of_peaks):
                if f'p{i}_{idx}' in name:
                    area[oxid_core_lvl_list[idx]] = area[oxid_core_lvl_list[idx]] + pars_df[spectra_i][name]

        df_o_0_0[spectra_i] = area[0]
        df_o_1_0[spectra_i] = area[1]
        df_o_2_0[spectra_i] = area[2]
        df_o_tot_0[spectra_i] = area[0] + area[1] + area[2]

        df_o_0_1[spectra_i] = area[3]
        df_o_1_1[spectra_i] = area[4]
        df_o_2_1[spectra_i] = area[5]
        df_o_tot_1[spectra_i] = area[3] + area[4] + area[5]

    df_container_0 = df_o_tot_0, df_o_0_0, df_o_1_0, df_o_2_0
    df_container_1 = df_o_tot_1, df_o_0_1, df_o_1_1, df_o_2_1

    return df_container_0, df_container_1


def area_ratio_calc_fkt(df_1, df_2, Inputs, nr_of_diff_elements):
    """
    This function calcs the ratios of different df´s ´. It also uses the preset values of corss section, IMFP, and the transmissionfkt.
    If the same elements are used (nr_of_diff_elements =[1,2]), only one iteration is done. (since the IMFP does not change since its all the same elements)
    But if different elements are used (nr_of_diff_elements = 3) a small iteration overits self runs. first one pre calculatuion is done with some basic IMFP´s.
    the previous calculated ratio is taken, compared to the ones for IMFP values (el{x}_IMFP_{ratio_in_%}) and then updated. this is done ~5000 times,
    to make sure, that there is no big change anymore.
    """
    number_of_spectra = Inputs["number_of_spectra"]

    if nr_of_diff_elements < 3:
        el1_sigma = Inputs["el{}_sigma".format(nr_of_diff_elements)]
        el1_trans_fkt = Inputs["el{}_trans_fkt".format(nr_of_diff_elements)]
        el1_IMFP = Inputs["el{}_IMFP".format(nr_of_diff_elements)]
        el1_factor = el1_sigma * el1_trans_fkt * el1_IMFP

        el2_sigma = Inputs["el{}_sigma".format(nr_of_diff_elements)]
        el2_trans_fkt = Inputs["el{}_trans_fkt".format(nr_of_diff_elements)]
        el2_IMFP = Inputs["el{}_IMFP".format(nr_of_diff_elements)]
        el2_factor = el2_sigma * el2_trans_fkt * el2_IMFP

    if nr_of_diff_elements == 3:
        el1_sigma = Inputs["el1_sigma"]
        el1_trans_fkt = Inputs["el1_trans_fkt"]
        el1_IMFP = Inputs["el1_IMFP"]
        el1_factor = el1_sigma * el1_trans_fkt * el1_IMFP

        el2_sigma = Inputs["el2_sigma"]
        el2_trans_fkt = Inputs["el2_trans_fkt"]
        el2_IMFP = Inputs["el2_IMFP"]
        el2_factor = el2_sigma * el2_trans_fkt * el2_IMFP

    df_ratio_abs = {}
    df_ratio_perc = {}

    for i in range(int(number_of_spectra)):
        spectra_i = "spectra_" + str(i)
        df_ratio_perc[spectra_i] = float(format((df_1[spectra_i] * el1_factor) / (
                    df_1[spectra_i] * el1_factor + df_2[spectra_i] * el2_factor), '.2f'))
        df_ratio_abs[spectra_i] = float(format((df_1[spectra_i] * el1_factor) / (df_2[spectra_i] * el2_factor), '.2f'))

    if nr_of_diff_elements == 3 and Inputs["matrix_bool"] == True:
        print("yasy")
        for n in range(5000):
            for i in range(int(number_of_spectra)):
                spectra_i = "spectra_" + str(i)

                ratio_lower_limit = 1000  # necessary since floats have to big errors when substracted
                while df_ratio_perc[spectra_i] * 1000 < ratio_lower_limit:
                    ratio_lower_limit -= 25
                ratio_lower_limit = ratio_lower_limit / 1000

                el1_IMFP = Inputs["el1_IMFP_{}".format(ratio_lower_limit)]
                el1_factor = el1_sigma * el1_trans_fkt * el1_IMFP
                el2_IMFP = Inputs["el2_IMFP_{}".format(ratio_lower_limit)]
                el2_factor = el2_sigma * el2_trans_fkt * el2_IMFP

                df_ratio_perc[spectra_i] = float(format((df_1[spectra_i] * el1_factor) / (
                            df_1[spectra_i] * el1_factor + df_2[spectra_i] * el2_factor), '.2f'))
                df_ratio_abs[spectra_i] = float(format((df_1[spectra_i] * el1_factor) / (df_2[spectra_i] * el2_factor), '.2f'))
    return df_ratio_perc, df_ratio_abs


def error_calc(df_1, df_2, df_ratio_perc, Inputs):
    """
    If you have an error estimation of your fit: then include this part here..
    if not, then not.. also export it by hand.. at the moment. so thats it not mandatory
    -----------------------------------------------------------------------
    """
    number_of_spectra = Inputs["number_of_spectra"]

    if Inputs["error_estimation"] == True:
        df_ratio_error_pos = {}
        df_ratio_error_neg = {}
        df_error_el1 = {}
        df_error_el2 = {}
        df_ratio_error_pos_diff = {}
        df_ratio_error_neg_diff = {}

        for i in range(int(number_of_spectra)):
            spectra_i = "spectra_" + str(i)

            df_error_el1[spectra_i] = Inputs["error_el1"][i]
            df_error_el2[spectra_i] = Inputs["error_el2"][i]
            error_factor_min = 1.2 * 1.1 * 1.05
            error_factor_max = 0.8 * 0.9 * 0.95

            df_ratio_error_pos[spectra_i] = float(
                format((df_1[spectra_i] * el1_factor * (1 - df_error_el1[spectra_i] / error_factor_min)) / (
                        (df_1[spectra_i] * el1_factor * (1 - df_error_el1[spectra_i] / error_factor_min)) +
                        (df_2[spectra_i] * el2_factor * (1 + df_error_el2[spectra_i] / error_factor_max))), '.2f'))

            df_ratio_error_neg[spectra_i] = float(
                format((df_1[spectra_i] * el1_factor * (1 + df_error_el1[spectra_i] / error_factor_max)) / (
                        (df_1[spectra_i] * el1_factor * (1 + df_error_el1[spectra_i] / error_factor_max)) +
                        (df_2[spectra_i] * el2_factor * (1 - df_error_el2[spectra_i] / error_factor_min))), '.2f'))

            df_ratio_error_pos_diff[spectra_i] = (df_ratio_perc[spectra_i] * 1000 - df_ratio_error_pos[
                spectra_i] * 1000) / 1000
            df_ratio_error_neg_diff[spectra_i] = (df_ratio_perc[spectra_i] * 1000 - df_ratio_error_neg[
                spectra_i] * 1000) / 1000


def area_calculations_fkt(df_1_a_sum, df_2_a_sum, Inputs):
    """
    This function calls the functions to do all the necessary/possible ratio calculations

    end result:
        df_1: the ratios / percentage of oxid state from the 1st to 2nd oxid state of the 1st element
        df_2: the ratios / percentage of oxid state from the 1st to 2nd oxid state of the 2nd element
        df_tot: the ratios / percentage of elements from the 1st to 2nd element
    """

    df_1_a_tot, df_1_a_1, df_1_a_2, df_1_a_3 = df_1_a_sum
    df_2_a_tot, df_2_a_1, df_2_a_2, df_2_a_3 = df_2_a_sum

    df_ratio_perc_1, df_ratio_abs_1 = area_ratio_calc_fkt(df_1_a_1, df_1_a_2, Inputs, 1)
    df_ratio_perc_2, df_ratio_abs_2 = area_ratio_calc_fkt(df_2_a_1, df_2_a_2, Inputs, 2)
    df_ratio_perc_tot, df_ratio_abs_tot = area_ratio_calc_fkt(df_1_a_tot, df_2_a_tot, Inputs, 3)

    df_1 = df_ratio_perc_1, df_ratio_abs_1
    df_2 = df_ratio_perc_2, df_ratio_abs_2
    df_tot = df_ratio_perc_tot, df_ratio_abs_tot
    return df_1, df_2, df_tot


"""-------------- center cals --------------------"""


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
    This function adds all the peaks corresponding to an oxidation state per spectra into a df each (and the sum of all)
    Also if your input oxid states > total peaks (for what ever reason), it´s send out an error
    """
    number_of_spectra = Inputs["number_of_spectra"]

    range_of_1st_state = 0 #Inputs["el{}_number_per_oxid_state_0".format(element_number)]
    range_of_2nd_state = range_of_1st_state + Inputs["el{}_number_per_oxid_state_0".format(element_number)]
    range_of_3rd_state = range_of_2nd_state + Inputs["el{}_number_per_oxid_state_1".format(element_number)]

    df_o_1 = {}
    df_o_2 = {}
    df_o_3 = {}

    for i in range(int(number_of_spectra)):
        spectra_i = "spectra_" + str(i)
        df_o_1[spectra_i] = 0
        df_o_2[spectra_i] = 0
        df_o_3[spectra_i] = 0

        for name in pars_df[spectra_i]:
            if f'p{i}_{range_of_1st_state}' in name:
                df_o_1[spectra_i] = pars_df[spectra_i][name]

            if f'p{i}_{range_of_2nd_state}' in name:
                df_o_2[spectra_i] = pars_df[spectra_i][name]

            if f'p{i}_{range_of_3rd_state}' in name:
                df_o_3[spectra_i] = pars_df[spectra_i][name]
    df_o_tot = df_o_1.copy()

    df_container = df_o_tot, df_o_1, df_o_2, df_o_3
    return df_container


def center_shift_between_2_df_calc_fkt(df_1, df_2, number_of_spectra):
    """
    This function cals the energy shift of an oxidstate towards the other df
    """
    df = {}
    for i in range(int(number_of_spectra)):
        spectra_i = "spectra_"+str(i)
        df[spectra_i] = df_2[spectra_i] - df_1[spectra_i]
    return df


def center_shift_intern_df_calc_fkt(df_1, number_of_spectra):
    """
    This function cals the energy shift of an oxidstate towards the first spectras oxid state the other df
    """
    df = {}
    for i in range(int(number_of_spectra)):
        spectra_i = "spectra_"+str(i)
        df[spectra_i] = df_1[spectra_i] - df_1["spectra_0"]
    return df


def center_calculations_fkt(df_1_c_sum, df_2_c_sum, Inputs):
    """
    This function calls the functions to do all the necessary/possible calculations.
    end result:
        df_center_shift_bw_oxid: the energy diff between both 1st main peaks of the oxid states
        df_center_shift_el1: the shift of all peaks within the first oxid state in dependence of the 1st peaks position of the 1st element
        df_center_shift_el2: the shift of all peaks within the first oxid state in dependence of the 1st peaks position of the 2nd element
    """
    number_of_spectra = Inputs["number_of_spectra"]
    df_1_c_tot, df_1_c_1, df_1_c_2, df_1_c_3 = df_1_c_sum
    df_2_c_tot, df_2_c_1, df_2_c_2, df_2_c_3 = df_2_c_sum

    df_center_shift_bw_oxid = center_shift_between_2_df_calc_fkt(df_1_c_1, df_1_c_2, number_of_spectra)
    df_center_shift_el1 = center_shift_intern_df_calc_fkt(df_1_c_tot, number_of_spectra)
    df_center_shift_el2 = center_shift_intern_df_calc_fkt(df_2_c_tot, number_of_spectra)

    return df_center_shift_bw_oxid, df_center_shift_el1, df_center_shift_el2
