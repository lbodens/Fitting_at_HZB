########################################################################################################################
#                                                                                                                      #
#               in this file The actual fit happends                                              #
#               For this the peak parameter are sorted, and the Models are evaluated                                   #
#               (with and w/o the shirley, which then gets subtracted to get the single shirley as well                #
#               Also can one choose if he wants to see multiple spectra at the same time (and how many)                #
#                                                                                                                      #
########################################################################################################################



import numpy as np
from lmfit import minimize, Parameters, report_fit
from plots_scripts.Param_updater import param_per_peak_sorting_fkt, param_per_spectra_sorting_fkt



def y_for_fit(d, number_of_spectra, number_of_peaks):
    y_d = np.array([[0.0] * len(d[f'dat_0']["Spectra"])] * (int(number_of_spectra)))
    resid = np.array([[0.0] * len(d[f'dat_0']["Spectra"])] * (int(number_of_spectra)))
    for i in range(int(number_of_spectra)):
        for j in range(len(d["dat_0"]["E"])):
            dat_holder = d[f'dat_{i}']
            y_d[i][j] = dat_holder["Spectra"][j]
    return y_d, resid


def model_eval_fit_fkt(params, mod_d, x, number_of_spectra, number_of_peaks):
    result = np.array( [[0.0] * len(x)] * (int(number_of_spectra)))

    for idx in range(int(number_of_peaks)):
        for i in range(int(number_of_spectra)):
            loop = str(i) + '_' + str(idx)
            result[i] = result[i] + mod_d['mod'+loop].eval(x=np.array(x), params=params['p'+loop])
    return result

def model_eval_fitted_fkt(params, mod_d,  x, number_of_spectra, number_of_peaks):
    result=np.array([[0.0] * len(x)] * (int(number_of_spectra)))

    for idx in range(int(number_of_peaks)):
        for i in range(int(number_of_spectra)):
            result[i] = result[i] + mod_d[f'mod{i}_{idx}'].eval(x=np.array(x), params=params[f'spectra_{i}'])
    
    return result

def fitting_over_all_spectra(p4fit, x, mod_d, y_d, resid, number_of_spectra, number_of_peaks):
#    start_time = time.time()                                       # <-- if you want to log something entcoment herem
    p4fit_d = param_per_peak_sorting_fkt(p4fit)
    model_eval= model_eval_fit_fkt(p4fit_d, mod_d, x, number_of_spectra, number_of_peaks)
    for i in range(int(number_of_spectra)):
        resid[i, :] = y_d[i,:] - model_eval[i,:]
    resid_sum = sum(resid.flatten())
#    logging.info("fitting_time: --- %s seconds ---" % (time.time() - start_time))
#    logging.info("fitting {}".format(resid_sum))
    return resid.flatten()





def fitting_function_main_fkt(d, p4fit, x, mod_d, number_of_spectra, number_of_peaks, nfev):
    print("starting fitting")
    y_d, resid = y_for_fit(d, number_of_spectra, number_of_peaks)
    out = minimize(fitting_over_all_spectra, p4fit, args=(x, mod_d,y_d, resid, number_of_spectra, number_of_peaks), max_nfev=nfev)
    print("end fitting")
    out_params = param_per_spectra_sorting_fkt(out.params, number_of_spectra, number_of_peaks)
    #report_fit(out.params)

    return out, out_params, y_d
