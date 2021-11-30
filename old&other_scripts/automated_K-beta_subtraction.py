# K beta subtraction


# Inputs:
#   1st Spectra (which is the source of the peak)   (BE in x.05, x.15, x.25 ... steps)
#   2nd spectra (from which the peak should be subtracted) (BE in x.05, x.15, x.25 ... steps))
#   K_beta peak spectra (use file in this folder).  I´ll also include the peak parameters for Origin, that one can calculate the peak them self, if they have different step sizes. If you do, make sure, they have only 2 decimal digits and are the same step sizes
#   if its a singulet or doublet. IF the latter: get a point inbetween the doublets to get the peak max of both for calculations 

# output:
# K_beta spectra for each spectra/column
# 2nd spectra - k_beta spectra


##############################################
# used packages
#
# used fkt´s
#
########################
# script input
#
# read in command line parameters:
# path input from data files
#
###############################################
# getting right K-Beta values
#
# take 1st spectra
#   split in two (3/2 and 1/2 peaks)
#       set the BE as value BE_cut
#       do everything for both halves
#   get the peak height (max_x_2 = df.max)
#   get peak position
#   get minimum of spectra 
#       set specific BE from where taken ?
#   get real peak intensity I_X/2 by subtracting min from max
#
########################
# take K_beta file
#   multiply height with I_X/2
#   move peak to right position (+69.7 eV)
#       use same BE boundaries as 2nd spectra        
#   do it for both and add both in one spectra
#
########################
# take 2nd spectra
#   find same Be of K-Beta peak in 2nd spectra
#   subtract K-Beta peak from 2nd
# 
########################
# output
# 
# K-Beta spectra
# 2nd-K_beta spectra


import pandas as pd
import numpy as np
import math


def correct_selected_path_fkt(path):  # fkt to check, if the path is correct
    print("\nIs this path:")
    print(path)
    print("correct? ")
    correct_path_check = input("If yes, please write 'yes'. If not: 'no'.\n")
    if correct_path_check == "yes":
        path_check = True
        return path, path_check
    else:
        path_check = False
        return path_check


def correct_selected_file_fkt(file_name):  # fkt to check, if the file name is correct
    print("\nIs this file:")
    print(file_name)
    print("correct? ")
    correct_file_check = input("If yes, please write 'yes'. If not: 'no'.\n")
    if correct_file_check == "yes":
        file_check = True
        return file_name, file_check
    else:
        selected_file_check = False
        return selected_file_check


def correct_selected_peak_nr_fkt(peaknr_name):  # fkt to check, if the file name is correct
    if peaknr_name == "double" or peaknr_name == "single":
        selected_peaknr_check = True
        return selected_peaknr_check
    else:
        print("error. please enter the right input")
        selected_peaknr_check = False
        return selected_peaknr_check


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


################################################################
# script input

# select file path, with verification, if its the correct one
# selected_path_check = False
# while selected_path_check == False:
selected_file_path_1st = input(
    "Please enter your file path for 1st Spectra (source of the peak) in python writing style like "
    "d:\\\\path\\\\here\\\\")
##    selected_path_check = correct_selected_path_fkt(selected_file_path_1st)

# selected_file_check = False
# while selected_file_check == False:
selected_file_name_1st = input(
    "Please enter your file name of 1st Spectra (source of the peak) but w/o the '.txt' "
    "\nMake sure, that there are no empty columns (nr of filled columns are the same)!\n")
#    selected_file_check = correct_selected_file_fkt(selected_file_name_1st)

# selected_path_check = False
# while selected_path_check == False:
selected_file_path_Kb = input(
    "Please enter your file path for K_beta Spectra in python writing style like d:\\\\path\\\\here\\\\")
#    selected_path_check = correct_selected_path_fkt(selected_file_path_Kb)

# selected_file_check = False
# while selected_file_check == False:
selected_file_name_Kb = input(
    "Please enter your file name of K_beta Spectra but w/o the '.txt' "
    "\nMake sure, that there are no empty columns (nr of filled columns are the same)!\n")
#    selected_file_check = correct_selected_file_fkt(selected_file_name_Kb)

# selected_path_check = False
# while selected_path_check == False:
selected_file_path_2nd = input(
    "Please enter your file path for 2nd Spectra (from which the peak gets subtracted) in python writing "
    "style like d:\\\\path\\\\here\\\\")
#    selected_path_check = correct_selected_path_fkt(selected_file_path_2nd)

# selected_file_check = False
# while selected_file_check == False:
selected_file_name_2nd = input(
    "Please enter your file name of 2nd Spectra (from which the peak gets subtracted) but w/o the '.txt' "
    "\nMake sure, that there are no empty columns (nr of filled columns are the same)!\n")
