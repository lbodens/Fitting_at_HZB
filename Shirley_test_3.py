from __future__ import division

import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import sys
from lmfit.models import GaussianModel, VoigtModel, LinearModel, LorentzianModel
import lmfit
import matplotlib as mpl
import yaml, json, lmfit

namespace = sys._getframe(0).f_globals
plt.style.use('seaborn-ticks')
mpl.rcParams.update({'font.size': 16})

def BE_or_KE_fkt(choice_input):                     # fkt to see if its in BE or KE and to get the necessary values (exertation energy)
    if choice_input == "KE":
        exertation_energy = float(input("please enter the exertation energy (in eV). like 1486.7\n"))
        BE_or_KE = "KE"
        return BE_or_KE, exertation_energy
    if choice_input == "BE":
        exertation_energy = 0
        BE_or_KE = "BE"
        return BE_or_KE, exertation_energy
    else:
        print("\nError, please type in 'BE' or 'KE'\n")
        BE_or_KE = False
        exertation_energy = 0
        return BE_or_KE, exertation_energy

def param_updater(param_file_type):
    if param_file_type == "yaml":
        param_file_type = yaml
        param_file_type_str = "yaml"
    if param_file_type == "json":
        param_file_type = json
        param_file_type_str = "json"
    params = param_file_type.load(open('test_param.' +param_file_type_str), Loader=param_file_type.FullLoader)
    pars = lmfit.Parameters()
    for name, rest in params.items():
        pars.add(lmfit.Parameter(name=name, **rest))
    return pars

def choose_spectra_to_plot():
    spectra_to_plot = int(input("please enter the spectra which you want to be shown\n"))
    return spectra_to_plot

def check_if_peak_inport_is_good():
    check_shown_peak_input = input("Are these init parameters good enough? please enter 'yes'/'y' or 'no'/'n':\n")
    if check_shown_peak_input == "yes" or check_shown_peak_input == "y":
        check_shown_peak_input = True
        return check_shown_peak_input
    else:
        check_shown_peak_input = False
        return check_shown_peak_input


def plotting(x, spectra_to_plot,number_of_peaks):
    pars = param_updater(param_file_type)
    mod, p4fit = shirley_param_calc(pars)
    init = mod.eval(x=x, params=p4fit)
    fig, axes = plt.subplots()
    x = dat["E"].to_numpy()
    yraw = dat["Spectra"].to_numpy()
    axes.plot(x, yraw, 'b')
    axes.plot(x, init, 'k--', label='initial fit')
    plt.xlim([min(x) + (int(spectra_to_plot) - 1) * 10000, max(x) + (int(spectra_to_plot) - 1) * 10000])
#    comps = mod.eval_components(x=x)
#    for i in range(int(number_of_peaks)):
#        #axes.plot(x, comps['lin_'], 'k-', label='const component')
#        axes.plot(x, comps['p%s_%s_'%(spectra_to_plot-1,number_of_peaks-1)], 'g--', label='voigt component %s'%i)
#        axes.legend(loc='best')
    plt.show()


def plot_checking():
    spectra_to_plot_bool = False
    are_pre_params_good_bool = False
    spectra_to_plot = choose_spectra_to_plot()
    while spectra_to_plot_bool == False and are_pre_params_good_bool == False:
        while are_pre_params_good_bool == False:
            plotting(x, spectra_to_plot, number_of_peaks)
            are_pre_params_good_bool = check_if_peak_inport_is_good()
            if are_pre_params_good_bool == True:
                plt.close()
                continue
            if are_pre_params_good_bool == False:
                plt.close()
                print("Please change the paramter to the desired one\n")
                continue
        while spectra_to_plot_bool == False:
            other_spectra_check = input("do you want to check other spectra as well?\n")
            if other_spectra_check == "yes" or other_spectra_check == "y":
                spectra_to_plot = choose_spectra_to_plot()
                spectra_to_plot_bool = False
                are_pre_params_good_bool = False
                break
            if other_spectra_check == "no" or other_spectra_check == "n":
                spectra_to_plot_bool = True
                continue

