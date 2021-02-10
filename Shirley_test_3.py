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

"""
def I_high_low_init_calc_fkt():
    I_low = [0] * number_of_spectra * number_of_peaks
    I_high = [0] * number_of_spectra * number_of_peaks
    I_low[0] = ymin
    I_high[0] = (ymax - ymin) / int(number_of_peaks) + I_low[0]
    for i in range(1, int(number_of_peaks * number_of_spectra)):
        I_low[i] = I_high[i - 1]
        I_high[i] = (ymax - ymin) / int(number_of_peaks) + I_low[i]
    return I_low, I_high
"""#---------------creating the wanted nr and type of peaks----------------------
"""
def peak_creation(pars, mod):
    Model = []
    for j in range(int(number_of_spectra)):
        for i in range(int(number_of_peaks)):
            if peak_type == "Voigt" or peak_type == "voigt":
                Model.append(VoigtModel(prefix='v' + str(j) + '_' + str(i) + '_'))
                pars.update(Model[i + int(number_of_peaks) * j].make_params())
                pars['v' + str(j) + '_' + str(i) + '_amplitude'].set(min=0)
                mod = mod + Model[i + int(number_of_peaks) * j]
            if peak_type == "Gauss":
                Model.append(GaussianModel(prefix='g' + str(j) + '_' + str(i) + '_'))
                pars.update(Model[i + int(number_of_peaks) * j].make_params())
                mod = mod + Model[i + int(number_of_peaks) * j]
            if peak_type == "Lorenz":
                Model.append(LorentzianModel(prefix='l' + str(j) + '_' + str(i) + '_'))
                pars.update(Model[i + int(number_of_peaks) * j].make_params())
                mod = mod + Model[i + int(number_of_peaks) * j]
    return Model, pars, mod
"""#--------------------------------------------------------------------------





dat = np.loadtxt("d:\\Profile\\ogd\\Desktop\\PhD\\Python\\Ni2p_ref_sat_sub.dat",skiprows=1)
x = dat[:, 0]
y = dat[:, 2]

number_of_spectra = 1
number_of_peaks = 9
peak_type = "Voigt"
attribute_nr = 6            #number of parameters in the para file for the voigt


#creating the vars for I_low & I_high and other boundaries
ymin = y[0]
ymax = y[len(y) - 1]
if ymin > ymax:
    ymin, ymax = ymax, ymin
xmin = min(x)
xmax = max(x)

#I_low, I_high = I_high_low_init_calc_fkt()







def shirley_bg(x, low=0., high=.1):
    print("CALLING SHIRLEY WITH low", low, "high:", high)
    return low, high

def create_bg(left, right):
    low, high = right
    cumsum = np.cumsum(left)
    return left + low + (high - low) * (cumsum/cumsum[-1])

def build_curve_from_peaks(n_peaks=1, peak_func=lmfit.models.VoigtModel):

    model = None
    for i in range(number_of_spectra):
        for idx in range(n_peaks):
            prefix = f'p{i}_{idx}_'
            peak = peak_func(prefix=prefix)
            bg = lmfit.Model(shirley_bg, prefix=prefix)
            comp = lmfit.CompositeModel(peak, bg, create_bg)

            if model:
                model += comp
            else:
                model = comp

        return model

mod = build_curve_from_peaks(number_of_peaks)
pars = mod.make_params()
print(y)
"""-----------creating the shirley BG steps fkt heights-----------"""
#pars['p{i}_0_high'].set(value=ymin)
for i in range(number_of_spectra):
    pars[f'p{i}_0_high'].set(value=y[int(len(y))-1])
    print(pars[f'p{i}_0_high'])
    for idx in range(number_of_peaks):
#     pars[f'p{idx}_center'].set(value=peak_pos[idx])
#        pars[f'p{idx}_sigma'].set(value=sigmas[idx])
#        pars[f'p{idx}_amplitude'].set(value=amplitudes[idx])
        pars.add(f'p{i}_{idx}_delta', value=0, min=0, max=ymax)
        print(pars[f'p{i}_{idx}_delta'])
        if idx > 0:
            pars[f'p{i}_{idx}_high'].set(expr=f'p{i}_{idx - 1}_low')
            print(pars[f'p{i}_{idx}_high'])
        pars[f'p{i}_{idx}_low'].set(expr=f'p{i}_{idx}_high-p{i}_{idx}_delta')
        print(pars[f'p{i}_{idx}_low'])


mod.eval(x=x, params=pars)
plt.plot(x, y, label='data')
plt.plot(x, mod.eval(x=x, params=pars), label='start values')
#plt.plot(x, fit_res.eval(x=x, params=pars), label='end values')
plt.legend(loc='best')
plt.show()
plt.close()


## define a model
param_file_type_str = "yaml"
if param_file_type_str == "yaml":
    param_file_type = yaml