#    selected_file_check = correct_selected_file_fkt(selected_file_name_2nd)

txt_or_dat = input("are you using .txt files or .dat files? Please enter 'txt' or 'dat'")
#   select_txt_or_dat = correct_input_fkt(txt_or_dat)

if txt_or_dat == "txt":
    txt = ".txt"
if txt_or_dat == "dat":
    txt = ".dat"

full_path_input_1st = selected_file_path_1st + selected_file_name_1st + txt
df_1st = pd.read_csv(full_path_input_1st, skiprows=0,
                     delim_whitespace=True)  # if different row start: change skiprow nr to correct values

full_path_input_Kb = selected_file_path_Kb + selected_file_name_Kb + ".txt"
df_Kb = pd.read_csv(full_path_input_Kb, skiprows=0,
                    delim_whitespace=True)  # if different row start: change skiprow nr to correct values

full_path_input_2nd = selected_file_path_2nd + selected_file_name_2nd + txt
df_2nd = pd.read_csv(full_path_input_2nd, skiprows=0,
                     delim_whitespace=True)  # if different row start: change skiprow nr to correct values

selected_peaknr_check = False
while selected_peaknr_check == False:
    peak_nr_1st = input("please enter if the 1st spectra is a doublet or singlet. "
                        "If doublett, enter 'double' if singulet : 'single':\n")
    selected_peaknr_check = correct_selected_peak_nr_fkt(peak_nr_1st)
################################################
# getting right K-Beta values

########################
# small works with df_kb

# turn "E"around, to match the E directuion of other spectra aswell
df_Kb["E"] = -df_Kb["E"]

# cut Kb[E] to decimal with only 2 decimal digits (0.xx)
i = 0
while i < df_Kb.shape[0]:
    df_Kb["E"][i] = round_up(df_Kb["E"][i], 2)
    i += 1

# flipping Kbeta spectra around, that highest value is on top of list
df_Kb_length = df_Kb.shape[0]  # getting length (nr of rows) of data frame ([1] would be nr of columns)
if df_Kb["E"][0] < df_Kb["E"][df_Kb_length - 1]:
    df_Kb = df_Kb.iloc[::-1]

# find peak of Kbeta and save position of it   
df_Kb_length = df_Kb.shape[0]
max_intensity_Kb = float(df_Kb.iloc[:, [1]].max())
m = 1
while m < df_Kb_length:  # go over all entries in column to find the position of max
    if float(df_Kb.iloc[m][1]) == max_intensity_Kb:  # get corresponding BE
        e_to_max_intensity_Kb = df_Kb.iloc[m][0]  # and save it as value
        m_Kb = m
        break
    else:
        m += 1

# global df, with which are worked in the loop, but should not be recreated/overridden every time
df_Kb_2nd_E_shift = df_2nd.copy()
df_2nd_Kb_subtr = df_2nd.copy()


# getting the position between the doublet, that the script later can find both peak positions
if peak_nr_1st == "double":
    # getting max of peaks and min of spectra to calculate actual peak height
    df_1st_length = df_1st.shape[0]

    # set the regions at which the peak max is looked for
    boundary_energy = input(
        "please enter the boundary which is between both peaks in eV with XX.X5 (to make sure its in the file)\n")
    w = 0
    while w < df_1st_length:  # go over all entries in column to find the position of max
        if float(df_1st.iloc[w][0]) == float(boundary_energy):  # get corresponding BE
            boundary_position = w
            break
        else:
            w += 1


