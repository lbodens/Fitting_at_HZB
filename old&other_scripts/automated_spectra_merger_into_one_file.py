# combining of up to 6 diferent elements from single spectra files in one file for each element

# Input
# single files with data columns
#   its necessary, that they have a headder! THe EMIL files are ok and everythign for that is included. for the other more genral ones it´s necessary since there:  the coulmn headder are changed to E, S00, S01 etc..
# different parameters which ara all asked one-by-one

# Output
# single file with all columns according to their "position" with naming of: S00, S01, S02...


###############################
# User packages
#
# used functions
###########################
# import of the other files
#   imput the general file path & name 
#   input what kind of file it is. One @ EMIL or one more general
#   input what type the files are. Do you use txt files or dat files? what type should the output be?
#
##########################
# selecting the right files to combine/spectra
#   at which number does it start
#   at which does it end?
#   input how many different elements do you want to combine?
#   enter the number of rows to skip, which are above the (necessary) header
#
#######################################################
# creating df for different spectra 
#   starting from file number entered before
# changing the header names to right one
#   input new header names, if its not EMIL files
#
##################################################
# adding all columns to data
#   importing files to add automatically by increasing the end value (which is looped over)
#   change the naming of the columns to S00, S01 etc
#   add the new column to existing df
#
############################
# delete 1st row with only "---------" for the EMIL case and all columns which are >q, which are somehow added as well..
#
###########################
# output of data frame


import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


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


def correct_selected_file_fkt(file_name):  # fkt to check, if the path is correct
    print("\nIs this file:")
    print(file_name)
    print("correct? ")
    correct_file_check = input("If yes, please write 'yes'. If not: 'no'.\n")
    if correct_file_check == "yes":
        file_check = True
        return file_name, file_check
    else:
        file_check = False
        return file_check


def correct_input_fkt(Input):  # fkt to check, if the path is correct
    print("\nIs this input:")
    print(Input)
    print("correct? ")
    input_check = input("If yes, please write 'yes'. If not: 'no'.\n")
    if input_check == "yes":
        input_check = True
        return Input, input_check
    else:
        input_check = False
        return input_check


def file_input_fkt(file_path, file_name, type_of_files, counter):
    """ fkt where one can select the file path & name
    if i´t the first time counter ==0, afterwards (the loop section counter ==1)
    in the 2nd part one can choose if he wants to change only the file_name (stay in folder)(0), change the folder (1)
    or both (2)"""

    if counter == 0:
        file_path = input("Please enter your file path in python writing style like d:\\path\\here\\ \n")
        type_of_files = input(
            "please choose the type of files which will be combined. \nIf you want to merge files from the ANA "
            "detector @EMIL (file_name---XX_1_Det[....].txt) please type '1'\n If you want to merge other files of "
            "the type Element_XX.txt please type '2':\n")

        if type_of_files == "1":
            end_string = "_1-Detector_Region"
            mid_string = "--"

        if type_of_files == "2":
            end_string = ""
            mid_string = "_"

        if type_of_files == "1":
            file_name = input(
                "Please enter your file name like 20200101_123456_Name_of_Stuff but w/o the '---' and everything "
                "after it(detector region etc.) \n")
        if type_of_files == "2":
            file_name = input(
                "Please enter your file name like Name-of-stuff but w/o the '_' before the digits\n")

    else:

        if type_of_files == "1":
            end_string = "_1-Detector_Region"
            mid_string = "--"

        if type_of_files == "2":
            end_string = ""
            mid_string = "_"

        folder_or_file = input(
            "Do you want to enter a new file name (0), folder name (1) or both (2)?\n Please enter the corresponding "
            "number):\n")
        if (folder_or_file == "0" or folder_or_file == "1") or folder_or_file == "2":
            check = True
        else:
            check = False

        while not check:
            if (folder_or_file != "0" or folder_or_file != "1") or folder_or_file != "2":
                print("There was an error with the input:", folder_or_file)
                folder_or_file = input("there was an error: please enter 0, 1 or 2")
            if (folder_or_file == "0" or folder_or_file == "1") or folder_or_file == "2":
                check = True

        folder_or_file = int(folder_or_file)

        if folder_or_file == 0:
            if type_of_files == "1":
                file_name = input(
                    "Please enter your file name like 20200101_123456_Name_of_Stuff but w/o the '---' and everything "
                    "after it(detector region etc.) \n")
            if type_of_files == "2":
                file_name = input(
                    "Please enter your file name like Name-of-stuff but w/o the '_' before the digits\n")

        if folder_or_file == 1:
            file_path = input("Please enter your file path in python writing style like d:\\path\\here\\ \n")

        if folder_or_file == 2:
            file_path = input("Please enter your file path in python writing style like d:\\path\\here\\ \n")
            if type_of_files == "1":
                file_name = input(
                    "Please enter your file name like 20200101_123456_Name_of_Stuff but w/o the '---' and everything "
                    "after it(detector region etc.) \n")
            if type_of_files == "2":
                file_name = input(
                    "Please enter your file name like Name-of-stuff but w/o the '_' before the digits\n")

    return (file_path, file_name, type_of_files, mid_string, end_string)


def txt_or_dat_fkt():
    """Input of the input and output file_type"""

    txt_or_dat = input("are you using .txt files or .dat files? Please enter 'txt' or 'dat'\n")
    if txt_or_dat == "txt":
        txt = ".txt"
    if txt_or_dat == "dat":
        txt = ".dat"

    txt_or_dat_output = input(
        "Which filetype should the resulting file have? .txt files or .dat files? Please enter 'txt' or 'dat'\n")
    if txt_or_dat_output == "txt":
        txt_output = ".txt"
    if txt_or_dat_output == "dat":
        txt_output = ".dat"

    return (txt, txt_output)


