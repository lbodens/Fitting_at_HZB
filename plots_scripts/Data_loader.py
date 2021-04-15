########################################################################################################################
#                                                                                                                      #
#                   this file is the file which loads the wanted data and saves it into a df "d"                       #
#                                                                                                                      #
########################################################################################################################



import numpy as np
import pandas as pd
from pandas import DataFrame
import glob


def folder_or_file_fkt(Inputs):

    folder_or_file = Inputs["folder_or_file"]

    if folder_or_file.lower() =="file" or folder_or_file.lower() == "files":
        structure_type="file"
        path = Inputs["file_path"]
    if folder_or_file.lower() == "folder":
        structure_type="folder"
        path = Inputs["folder_path"]

    txt_or_dat= Inputs["txt_or_dat"]
    skip_row_nr = Inputs["skip_row_nr"]

    return path, structure_type ,txt_or_dat, skip_row_nr

def BE_or_KE_fkt(Inputs):
    BE_or_KE_check = True
    while BE_or_KE_check:
        choice_input = Inputs["BE_or_KE"]
        if choice_input.lower() == "ke":
            exertation_energy = Inputs["KE_excertation_E"]
            BE_or_KE = "KE"
            BE_or_KE_check = False
            break
        elif choice_input.lower() == "be":
            exertation_energy = 0
            BE_or_KE = "BE"
            BE_or_KE_check = False
            break
    return BE_or_KE, exertation_energy

def energy_test_fkt(d, number_of_spectra):
    dat_E = d["dat_0"]["E"]
    if dat_E[0] > dat_E[len(dat_E) - 1]:
        print("The data energy was decreasing instead of increasing. Therefore the data got swapped\n")
        for i in range(int(number_of_spectra)):
            dat_i = "dat_" + str(i)
            d[dat_i] = d[dat_i][::-1]
            d[dat_i] = d[dat_i].reset_index(drop=True)
    return d

def dat_merger_single_file_fkt(file_path, txt, Inputs, skip_rows, number_of_spectra):
    df = pd.read_csv(file_path + txt, skiprows=skip_rows, delim_whitespace=True, header=None)
    d={}
    BE_or_KE, exertation_energy  = BE_or_KE_fkt(Inputs)
    for i in range(int(number_of_spectra)):
        dat_i = "dat_" + str(i)
        d[dat_i]=pd.DataFrame(columns=["E", "Spectra"])
        if BE_or_KE == "BE":
            d[dat_i]["E"] = df.iloc[:, 0]
        if BE_or_KE == "KE":
            d[dat_i]["E"] = df.iloc[:, 0] - exertation_energy
        d[dat_i]["Spectra"] = df.iloc[:, i+1]

    d = energy_test_fkt(d, number_of_spectra)
    return d

def dat_merger_multiple_files_fkt(folder_path, txt, Inputs, skip_rows, number_of_spectra):
    txt_files = glob.glob(folder_path + "*" + txt)
    BE_or_KE, exertation_energy = BE_or_KE_fkt(Inputs)

    d={}
    for i in range(int(number_of_spectra)):
        df = pd.read_csv(txt_files[i], skiprows=skip_rows, delim_whitespace=True, header=None)
        dat_i = "dat_" + str(i)
        d[dat_i] = pd.DataFrame(columns=["E", "Spectra"])
        if BE_or_KE == "BE":
            d[dat_i]["E"] = df.iloc[:, 0]
        if BE_or_KE == "KE":
            d[dat_i]["E"] = df.iloc[:, 0] - exertation_energy
        d[dat_i]["Spectra"] = df.iloc[:, 1]

    d = energy_test_fkt(d)
    return d


def df_creator_main_fkt(Inputs):
    path, file_type, txt, skip_rows = folder_or_file_fkt(Inputs)
    number_of_spectra = Inputs["number_of_spectra"]

    if file_type == "file":
        d = dat_merger_single_file_fkt(path, txt, Inputs, int(skip_rows), int(number_of_spectra))
    if file_type == "folder":
        d = dat_merger_multiple_files_fkt(path, txt, Inputs, int(skip_rows),int(number_of_spectra))
    return d, number_of_spectra