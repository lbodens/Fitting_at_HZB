import numpy as np
from numpy import array, linspace, arange, zeros, ceil, amax, amin, argmax, argmin, abs
from numpy.linalg import norm
import pandas as pd
from pandas import DataFrame
import scipy as sp
from scipy.optimize import leastsq
from tkinter import filedialog
from tkinter import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import re, os, fnmatch, sys, functools
import yaml, json, lmfit
import lmfit.models
from lmfit import minimize, Parameters, report_fit
from lmfit.models import ExponentialModel, GaussianModel, VoigtModel, LinearModel, ConstantModel, StepModel, \
    ExpressionModel, LorentzianModel
import glob
import time
import math

namespace = sys._getframe(0).f_globals
plt.style.use('seaborn-ticks')
mpl.rcParams.update({'font.size': 16})


"""-------------------------------------------------------Import the data file------------------------------------------------------------"""

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
    for i in range(int(number_of_spectra)):
        df = pd.read_csv(txt_files[i], skiprows=skip_rows, delim_whitespace=True, header=None)
        d["dat_%i" % i] = pd.DataFrame(columns=["E", "Spectra"])
        if BE_or_KE == "BE":
            d["dat_%i" % i]["E"] = df.iloc[:, 0]
        if BE_or_KE == "KE":
            d["dat_%i" % i]["E"] = df.iloc[:, 0] - exertation_energy
        d["dat_%i" % i]["Spectra"] = df.iloc[:, 1]

    d = energy_test_fkt(d)
    return d
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------"""

"""------------------------------------Check, if the input is correct or not/catch it if its wrong ------------------------------------------------------------"""
def correct_input_fkt(Input):
    print("\nThe input:")
    print(Input)
    print("seem to be incorrect.\nYou seem to have misspelled the type or it is not included.\nPlease try again: ")
    return False
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------"""

"""----------------------------------------------------------------------------------------------------------------------------------------"""
"""--------------------------------------------------------XPS peak fitting----------------------------------------------------------------"""
"""----------------------------------------------------------------------------------------------------------------------------------------"""

"""--------------Peak fit models----------------"""
from lmfit.models import GaussianModel          
#parameters amplitude, center, sigma
# f(x:A, mu, sigma) =(A/sigma*sqrt(2*pi))*exp(-(x-mu)^2/(2*sigma*2))
#fwhm = 2*sigma*swrt(2*ln(2))
#prefix = "Gaus_"

from lmfit.models import LorentzianModel        
#amplitude, center, sigma
# f(x:A, mu, sigma) = (A/pi)*(sigma/((x-mu)^2+sigma^2))
#prefix = "Loren_"

from lmfit.models import VoigtModel             
#parameters amplitude, center, sigma, gamma
#Default gamma = sigma, then fwhm = 3.6013*sigma
# f(x:A, mu, sigma, gamma) = A*RE(w(z))/(sigma*sqrt(2*pi))
# z = (x - mu + i*gamma)/(sigma*sqrt(2))
# w(z) = exp(-z^2)*erfc(-i*z)
#prefix = "Voigt_"

from lmfit.models import DoniachModel
#parameters amplitude, center, sigma, gamma
# f(x:A, mu, sigma, gamma)
#prefix = "DS_"

"""----------------------------------------------------------------------------------------------------------------------------------------"""
"""------------------------------------------------------Shirley background fit------------------------------------------------------------"""
"""----------------------------------------------------------------------------------------------------------------------------------------"""
def shirley_bg(x, low=0., high=.1):
    return low, high

def create_bg(left, right):
    low, high = right
    cumsum = np.cumsum(left)
    return left + low + (high - low) * (cumsum / cumsum[-1])

