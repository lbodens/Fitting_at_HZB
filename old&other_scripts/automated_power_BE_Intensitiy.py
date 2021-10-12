# plotting time over power over BE

#input:
# sheet with all spectra summed up

#output:
# file with peak BE position & height over Power/time


############################################
#input
#
# input data sheet
# 
#########################################
#calculate
#
# Input power (Watt of XPS gun)
# search for peak (max value)
# get corresponding BE value
# save the peak value in dependence of W*time_frame (input(W)*column_nr) 
# save all data in df with 3 columns (W*time|BE|Intensity)
#
####################################
#output
#  
# save all data in df/plot it




import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


#############################################
# used functions

def correct_selected_path_fkt(path):                # fkt to check, if the path is correct
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

def correct_selected_file_fkt(file_name):                # fkt to check, if the path is correct
    print("\nIs this file:")
    print(file_name)
    print("correct? ")
    correct_file_check = input("If yes, please write 'yes'. If not: 'no'.\n")
    if correct_file_check == "yes":
        file_check = True
        return file_name, file_check
    else: 
        selected_file_check = False
        return file_check

def correct_selected_power_fkt(power):                # fkt to check, if the path is correct
    print("\nIs this Power:")
    print(power)
    print("correct? ")
    correct_power_check = input("If yes, please write 'yes'. If not: 'no'.\n")
    if correct_power_check == "yes":
        power_check = True
        return power_value, power_check
    else: 
        selected_power_check = False
        return power_check

################################################################
# script input

# select file path, with verification, if its the correct one
selected_path_check = False                               
while selected_path_check == False:
    selected_file_path = input("Please enter your file path in python writng style like d:\\\\path\\\\here\\\\")
    selected_path_check = correct_selected_path_fkt(selected_file_path)

selected_file_check = False                               
while selected_file_check == False:
    selected_file_name = input("Please enter your file name like Awesome_data but w/o the '.txt' \nMake sure, that there are no empty columns (nr of filled columns are the same)!\n")
    selected_file_check = correct_selected_file_fkt(selected_file_name)

txt=".txt"
full_path_input=selected_file_path +selected_file_name +txt 
df= pd.read_csv(full_path_input, skiprows=0, delim_whitespace=True) # if different row start: change spciprow nr to correct values

selected_power_check = False                               
while selected_power_check == False:
    selected_power_value = input("Please enter the power of the X-ray source (in Watt)\n")
    selected_power_check = correct_selected_power_fkt(selected_file_value)
power=selected_power_value


################################################################
# find max peak and save in 2nd df

# create 2nd df with first column power*columnnr

df2=pd.DataFrame()
df2["power*time"] = None
df2["BE"] = None
df2["Intensity"] = None


# find peak max and save in df2
i=1
while i < len(df.columns):												#go over all columns in sheet
    max_intensity = float(df.iloc[:, [i]].max())						# find max in each columns  
    j=1
    df_length = df.shape[0] 
    while j < df_length: 												# go over all entries in colum to find teh position of max
        if float(df.iloc[j][i]) ==max_intensity:						# get corresponding BE
            e_to_max_intensity=df["E"][j]								# and save it as value
            break
        else: j +=1
    df2.loc[len(df2.index)] = [float(power) * i, e_to_max_intensity,  max_intensity]  # save all values in df2
    i +=1

#######################################################
# outupt df

output= "_power_BE_intensity_ana.txt"
    
full_path_output =selected_file_path+selected_file_name+output 
    
df2.to_csv(full_path_output, header=True, index=False, sep='\t', mode='w')




