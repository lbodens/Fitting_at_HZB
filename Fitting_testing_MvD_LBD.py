import matplotlib as mpl
import sys
from Data_loader import *
from Shirley_fkt_build import *
from Param_updater import *
from Param_check_via_plotting import *
from Fitting_functions import *
from Plotting_functions import *

namespace = sys._getframe(0).f_globals
plt.style.use('seaborn-ticks')
mpl.rcParams.update({'font.size': 16})



"""-----------------here all the functions from the other files are called and executed-----------------------"""
# loading the data into a df d
d, number_of_spectra = df_creator_main_fkt()

#just to plot once for an overview
plot_1st_spectra_for_overview(d)

# building the Models (peak + shirley) and save it as df
mod_d, number_of_peaks, peak_func = peak_model_build_main_fkt(d, number_of_spectra)

#Importing previous parameter file and check inputs
param_file_type = input("please enter if you are using 'yaml' or 'json':\n")
param_file_name = input("please enter the name of the parameter file:\n")
p4fit, p4fit_s_d, p4fit_p_d = param_updater_main_fkt(d,param_file_type, param_file_name, number_of_spectra, number_of_peaks)


#plot selected spectra with the selected starting parameters, which then can be updated
x = d[f'dat_0']["E"].to_numpy()
y_d, resid = y_for_fit(d, number_of_spectra, number_of_peaks)
pre_param_check = input("Now you can check the pre-set parameters. If you don´t want to do that, enter 'yes'/'y'?")
if pre_param_check.lower() == ("yes" or "y"):
    params_via_plot_checking(x,d, y_d, mod_d,peak_func, param_file_type, param_file_name,number_of_spectra, number_of_peaks)


"""--------------------------------------actual fitting fkt------------------------------------------------"""
nfev = int(input("How many max iterations do you want to use? Please insert a number here:"))
out, out_params,  y_d = fitting_function_main_fkt(d, p4fit, x, mod_d, number_of_spectra, number_of_peaks, nfev)

"""-------------plotting the fitted spectra------------------------------"""


fit_loop = False
while fit_loop == False:
    plotting_subplots_main_fkt(x, out_params, mod_d, y_d, peak_func, d, number_of_spectra, number_of_peaks)
    fit_qualtity_test=input("Is the fit good enough? \nIf yes please enter 'yes'/'y'. if Not enter #/'n':\n")
    if fit_qualtity_test.lower() == ("yes" or "y"):
        fit_loop = True
        break
    if fit_qualtity_test.lower() == ("no" or "n"):
        print("please update the starting parameters then")
        #insert plot per single peaks of coice here TODO
        out, out_params, model_d_fitted, y_d = fitting_function_main_fkt(d, p4fit, x, mod_d, number_of_spectra,
                                                                         number_of_peaks)


"""-------------------------------------------------Exporting Data-----------------------------------------------------------"""

""" saving output into diff file"""
"""data_param_file={}
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
"""









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
