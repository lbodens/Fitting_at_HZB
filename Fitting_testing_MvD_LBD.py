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
osdirr=[]
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
Directory,NoFiles,filetype,osdirr = directory(Directory,NoFiles,filetype,osdirr)
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------"""


"""--------------------------------------------Reads the files and saves in a dataframe [array of eV & count]-------------------------------------------------"""
filesread=[]
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
filesread = filereader(Directory,filesread,filetype)
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------"""
    
    
    
"""-------------------------------------------------------Saves all the names of the read files ------------------------------------------------------------"""    
names=[]
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
names = filenamer(Directory,osdirr)   
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------"""

"""-------------------------------------------------------Makes eV the index of the arrays------------------------------------------------------------"""   
filesread_eV=[]
def energyscalebasis(filesread):
    filesread_eV=[x.copy() for x in filesread]
    filesread_eV=[x.set_index('eV') for x in filesread_eV]   
    return filesread_eV

filesread_eV = energyscalebasis(filesread)
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------"""

 
"""-------------------------------------------------------Cuts all of the files in the filesread to the same eV range---------------------------------------------"""    
filesread_sameeV=[]
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
filesread_sameeV,eVrange = sameenergyrange(filesread,eVrange)    
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


def dat_merger_single_file_fkt(file_path, skip_rows, number_of_spectra):
    df = pd.read_csv(file_path + txt, skiprows=skip_rows, delim_whitespace=True, header=None)
    df_E=pd.DataFrame(columns=["E"])
    df_S=pd.DataFrame(columns=["Spectra"])
    df_E_hold=pd.DataFrame(columns=["E"])
    df_S_hold=pd.DataFrame(columns=["Spectra"])
    df_E["E"] = df.iloc[:, 0]
    df_S["Spectra"] = df.iloc[:, 1]
    for i in range(1, int(number_of_spectra)):
        df_S_i = pd.DataFrame(columns=["Spectra"])
        df_S_i["Spectra"] = df.iloc[:, i + 1]
        if i == 1:
            df_E_hold["E"] = df_E["E"].append(df_E["E"] + 10000 * i, ignore_index=True)
            df_S_hold["Spectra"] = df_S["Spectra"].append(df_S_i["Spectra"], ignore_index=True)
        else:
            df_E_hold["E"] = df_E_hold["E"].append(df_E["E"] + 10000 * i, ignore_index=True)
            df_S_hold["Spectra"] = df_S_hold["Spectra"].append(df_S_i["Spectra"], ignore_index=True)
    df_total = pd.concat([df_E_hold, df_S_hold], axis=1, names=["E", "Spectra"])
    return df_total


def dat_merger_multiple_files_fkt(folder_path, skip_rows, number_of_spectra):
    txt_files = glob.glob(folder_path + "*" + txt)
    df = pd.read_csv(txt_files[0], skiprows=skip_rows, delim_whitespace=True, header=None)
    df_E=pd.DataFrame(columns=["E"])
    df_S=pd.DataFrame(columns=["Spectra"])
    df_E_hold=pd.DataFrame(columns=["E"])
    df_S_hold=pd.DataFrame(columns=["Spectra"])
    df_E["E"] = df.iloc[:, 0]
    df_S["Spectra"] = df.iloc[:, 1]
    for i in range(1, int(number_of_spectra)):
        df = pd.read_csv(txt_files[i], skiprows=skip_rows, delim_whitespace=True, header=None)
        df_E_i = pd.DataFrame(columns=["E"])
        df_E_i["E"] = df.iloc[:, 0]
        df_S_i = pd.DataFrame(columns=["Spectra"])
        df_S_i["Spectra"] = df.iloc[:, 1]
        if i == 1:
            df_E_hold["E"] = df_E["E"].append(df_E["E"] + 10000 * i, ignore_index=True)
            df_S_hold["Spectra"] = df_S["Spectra"].append(df_S_i["Spectra"], ignore_index=True)
        else:
            df_E_hold["E"] = df_E_hold["E"].append(df_E["E"] + 10000 * i, ignore_index=True)
            df_S_hold["Spectra"] = df_S_hold["Spectra"].append(df_S_i["Spectra"], ignore_index=True)
    df_total = pd.concat([df_E_hold, df_S_hold], axis=1, names=["E", "Spectra"])
    return df_total
"""-----------------------------------------------------------------------------------------------------------------------------------------------------------"""