def shirley_bg(x, low=0., high=.1):
    return low, high


def create_bg(left, right):
    low, high = right
    cumsum = np.cumsum(left)
    return left + low + (high - low) * (cumsum / cumsum[-1])


def build_curve_from_peaks(n_peaks=1):
    if peak_type == "Voigt":
        peak_func = lmfit.models.VoigtModel
    if peak_type == "Gauss":
        peak_func = lmfit.models.GaussiantModel
    if peak_type == "Lorentz":
        peak_func = lmfit.models.LorentzianModel
    #if peak_type == ???:
    #    peak_func = lmfit.models.???Model
    model = None
    for i in range(number_of_spectra):
        for idx in range(n_peaks):
            prefix = f'p{i}_{idx}_'
            peak = peak_func(prefix=prefix)
            bg = lmfit.Model(shirley_bg, prefix=prefix)
            comp = lmfit.CompositeModel(peak, bg, create_bg)
            print(idx)
            if model:
                model += comp
            else:
                model = comp

        return model

def shirley_param_calc(pars):

    deltas = (yraw[len(yraw) - 1] - yraw[0])
    for i in range(number_of_spectra):
        p4fit[f'p{i}_0_low'].set(value=yraw[0])
        for idx in range(number_of_peaks):
            p4fit[f'p{i}_{idx}_center'].set(value=pars[f'p{i}_{idx}_center'].value)
            p4fit[f'p{i}_{idx}_amplitude'].set(value=pars[f'p{i}_{idx}_amplitude'].value)
            p4fit[f'p{i}_{idx}_sigma'].set(value=pars[f'p{i}_{idx}_sigma'].value)
            p4fit[f'p{i}_{idx}_gamma'].set(value=pars[f'p{i}_{idx}_gamma'].value)

            p4fit.add(f'p{i}_{idx}_delta', value=deltas / 9, min=0)
            if idx > 0:
                p4fit[f'p{i}_{idx}_low'].set(value=0, vary=False)
            p4fit[f'p{i}_{idx}_high'].set(expr=f'p{i}_{idx}_low+p{i}_{idx}_delta')
            print(p4fit[f'p{i}_{idx}_high'])
    return mod, p4fit



skip_rows=1

dat = np.loadtxt("Ni2p_ref_sat_sub.dat", skiprows=1)
x = dat[:, 0][::-1]
#yraw = dat[:, 2][::-1]

dat_input = np.loadtxt("Ni2p_ref_sat_sub.dat", skiprows=skip_rows)
dat=pd.DataFrame(columns=["E", "Spectra"])


dat["E"] = dat_input[:, 0]
dat["Spectra"] = dat_input[:, 2]

plt.plot(dat["E"], dat["Spectra"], label='data')
if dat["E"][0] > dat["E"][len(dat) - 1]:
    dat = dat[::-1]
#    print("The input data was in decreasing energy. It was swapped for further process")
xraw = dat["E"]
yraw = dat["Spectra"]



number_of_spectra = 1
number_of_peaks = 9
peak_type = "Voigt"
attribute_nr = 6            #number of parameters in the para file for the voigt



"""------------------fkt to show spectra with init peaks------------------------------------------"""


param_file_type = input("please enter if you are using 'yaml' or 'json'")
pars= param_updater(param_file_type)

mod = build_curve_from_peaks(number_of_peaks)
p4fit = mod.make_params()

mod, p4fit=shirley_param_calc(pars)


plot_checking()



fit_res = mod.fit(yraw, x=x, params=p4fit, max_nfev=1000)
plt.plot(x, yraw, '.', label='data')
plt.plot(x, fit_res.best_fit, '--', label='fit')
plt.plot(x, mod.eval(x=x, params=p4fit), label='start values')
plt.legend(loc='best')
plt.show()

print(fit_res)