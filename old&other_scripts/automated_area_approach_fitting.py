# fast scan of spectra

# inputs
#file : input file

#output
# plot of plot
# matrix with all integrated values
# file with lin BG

#####################################################################################################################
#                                                                                                                   #
#                                               IMPORTANT                                                           #
#                                                                                                                   #
# what you need: the file has to be in the following style                                                          #
# (with 'E' as the Energy (doesnt matter if KE or BE) name and the single spectra with the names 'S00' etc.):       #
#                                                                                                                   #
#   E        S00       S01       S02       S03       S04       ...                                                  #
# 969.95  1391.5362 1664.0262 1719.9869 1670.4967 1687.8547    ...                                                  #
# 969.85  1398.9735 1677.9272 1708.2657 1678.4641 1654.1115    ...                                                  #
#####################################################################################################################

##############################################
# used packages
#
# used fkt´s
#
################################
# script input
#
# read in command line parameters:
# path input from data file
# choose, if you want to do the plotting or create the matrix
# Is the Energy in kinetic or binding energy
#   1st: check, if the following energy is in kinetic (KE) or binding (BE) energy.
#   2nd: If necessary Be will be calculated  
#   3rd: if the BE energy in the file starts with the higher number, the df gets flipped
# 
##############################
# plot the plot
#
#   select x values
#   select y values from data's X´s column
#   use this data to plot line plot
#   calculate y values for 2nd line
#   add 2nd data (line)
#   plot plot
#   check if plot is specifiet. If plot = true, terminate program, else calculate matrix
# 
##########################
# calculate matrix
# 
#   create result array /open already existing one
#   for every column do:
#       give boundaries for lin bg
#       calculate lin BG
#       give in right boundaries for integration
#       subtract from curve
#       integrate
#       integrate
#       add value to result array
#   
#   output matrix to file (first flat file, structure later)


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
    if correct_path_check.lower() == "yes" or correct_path_check.lower() == "y":
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
    if correct_file_check == "yes" or correct_file_check == "y":
        file_check = True
        return file_name, file_check
    else: 
        selected_file_check = False
        return file_check


def choice_fkt(choice_input):                       # function to get the possibilities for the follwoing question do you want to:
    if choice_input == "yes" or choice_input == "y":                       # do the 1st part of the script (plotting and selectring the regions)
        plot_matrix_choice = True
        return plot_matrix_choice
    if choice_input == "no" or choice_input == "n":                        # create the Martix
        plot_matrix_choice = True
        return plot_matrix_choice
    else:                                           # if you made a spelling mistake
        print("\nError, please type in 'yes' or 'no'\n") 
        plot_matrix_choice = False
        return plot_matrix_choice


def BE_or_KE_fkt(choice_input):                     # fkt to see if its in BE or KE and to get the necessary values (exertation energy)
    if choice_input == "KE":
        exertation_energy = input("please enter the exertation energy (in eV). like 1486.7\n")
        exertation_energy = float(exertation_energy)                    # changing the input (string) to a number (float)
        BE_or_KE = "KE"
        return BE_or_KE, exertation_energy
    if choice_input == "BE":
        exertation_energy = 0
        BE_or_KE = "BE"
        return BE_or_KE, exertation_energy
    else:
        print("\nError, please type in 'BE' or 'KE'\n") 
        BE_or_KE = False
        exertation_energy = 0
        return BE_or_KE, exertation_energy


def energy_range_limits_fit_fkt(limit):                 #fkt to get the upper and lower limits for the lin fit aswell as for the integration
    i = 0
    for i in range(df_length): 
        if df["E"][i] == float(limit):              # see at which i the choosen limit energy is same as the the onein the file
            fit_E = df["E"][i]                      # save the choosen values
            fit_spectra = spectra[i]                # as well as the corresponding specctra value       
            print("The Energy value is: ",fit_E, "eV, and the spectra value is: ", fit_spectra)
            correct_range = True
            return correct_range, fit_E, fit_spectra, i
        if i == df_length-1:
            print("The chosen energy was not in the list. Make sure, to use the same step ticks like 123.45 eV")
            correct_range = False
            return correct_range
        else: 
            i += 1


