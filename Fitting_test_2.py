import matplotlib.pyplot as plt
import numpy as np
from lmfit.models import ExponentialModel, GaussianModel, VoigtModel, LinearModel, ConstantModel, StepModel, \
    ExpressionModel, LorentzianModel
from numpy import array, linspace, arange, zeros, ceil, amax, amin, argmax, argmin, abs
from numpy.linalg import norm
import pandas as pd
import functools, sys
import scipy as sp
from pandas import DataFrame
import re,os,fnmatch,sys
import lmfit.models
from lmfit import minimize, Parameters, report_fit
from scipy.optimize import leastsq
from tkinter import filedialog
from tkinter import *
import glob
import time
import math
import matplotlib as mpl
import yaml, json, lmfit



namespace = sys._getframe(0).f_globals
plt.style.use('seaborn-ticks')
mpl.rcParams.update({'font.size': 16})


def select_txt_or_dat():
    txt_or_dat = input("are you using .txt files or .dat files? Please enter 'txt' or 'dat'")
    if txt_or_dat == "txt":
        txt = ".txt"
    if txt_or_dat == "dat":
        txt = ".dat"
    return txt

def folder_or_file():
    print("Do you want to use a single file with all spectra in one or multiple ones (all files in one folder)?")
    folder_or_file = input("If you want to use a single file please enter 'file'. If you want to use multiple files, please enter 'folder'\n")
    if folder_or_file =="file":
        type="file"
        file_path = input("Please enter the complete file path (incl the filde_name w/o the .txt/dat")
        txt=select_txt_or_dat()
        skip_row_nr = input("Please enter number of rows above incl the heaader line ('E S00 S01' or what ever the header is)\n")
        return file_path, type, txt, skip_row_nr
    if folder_or_file == "folder":
        type="folder"
        folder_path = input("Please enter the folder path to the files")
        txt=select_txt_or_dat()
        skip_row_nr = input("Please enter number of rows above incl the headder line ('# Energy Kinetic' or what ever the header is)\n")
        return folder_path,type,txt, skip_row_nr

def BE_or_KE_fkt():
    BE_or_KE_check = False
    while BE_or_KE_check == False:
        choice_input = input(
            "Is the following energy scale in binding (BE) or kinetic (KE)? please enter 'BE' for binding or 'KE' for kinetic\n")
        if choice_input == "KE":
            exertation_energy = float(input("Please enter the exertation energy (in eV). like 1486.7\n"))
            BE_or_KE = "KE"
            BE_or_KE_check = True
        elif choice_input == "BE":
            exertation_energy = 0
            BE_or_KE = "BE"
            BE_or_KE_check = True
        else:
            print("\nError, please type in 'BE' or 'KE'\n")
            BE_or_KE_check = False

    return BE_or_KE, exertation_energy

def energy_test_fkt(d):
    dat_E = d["dat_0"]["E"]
    if dat_E[0] > dat_E[len(dat_E) - 1]:
        print("The data energy was decreasing instead of increasing. Therefore the data got swapped\n")
        for i in range(int(number_of_spectra)):
            d["dat_%i" % i] = d["dat_%i" % i][::-1]
            d["dat_%i" % i] = d["dat_%i" % i].reset_index(drop=True)
    return d

def dat_merger_single_file_fkt(file_path, skip_rows, number_of_spectra):
    df = pd.read_csv(file_path + txt, skiprows=skip_rows, delim_whitespace=True, header=None)
    d={}
    BE_or_KE, exertation_energy  = BE_or_KE_fkt()

    for i in range(int(number_of_spectra)):
        d["dat_%i"%i]=pd.DataFrame(columns=["E", "Spectra"])
        if BE_or_KE == "BE":
            d["dat_%i"%i]["E"] = df.iloc[:, 0]
        if BE_or_KE == "KE":
            d["dat_%i" % i]["E"] = df.iloc[:, 0] - exertation_energy
        d["dat_%i" % i]["Spectra"] = df.iloc[:, i+1]

    d = energy_test_fkt(d)
    return d

def dat_merger_multiple_files_fkt(folder_path, skip_rows, number_of_spectra):
    txt_files = glob.glob(folder_path + "*" + txt)
    BE_or_KE, exertation_energy = BE_or_KE_fkt()

    d={}
    for i in range(number_of_spectra):
        df = pd.read_csv(txt_files[i], skiprows=skip_rows, delim_whitespace=True, header=None)
        d["dat_%i" % i] = pd.DataFrame(columns=["E", "Spectra"])
        if BE_or_KE == "BE":
            d["dat_%i" % i]["E"] = df.iloc[:, 0]
        if BE_or_KE == "KE":
            d["dat_%i" % i]["E"] = df.iloc[:, 0] - exertation_energy
        d["dat_%i" % i]["Spectra"] = df.iloc[:, 1]

    d = energy_test_fkt(d)
    return d