"""------------------------------------Check, if the input is correct or not/catch it if its wrong ------------------------------------------------------------"""
def correct_input_fkt(Input):                # fkt to check, if the path is correct
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
def shirley_baseline(x,y,I1,I2):
    ''' Function calculates the Shirley background 
    following Bruckner's approach. The background 
    is calculated iteratively and then subtracted from the dataset.'''
    npts=len(y);
    limsy=np.array([I1,I2])
    lowlim = np.min(limsy);
    BGND = np.repeat(lowlim,npts)#inital guess of linear background based on lower limit in y
    SumBGND = np.sum(BGND);
    SumRTF = np.sum(y)
    RangeY = np.diff(list(reversed(limsy)));#print RangeY
    
    maxit = 50 
    err = 1e-6
    if  np.diff(limsy) > 0:
        nloop = 0
        while nloop < maxit:
            nloop = nloop + 1
            for idx in list(reversed(range(npts))):
                #print (npts-idx-1),BGND[npts-idx-1]
                BGND[npts-idx-1] = ((RangeY/(SumRTF-np.sum(BGND)))*
                    (np.sum(y[idx:(npts)]))-np.sum(BGND[idx:(npts)]))+lowlim
                #print BGND[npts-idx-1]
            if (np.abs((np.sum(BGND)-SumBGND)/SumBGND ) < err):
                break
            SumBGND = np.abs(np.sum(BGND))
    else:
        nloop=0
        while nloop < maxit:
            nloop=nloop+1
            for idx in range(npts):
                BGND[idx] = ((RangeY/(SumRTF-np.sum(BGND)))*
                    (np.sum(y[idx:npts])-np.sum(BGND[idx:npts])))+lowlim
            if (np.abs((np.sum(BGND)-SumBGND)/SumBGND ) < err):
                break
            SumBGND = np.abs(np.sum(BGND))

    BGND
    return BGND


def shirley_BG_fkt(i):#,I_low_i,I_high_i):
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


"""----------------------------------------------------------------------------------------------------------------------------------------"""

'''------Cut the upper limit of the data------'''
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx
#limit = find_nearest(eVrange,468)


"""--------------Create linear offset----------------"""
def straightline (x,y):
    #First point
    I1=np.average(y[0:10])  # dx = 0.05--> average over 1 eV
    x1=x[0]
    #End point
    I2=np.average(y[-10:-1]) # dx = 0.1--> average over 1 eV
    x2=x[-1]
    #Straight line approximation
    m=(I1-I2)/(x1-x2)
    c=I1-((I1-I2)/(x1-x2))*x1
    Straightline=m*x+c #array of straight line background approximation
    return (Straightline, I1,I2)
'''---------------------------------------------------------------------------------'''


"""--------------------general commands like: spectra merging & peak types--------------------------""" #TODO putting all of this at a good/practical/reasonable place in the code (like where it really starts and then it calls all the functions)
#taking the wanted spectra and merge them into one long
folder_or_file=folder_or_file()
path = folder_or_file[0]
file_type = folder_or_file[1]
txt=folder_or_file[2]
skip_rows = folder_or_file[3]
number_of_spectra = input("please enter the number of spectra you want to fit\n")
if file_type == "file":
    dat = dat_merger_single_file_fkt(file_path, int(skip_rows), number_of_spectra)
if file_type == "folder":
    dat = dat_merger_multiple_files_fkt(folder_path,int(skip_rows),number_of_spectra)

# creating the vars for I_low & I_high and other boundaries
ymin = 156.9            # TODO change the ymin and x calculations
ymax = 170
if ymin > ymax:
    y_holder = ymin
    ymin = ymax
    ymax = y_holder
xmin = 1191.75
xmax = 1206.75
xraw=dat["E"].to_numpy()

I_low = [0]*number_of_spectra*number_of_peaks
I_high = [0]*number_of_spectra*number_of_peaks
I_low[0] = ymin
I_high[0]= (ymax-ymin)/int(number_of_peaks)+I_low[0]
for i in range(1,int(number_of_peaks*number_of_spectra)):
    I_low[i] = I_high[i-1]
    I_high[i]= (ymax-ymin)/int(number_of_peaks)+I_low[i]



#plotting the first spectra to get better overview
fig, axes = plt.subplots()
axes.plot(dat["E"], dat["Spectra"], 'b')
plt.xlim([xmin, xmax])
print("now a plot of the 1st spectra is shown, that you can quickly look if you want to change some pre set parameters. Close it to continue")
plt.show()
plt.colse()

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