def energy_range_limits_int_fkt(limit, wanted_spectra):                 #fkt to get the upper and lower limits for the lin fit aswell as for the integration
    i = 0
    for i in range(df_length): 
        if df["E"][i] == float(limit):              # see at which i the choosen limit energy is same as the the one in the file
            fit_E = df["E"][i]                      # save the choosen values
            fit_spectra = df.iloc[df_length-1-i][wanted_spectra]                # as well as the corresponding specctra value. here it´s important to do the df_length -1-i, since iloc doesn´t use the actual postion but takes the nr written on the far left, when printing the df. (orig i before the flip)      
            print("For spectra Nr:", wanted_spectra, "the energy value is: ", fit_E, "eV, and the spectra value is: ", fit_spectra)
            correct_range = True
            return correct_range, fit_E, fit_spectra, i
        if i == df_length-1:
            print("The chosen energy was not in the list. Make sure, to use the same step ticks like 123.45 eV")
            correct_range = False
            return correct_range
        else: 
            i += 1


def lin_BG_fit_fkt(value):                              # fkt to calculate the lin BG
    m = (fit_upper_E_spectra - fit_lower_E_spectra)//(fit_upper_E - fit_lower_E)
    y_lin_BG = m*(value - fit_lower_E) + fit_lower_E_spectra 
    print("The function is: y=", m, "*(x -", fit_lower_E, ") +", fit_lower_E_spectra)
    return y_lin_BG


def lin_BG_int_fkt():                              # fkt to calculate the lin BG
    j = 1                                                 # looping over columns(spectras). Starting with 1 since 0 is "E"
    while j <= spectra_nr:
        i = 0
        correct_range_low = energy_range_limits_int_fkt(fit_lower_E_input, j)
        fit_lower_E = correct_range_low[1]                                        # to get the E value
        fit_lower_E_spectra = correct_range_low[2]                              # to get the actual spectra value
        int_lower_E_position = correct_range_low[3]
        
        correct_range_up = energy_range_limits_int_fkt(fit_upper_E_input, j)
        fit_upper_E = correct_range_up[1]
        fit_upper_E_spectra = correct_range_up[2]
        int_upper_E_position = correct_range_up[3]
        
        while i <= df_length-1:
           
            energy_position=df["E"][i]                                                 # getting energy position (from back to front)?????
            m = (fit_upper_E_spectra - fit_lower_E_spectra)//(fit_upper_E - fit_lower_E)                   # with m= (\delta y)/(\delta x) = (y1-y2)(x1-x2)
            y_lin_BG = m*(energy_position - fit_lower_E) + fit_lower_E_spectra 
            df2.iat[df_length-1-i, j] = y_lin_BG                    # sama eas with the range_limit_int_fkt. iat uses not the actual position in the df but uses the i value before the flip (row 224 at this point of coding) (which flips aswell)
            i += 1
        j += 1
    return y_lin_BG, int_lower_E_position, int_upper_E_position


def integration_fkt(df, int_lower_E_position, int_upper_E_position):
    # getting the positions of the lower and higher integrations
    m = df_length-1-int_lower_E_position
    n = df_length-1-int_upper_E_position
    if m > n: # swap the boundaries value, and continue the run
        m, n = n, m
        print("The boundaries where the wrong order and were swaped")
    l = m-1        # this is only possible, if the lower boundary is not the first value
    o = n
    j = 1
    df_sum = [0.0]*spectra_nr
    # for i in raange(spectra_nr):

    while j <= spectra_nr:
        while m <= n:
            df.iat[m, j] = df.iat[m, j]+df.iat[l, j]
            l += 1
            m += 1
            if m == n:
                print("The integral for spectra", j, "=", df.iat[int_lower_E_position, j])
                df_sum[0, j] = df.iat[n, j]
        j += 1
    return df, df_sum


################################################################
# script input

# select file path, with verification, if its the correct one
selected_path_check = False
while selected_path_check == False:
    selected_file_path = input("Please enter your file path in python writng style like d:\\\\path\\\\here\\\\ \n")
    selected_path_check = correct_selected_path_fkt(selected_file_path)

selected_file_check = False                               
while selected_file_check == False:
    selected_file_name = input("Please enter your file name like Awesome_data but w/o the '.txt' \nMake sure, that there are no empty columns (nr of filled columns are the same)!\n")
    selected_file_check = correct_selected_file_fkt(selected_file_name)

txt = ".txt"
full_path_input = selected_file_path +selected_file_name +txt
df = pd.read_csv(full_path_input, skiprows=0, delim_whitespace=True) # if different row start: change spciprow nr to correct values



# choose, if you want to do the plotting or matrix stuff
plot_matrix_choice = False
while plot_matrix_choice == False:                              
    plot_or_calculation = input("\nDo you want to show the plots & select the ranges for calculations type: 'yes'. \nIf not and you want to create the measuremnt matrix type: 'no'. \n")
    plot_or_calculation_continue = 'no'                      # default to make sure, taht you can enter the values later. if you want to continue later, you can enter it here
    plot_matrix_choice = choice_fkt(plot_or_calculation)



