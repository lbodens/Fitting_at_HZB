########################################################################################################################
#                                                                                                                      #
#                   Taking the prevoiulsy set parameters from the YAML/JSOn files and update                           #
#                   the parameters, which are created before                                                           #
#                                                                                                                      #
########################################################################################################################



import yaml, json, lmfit
import lmfit.models



def param_updater(param_file_type,param_file_name):
    if param_file_type == "yaml":
        param_file_type = yaml
        param_file_type_str = "yaml"
    if param_file_type == "json":
        param_file_type = json
        param_file_type_str = "json"
    params = param_file_type.load(open(str(param_file_name) + '.' + param_file_type_str), Loader=param_file_type.FullLoader)
    pars = lmfit.Parameters()
    for name, rest in params.items():
        pars.add(lmfit.Parameter(name=name, **rest))
    return pars


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
            print(pars[f'p{i}_{idx}_high'])
    return pars

def param_per_peak_sorting_fkt(p4fit,  number_of_spectra, number_of_peaks):
    p4fit_di={}
    for idx in range(int(number_of_peaks)):
        for i in range(int(number_of_spectra)):
            p4fit_di[f"p{i}_{idx}"] = {}
    for idx in range(int(number_of_peaks)):
        for i in range(int(number_of_spectra)):
            for name in p4fit:
                if f'p{i}_{idx}_' in name:
                    p4fit_di[f'p{i}_{idx}'][f"{name}"]= p4fit[name]
    return p4fit_di

def param_per_spectra_sorting_fkt(p4fit,  number_of_spectra, number_of_peaks):
    p4fit_di={}
    for i in range(int(number_of_spectra)):
        p4fit_di[f"spectra_{i}"] = {}
    for idx in range(int(number_of_peaks)):
        for i in range(int(number_of_spectra)):
            for name in p4fit:
                if f'p{i}_{idx}_' in name:
                    p4fit_di[f'spectra_{i}'][f"{name}"]= p4fit[name]
    return p4fit_di




def param_updater_main_fkt(d,param_file_type, param_file_name, number_of_spectra, number_of_peaks):
    pars = param_updater(param_file_type, param_file_name)

    pars_new = pars.copy()
    p4fit = shirley_param_calc(pars_new, d, number_of_spectra, number_of_peaks)
    p4fit_s_d = param_per_spectra_sorting_fkt(p4fit,  number_of_spectra, number_of_peaks)
    p4fit_p_d = param_per_peak_sorting_fkt(p4fit,  number_of_spectra, number_of_peaks)

    return p4fit, p4fit_s_d, p4fit_p_d