"""---------------creating the wanted nr and type of peaks----------------------"""
Model = []
pars = Parameters()
for j in range(int(number_of_spectra)):
    for i in range(int(number_of_peaks)):
        if peak_type =="Voigt" or peak_type =="voigt":
            Model.append(VoigtModel(prefix='v'+str(j)+'_'+str(i)+'_'))
            pars.update(Model[i+int(number_of_peaks)*j].make_params())
            pars['v'+str(j)+'_'+str(i)+'_amplitude'].set(min=0)
            mod = mod + Model[i+int(number_of_peaks)*j]
        if peak_type =="Gauss":
            Model.append(GaussianModel(prefix='g'+str(j)+'_'+str(i)+'_'))
            pars.update(Model[i+int(number_of_peaks)*j].make_params())
            mod = mod + Model[i+int(number_of_peaks)*j]
        if peak_type =="Lorentz":
            Model.append(LorentzianModel(prefix='l'+str(j)+'_'+str(i)+'_'))
            pars.update(Model[i+int(number_of_peaks)*j].make_params())
            mod = mod + Model[i+int(number_of_peaks)*j]
"""--------------------------------------------------------------------------"""


"""---------------Importing previous parameter file ----------------------"""
# checking for prevoius parameters
prev_params = input("do you have prevoius parameters?")
if prev_params == "yes" or prev_params == "y":
    parameter_file_direc = input("is it in the same directory?")
    if parameter_file_direc == "yes" or parameter_file_direc == "y":
        from parameter_file import *
        parameter_file(pars, number_of_spectra)
    else:
        import sys
        parameter_file_path = input(
            "enter the file path to the parameters (w/o the filename itself but with the \ at the end!)")
        sys.path.insert(1, parameter_file_path)
        from parameter_file import *
        parameter_file(pars, number_of_spectra)
"""-------------------------------------------------------------------------"""


"""------------------fkt to show spectra with init peaks------------------------------------------"""
def choose_spectra_to_plot():
    spectra_to_plot = int(input("please enter the spectra which you want to be shown"))
    return spectra_to_plot


def check_if_peak_inport_is_good():
    check_shown_peak_input = input("Are these init parameters good enough? please enter 'yes'/'y' or 'no'/'n':")
    if check_shown_peak_input == "yes" or check_shown_peak_input == "y":
        check_shown_peak_input = True
        return check_shown_peak_input
    else:
        check_shown_peak_input = False
        return check_shown_peak_input



def plotting(spectra_to_plot,number_of_peaks):
    params_input(1,pars,number_of_spectra)
    print(pars)
    init = mod.eval(pars, x=xraw)
    fig, axes = plt.subplots()
    x = dat["E"].to_numpy()
    yraw = dat["Spectra"].to_numpy()
    axes.plot(x, yraw, 'b')
    axes.plot(x, init, 'k--', label='initial fit')
    plt.xlim([xmin + (int(spectra_to_plot) - 1) * 10000, xmax + (int(spectra_to_plot) - 1) * 10000])
#    comps = init.eval_components(x=x)
#    for i in range(int(number_of_peaks)):
#        axes.plot(x, comps['lin_'], 'k-', label='const component')
#        axes.plot(x, comps['v%s_%s'%(spectra_to_plot-1,number_of_peaks)], 'g--', label='voigt component 1')
#        axes.legend(loc='best')
    plt.show()


def plot_checking():
    spectra_to_plot_bool = False
    are_pre_params_good_bool = False
    spectra_to_plot = choose_spectra_to_plot()
    while spectra_to_plot_bool == False and are_pre_params_good_bool == False:
 #       plotting(spectra_to_plot, number_of_peaks)
 #       plt.close()
        while are_pre_params_good_bool == False:
            params_input(1,pars,number_of_spectra)
            print(pars)
            init = mod.eval(pars, x=xraw)
            plotting(spectra_to_plot, number_of_peaks)
            are_pre_params_good_bool = check_if_peak_inport_is_good()
            if are_pre_params_good_bool == True:
                plt.close()
                continue
            if are_pre_params_good_bool == False:
                plt.close()
                print("Please change the paramter to the desired one")
                continue
        while spectra_to_plot_bool == False:
            other_spectra_check = input("do you want to check other spectra as well?")
            if other_spectra_check == "yes" or other_spectra_check == "y":
                spectra_to_plot = choose_spectra_to_plot()
                spectra_to_plot_bool = False
                are_pre_params_good_bool = False
                break
            if other_spectra_check == "no" or other_spectra_check == "n":
                spectra_to_plot_bool = True
                continue

plot_checking()
"""-------------------------------------------------------------------------"""

"""--------------------------------------actual fitting fkt------------------------------------------------"""

#here the shirley calc for each peac starts
shirley_BG=[[]]

shirley_BG_sum=[0]*len(y)
for i in range(int(number_of_peaks*number_of_spectra)):
    S_BG=shirley_BG_fkt(i)
    I_high[i]=np.sum(S_BG)
    shirley_BG.append(S_BG)
    for j in range(len(y)):
        shirley_BG_sum[j]=shirley_BG_sum[j] + S_BG[j]-I_low[i]

pars["lin_slope"].set(value=0, vary=False)
pars["lin_intercept"].set(value=I_low[0])






















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