# Working with the Energy column.
#   1st: check, if the following energy is in kinetic (KE) or binding (BE) energy.
#   2nd: If necessary Be will be calculated  
#   3rd: if the BE energy in the file starts with the higher number, the df gets flipped
BE_or_KE = False                                      
while BE_or_KE == False:
    BE_or_KE_input = input("Is the following energy scale in binding (BE) or kinetic (KE)? "
                           "Please enter 'BE' for binding or 'KE' for kinetic\n")
    BE_or_KE = BE_or_KE_fkt(BE_or_KE_input)
exertation_energy = BE_or_KE[1]                            # extracting the exceration energy from BE_or_KE_fkt return
BE_or_KE = BE_or_KE[0]                                     # extracting the fact, if its KE or BE from BE_or_KE_fkt return

if BE_or_KE_input == "BE":                                 # getting the energy from file and calculate the BE, if it was KE
    BE = df["E"]
if BE_or_KE_input == "KE":
    KE = df["E"]
    BE = KE - exertation_energy
df["E"] = BE
x = df["E"]                                                  # for the functions later

df_length = df.shape[0]                     # getting lenght (nr of rows) of data frame ([1] would be nr of columns)
i = 0
if df["E"][i] > df["E"][df_length-1]:
    df = df.iloc[::-1]

# coppy df to createa a df for each task itself
df2 = df.copy()                                                       # copy df to get 2nd one for all lin BG fkt
df3 = df.copy()                                                       # copy df to get 3rd one for all df - lin fkt
df4 = df.copy()                                                       # copy df to get 4th one for all sum of df3 cells

# getting the number of samples is necessary for the loop over all columns later
spectra_nr = int(input("How many spectra (columns, energy not inlcuded) are in the file?\n"))

#################################################################
# plot the plot

if plot_or_calculation == "yes" or plot_or_calculation == "y":
    
    # choose the wanted column
    wanted_spectra = input("Please enter the wanted spectra in the style: 1st: 'S00:, 2nd: 'S01' 3rd: 'S03' etc.")
    spectra = df[wanted_spectra]

    # plot the spectra
    axs = plt.axes()
    fig = plt.gcf()                                                                     
    sns.lineplot(x="E", y=wanted_spectra, data=df, color='black', marker='s', mec='black', linestyle='solid') 
 
    plt.xlim(max(df["E"]), min(df["E"]))                                                                 #reverse the x axis
    plt.xticks(np.arange(int(min(df["E"])), int(max(df["E"])), 5))                                        #set x axis tick step size to 5 (according to E min and max)
    fig.set_size_inches(15, 10)                                                                         # increase fig size so its better to read
    plt.show()



    #coose the lower and upper fit range
    correct_range=False
    while correct_range == False:
        fit_lower_E_input = input("Please enter the lower energy range for the linear fit in eV\n")
        #    fit_lower_E_input = float(fit_E_input)
        correct_range = energy_range_limits_fit_fkt(fit_lower_E_input)

    fit_lower_E=correct_range[1]                                        # to get the E value
    fit_lower_E_spectra = correct_range[2]                              # to get the actual spectra value
    fit_lower_E_position = correct_range[3]                             # to get the potisition i in the file
      
    correct_range=False
    while correct_range == False:
        fit_upper_E_input = input("Please enter the upper energy range for the linear fit in eV\n")
        #    fit_lower_E_input = float(fit_E_input)
        correct_range = energy_range_limits_fit_fkt(fit_upper_E_input)

    fit_upper_E = correct_range[1]
    fit_upper_E_spectra = correct_range[2]
    fit_upper_E_position = correct_range[3]

    # calculate the lin fkt
    y_lin_BG = lin_BG_fit_fkt(x)

    # plot the function