def shirley_bg(x, low=0., high=.1):
    return low, high


def create_bg(left, right):
    low, high = right
    cumsum = np.cumsum(left)
    return left + low + (high - low) * (cumsum / cumsum[-1])


def build_curve_from_peaks(i, idx, n_spectra=1):
    #if peak_type == "Voigt":
    #    peak_func = lmfit.models.VoigtModel
    #if peak_type == "Gauss":
    #    peak_func = lmfit.models.GaussiantModel
    #if peak_type == "Lorentz":
    #    peak_func = lmfit.models.LorentzianModel
    #if peak_type == ???:
    #    peak_func = lmfit.models.???Model
    model = None
    prefix = f'p{i}_{idx}_'
    peak = peak_func(prefix=prefix)
    bg = lmfit.Model(shirley_bg, prefix=prefix)
    comp = lmfit.CompositeModel(peak, bg, create_bg)
    if model:
        model += comp
    else:
        model = comp

    return model

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


def shirley_param_calc(pars):
    p4fit_d = {}
    for idx in range(0, int(number_of_peaks)):
        for i in range(int(number_of_spectra)):
            p4fit_d[f'p{i}_{idx}'] = mod_d[f'mod{i}_{idx}'].make_params()
    for i in range(int(number_of_spectra)):
        yraw = d[f'dat_{i}']["Spectra"]
        deltas = (yraw[len(yraw) - 1] - yraw[0])
        p4fit_d[f'p{i}_0'].add(f'p{i}_0_low', value=yraw[0])
        for idx in range(int(number_of_peaks)):
            p4fit_d[f'p{i}_{idx}'][f'p{i}_{idx}_center'].set(value=pars[
                f'p{i}_{idx}_center'].value)  # TODO: make it more general (using the vars which one want to give not generic ones) --> through list?
            p4fit_d[f'p{i}_{idx}'][f'p{i}_{idx}_amplitude'].set(value=pars[f'p{i}_{idx}_amplitude'].value)
            p4fit_d[f'p{i}_{idx}'][f'p{i}_{idx}_sigma'].set(value=pars[f'p{i}_{idx}_sigma'].value)
            p4fit_d[f'p{i}_{idx}'][f'p{i}_{idx}_gamma'].set(value=pars[f'p{i}_{idx}_gamma'].value)

            p4fit_d[f'p{i}_{idx}'].add(f'p{i}_{idx}_delta', value=deltas / int(number_of_peaks), min=0)
            if idx > 0:
                p4fit_d[f'p{i}_{idx}'][f'p{i}_{idx}_low'].set(value=0, vary=False)
            p4fit_d[f'p{i}_{idx}'][f'p{i}_{idx}_high'].set(expr=f'p{i}_{idx}_low+p{i}_{idx}_delta')
            print(p4fit_d[f'p{i}_{idx}'][f'p{i}_{idx}_high'])
    return p4fit_d

def peak_eval_fkt(param_file_type, y):
    pars = param_updater(param_file_type, y)
    p4fit_d = shirley_param_calc(pars)
    return pars, p4fit_d



folder_or_file=folder_or_file()
path, file_type, txt, skip_rows= folder_or_file
number_of_spectra = 169#input("please enter the number of spectra you want to fit\n")

if file_type == "file":
    d = dat_merger_single_file_fkt(path, int(skip_rows), number_of_spectra)
if file_type == "folder":
    d = dat_merger_multiple_files_fkt(path,int(skip_rows),number_of_spectra)

number_of_spectra = 2
number_of_peaks = 9
select_peak_type = False
while select_peak_type == False:
    peak_type = input("please enter the type of peak you are using.\n e.G. Voigt, Gauss, Lorentz")
    if peak_type.lower() == "voigt":
        peak_type == "Voigt"
        select_peak_type == True
        peak_func = lmfit.models.VoigtModel
        break
    if peak_type.lower() == "gauss":
        peak_type == "Gauss"
        select_peak_type == True
        peak_func = lmfit.models.GaussianModel
        break
    if peak_type.lower() == "lorentz":
        peak_type == "Lorentz"
        select_peak_type == True
        peak_func = lmfit.models.LorentzianModel
        break
    else:
        select_peak_type = correct_input_fkt(peak_type)
attribute_nr = 6


d["dat_0"] = d["dat_100"].copy()
d["dat_1"] = d["dat_121"].copy()


param_file_type = "yaml" #input("please enter if you are using 'yaml' or 'json'")
pars = param_updater(param_file_type)

