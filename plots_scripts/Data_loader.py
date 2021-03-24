########################################################################################################################
#                                                                                                                      #
#                   this file is the file which loads the wanted data and saves it into a df "d"                       #
#                                                                                                                      #
########################################################################################################################



import numpy as np
import pandas as pd
from pandas import DataFrame
import glob

def select_txt_or_dat():
    txt_or_dat = input("are you using .txt files or .dat files? Please enter 'txt' or 'dat'\n")
    if txt_or_dat == "txt":
        txt = ".txt"
    if txt_or_dat == "dat":
        txt = ".dat"
    return txt

def folder_or_file_fkt():
    print("Do you want to use a single file with all spectra in one or multiple ones (all files in one folder)?")
    folder_or_file = input("If you want to use a single file please enter 'file'. If you want to use multiple files, please enter 'folder'\n")
    if folder_or_file.lower() =="file" or folder_or_file.lower() == "files":
        type="file"
        file_path = input("Please enter the complete file path (incl the filde_name w/o the .txt/dat\n")
        txt=select_txt_or_dat()
        skip_row_nr = input("Please enter number of rows above incl the heaader line ('E S00 S01' or what ever the header is)\n")
        return file_path, type, txt, skip_row_nr
    if folder_or_file.lower() == "folder":
        type="folder"
        folder_path = input("Please enter the folder path to the files\n")
        txt=select_txt_or_dat()
        skip_row_nr = input("Please enter number of rows above incl the headder line ('# Energy Kinetic' or what ever the header is)\n")
        return folder_path,type,txt, skip_row_nr

def BE_or_KE_fkt():
    BE_or_KE_check = False
    while BE_or_KE_check == False:
        choice_input = input(
            "Is the following energy scale in binding (BE) or kinetic (KE)? please enter 'BE' for binding or 'KE' for kinetic\n")
        if choice_input.lower() == "ke":
            exertation_energy = float(input("Please enter the exertation energy (in eV). like 1486.7\n"))
            BE_or_KE = "KE"
            BE_or_KE_check = True
        elif choice_input.lower() == "be":
            exertation_energy = 0
            BE_or_KE = "BE"
            BE_or_KE_check = True
        else:
            print("\nError, please type in 'BE' or 'KE'\n")
            BE_or_KE_check = False

    return BE_or_KE, exertation_energy

def energy_test_fkt(d, number_of_spectra):
    dat_E = d["dat_0"]["E"]
    if dat_E[0] > dat_E[len(dat_E) - 1]:
        print("The data energy was decreasing instead of increasing. Therefore the data got swapped\n")
        for i in range(int(number_of_spectra)):
            d["dat_%i" % i] = d["dat_%i" % i][::-1]
            d["dat_%i" % i] = d["dat_%i" % i].reset_index(drop=True)
    return d

def dat_merger_single_file_fkt(file_path, skip_rows, number_of_spectra, txt):
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

    d = energy_test_fkt(d, number_of_spectra)
    return d

def dat_merger_multiple_files_fkt(folder_path, skip_rows, number_of_spectra, txt):
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


def df_creator_main_fkt():
    folder_or_file = folder_or_file_fkt()
    path, file_type, txt, skip_rows = folder_or_file

    number_of_spectra = input("please enter the number of spectra you want to fit\n")
    if file_type == "file" :
        d = dat_merger_single_file_fkt(path, int(skip_rows), int(number_of_spectra), txt)
    if file_type == "folder":
        d = dat_merger_multiple_files_fkt(path,int(skip_rows),int(number_of_spectra),txt)
    return d, number_of_spectra