#    axs = plt.axes()
#    fig = plt.gcf()
    sns.lineplot(x="E", y=wanted_spectra, data=df, color='black', marker='s', mec='black', linestyle='solid')  
    sns.lineplot(x="E", y=y_lin_BG, data=df2, color='blue')
    fig.set_size_inches(15, 10)    
    plt.xlim(max(df["E"]), min(df["E"]))
    plt.xticks(np.arange(int(min(df["E"])), int(max(df["E"])), 5))
    plt.show()

    # choose the integration range and check, if its the correct one
    int_range = False                                           # to check, if the wanted boundaries the same as before
    while int_range == False:                              
        print("Are the integration limits the same as the chosen ones:", fit_lower_E, "eV & ", fit_upper_E, "eV?\n ")
        int_range_input = input("If yes, please type 'yes'. If not: 'no'\n")
        if int_range_input != 'yes' and int_range_input != 'no':
            print("\nError, please type in 'yes' or 'no'\n")             
            int_range= False 
        if int_range_input == "yes" or int_range_input == "y":
            int_lower_E = fit_lower_E
            int_upper_E = fit_upper_E
            int_lower_E_spectra = fit_lower_E_spectra
            int_upper_E_spectra = fit_upper_E_spectra
            int_range= True

        if int_range_input == "no" or int_range_input == "n":
            # to check if, after this run, the boundaries are good enough
            correct_int_range = False                                               
            while correct_int_range == False:
                
                # to enter the new boundaries
                correct_range = False
                while correct_range == False:
                    int_lower_E_input = input("Please enter the lower energy range for integration eV. \nPlease make sure, that it is not the first(lowest) number in the file! If so, the programm will crash later by calculating the integral\n")
                    correct_range = energy_range_limits_fit_fkt(int_lower_E_input)
            
                int_lower_E=correct_range[1]                                        # to get the E value
                int_lower_E_spectra = correct_range[2]                              # to get the actual spectra value
                int_lower_E_position = correct_range[3]                             # to get the position i in the file
                
                correct_range = False
                while correct_range == False:
                    int_upper_E_input = input("Please enter the upper energy range for integration in eV\n")
                    correct_range = energy_range_limits_fit_fkt(int_upper_E_input)
            
                int_upper_E=correct_range[1]
                int_upper_E_spectra = correct_range[2]
                int_upper_E_position = correct_range[3]
            
                int_range = True

                # plot the function with integral boundaries area
                fig = plt.gcf()
                sns.lineplot(x="E", y=wanted_spectra, data=df, color='black', marker='s', mec='black', linestyle='solid', label='Data')  
                sns.lineplot(x="E", y=wanted_spectra, data=df2, color='blue', label='lin BG of ')#{}'.wanted_spectra)   
            
                plt.axvline(x=fit_lower_E, label='lower E range for fit', color='blue')
                plt.axvline(x=fit_upper_E, label='upper E range for fit', color='blue')
                plt.axvline(x=int_lower_E, label='lower E range for int', color='red')
                plt.axvline(x=int_upper_E, label='upper E range for int', color='red')
                
                fig.set_size_inches(15, 10)    
                plt.xlim(max(df["E"]), min(df["E"]))
                plt.xticks(np.arange(int(min(df["E"])), int(max(df["E"])), 5))
                plt.show()

                # 2n pard of the check, if boundaries are ok
                correct_int_range_input_error = False                                               
                while correct_int_range_input_error == False:
                    print("Are", int_lower_E, "eV &", int_upper_E, "eV the right integration boundaries? \n")
                    correct_int_range_input = input("If yes: type 'yes'. If not 'no'\n")
                    if correct_int_range_input != 'yes' and correct_int_range_input != 'no':
                        print("\nError, please type in 'yes' or 'no'\n")
                        correct_int_range = False
                        correct_int_range_input_error = False   
                    if correct_int_range_input == 'yes':
                        correct_int_range = True
                        correct_int_range_input_error = True
                        break
                    if correct_int_range_input == 'no':
                        correct_int_range = False
                        correct_int_range_input_error = True


    #end of plotting programm
    plot_or_calculation_continue = input("do you want to continue? if yes: enter 'yes'. if you want to continue enter 'no'")

    if plot_or_calculation_continue == 'yes':
        plot_or_calculation = 'no'                   # to swap the result and continue with the script


    if plot_or_calculation_continue == 'no':                  # to terminate the program
        quit()






##############################################################################
# calculate the matrix

