########################################################################################################################
#                                                                                                                      #
#                   Taking the previous set parameters from the YAML/JSOn files and update                           #
#                   the parameters, which are created before                                                           #
#                                                                                                                      #
########################################################################################################################

import yaml, json, lmfit
import lmfit.models
import re


def param_updater(param_file_type, param_file_name):
    if param_file_type == "yaml":
        param_file_type = yaml
        param_file_type_str = "yaml"
    if param_file_type == "json":
        param_file_type = json
        param_file_type_str = "json"
    params = param_file_type.load(open(param_file_name + '.' + param_file_type_str), Loader=param_file_type.FullLoader)
    pars = lmfit.Parameters()
    for name, rest in params.items():
        pars.add(lmfit.Parameter(name=name, **rest))
    return pars, param_file_type, param_file_type_str


def shirley_param_calc(pars, d, number_of_spectra, number_of_peaks):
    for i in range(int(number_of_spectra)):
        yraw = d[f'dat_{i}']["Spectra"]
        deltas = (yraw[len(yraw) - 1] - yraw[0])
        pars.add(f'p{i}_0_low', value=yraw[0])
        for idx in range(int(number_of_peaks)):

            pars.add(f'p{i}_{idx}_delta', value=deltas / int(number_of_peaks), min=0)
            if idx > 0:
                pars.add(f'p{i}_{idx}_low', value=0, vary=False)
            pars.add(f'p{i}_{idx}_high', expr=f'p{i}_{idx}_low+p{i}_{idx}_delta')
#            print(pars[f'p{i}_{idx}_high'])
    return pars


def param_per_peak_sorting_fkt(pars):
    result = {}
    p = re.compile('p[0-9]+_[0-9]+')

    for name in pars:
        prefix = p.search(name).group(0)
        if result.get(prefix) is None:
            result[prefix] = {}
        result[prefix][name] = pars[name]

    return result


def param_per_spectra_sorting_fkt(pars):
    result = {}
    p = re.compile('^p[0-9]+')

    for name in pars:
        prefix = p.search(name)
        prefix = 'spectra_' + prefix.group(0)[1:]
        if result.get(prefix) is None:
            result[prefix] = {}
        result[prefix][name] = pars[name]

    return result


def param_updater_main_fkt(d, param_file_type, param_file_name, number_of_spectra, number_of_peaks):
    pars, param_file_type, param_file_type_str = param_updater(param_file_type, param_file_name)

    pars_new = pars.copy()
    p4fit = shirley_param_calc(pars_new, d, number_of_spectra, number_of_peaks)
    p4fit_s_d = param_per_spectra_sorting_fkt(p4fit)
    p4fit_p_d = param_per_peak_sorting_fkt(p4fit)
    return p4fit, p4fit_s_d, p4fit_p_d, param_file_type, param_file_type_str
