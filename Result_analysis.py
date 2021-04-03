######################################
#
#
#
#
#
#
#
#
#
#

"""
1st load result.txt

2nd sort the entries into center, area etc

3rd putt all into df´s

4th: work with them
    - area: first 9 and 2nd 9 together, diff
    - center: shift if 1st peak for all

"""

import yaml, json




def result_param_reader(param_file_type,param_file_name):
    if param_file_type == "yaml":
        param_file_type = yaml
        param_file_type_str = "yaml"
    if param_file_type == "json":
        param_file_type = json
        param_file_type_str = "json"
    params = param_file_type.load(open(str(param_file_name) + '.' + param_file_type_str), Loader=param_file_type.FullLoader)
    return params


def param_area_sorting_fkt(pars, number_of_spectra, number_of_peaks, number_of_digits):
    pars_area_di = {}
    for i in range(int(number_of_spectra)):
        pars_area_di[f"spectra_{i}"] = {}
    for idx in range(int(number_of_peaks)):
        for i in range(int(number_of_spectra)):
            for name in pars:
                if f'p{i}_{idx}_amplitude' in name:
                    pars_value = ""
                    for k in range(int(number_of_digits)):
                        pars_value = pars_value + pars[f"p{i}_{idx}_amplitude"][k]
                    pars_value = float(pars_value)
                    pars_area_di[f'spectra_{i}'][f"{name}"] = pars_value
    return pars_area_di


def param_center_sorting_fkt(pars, number_of_spectra, number_of_peaks, number_of_digits):
    pars_center_di = {}
    for i in range(int(number_of_spectra)):
        pars_center_di[f"spectra_{i}"] = {}
    for idx in range(int(number_of_peaks)):
        for i in range(int(number_of_spectra)):
            for name in pars:
                if f'p{i}_{idx}_center' in name:
                    pars_value = ""
                    for k in range(int(number_of_digits)):
                        pars_value = pars_value + pars[f"p{i}_{idx}_center"][k]
                    pars_value = float(pars_value)
                    pars_center_di[f'spectra_{i}'][f"{name}"] = pars_value
    return pars_center_di


def two_oxid_state_area_calc(pars_df, number_of_peaks_1st_state, number_of_spectra, number_of_peaks):
    area = {}
    area[0] = 0
    area[1] = 0
    nr_of_1st_state = int(number_of_peaks_1st_state)
    df = {}
    for i in range(int(number_of_spectra)):
        df[f"spectra_{i}"] = {}

    for i in range(int(number_of_spectra)):
        for j in range(int(nr_of_1st_state)):
            for name in pars_df[f"spectra_{i}"]:
                if f'p{i}_{j}' in name:
                    area[0] = area[0] + pars_df[f"spectra_{i}"][name]

        for k in range(int(nr_of_1st_state), int(number_of_peaks)):
            for name in pars_df[f"spectra_{i}"]:
                if f'p{i}_{k}' in name:
                    area[1] = area[1] + pars_df[f"spectra_{i}"][name]

        for o in range(2):  # here the nr of oxid states can be included/increases, if necessary
            df[f"spectra_{i}"][f"oxid_state_{o + 1}"] = area[o]

    return df


def center_shift_calc_fkt(pars_df, number_of_oxid_states, number_of_peaks_1st_state, number_of_spectra,
                          number_of_peaks):
    center_df = {}
    for i in range(int(number_of_spectra)):
        center_df[f"spectra_{i}"] = {}
    nr_of_1st_state = int(number_of_peaks_1st_state)

    for i in range(int(number_of_spectra)):
        for j in range(int(nr_of_1st_state)):
            for name in pars_df[f"spectra_{i}"]:
                if f'p{i}_{j}' in name:
                    "stuff"

    return


def result_ana_main_fkt(in1, in2, in3, in4, in5):
    param_file_type = in1  # input("please enter if you are using 'yaml' or 'json':\n")
    param_file_name = in2  # input("please enter the name of the result file (with path, e.g.: 'results/results_file'):\n")
    res_pars = result_param_reader(param_file_type, param_file_name)
    # print(res_pars)

    number_of_spectra = in3  # input("please enter the number of spectra used:\n")
    number_of_peaks = in4  # input("please enter the number of peaks used:\n")
    number_of_digits = in5  # input("please enter the number of digits of the values:\n")
    pars_area = param_area_sorting_fkt(res_pars, number_of_spectra, number_of_peaks, number_of_digits)
    pars_center = param_center_sorting_fkt(res_pars, number_of_spectra, number_of_peaks, number_of_digits)
    print("sucess")
    return res_pars, pars_area, pars_center