def build_curve_from_peaks(i, idx, n_spectra=1):
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
            p4fit_d[f'p{i}_{idx}'][f'p{i}_{idx}_center'].set(value=pars[f'p{i}_{idx}_center'].value)  # TODO: make it more general (using the vars which one want to give not generic ones) --> through list?
            p4fit_d[f'p{i}_{idx}'][f'p{i}_{idx}_amplitude'].set(value=pars[f'p{i}_{idx}_amplitude'].value)
            p4fit_d[f'p{i}_{idx}'][f'p{i}_{idx}_sigma'].set(value=pars[f'p{i}_{idx}_sigma'].value)
            p4fit_d[f'p{i}_{idx}'][f'p{i}_{idx}_gamma'].set(value=pars[f'p{i}_{idx}_gamma'].value)

            p4fit_d[f'p{i}_{idx}'].add(f'p{i}_{idx}_delta', value=deltas / int(number_of_peaks), min=0)
            if idx > 0:
                p4fit_d[f'p{i}_{idx}'][f'p{i}_{idx}_low'].set(value=0, vary=False)
            p4fit_d[f'p{i}_{idx}'][f'p{i}_{idx}_high'].set(expr=f'p{i}_{idx}_low+p{i}_{idx}_delta')
            print(p4fit_d[f'p{i}_{idx}'][f'p{i}_{idx}_high'])
    return p4fit_d


"""------------------fkt to show spectra with init peaks------------------------------------------"""

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

def peak_eval_fkt(param_file_type):
    pars = param_updater(param_file_type)
    mod, p4fit = shirley_param_calc(pars)
    init = mod.eval(x=x, params=p4fit)
    return pars, mod, p4fit, init

def plotting(x, spectra_to_plot,number_of_peaks):
    pars, mod, p4fit, init = peak_eval_fkt(param_file_type)
    fig, axes = plt.subplots()
    x = dat["E"].to_numpy()
    yraw = dat["Spectra"].to_numpy()
    axes.plot(x, yraw, 'b')
    axes.plot(x, init, 'k--', label='initial fit')
    plt.xlim([min(x) + (int(spectra_to_plot) - 1) * 10000, max(x) + (int(spectra_to_plot) - 1) * 10000])
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

"""-------------------------------------------------------------------------"""

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



"""--------------------general commands like: spectra merging & peak types--------------------------""" #TODO putting all of this at a good/practical/reasonable place in the code (like where it really starts and then it calls all the functions)
#taking the wanted spectra and merge them into one long
folder_or_file = folder_or_file()
path, file_type, txt, skip_rows = folder_or_file

number_of_spectra = input("please enter the number of spectra you want to fit\n")
if file_type == "file":
    d = dat_merger_single_file_fkt(path, int(skip_rows), int(number_of_spectra))
if file_type == "folder":
    d = dat_merger_multiple_files_fkt(path,int(skip_rows),int(number_of_spectra))


#plotting the first spectra to get better overview
fig, axes = plt.subplots()
axes.plot(d["dat_0"]["E"], d["dat_0"]["Spectra"], 'b')
plt.xlim([min(d["dat_0"]["E"]), max(d["dat_0"]["E"])])
print("Now a plot of the 1st spectra is shown, that you can quickly look if you want to change some pre set parameters. Close it to continue")
plt.show()
plt.close()


#creating wanted number and types of peaks
number_of_peaks = input("please enter the number of peaks you want to use for fitting\n")
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
   # if peak_type.lower() == ???:                                           TODO: include more peak types
        #    peak_func = lmfit.models.???Model
    else:
        select_peak_type = correct_input_fkt(peak_type)

if peak_type == "Voigt":
   attribute_nr = 6
if peak_type == "Gauss":
   attribute_nr = 5
if peak_type == "Lorentz":
   attribute_nr = 5
#if peak_type =="???"                       TODO
#    attribute_nr = ???
"""-----------------------------------------------------------------------------"""

"""---------------Importing previous parameter file and check imputs ----------------------"""
param_file_type = input("please enter if you are using 'yaml' or 'json'")
pars= param_updater(param_file_type)

mod_d = {}
for idx in range(0, int(number_of_peaks)):
    for i in range(int(number_of_spectra)):
        mod_d[f'mod{i}_{idx}'] = build_curve_from_peaks(i, idx, number_of_spectra)

p4fit_d = shirley_param_calc(pars)

plot_checking()

"""--------------------------------------actual fitting fkt------------------------------------------------"""
x = d[f'dat_0']["E"].to_numpy()

model_eval = model_eval_fit_fkt(p4fit_d)
p4fit_pars = param_merger_from_per_peak_fkt(p4fit_d)

out = minimize(fitting_over_all_spectra, p4fit_pars, args=(x, d), max_nfev=1000)

out_params= param_per_spectra_sorting_fkt(out.params)
model_d_fitted = model_eval_fitted_fkt(out_params)
report_fit(out.params)

