import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
from pandas import DataFrame
import re,os,fnmatch,sys
import lmfit.models
from lmfit import minimize, Parameters
from scipy.optimize import leastsq
import re,os,fnmatch,sys
from tkinter import filedialog
from tkinter import *
import glob
import time
import math





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

#------------------^------------------------------------------
#------------------|------------------------------------------
#------all of this | is more or less the same as this |-------    <-- so which one using? #TODO
#-----------------------------------------------------|-------
#-----------------------------------------------------v-------

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
        for i in range(number_of_spectra):
            d["dat_%i" % i] = d["dat_%i" % i][::-1]
    return d

def dat_merger_single_file_fkt(file_path, skip_rows, number_of_spectra):
    df = pd.read_csv(file_path + txt, skiprows=skip_rows, delim_whitespace=True, header=None)
    d={}
    BE_or_KE, exertation_energy  = BE_or_KE_fkt()

    for i in range(number_of_spectra):
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


def build_curve_from_peaks(n_peaks=1):
    if peak_type == "Voigt":
        peak_func = lmfit.models.VoigtModel
    if peak_type == "Gauss":
        peak_func = lmfit.models.GaussiantModel
    if peak_type == "Lorentz":
        peak_func = lmfit.models.LorentzianModel
    #if peak_type == ???:                       TODO if one want to add one
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



"""------------------fkt to show spectra with init peaks------------------------------------------"""
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

"""-------------------------------------------------------------------------"""



"""--------------------general commands like: spectra merging & peak types--------------------------""" #TODO putting all of this at a good/practical/reasonable place in the code (like where it really starts and then it calls all the functions)
"""#taking the wanted spectra and merge them into one long                      <-- TODO: somehow the append doesn´t work anymore. also the dat needs to be updatet etc. this is the next/last step when going into multiple dimensions
folder_or_file=folder_or_file()
path, file_type, txt, skip_rows= folder_or_file
number_of_spectra = input("please enter the number of spectra you want to fit\n")
if file_type == "file":
    dat = dat_merger_single_file_fkt(file_path, int(skip_rows), number_of_spectra)
if file_type == "folder":
    dat = dat_merger_multiple_files_fkt(folder_path,int(skip_rows),number_of_spectra)"""
skip_rows=1                 # this needs to be deleted later, when the part from above is fixed/updated



dat_input = np.loadtxt("Ni2p_ref_sat_sub.dat", skiprows=skip_rows)                    # TODO just for testing (in 1D)
dat=pd.DataFrame(columns=["E", "Spectra"])

BE_or_KE_output  = False
while BE_or_KE_output  == False:
    BE_or_KE_input = input("Is the following energy scale in binding (BE) or kinetic (KE)? please enter 'BE' for binding or 'KE' for kinetic\n")
    BE_or_KE_output = BE_or_KE_fkt(BE_or_KE_input)
BE_or_KE,exertation_energy = BE_or_KE_output                        # extracting the exceration energy from BE_or_KE_fkt return

if BE_or_KE_input == "BE":                                 #getting the energy from file and calculate the BE, if it was KE
    dat["E"] = dat_input[:, 0]
if BE_or_KE_input == "KE":
    KE = dat_input[:, 0]
    dat = KE - exertation_energy

#swapping data in 1D --> neesds to be done automatically in the function dat_merger_single_file_fkt TODO
dat["Spectra"] = dat_input[:, 2]                    #TODO<<-- will be changed to dat_input[:,1] later for multiple spectra/after testing

if dat["E"][0] > dat["E"][len(df_E) - 1]:
    dat = dat[::-1]
    print("The input data was in decreasing energy. It was swapped for further process")



#plotting the first spectra to get better overview
fig, axes = plt.subplots()
axes.plot(dat["E"], dat["Spectra"], 'b')
plt.xlim([min(x), max(x)])
print("Now a plot of the 1st spectra is shown, that you can quickly look if you want to change some pre set parameters. Close it to continue")
plt.show()
plt.close()





#creating wanted number and types of peaks
number_of_peaks = input("please enter the number of peaks you want to use for fitting\n")
select_peak_type = False
while select_peak_type == False:
    peak_type = input("please enter the type of peak you are using.\n e.G. Voigt, Gauss, Lorentz")
    if peak_type == "Voigt"  or peak_type == "Gauss" or peak_type == "Lorentz":              # TODO: Update to new peaks
        select_peak_type == True
        break
    if peak_type == "voigt":
        peak_type == "Voigt"
        select_peak_type == True
        break
    if peak_type == "gauss":
        peak_type == "Gauss"
        select_peak_type == True
        break
    if peak_type == "lorentz":
        peak_type == "Lorentz"
        select_peak_type == True
        break
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

mod = build_curve_from_peaks(number_of_peaks)
p4fit = mod.make_params()
mod, p4fit=shirley_param_calc(pars)

#plt.plot(x, mod.eval(x=x, params=p4fit), label='start values')
#plt.legend(loc='best')
#plt.show()
plot_checking()



"""--------------------------------------actual fitting fkt------------------------------------------------"""
fit_res = mod.fit(yraw, x=x, params=p4fit, max_nfev=1000)



plt.plot(x, yraw, '.', label='data')
plt.plot(x, fit_res.best_fit, '--', label='fit')
plt.plot(x, mod.eval(x=x, params=p4fit), label='start values')
plt.legend(loc='best')
plt.show()


""" saving output into diff file"""
for p_name, p_value in fit_res.values.items():
    # important, otherwise expr will not work anymore!
    if pars[p_name].vary:
        if p_name not in data_param_file:
            data_param_file[p_name] = {}
            data_param_file[p_name]["value"] = 0
        data_param_file[p_name]["value"] = p_value
param_file_type.dump(data_param_file, open("updated_test_param."+param_file_type_str, "w"))


"""---------------------------untill here the code should work "wuhoooo!!!!"-------------------------""" #TODO the x, xraw, dat["E"]needs to be sortet out!






















def PeakModel (xraw,yraw,Straightline,I1,I2):
    
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

        """--------------calculate the fit for a straight line background----------------"""
        out = mod.fit(yguess, pars,x=xraw)    
        Fit = out.best_fit
        #print('Best fit' + str(Fit))
        comps = out.eval_components(x=xraw)
        Peaks = comps
        Values = out.values
        #print('values' + str(Values))
        """--------------Add straight line back in----------------"""
        Fit_BGND=Fit+BGND
        """--------------calculate shirley background for fitted data----------------"""
        BGND=shirley_baseline(xraw,Fit_BGND,I1,I2)
        #print('Background '+str(BGND))
        """--------------check fit to raw data----------------"""
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
"""------------------------------------------------------------------------------------------------------------------"""


"""-------------------------------updating the parameters in the fits--------------------------------------"""
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
"""------------------------------------------------------------------------------------------------------------------"""


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
    
    
    
"""----------------------------------------------------------------------------------------------------------------------------------------"""
"""-----------------------------------------------------------Plotting---------------------------------------------------------------------"""
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
"""----------------------------------------------------------------------------------------------------------------------------------------"""  




"""-------------------------------------------------Exporting Data-----------------------------------------------------------"""  
Header=['eV', 'raw count', 'Overall fit', 'BGND' 'v1', 'v2', 'v3']