if param_file_type_str == "json":
    param_file_type = json
# json


data_param_file = param_file_type.load(open('test_param.'+param_file_type_str), Loader=param_file_type.FullLoader)
#pars = mod.make_params()

for p_name, p_vals in data_param_file.items():
    pars[p_name].set(**p_vals)
print(pars)
mod.eval(x=x, params=pars)
plt.plot(x, y, label='data')
plt.plot(x, mod.eval(x=x, params=pars), label='start values')
#plt.plot(x, fit_res.eval(x=x, params=pars), label='end values')
plt.legend(loc='best')
plt.show()
plt.close()
fit_res = mod.fit(y, x=x, params=pars)
print(pars)

"""------------------fitting of the peaks wit lin BG------------"""
mod.eval(x=x, params=pars)
plt.plot(x, y, label='data')
plt.plot(x, mod.eval(x=x, params=pars), label='start values')
plt.plot(x, fit_res.eval(x=x, params=pars), label='end values')
plt.legend(loc='best')
plt.show()


for p_name, p_value in fit_res.values.items():
    # important, otherwise expr will not work anymore!
    if pars[p_name].vary:
        if p_name not in data_param_file:
            data_param_file[p_name] = {}
            data_param_file[p_name]["value"] = 0
        data_param_file[p_name]["value"] = p_value
param_file_type.dump(data_param_file, open("updated_test_param."+param_file_type_str, "w"))

print(pars)








#######################################################################################################################################
#######################################################################################################################################


init = mod.eval(pars, x=x)
out = mod.fit(y, pars, x=x)
#print(out.fit_report(min_correl=0.5))
"""--------------calculate the fit for a straight line background----------------"""
Fit = out.best_fit
#print('Best fit' + str(Fit))
comps = out.eval_components(x=x)
Peaks = comps
Values = out.values











fig, axes = plt.subplots(1, 2, figsize=(12.8, 4.8))
axes[0].plot(x, y, 'b')
# axes[0].plot(x, init, 'k--', label='initial fit')
axes[0].plot(x, out.best_fit, 'r-', label='best fit')
axes[0].legend(loc='best')

comps = out.eval_components(x=x)
axes[1].plot(x, y, 'b')
#axes[1].plot(x, shirley_BG_sum+ymin,'b-', label='shirley_BG' )
#axes[1].plot(x, S_BG_curve+ymin,'g-', label='shirley_BG' )
# axes[1].plot(x, comps['const_'], 'k-', label='const component 1')
axes[1].plot(x, comps['v0_0_']+ymin, 'g--', label='voigt component 1')
axes[1].plot(x, comps['v0_1_']+ymin, 'm--', label='voigt component 2')
axes[1].plot(x, comps['v0_2_']+ymin, 'r--', label='voigt component 3')
axes[1].plot(x, comps['v0_3_']+ymin, 'b--', label='voigt component 4')
axes[1].plot(x, comps['v0_4_']+ymin, 'c--', label='voigt component 5')
axes[1].plot(x, comps['v0_5_']+ymin, 'y--', label='voigt component 6')
axes[1].plot(x, comps['v0_6_']+ymin, 'g-', label='voigt component 7')
axes[1].plot(x, comps['v0_7_']+ymin, 'm-', label='voigt component 8')
axes[1].plot(x, comps['v0_8_']+ymin, 'r-', label='voigt component 9')
#axes[1].legend(loc='best')

plt.show()




#this is in theory how the shirley would be calculated if only 2 fkt were used. still w/o the change of the I_high parameter
"""def shirley_BG_fkt(i):#,I_low_i,I_high_i):
    I_low_i = I_low[i]                      # take the ith element of the low list
    I_high_i = I_high[i]
    voigt_i = Model[i]
    voigt_fkt = voigt_i.eval(pars, x=x)     #change the voigtModel into actual numbers
    voigt_sum = np.sum(voigt_i.eval(pars, x=x))     # get the total area of the peak
    shirley_BG=[]
    for idx in range(len(y)):
        S_BG = I_low_i + (I_high_i - I_low_i) * (np.sum(voigt_fkt[idx:len(y)])) / (voigt_sum)
        shirley_BG.append(S_BG)

    return shirley_BG


#here the shirley calc for each peac starts
shirley_BG=[[]]
def shirley_BG_total_fkt():
    shirley_BG_sum = [0] * len(y)
    for i in range(int(number_of_peaks)):
        S_BG = shirley_BG_fkt(i)
        shirley_BG.append(S_BG)
        for j in range(len(y)):
            shirley_BG_sum[j] = shirley_BG_sum[j] + S_BG[j] - I_low[i]
    return shirley_BG_sum

shirley_BG_sum=shirley_BG_total_fkt()
#print(shirley_BG_sum)"""


