y_d, resid = y_for_fit(d)
fig, axes = plt.subplots()
axes.plot(x, y_d[0], 'black',label='data')
axes.plot(x, y_d[1], 'r',label='data')
axes.plot(x, model_eval[0], 'b',label='start values')
axes.plot(x, model_eval[1], 'g',label='start values')
axes.plot(x, model_d_fitted[0], 'grey',label='fit')
axes.plot(x, model_d_fitted[1], 'y',label='fit')
plt.legend(loc='best')
plt.show()


"""-------------------------------------------------Exporting Data-----------------------------------------------------------"""
Header=['eV', 'raw count', 'Overall fit', 'BGND' 'v1', 'v2', 'v3']



""" saving output into diff file"""
data_param_file={}
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










"""-------------------------------------------------------Gets the working directory, and the number & type of files in it------------------------------------------------------------"""
"""osdirr=[]
Directory=[]
NoFiles=[]
filetype=0
def directory(Directory,NoFiles,filetype,osdirr):
    print ('Current working directory')
    #dirr=os.getcwd()
    #dirr=dirr.replace("\\","/")
    #print(dirr)     
    '''------Only when testing the code!!!------'''
    dirr='C:\Python scripts\XPS - Ti 2p'    
    print(dirr)
    '''-----------------------------------------'''  
    osdirr=dirr

    '''------Loads all the csv & dat files------'''
    File1=glob.glob(os.path.join(dirr,'*.csv'))
    File2=glob.glob(os.path.join(dirr,'*.dat'))
    '''-----------------------------------------''' 
    '''------Assigns a value to csv & dat-------'''
    filetype=0
    if File1 == []:  #if the files are dat files
        Directory = File2
        filetype = 1
    else:           #if the files are csv files
        Directory = File1
        filetype = 0
    '''-----------------------------------------'''
    #print(Directory)    
    print('There are ' +str(len(Directory))+ ' files in the directory')
    #print(filetype)
    NoFiles = len(Directory)
    return (Directory,NoFiles,filetype,osdirr)
Directory,NoFiles,filetype,osdirr = directory(Directory,NoFiles,filetype,osdirr)"""
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------"""

"""--------------------------------------------Reads the files and saves in a dataframe [array of eV & count]-------------------------------------------------"""
"""filesread=[]
def filereader(Directory,filesread,filetype):
    print(Directory)
    len(Directory)
    file1=[]
    for i,x in enumerate(Directory):
        if filetype ==0:
            file1 = pd.read_csv(x,sep=',', names=['eV','Count'])
            print(file1)
            eV=file1.eV.values.tolist()
            count=file1.Count.values.tolist()
            filesread.append(file1)            
        else:
            print(x)
            print(i)
            file1 = pd.read_csv(x,sep='\t',names=['eV','Count'])
            print(file1)
            eV=file1.eV.values.tolist()
            count=file1.Count.values.tolist()
            filesread.append(file1)    
    print(filesread)
    return filesread
filesread = filereader(Directory,filesread,filetype)"""
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------"""

"""-------------------------------------------------------Saves all the names of the read files ------------------------------------------------------------"""
"""names=[]
def filenamer(Directory,osdirr):   
    #print(Directory)
    '''------Stores the file names of the imported csv/dat files------'''
    for i,x in enumerate(Directory):
        #print(x)
        #print(i)        
        x1=(x.split(osdirr))[1]
        #print(x1)
        name=re.findall(r'\\([a-zA-Z0-9\s\-\_\'\,\&\!]*)',x1)
        #print('name: '+str(name))
        if name==[]:
            name=re.findall(r'\\([a-zA-Z0-9\s\-\'\,\&\!]*)\.',x1)
            if name==[]:
                print("Unable to establish file name from:  " +str(x1))
                while True:
                    name=[input("What would you like to name the file?\n")]
                    if name[0]=='':
                        print("Invalid file name")
                        continue
                    else:
                        break
            else:
                name=name[0]
        else:
            name=name[0]
        #print(name)
        #name=i1[0]
        names.append(name)
        print(names)
    return names
names = filenamer(Directory,osdirr)   """
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------"""

"""-------------------------------------------------------Makes eV the index of the arrays------------------------------------------------------------"""
"""filesread_eV=[]
def energyscalebasis(filesread):
    filesread_eV=[x.copy() for x in filesread]
    filesread_eV=[x.set_index('eV') for x in filesread_eV]   
    return filesread_eV

filesread_eV = energyscalebasis(filesread)"""
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------"""