def regions_fkt():
    """selecting specific parameters for the merging (the file nr to merge, and the naming of the output files)"""

    starting_region = int(input(
        "please enter the starting region, e.g. file_name--XX_1*/file_name_XX. If e.g. a survey was measured it would "
        "be 2 etc.\n"))

    last_file_nr = int(input(
        "please enter the numbers of files which will be combined (last detector region e.g. "
        "file_name--XX_1*/file_name_XX)\n"))

    spectra_nr = int(
        input("please enter the total nr of measured spectra of elements in the loop e.g. O, C & N =3 etc.\n"))

    output = []
    for i in range(int(spectra_nr)):
        output.append("_region_" + str(i) + txt_output)

    spectra_name = []
    # naming the different output files
    print("in the following please enter the name of the element or the wanted name ending of the file.")
    for i in range(int(spectra_nr)):
        spectra_name.append(input("please enter the Element " + str(i + 1) + " e.g. 'Ni' or the name ending of output "
                                                                             "file here: \n"))
        output[i] = "_" + spectra_name[i] + txt_output

    return (starting_region, last_file_nr, spectra_nr, spectra_name, output)


def spec_params():
    """ params of the files (rows above the data and the column used"""

    skip_row_nr = int(input(
        "please enter number of rows above the header line ('# Energy Kinetic' or what ever the header is)\n"))

    column_nr = int(input(
        "please enter the wanted column nr from the files to combine. starting crounting from 1!\n(Normally 2 for "
        "EMIL files. But can be changed for all) \n"))

    return (skip_row_nr, column_nr)


def spectra_merger(file_path, file_name, mid_string, end_string, txt, spectra_nr, skip_row_nr, last_file_nr,
                   starting_region, counter):
    """the 'real' merging fkt.
    1.) creating a list of path´s the same amount of df entries
    2.) adding all columns form the files with the increasing count nr of the file (step calc by the pre-entered params)
    3.) deleting the unnecessary columns which are added for what ever reason
    """

    full_path = []
    for i in range(int(spectra_nr)):
        full_path.append(
            file_path + file_name + mid_string + str(i + int(starting_region)) + end_string + txt)

    col_list = [0, column_nr - 1]
    df = []
    for i in range(int(spectra_nr)):
        df.append(pd.read_csv(full_path[i], skiprows=skip_row_nr, usecols=col_list, delim_whitespace=True,
                              names=["E", "S00"]))

    ###############################################################################################################
    # adding all columns to data
    q = 1  # starting with 1 instead of 0 bc of the already included 1st column in the df in the step above

    q_limit = int((last_file_nr - starting_region) / spectra_nr)  # calculating the last file until that q runs.

    while q <= q_limit:  # going through all files with q = number of loops.
        # renaming the columns to S00, S01 etc
        if q <= 9:
            column_name = "S0" + str(q)
        if q > 9:
            column_name = "S" + str(q)

        # select the new file (with increasing number per loop) which will be added
        for i in range(int(spectra_nr)):
            full_path[i] = file_path + file_name + mid_string + str(
                i + int(spectra_nr) * q + int(starting_region)) + end_string + txt
            # print(full_path)
            df2 = (pd.read_csv(full_path[i], skiprows=skip_row_nr, usecols=col_list, delim_whitespace=True,
                               names=["E", "Spectra"]))
            df_i = df[i]
            df_i[q + 1] = df_i.insert(loc=q + 1, column=column_name, value=df2["Spectra"])

        q += 1

    ############################
    # delete columns which are >q, which are somehow added as well....
    number_of_columns = len(df_i.columns)

    col_nr = q + 1
    while col_nr < number_of_columns:
        for i in range(int(spectra_nr)):
            df_j = df[i]
            df_j.drop(df_j.columns[[q + 1]], axis=1, inplace=True)
        col_nr += 1

    return (df)


def file_output(file_path, file_name, output, df):
    """ fkt for the output saving """

    full_path_output = []
    for i in range(int(spectra_nr)):
        full_path_output = file_path + file_name + output[i]

        df_out = df[i].copy()
        df_out.to_csv(full_path_output, header=True, index=False, sep='\t', mode='w')
    return ()


######################################################################################################
# just to name them once (needed to be able to use the same fkt later in the loop with the params
file_path = ""
file_name = ""
type_of_file = ""
counter = 0

# first time entering all params
file_path, file_name, type_of_file, mid_string, end_string = file_input_fkt(file_path, file_name, type_of_file, counter)
txt, txt_output = txt_or_dat_fkt()
starting_region, last_file_nr, spectra_nr, spectra_name, output = regions_fkt()
skip_row_nr, column_nr = spec_params()


# first time merging & saving the files
if counter == 0:
    df = spectra_merger(file_path, file_name, mid_string, end_string, txt, spectra_nr, skip_row_nr, last_file_nr,
                        starting_region, counter)
    file_output(file_path, file_name, output, df)


# loop if one wants to do it for multiple files in same/diff folder
counter = 1
continue_merging = input("do you want to merge other spectra as well? \n then please enter 'yes/y': \n")

while continue_merging.lower() == "yes" or continue_merging.lower() == "y":
    file_path, file_name, type_of_file, mid_string, end_string = file_input_fkt(file_path, file_name, type_of_file,
                                                                                counter)
    df = spectra_merger(file_path, file_name, mid_string, end_string, txt, spectra_nr, skip_row_nr, last_file_nr,
                        starting_region, counter)
    file_output(file_path, file_name, output, df)

    continue_merging = input("do you want to merge other spectra as well? \n Then please enter 'yes/y' or type 'no/n'")
