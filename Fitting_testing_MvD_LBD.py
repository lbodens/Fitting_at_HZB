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

"""----------------------------------------------------------------------------------------------------------------------------------------"""


"""-------------------------------------------------------Import the data file------------------------------------------------------------"""
'''------Only when testing the code!!!------'''
#data=pd.read_csv('C://Python scripts/Ti2pAnatase.csv')
#data=pd.read_csv('C://Python scripts/Ti2pNo5.csv')
#data=pd.read_csv('C://Python scripts/Ti2pNo5Spring8.csv')
#Data=pd.DataFrame(data).to_numpy()

#xraw=Data[limit:,0]  #high to low
#yraw=Data[limit:,1]  #high to low

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
        """--------------Define peaks----------------"""
        ''' Ti4+ '''
        Voigt1 = VoigtModel(prefix='v1_')
        pars1 = Voigt1.make_params()
        Voigt2 = VoigtModel(prefix='v2_')
        pars2 = Voigt2.make_params()
        ''' Ti0 '''
        Voigt3 = VoigtModel(prefix='v3_')
        pars3 = Voigt3.make_params()    
        Voigt4 = VoigtModel(prefix='v4_')
        pars4 = Voigt4.make_params()    
        ''' Ti2+ '''
        Voigt5 = VoigtModel(prefix='v5_')
        pars5 = Voigt5.make_params()    
        Voigt6 = VoigtModel(prefix='v6_')
        pars6 = Voigt6.make_params()     
        ''' Ti3+ '''
        Voigt7 = VoigtModel(prefix='v7_')
        pars7 = Voigt7.make_params()    
        Voigt8 = VoigtModel(prefix='v8_')
        pars8 = Voigt8.make_params()     
        
        sigmin=0.5/3.6013
        sigmax=2.5/3.6013
        
        """Modify the inital guessed parameter values"""
        ''' Ti4+ '''
        pars1['v1_amplitude'].set(value=max(yraw), min = 0)      
        pars1['v1_center'].set(value=459, min = 457, max =462)       
        pars1['v1_sigma'].set(value=0.2, min=sigmin, max=sigmax)  #FWHM varies between 0.5 and 2.5       
                
        pars2['v2_amplitude'].set(value=0.45*pars1['v1_amplitude'], min=0.2*pars1['v1_amplitude'], max=0.5*pars1['v1_amplitude']) #
        pars2['v2_center'].set(value=5.72+pars1['v1_center'], vary = False)
        pars2['v2_sigma'].set(value=0.2, min=sigmin, max=sigmax)

                
        ''' Ti0 '''
        pars3['v3_amplitude'].set(value=max(yraw)*0.2, vary=True, min = 0)      
        pars3['v3_center'].set(value=pars1['v1_center']-4.3, vary = False)         
        pars3['v3_sigma'].set(value=0.2, min=sigmin, max=sigmax)
        pars4['v4_amplitude'].set(value=(pars2['v2_amplitude']/pars1['v1_amplitude'])*pars3['v3_amplitude'], vary = False)  
        pars4['v4_center'].set(value=5.72+pars3['v3_center'], vary = False) #min=5.62+pars3['v3_center'], max=5.82+pars3['v3_center']
        pars4['v4_sigma'].set(value=0.2, min=sigmin, max=sigmax)    
        
        
        ''' Ti2+ '''
        pars5['v5_amplitude'].set(value=max(yraw)*0.1, vary=True, min = 0)      
        pars5['v5_center'].set(value=pars1['v1_center']-3, vary = False) #min=pars1['v1_center']-2.9, max=pars1['v1_center']-3.1         
        pars5['v5_sigma'].set(value=pars1['v1_sigma'], min=sigmin, max=sigmax)

        pars6['v6_amplitude'].set(value=(pars2['v2_amplitude']/pars1['v1_amplitude'])*pars5['v5_amplitude'], vary=False)
        pars6['v6_center'].set(value=5.72+pars5['v5_center'], vary = False)  #min=5.62+pars5['v5_center'], max=5.82+pars5['v5_center']
        pars6['v6_sigma'].set(value=pars2['v2_sigma'],min=sigmin, max=sigmax)    

        
        ''' Ti3+ '''
        pars7['v7_amplitude'].set(value=max(yraw)*0.1, vary=True, min = 0)      
        pars7['v7_center'].set(value=pars1['v1_center']-1.8, vary = False) #, min=pars1['v1_center']-1.7, max=pars1['v1_center']-1.9         
        pars7['v7_sigma'].set(value=pars1['v1_sigma'],min=sigmin, max=sigmax)

        pars8['v8_amplitude'].set(value=(pars2['v2_amplitude']/pars1['v1_amplitude'])*pars7['v7_amplitude'], vary = False) 
        pars8['v8_center'].set(value=5.72+pars7['v7_center'], vary = False)  #min=5.62+pars7['v7_center'], max=5.82+pars7['v7_center']
        pars8['v8_sigma'].set(value=pars2['v2_sigma'],min=sigmin, max=sigmax)

        
        pars = pars1 + pars2 + pars3 + pars4 + pars5 + pars6 + pars7 + pars8
        mod = Voigt1 + Voigt2 + Voigt3 + Voigt4 + Voigt5 + Voigt6 + Voigt7 + Voigt8
        #print('Parameters are' +str(pars))
        #print('Model is '+str(mod))
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