"""-------------------------------------------------------Cuts all of the files in the filesread to the same eV range---------------------------------------------"""
"""filesread_sameeV=[]
eVrange=[]
def sameenergyrange(filesread,eVrange):
    filesread_sameeV=[x.copy() for x in filesread]
    min1=max([min(x['eV']) for x in filesread_sameeV])
    max1=min([max(x['eV']) for x in filesread_sameeV])
    filesread_sameeVCopy=[x.set_index('eV') for x in filesread_sameeV]
    filesread_sameeVCopy=[x[468:min1] for x in filesread_sameeVCopy]
    print(filesread_sameeVCopy[0])
    len(filesread_sameeVCopy[0])
    eVlist=filesread_sameeVCopy[0].index.values.tolist()
    eVrange=np.array(eVlist)
    return (filesread_sameeVCopy,eVrange)
filesread_sameeV,eVrange = sameenergyrange(filesread,eVrange)    """
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------"""




"""def PeakModel (xraw,yraw,Straightline,I1,I2):

    initialtime=time.time()
    maxiter=10
    Residuals=[]
    Fit=[]
    Peaks=[]
    Values=[]
    BGND=Straightline #straight line approximation between yraw[0] and yraw[-1] as first guess
    nloop=0
    err = 1
    while err > 1e-6 and nloop < maxiter:  

        print('PeakMModel Iteration no. '+str(nloop+1))
        yguess = yraw - BGND
        #print('yguess is' +str(yguess))

     - -------------calculate
the
fit
for a straight line background----------------"""
"""
        out = mod.fit(yguess, pars,x=xraw)    
        Fit = out.best_fit
        #print('Best fit' + str(Fit))
        comps = out.eval_components(x=xraw)
        Peaks = comps
        Values = out.values
        #print('values' + str(Values))
        """#--------------Add straight line back in ----------------
"""
        Fit_BGND=Fit+BGND
        """#--------------calculate shirley background for fitted data----------------
"""
        BGND=shirley_baseline(xraw,Fit_BGND,I1,I2)
        #print('Background '+str(BGND))
        """#--------------check fit to raw data----------------
"""
        Overall=Fit+BGND
        Diff=yraw-Overall
        Residuals=Diff
        sumDiff=np.abs(sum(Diff))
        #print(err)
        #print(sumDiff)
        if np.abs(sumDiff - err) < 1e-4:
            break
        else:
            err=sumDiff
        print(err)
        nloop += 1


    print('Done with PeakModel Fit')
    finaltime=time.time()
    Duration = finaltime-initialtime
    print('It took {:.2f} seconds for PeakModel Fit'.format(Duration))

    report=out.fit_report
    #print(out.fit_report(min_correl=0.5))
    return (Fit, BGND, Peaks, Values, Residuals) 
"""#------------------------------------------------------------------------------------------------------------------


#-------------------------------updating the parameters in the fits--------------------------------------
"""
def peak_values_update():
    read_lines = pd.read_csv("d:\\Profile\\ogd\\Desktop\\PhD\\Python\\fit_result_1.txt", header=None, skiprows=0,
                             delim_whitespace=True)                         #TODO change path/make it general/take it directly from Out, also set the right skiprows
    rows_to_skip = int(input(
        "If you are using the unchanged list from 'out', please enter the number of rows before (including) [Values]. So that the 'lin_slope' is at position 0\n")) #TODO directly searc for [[Variables]] and scip everytin above
    for j in range(int(number_of_spectra)):

        for i in range(int(number_of_peaks)):
            peak_nr = (rows_to_skip + 2) + attribute_nr * (i + int(number_of_peaks) * j)

            for k in range(attribute_nr):
                para_name = read_lines.loc[peak_nr + k][0]
                para_name = para_name.replace(":", "")
                para_value = read_lines.loc[peak_nr + k][1]
                para_test = read_lines.loc[peak_nr + k][6]
                if type(para_test) == type(str()):  # first loop to see if its a string to cath the "=" or expr
                    if para_test == "=":
                        print(para_name)
                        pars[para_name].set(value=para_value)
                    continue
                if type(para_test) == type(float()):  # if its not a str it might be the NaN
                    if math.isnan(para_test) == True:
                        print(para_name)
                        pars[para_name].set(value=para_value)
"""#------------------------------------------------------------------------------------------------------------------
"""