if plot_or_calculation == 'no':
    
    #enter the fit & int range again. if yes, the fit & int boundaries from above will be used automaticaly
    if plot_or_calculation_continue !='yes' or plot_or_calculation_continue != "y":

        # to check if, after this run, the boundaries are right     
        correct_fit_range = False                                               
        while correct_fit_range == False:
            
            # to enter the new boundaries (its just necessary to get the input (+ the value for E for the next question(check) part (2nd part of check)). the exact values will be calculated in the lin_bg_intfkt loop)
            correct_range=False                                                 
            while correct_range == False:
                fit_lower_E_input = input("Please enter the lower energy range for the lin BG fit in eV\n")
                correct_range = energy_range_limits_fit_fkt(fit_lower_E_input)   
            fit_lower_E=correct_range[1]                                        # to get the E value
            
            correct_range=False
            while correct_range == False:
                fit_upper_E_input = input("Please enter the upper energy range for the lin BG fit in eV\n")
                correct_range = energy_range_limits_fit_fkt(fit_upper_E_input)        
            fit_upper_E=correct_range[1] #

            # 2n part of the check, if boundaries are ok
            correct_fit_range_input_error = False                                               
            while correct_fit_range_input_error == False:
                print("Are", fit_lower_E,"eV &",fit_upper_E ,"eV chosen boundaries for the linear BG fit? The integration boundaries will be asked later. \n")
                correct_fit_range_input = input("If yes: type 'yes'. If not 'no'\n")
                if correct_fit_range_input != 'yes' and correct_fit_range_input != 'no':
                    print("\nError, please type in 'yes' or 'no'\n")
                    correct_fit_range = False
                    correct_fit_range_input_error = False   
                if correct_fit_range_input == 'yes':
                    correct_fit_range = True
                    correct_fit_range_input_error = True
                    break
                if correct_fit_range_input == 'no':
                    correct_fit_range = False
                    correct_fit_range_input_error = True        

        # enter the integration boundaries
        # to check if, after this run, the fit boundaries are right     
        correct_int_range = False                                               
        k = 0
        while correct_int_range == False:
            if k == 0:
                print("Are", fit_lower_E, "eV &", fit_upper_E, "eV the same boundaries for integration? \n")
            if k > 0:
                print("Are", int_lower_E, "eV &", int_upper_E, "eV the right boundaries for integration? \n")
            correct_int_range_input = input("If yes: type 'yes'. If not 'no'\n")
            if correct_int_range_input != 'yes' and correct_int_range_input != 'no':
                print("\nError, please type in 'yes' or 'no'\n")
                correct_int_range = False
            if correct_int_range_input == 'yes' and k == 0:
                int_lower_E = fit_lower_E
                int_upper_E = fit_upper_E
                correct_int_range = True
            if correct_int_range_input == 'yes' and k > 0:
                correct_int_range = True
            if correct_int_range_input == 'no':
                # to enter the new boundaries (its just necessary to get the input (+ the value for E for the next question. the exact values will be calculated in the lin_bg_int_fkt() loop)
                correct_range=False                                                 
                while correct_range == False:
                    int_lower_E_input = input("Please enter the lower energy range for integration in eV.\nPlease make sure, that it is not the first(lowest) number in the file! If so, the programm will crash later by calculating the integral\n")
                    correct_range = energy_range_limits_fit_fkt(int_lower_E_input)                                  # using the fit_fkt, since its only to get the boundareis. The real calculation is done in lin_BG-int_fkt() loop
                int_lower_E=correct_range[1]                                                                        # to get the E value
                int_lower_E_spectra = correct_range[2]                              # to get the actual spectra value
                int_lower_E_position = correct_range[3]                             # to get the potisition i in the file

                correct_range=False
                while correct_range == False:
                    int_upper_E_input = input("Please enter the upper energy range for integration in eV\n")
                    correct_range = energy_range_limits_fit_fkt(int_upper_E_input)        
                int_upper_E=correct_range[1] #
                int_upper_E_spectra = correct_range[2]                              # to get the actual spectra value
                int_upper_E_position = correct_range[3]                             # to get the potisition i in the file
                
                k +=1
                correct_int_range = False

    # claclulate all the lin fkt´s for all spectra and save it in df2
    y_lin_BG, int_lower_E_position, int_upper_E_position = lin_BG_int_fkt()
                               
    # plot the function
    axes= plt.axes()
    fig = plt.gcf()
    sns.lineplot(x="E", y=wanted_spectra, data=df, color='black', marker='s', mec='black', linestyle='solid')  
    sns.lineplot(x="E", y=wanted_spectra, data=df2,color='blue')  
    plt.axvline(x=fit_lower_E, label='lower E range for fit', color='blue')
    plt.axvline(x=fit_upper_E, label='upper E range for fit', color='blue')
    plt.axvline(x=int_lower_E, label='lower E range for int', color='red')
    plt.axvline(x=int_upper_E, label='upper E range for int', color='red')
    fig.set_size_inches(15, 10)    
    plt.xlim(max(df["E"]),min(df["E"])) 
    plt.xticks(np.arange(int(min(df["E"])),int(max(df["E"])),5))
    plt.show()


    # calculation of the difference of the spectra and the lin BG
    df3 = df - df2
    df3["E"] = df["E"]                        # to get the E back into the df3 (which will be 0 otherwise since df["E"]=df2["E"])

    fig = plt.gcf()
    sns.lineplot(x="E", y=wanted_spectra, data=df, color='black', marker='s', mec='black', linestyle='solid')  
    sns.lineplot(x="E", y=wanted_spectra, data=df2, color='blue')
    sns.lineplot(x="E", y=wanted_spectra, data=df3, color='red')
    plt.axvline(x=fit_lower_E, label='lower E range for fit', color='blue')
    plt.axvline(x=fit_upper_E, label='upper E range for fit', color='blue')
    plt.axvline(x=int_lower_E, label='lower E range for int', color='red')
    plt.axvline(x=int_upper_E, label='upper E range for int', color='red')
    fig.set_size_inches(15, 10)    
    plt.xlim(max(df["E"]), min(df["E"]))
    plt.xticks(np.arange(int(min(df["E"])), int(max(df["E"])), 5))
    plt.show()

    # integration of the spectra
    df4 = df3.copy()                          # create a df to calcualte the sum (integration)

    df4, df_sum = integration_fkt(df4, int_lower_E_position, int_upper_E_position)

    print(df4)
    fig = plt.gcf()
    """    
    j = 1
    while j <= spectra_nr:  
        if j == 1: sns.lineplot(x="E", y=j, data=df4[j], color=(0, 0, 255))
        if j == 2: sns.lineplot(x="E", y=j, data=df4[j], color=(30, 60, 255))
        if j == 3: sns.lineplot(x="E", y=j, data=df4[j], color=(94, 144, 255))
        if j == 4: sns.lineplot(x="E", y=j, data=df4[j], color=(157, 60, 255))
        if j == 5: sns.lineplot(x="E", y=j, data=df4[j], color=(214, 49, 255))
        if j == 6: sns.lineplot(x="E", y=j, data=df4[j], color=(240, 00, 130))
        if j == 7: sns.lineplot(x="E", y=j, data=df4[j], color=(255, 0, 0))
        if j == 8: sns.lineplot(x="E", y=j, data=df4[j], color=(240, 130, 40))
        if j == 9: sns.lineplot(x="E", y=j, data=df4[j], color=(230, 175, 45))
        if j == 10: sns.lineplot(x="E", y=j, data=df4[j], color=(230, 220, 50))
        if j == 11: sns.lineplot(x="E", y=j, data=df4[j], color=(0, 220, 0))
        if j == 12: sns.lineplot(x="E", y=j, data=df4[j], color=(60, 255, 60))
        if j == 12: sns.lineplot(x="E", y=j, data=df4[j], color=(0, 255, 0))
        j += 1
    plt.axvline(x=fit_lower_E, label='lower E range for fit', color='blue')
    plt.axvline(x=fit_upper_E, label='upper E range for fit', color='blue')
    plt.axvline(x=int_lower_E, label='lower E range for int', color='red')
    plt.axvline(x=int_upper_E, label='upper E range for int', color='red')
    fig.set_size_inches(15, 10)    
    plt.xlim(max(df["E"]), min(df["E"]))
    plt.xticks(np.arange(int(min(df["E"])), int(max(df["E"])), 5))
    plt.show()
    """
    # output of the data file in the same folder witht he following names
    output = "_data.txt"
    output2 = "_lin_BG.txt"
    output3 = "_data-lin_BG.txt"
    output4 = "_sum.txt"
    output5 = "_integral.txt"

    full_path_output = selected_file_path + selected_file_name + output
    full_path_output2 = selected_file_path + selected_file_name + output2
    full_path_output3 = selected_file_path+selected_file_name+output3
    full_path_output4 = selected_file_path+selected_file_name+output4
    full_path_output5 = selected_file_path+selected_file_name+output5

    df.to_csv(full_path_output, header=True, index=False, sep='\t', mode='w')
    df2.to_csv(full_path_output2, header=True, index=False, sep='\t', mode='w')
    df3.to_csv(full_path_output3, header=True, index=False, sep='\t', mode='w')
    df4.to_csv(full_path_output4, header=True, index=False, sep='\t', mode='w')
    df_sum.to_csv(full_path_output5, header=True, index=False, sep='\t', mode='w')




#integration
# will look something like this
# intnr= integration(df3)[int_lower_E:int_upper_E]