mod_d = {}
for idx in range(0, int(number_of_peaks)):
    for i in range(int(number_of_spectra)):
        mod_d[f'mod{i}_{idx}'] = build_curve_from_peaks(i, idx, number_of_spectra)

p4fit_d = shirley_param_calc(pars)



"""-----------------------------------------------------------------------------------------------------------------"""
################################### the fitting starts here ##########################################################
"""-----------------------------------------------------------------------------------------------------------------"""

def y_for_fit(d):
    y_d = np.array([[0.0] * len(d[f'dat_0']["Spectra"])] * (number_of_spectra))
    resid = np.array([[0.0] * len(d[f'dat_0']["Spectra"])] * (int(number_of_spectra)))
    for i in range(int(number_of_spectra)):
        for j in range(len(d["dat_0"]["E"])):
            dat_holder = d[f'dat_{i}']
            y_d[i][j] = dat_holder["Spectra"][j]
    return y_d, resid

def param_per_peak_sorting_fkt(p4fit):
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

def param_per_spectra_sorting_fkt(p4fit):
    p4fit_di={}
    for i in range(int(number_of_spectra)):
        p4fit_di[f"spectra_{i}"] = {}
    k=0
    for idx in range(int(number_of_peaks)):
        for i in range(int(number_of_spectra)):
            for name in p4fit:
                if f'p{i}_{idx}_' in name:
                    p4fit_di[f'spectra_{i}'][f"{name}"]= p4fit[name]
    return p4fit_di

def param_merger_from_per_peak_fkt(p4fit_d):
    p4fit = p4fit_d[f"p0_0"]
    print(type(p4fit_d[f"p0_0"]))
    for idx in range(int(number_of_peaks)):
        for i in range(int(number_of_spectra)):
            p4fit=p4fit + p4fit_d[f"p{i}_{idx}"]
    return p4fit

def model_eval_fit_fkt(params):
    model_eval=np.array([[0.0] * len(d[f'dat_0']["Spectra"])] * (number_of_spectra))
    for idx in range(int(number_of_peaks)):
        for i in range(int(number_of_spectra)):
            model_eval[i] = model_eval[i] + mod_d[f'mod{i}_{idx}'].eval(x=np.array(x), params=params[f"p{i}_{idx}"])
    return model_eval

def model_eval_fitted_fkt(params):
    model_eval=np.array([[0.0] * len(d[f'dat_0']["Spectra"])] * (number_of_spectra))
    for idx in range(int(number_of_peaks)):
        for i in range(int(number_of_spectra)):
            model_eval[i] = model_eval[i] + mod_d[f'mod{i}_{idx}'].eval(x=np.array(x), params=params[f'spectra_{i}'])
    return model_eval

def fitting_over_all_spectra(p4fit, x, d):
    y_d, resid = y_for_fit(d)
    p4fit_d = param_per_peak_sorting_fkt(p4fit)
    model_eval= model_eval_fit_fkt(p4fit_d)
    for i in range(int(number_of_spectra)):
        resid[i, :] = y_d[i,:] - model_eval[i,:]
    return resid.flatten()

x = d[f'dat_0']["E"].to_numpy()


y_d, resid = y_for_fit(d)

p4fit_pars = param_merger_from_per_peak_fkt(p4fit_d)
model_eval = model_eval_fit_fkt(p4fit_d)

out = minimize(fitting_over_all_spectra, p4fit_pars, args=(x, d), max_nfev=1000)

out_params= param_per_spectra_sorting_fkt(out.params)
model_d_fitted = model_eval_fitted_fkt(out_params)
print(out)

#report_fit(out.params)


#out = minimize(fitting_over_all_spectra(), p4fit, args=(x, d))
#report_fit(out.params)
fig, axes = plt.subplots()
axes.plot(x, y_d[0], 'black')
axes.plot(x, y_d[1], 'r')
axes.plot(x, model_eval[0], 'b')
axes.plot(x, model_eval[1], 'g')
axes.plot(x, model_d_fitted[0], 'grey')
axes.plot(x, model_d_fitted[1], 'y')
print("Plot of fitted data. Close it to continue")
plt.show()
plt.close()



data_param_file={}
bla=input("continue the param_writing")
""" saving output into diff file"""
for p_name, p_value in out.params.items():
    # important, otherwise expr will not work anymore!
    print(p_name, p_value)
    if pars[p_name].vary:
        if p_name not in data_param_file:
            print(p_name, p_value, "inner loop")
            data_param_file[p_name] = {}
            data_param_file[p_name]["value"] = 0
        data_param_file[p_name]["value"] = p_value
param_file_type.dump(data_param_file, open("updated_test_param."+param_file_type_str, "w"))
