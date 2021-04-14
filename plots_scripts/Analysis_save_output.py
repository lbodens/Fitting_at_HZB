import numpy as np


def matrix_creation_and_save(df, message, Inputs):
    A = matrix_creation(df, Inputs)
    write_to_file(A, message, Inputs)
    return


def matrix_creation(df, Inputs):
    """
    changes the given df into a matrix style function
    """
    nr_of_columns = Inputs["number_of_columns"]
    nr_of_rows = Inputs["number_of_rows"]

    array_d = []
    for name, rest in df.items():
        array_d.append(rest)
    array = np.array(array_d)

    A = array.reshape(nr_of_columns, nr_of_rows)
    return A


def write_to_file(A, message, Inputs):
    file = open(Inputs["result_file_path"], "a")

    content = str(A)
    file.write(message)
    file.write("\n")
    file.write("\n")
    file.write(content)
    file.write("\n")
    file.write("\n")
    file.write("\n")
    file.close()


def save_to_file_main_fkt(Inputs, df_a_1, df_a_2, df_a_tot, df_c_shift_bw_oxid, df_c_shift_el1, df_c_shift_el2):
    df_ratio_perc_1, df_ratio_abs_1 = df_a_1
    df_ratio_perc_2, df_ratio_abs_2 = df_a_2
    df_ratio_perc_tot, df_ratio_abs_tot = df_a_tot

    matrix_creation_and_save(df_ratio_perc_1, "Percentage ratio of oxid state 1 to 2 of {}:".format(Inputs["el1_name"]),
                             Inputs)
    matrix_creation_and_save(df_ratio_abs_1, "Absolute ratio of oxid state 1 to 2 of {}:".format(Inputs["el1_name"]),
                             Inputs)
    matrix_creation_and_save(df_ratio_perc_2, "Percentage ratio of oxid state 1 to 2 of {}:".format(Inputs["el2_name"]),
                             Inputs)
    matrix_creation_and_save(df_ratio_abs_2, "Absolute ratio of oxid state 1 to 2 of {}:".format(Inputs["el2_name"]),
                             Inputs)
    matrix_creation_and_save(df_ratio_perc_tot,
                             "Percentage ratio of {} to {}:".format(Inputs["el1_name"], Inputs["el2_name"]), Inputs)
    matrix_creation_and_save(df_ratio_abs_tot,
                             "Absolute ratio of {} to {}:".format(Inputs["el1_name"], Inputs["el2_name"]), Inputs)

    matrix_creation_and_save(df_c_shift_bw_oxid, "Energy shift of main peak between oxid state 1 & 2", Inputs)
    matrix_creation_and_save(df_c_shift_el1,
                             "Energy shift of the main peak over the sample in dependence of the 1st main peaks position of {}:".format(
                                 Inputs["el1_name"]), Inputs)
    matrix_creation_and_save(df_c_shift_el2,
                             "Energy shift of the main peak over the sample in dependence of the 1st main peaks position of {}:".format(
                                 Inputs["el2_name"]), Inputs)
    return