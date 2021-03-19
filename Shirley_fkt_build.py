########################################################################################################################
#                                                                                                                      #
#                   in this file the actual peaks + the linked shirley functions are                                   #
#                   generated and returned as a df of models with the naming mod_i_idx                                 #
#                                                                                                                      #
########################################################################################################################




import numpy as np
import lmfit
import lmfit.models

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

def build_curve_from_peaks(i, idx, peak_func, n_spectra=1):
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

def correct_input_fkt(Input):
    print("\nThe input:")
    print(Input)
    print("seem to be incorrect.\nYou seem to have misspelled the type or it is not included.\nPlease try again: ")
    return False




def peak_model_build_main_fkt(d, number_of_spectra):
    # creating wanted number and types of peaks
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

    mod_d = {}
    for idx in range(int(number_of_peaks)):
        for i in range(int(number_of_spectra)):
            mod_d[f'mod{i}_{idx}'] = build_curve_from_peaks(i, idx, peak_func, number_of_spectra)

    return mod_d, number_of_peaks, peak_func