###################################################################
# looping over all spectra
i = 1
while i < (len(df_1st.columns) - 1):  # go over all columns in sheet
    if i <= 9:
        column_name = "S0" + str(i)
    if i > 9:
        column_name = "S" + str(i)

    ##############################
    # working with 1st
    if peak_nr_1st == "double":

        max_intensity_1_2 = float(
            df_1st.iloc[1:int(boundary_position), [i]].max())  # find max in each columns for 1st 1/2
        max_intensity_3_2 = float(
            df_1st.iloc[int(boundary_position):int(df_1st_length), [i]].max())  # find max in each columns for 1st 3/2
        min_intensity = float(df_1st.iloc[:, [i]].min())  # find min in each columns For 1st
        intensity_3_2 = max_intensity_3_2 - min_intensity
        intensity_1_2 = intensity_3_2 / 2  # max_intensity_1_2 - min_intensity         <-------------------- what is rigth intensity cal1stlation?

        # get position of max peaks of 1st
        n = 1  # var to get position of peaks in 1st spectra
        while n < df_1st_length:  # go over all entries in column to find teh position of max
            if float(df_1st.iloc[n][i]) == max_intensity_1_2:  # get corresponding BE
                e_to_max_intensity_1_2 = df_1st.iloc[n][0]  # and save it as value
                n_1_2 = n
                n += 1  # go over all entries in column to find teh position of max
            if float(df_1st.iloc[n][i]) == max_intensity_3_2:  # get corresponding BE
                e_to_max_intensity_3_2 = df_1st.iloc[n][0]  # and save it as value
                n_3_2 = n
                n += 1
            else:
                n += 1

    if peak_nr_1st == "single":
        # getting max of peaks and min of spectra to calculate actual peak height
        df_1st_length = df_1st.shape[0]
        max_intensity = float(df_1st.iloc[1:int(df_1st_length), [i]].max())  # find max in each columns for 1st 1/2
        min_intensity = float(df_1st.iloc[:, [i]].min())  # find min in each columns For 1st
        intensity = max_intensity - min_intensity

        # get position of max peaks of 1st
        n = 1  # var to get position of peaks in 1st spectra
        while n < df_1st_length:  # go over all entries in column to find teh position of max
            if float(df_1st.iloc[n][i]) == max_intensity:  # get corresponding BE
                e_to_max_intensity = df_1st.iloc[n][0]  # and save it as value
                break  # go over all entries in column to find teh position of max
            else:
                n += 1
    ##################################
    # working with K-beta spectrum    

    df_Kb_1_2 = df_Kb.copy()
    df_Kb_3_2 = df_Kb.copy()
    df_Kb_combined = df_Kb.copy()

    if peak_nr_1st == "double":
        # calculate the amount to shift (x) the Kbeta spectra with for each peak and shift it
        x_1_2 = n_1_2 - m_Kb
        x_3_2 = n_3_2 - m_Kb

        df_Kb_3_2 = df_Kb_3_2.shift(x_3_2, axis=0)
        df_Kb_1_2 = df_Kb_1_2.shift(x_1_2, axis=0)

        # calculate the correct intensities for each peak
        df_Kb_1_2["K_beta"] = df_Kb_1_2["K_beta"] * intensity_1_2
        df_Kb_3_2["K_beta"] = df_Kb_3_2["K_beta"] * intensity_3_2

        # combine both in one spectra
        df_Kb_combined["K_beta"] = df_Kb_1_2["K_beta"].add(df_Kb_3_2["K_beta"], fill_value=0)

        # shift new df to the 2nd energies
        df_Kb_combined_shifted = df_Kb_combined.copy()
        df_Kb_combined_shifted["E"] = df_1st["E"] + e_to_max_intensity_Kb

    if peak_nr_1st == "single":
        # calculate the amount to shift (x) the Kbeta spectra with for each peak and shift it
        x = n - m_Kb

        df_Kb = df_Kb.shift(x, axis=0)

        # calculate the correct intensities for each peak
        df_Kb_combined["K_beta"] = df_Kb["K_beta"] * intensity

        # shift new df to the 2nd energies
        df_Kb_combined_shifted = df_Kb_combined.copy()
        df_Kb_combined_shifted["E"] = df_1st["E"] + e_to_max_intensity_Kb

        ################################
    # working with 2nd spectrum
    # get the BE value of the 2nd spectra, to calculate the amount, at which the Kb later will be shifted (y_2nd)
    e_max_2nd = df_2nd.iloc[0][0]

    j = 1
    while j < df_Kb_length:  # go over all entries in column to find the position of max
        if float(df_Kb_combined_shifted.iloc[j][0]) == e_max_2nd:  # get position of corresponding E
            y_2nd = j  # save position of it
            break
        else:
            j += 1

    # shift the K-beta spectra to the right position, that they are aligned with the right BE of the 2nd spectra
    df_Kb_combined_2nd = df_Kb_combined_shifted.shift(-y_2nd, axis=0)

    # save k_beta and the difference of 2nd-K-Beta for each spectra in df
    df_2nd_Kb_subtr[column_name] = df_2nd[column_name].subtract(df_Kb_combined_2nd["K_beta"], fill_value=0)
    df_Kb_2nd_E_shift[column_name] = df_Kb_combined_2nd["K_beta"]

    i += 1

output_2nd_Kb = "_2nd-Kbeta_subtr.txt"
output_Kb_2nd_E = "_Kbeta_for_2nd_E.txt"

full_path_output_2nd_Kb = selected_file_path_2nd + selected_file_name_2nd + output_2nd_Kb
full_path_output_Kb_2nd_E = selected_file_path_2nd + selected_file_name_2nd + output_Kb_2nd_E

df_2nd_Kb_subtr.to_csv(full_path_output_2nd_Kb, header=True, index=False, sep='\t', mode='w')
df_Kb_2nd_E_shift.to_csv(full_path_output_Kb_2nd_E, header=True, index=False, sep='\t', mode='w')
