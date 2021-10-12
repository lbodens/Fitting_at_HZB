from plots_scripts.Analysis_save_output import matrix_creation
from plots_scripts.Data_loader import BE_or_KE_fkt
import pandas as pd

"""-----------------------------------loading of data-----------------------------------------------"""
def energy_flip_fkt(df):
    df_length = df.shape[0]                     # getting length (nr of rows) of data frame ([1] would be nr of columns)
    i = 0
    if df["E"][i] > df["E"][df_length - 1]:
        df = df.iloc[::-1]
        df = df.reset_index(drop=True)
    return df


def BE_or_KE_calc_fkt(df, Inputs, number_of_spectra):
    BE_or_KE, exertation_energy = BE_or_KE_fkt(Inputs)
    for i in range(int(number_of_spectra)):
        if BE_or_KE == "BE":
            df["E"] = df.iloc[:, 0]
        if BE_or_KE == "KE":
            df["E"] = df.iloc[:, 0] - exertation_energy
    df = energy_flip_fkt(df)
    return df


def load_data_main_fkt(Inputs):
    number_of_spectra = Inputs["number_of_spectra"]
    file_path = Inputs["file_path"]
    txt = Inputs["txt_or_dat"]
    skip_rows = Inputs["skip_row_nr"]

    df = pd.read_csv(file_path + txt, skiprows=skip_rows, delim_whitespace=True, header=None)
    if df.iloc[0][0] != "E":
        head = [None]*(number_of_spectra+1)
        head[0] = "E"
        for i in range(1, number_of_spectra+1):
            if i <= 10:
                head[i] = "S0" + str(i-1)
            else:
                head[i] = "S" + str(i-1)
    df.columns = head

    df = BE_or_KE_calc_fkt(df, Inputs, number_of_spectra)
    return df


def save_output_fkt(Inputs, e_bound_container, df, df2=None, df3=None, df4=None, df5=None, df6=None):
    ##############################################################################
    # calculate the matrix

    output = "_data.txt"
    output2 = "_lin_BG.txt"
    output3 = "_data-lin_BG.txt"
    output4 = "_integral.txt"
    output5 = "_integral_matrix.txt"
    output_params = "_energy_bounds.txt"

    fit_E_low, fit_E_up, int_E_low, int_E_up = e_bound_container

    full_path_output_params = Inputs["file_path"] + output_params
    file = open(full_path_output_params, "a")
    file.write("The follwoing bounds where choosen:")
    file.write("\n")
    file.write("lower energy for fitting: ")
    file.write(str(fit_E_low))
    file.write("\n")
    file.write("upper energy for fitting: ")
    file.write(str(fit_E_up))
    file.write("\n")
    file.write("lower energy for integration: ")
    file.write(str(int_E_low))
    file.write("\n")
    file.write("upper energy for integration: ")
    file.write(str(int_E_up))
    file.close()

    if df2 is None:       # break, if only the plot path was chosen, but the set limits still got saved
        quit()

    full_path_output = Inputs["file_path"] + output
    full_path_output2 = Inputs["file_path"] + output2
    full_path_output3 = Inputs["file_path"] + output3
    full_path_output4 = Inputs["file_path"] + output4
    full_path_output5 = Inputs["file_path"] + output5

    df.to_csv(full_path_output, header=True, index=False, sep='\t', mode='w')
    df2.to_csv(full_path_output2, header=True, index=False, sep='\t', mode='w')
    df3.to_csv(full_path_output3, header=True, index=False, sep='\t', mode='w')
    df4.to_csv(full_path_output4, header=True, index=False, sep='\t', mode='w')

    A = matrix_creation(df5, Inputs)
    B = matrix_creation(df6, Inputs)

    A_str = str(A)
    B_str = str(B)
    file = open(full_path_output5, "a")
    file.write("The area calculated by the area approach\n")
    file.write(A_str)
    file.write("\n")
    file.write("\n")
    file.write("The area calculated by the area approach, corrected with cross section, IMFP etc.\n")
    file.write(B_str)
    file.close()
    quit()