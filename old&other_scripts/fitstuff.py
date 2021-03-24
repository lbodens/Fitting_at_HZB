import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import sys
import math
from lmfit.models import GaussianModel, VoigtModel, LinearModel, LorentzianModel
import lmfit

plt.style.use('seaborn-ticks')
mpl.rcParams.update({'font.size':16})


dat = np.loadtxt("Ni2p_ref_sat_sub.dat",skiprows=1)


def shirley_bg(x, low=0., high=.1):
    print("CALLING SHIRLEY WITH low", low, "high:", high)
    return low, high

def create_bg(left, right):
    low, high = right
    cumsum = np.cumsum(left)
    print(low, high)
    plt.plot(left)
    plt.plot(low + (high - low) * (cumsum/cumsum[-1]))
    plt.plot(left + low + (high - low) * (cumsum/cumsum[-1]))
    plt.show()
    return left + low + (high - low) * (cumsum/cumsum[-1])

def build_curve_from_peaks(n_peaks=1, peak_func=lmfit.models.VoigtModel):

    model = None
    for idx in range(n_peaks):
        prefix = f'p{idx}_'
        peak   = peak_func(prefix=prefix)
        bg     = lmfit.Model(shirley_bg, prefix=prefix)
        comp = lmfit.CompositeModel(peak, bg, create_bg)

        if model:
            model += comp
        else:
            model  = comp

    return model


mod_1_peak = build_curve_from_peaks(1)
params = mod_1_peak.make_params()

x = np.linspace(0, 200, 200)
params['p0_center'].set(value=60)
params['p0_sigma'].set(value=4)
params['p0_amplitude'].set(value=4)

params.add('p0_delta', value=.2, min=0)
params['p0_high'].set(value=.3, min=0)
params['p0_low'].set(expr='p0_high-p0_delta')

y  = mod_1_peak.eval(params, x=x)
dy = np.random.normal(y, 0.015)
plt.plot(x, dy, '.', label='dummy data')
plt.plot(x, y, '--', label='ground truth')


#res = mod_1_peak.fit(dy, params, x=x)
#plt.plot(x, res.best_fit, '--', label='fit')

plt.legend(loc='best')
plt.show()


mod_2_peak = build_curve_from_peaks(2)
params = mod_2_peak.make_params()

x = np.linspace(0, 200, 200)
params['p0_center'].set(value=40)
params['p0_sigma'].set(value=3)
params['p0_amplitude'].set(value=4)
params.add('p0_delta', value=.2, min=0)
params['p0_high'].set(value=.8, min=.2)
print(params['p0_high']-params['p0_delta'])
params['p0_low'].set(expr='p0_high-p0_delta')
print(params['p0_low'])
params['p1_center'].set(value=70)
params['p1_sigma'].set(value=3)
params['p1_amplitude'].set(value=4)
params.add('p1_delta', value=.1, min=0)
params['p1_high'].set(expr='p0_low')
print(params['p1_high']-params['p1_delta'])

params['p1_low'].set(expr='p1_high-p1_delta')
print(params['p1_high'],params['p1_low'])
y  = mod_2_peak.eval(params, x=x)
dy = np.random.normal(y, 0.015)
plt.plot(x, dy, '.', label='dummy data')
plt.plot(x, y, '--', label='ground truth')


# res = mod_2_peak.fit(dy, params, x=x)
# plt.plot(x, res.best_fit, '--', label='fit')

plt.legend(loc='best')
plt.show()


def shirley_bg(x, low=0., high=.1):
    print("CALLING SHIRLEY WITH low", low, "high:", high)
    return low, high

def create_bg(left, right):
    low, high = right
    cumsum = np.cumsum(left)
    return left + low + (high - low) * (1-cumsum/cumsum[-1])

def build_curve_from_peaks(n_peaks=1, peak_func=lmfit.models.VoigtModel):

    model = None
    for idx in range(n_peaks):
        prefix = f'p{idx}_'
        peak   = peak_func(prefix=prefix)
        bg     = lmfit.Model(shirley_bg, prefix=prefix)
        comp = lmfit.CompositeModel(peak, bg, create_bg)

        if model:
            model += comp
        else:
            model  = comp

    return model

mod_3_peaks = build_curve_from_peaks(3)
params = mod_3_peaks.make_params()

x = np.linspace(0, 100, 200)
params['p0_center'].set(value=35)
params['p0_sigma'].set(value=2)

params['p1_center'].set(value=50)
params['p1_sigma'].set(value=2)

params['p2_center'].set(value=70)
params['p2_sigma'].set(value=1)

params['p0_high'].set(value=.8)
for idx in range(3):
    params.add(f'p{idx}_delta', value=.1, min=0, vary=True)
    if idx > 0:
        params[f'p{idx}_high'].set(expr=f'p{idx-1}_high-p{idx-1}_delta')
        print(params[f'p{idx}_high'])
    params[f'p{idx}_low'].set(expr=f'p{idx}_high-p{idx}_delta')
    print(params[f'p{idx}_low'])


y  = mod_3_peaks.eval(x=x, params=params)
dy = np.random.normal(y, 0.015)
plt.plot(x, dy, '.', label='dummy data')
plt.plot(x, y, '--', label='ground truth')
plt.legend(loc='best')
plt.show()



x = dat[:, 0]
y = dat[:,2]

plt.plot(900-x, y/y.max(), label='data')
mod_8_peaks = build_curve_from_peaks(8)
p = mod_8_peaks.make_params()
peak_pos   = [20, 25, 27.5, 35, 38.5, 43.5, 45.5, 55]
amplitudes = [.5, .3, .4, .6, .7, .9, .45, .05]
sigmas     = np.ones(8)*.5#[1.5, 1, .8, 2, 1, .9, .45, 1]

plt.plot(900-x, y/y.max(), label='data')
plt.plot(900-x, mod_8_peaks.eval(x=900-x, params=p), label='start values')
plt.legend(loc='best')
plt.show()

p['p0_high'].set(value=0.15)
for idx in range(8):
    p[f'p{idx}_center'].set(value=peak_pos[idx])
    p[f'p{idx}_sigma'].set(value=sigmas[idx])
    p[f'p{idx}_amplitude'].set(value=amplitudes[idx])
    p.add(f'p{idx}_delta', value=0.015, min=0, max=.15)
    print(p[f'p{idx}_delta'])
    if idx > 0:
        p[f'p{idx}_high'].set(expr=f'p{idx-1}_low')
        print(p[f'p{idx}_high'])
    p[f'p{idx}_low'].set(expr=f'p{idx}_high-p{idx}_delta')  
    print(p[f'p{idx}_low'])
    plt.plot(900 - x, y / y.max(), label='data')
    plt.plot(900 - x, mod_8_peaks.eval(x=900 - x, params=p), label='start values')
    #plt.legend(loc='best')
    plt.show()


mod_8_peaks.eval(x=900-x, params=p)
plt.plot(900-x, y/y.max(), label='data')
plt.plot(900-x, mod_8_peaks.eval(x=900-x, params=p), label='start values')
plt.legend(loc='best')
plt.show()



fit_res = mod_8_peaks.fit(y/y.max(), x=900-x, params=p)
x = dat[:, 0]
y = dat[:,2]

plt.plot(900-x, y/y.max(), '.', label='data')

plt.plot(900-x, fit_res.best_fit, '--', label='fit')
plt.legend(loc='best')