'''-----------------------------File looper------------------------------------------'''
t1=time.time()
fileslen=len(filesread_sameeV)
Fit=[] 
BGND =[] 
Peaks=[] 
Values=[] 
Residuals=[]
Spectra=[]
for i in range (fileslen):
    xraw=filesread_sameeV[i].index.to_numpy()
    yraw=filesread_sameeV[i]['Count'].to_numpy()
    Spectra.append(yraw)
    print('File iteration no. ' +str(i))
    #print(xraw)
    #print(yraw)
    Straightline,I1,I2 = straightline(xraw,yraw)
    #print(Straightline)
    (Fit1, BGND1, Peaks1, Values1,Residuals1) = PeakModel(xraw,yraw,Straightline,I1,I2)
    Fit.append(Fit1)
    BGND.append(BGND1)
    Peaks.append(Peaks1)
    Values.append(Values1)
    Residuals.append(Residuals1)
    t2=time.time()
    Duration = t2-t1
    print('It took {:.2f} seconds to fit all the files with 3 PeakModel iterations'.format(Duration))



centeraverage=[]
for j in range(8):
    centeraverage.append(0)
    #print(centeraverage)
    centerstring='v'+str(j+1)+'_center'
    #print(j)
    #print(centerstring)
    for i in range(len(Values)):
        centeraverage[j]+=Values[i][centerstring]
        #print(i)
        #print(centeraverage)
    centeraverage[j]=centeraverage[j]/(i+1)
    #print(centeraverage)


sigmaaverage=[]
for j in range(8):
    sigmaaverage.append(0)
    print(sigmaaverage)
    sigmastring='v'+str(j+1)+'_sigma'
    print(j)
    print(sigmastring)
    for i in range(len(Values)):
        sigmaaverage[j]+=Values[i][sigmastring]
        print(i)
        print(sigmaaverage)
    sigmaaverage[j]=sigmaaverage[j]/(i+1)
    print(sigmaaverage)    



gammaaverage=[]
for j in range(8):
    gammaaverage.append(0)
    #print(gammaaverage)
    gammastring='v'+str(j+1)+'_gamma'
    #print(j)
    #print(gammastring)
    for i in range(len(Values)):
        gammaaverage[j]+=Values[i][gammastring]
        #print(i)
        #print(gammaaverage)
    gammaaverage[j]=gammaaverage[j]/(i+1)
    print(gammaaverage)




"""#-----------------------------------------------------------Plotting---------------------------------------------------------------------
"""
fig, ((ax1, ax2, ax3,ax4,), (ax5, ax6,ax7,ax8)) = plt.subplots(2,4)  #figsize = (height, width)
fig.suptitle('Fitting steps',fontsize = 14, fontname='Arial')

axes=[ax1,ax2,ax3,ax4,ax5,ax6,ax7]
Peaklabel = ['Ti4+','Ti4+','Ti0', 'Ti0', 'Ti2+', 'Ti2+', 'Ti3+', 'Ti3+']
Colour = ['g--', 'g--','m--','m--','c--','c--','b--', 'b--']

for j in range(8):
    Peakstring='v'+str(j+1)+'_'
    peaklabel=Peaklabel[j]
    colour=Colour[j]
    for i in range(len(Spectra)):
        axes[i].set_xlim(max(xraw),min(xraw))
        axes[i].set_ylim(min(Spectra[i])-1,(np.max(Spectra[i])*1.1))
        axes[i].set_xlabel("Binding Energy (eV)", fontsize = 6, fontname='Arial')
        axes[i].set_ylabel("Intensity (C/s)", fontsize = 6, fontname ='Arial')
        axes[i].set_title(names[i], fontsize = 8)

        axes[i].plot(xraw,Spectra[i], 'bo', label='Raw data', markersize=3)
        axes[i].plot(xraw,BGND[i], 'lime',linestyle='dashed', label='BGND fit', linewidth =2.0)
        axes[i].plot(xraw,Fit[i]+BGND[i],'r-',label='Best fit',linewidth=2.0)
        axes[i].plot(xraw,Peaks[i][Peakstring]+BGND[i], colour, label=peaklabel,linewidth =2.0)

axes[3].legend(fontsize =5,  bbox_to_anchor=(1.05, 1), loc='upper left',frameon=False)


plt.show()
"""#----------------------------------------------------------------------------------------------------------------------------------------
