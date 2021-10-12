# import matplotlib as plt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plotting_just_spectra(df, spectra_to_plot):
    axs = plt.axes()
    fig = plt.gcf()
    sns.lineplot(x="E", y=spectra_to_plot, data=df, color='black', marker='s', mec='black', linestyle='solid')

    plt.xlim(max(df["E"]), min(df["E"]))
    plt.xticks(
        np.arange(int(min(df["E"])), int(max(df["E"])), 5))
    fig.set_size_inches(15, 10)
    plt.show()


def plot_plus_lin_bg(df, y_lin_bg, spectra_to_plot):
    # plot the function
    axs = plt.axes()
    fig = plt.gcf()
    sns.lineplot(x="E", y=spectra_to_plot, data=df, color='black', marker='s', mec='black', linestyle='solid')
    sns.lineplot(x="E", y=y_lin_bg, color='blue')
    fig.set_size_inches(15, 10)
    plt.xlim(max(df["E"]), min(df["E"]))
    plt.xticks(np.arange(int(min(df["E"])), int(max(df["E"])), 5))
    plt.show()


def plot_with_int_bounds(df, y_lin_bg, spectra_to_plot, fit_E_low, fit_E_up, int_E_low, int_E_up):
    # plot the function with integral boundaries area
    fig = plt.gcf()
    sns.lineplot(x="E", y=spectra_to_plot, data=df, color='black', marker='s', mec='black',
                 linestyle='solid',
                 label='Data')
    sns.lineplot(x="E", y=y_lin_bg, data=df, color='blue', label='lin BG of {}'.format(spectra_to_plot))

    plt.axvline(x=fit_E_low, label='lower E range for fit', color='blue')
    plt.axvline(x=fit_E_up, label='upper E range for fit', color='blue')
    plt.axvline(x=int_E_low, label='lower E range for int', color='red')
    plt.axvline(x=int_E_up, label='upper E range for int', color='red')

    fig.set_size_inches(15, 10)
    plt.xlim(max(df["E"]), min(df["E"]))
    plt.xticks(np.arange(int(min(df["E"])), int(max(df["E"])), 5))
    plt.show()


def choose_bound_fkt(df, Inputs, b):
    min_bound = min(df["E"])
    max_bound = max(df["E"])
    if b == 0:
        limit = float(input("please enter the lower fit bound within range [{} - {}]"
                            .format(min_bound + Inputs["step_size"], max_bound - Inputs["step_size"])))
    if b == 1:
        limit = float(input("please enter the upper fit bound within range [{} - {}]"
                            .format(min_bound + Inputs["step_size"], max_bound - Inputs["step_size"])))
    if b == 2:
        limit = float(input("please enter the lower integral bound within range [{} - {}]"
                            .format(min_bound + Inputs["step_size"], max_bound - Inputs["step_size"])))
    if b == 3:
        limit = float(input("please enter the upper integral bound within range [{} - {}]"
                            .format(min_bound + Inputs["step_size"], max_bound - Inputs["step_size"])))

    limits, bound, i = bounds_calc_fkt(df, limit)
    return limits, bound, i


def bounds_calc_fkt(df, limit):
    i = 0
    while df["E"][i] * 100 < limit * 100 and i < len(df["E"]):
        i += 1
    bound = df["E"][i]
    print("The input energy was: ", limit, ". The used will be: ", bound)
    return limit, bound, i


def lin_bg_fkt(df, i_low, i_up, spec_name):
    # to get the average of the point, to not be so sensitive to statistic noise
    delta_y_1 = (df[spec_name][i_low - 2] + df[spec_name][i_low - 1] + df[spec_name][i_low] +
                 df[spec_name][i_low - 1] + df[spec_name][i_low + 2]) / 5
    delta_y_2 = (df[spec_name][i_up - 2] + df[spec_name][i_up - 1] + df[spec_name][i_up] +
                 df[spec_name][i_up - 1] + df[spec_name][i_up + 2]) / 5

    # calc of the lin function
    m = (delta_y_2 - delta_y_1) / (df["E"][i_up] - df["E"][i_low])
    y_lin_bg = m * (df["E"] - df["E"][i_low]) + delta_y_1
    print("The function is: y=", m, "*(x -", df["E"][i_low], ") +", delta_y_1)
    return y_lin_bg


def plotting_path_main_fkt(df, Inputs):
    # choose the wanted column
    spectra_to_plot = input("Please enter the wanted spectra in the style: 1st: 'S00:, 2nd: 'S01' 3rd: 'S03' etc.")
    spectra = df[spectra_to_plot]

    plotting_just_spectra(df, spectra_to_plot)

    lower_fit_bound, fit_E_low, i_low_fit = choose_bound_fkt(df, Inputs, 0)
    upper_fit_bound, fit_E_up, i_up_fit = choose_bound_fkt(df, Inputs, 1)

    y_lin_bg = lin_bg_fkt(df, i_low_fit, i_up_fit, spectra_to_plot)

    int_range = False  # to check, if the wanted boundaries the same as before
    while not int_range:
        print("Are the integration limits the same as the chosen ones:", fit_E_low, "eV & ", fit_E_up, "eV?\n ")
        plot_with_int_bounds(df, y_lin_bg, spectra_to_plot, fit_E_low, fit_E_up, fit_E_low, fit_E_up)
        int_range_input = input("If yes, please type 'yes'. If not: 'no'\n")
        if int_range_input == "yes" or int_range_input == "y":
            lower_int_bound = lower_fit_bound
            int_E_low = fit_E_low
            i_low_int = i_low_fit
            upper_int_bound = upper_fit_bound
            int_E_up = fit_E_up
            i_up_int = i_up_fit

            int_range = True
            continue

        if int_range_input == "no" or int_range_input == "n":

            lower_int_bound, int_E_low, i_low_int = choose_bound_fkt(df, Inputs, 2)
            upper_int_bound, int_E_up, i_up_int = choose_bound_fkt(df, Inputs, 3)

            int_range = True

            # 2n part of the check, if boundaries are ok
            correct_int_range = False
            while not correct_int_range:
                print("Are", int_E_low, "eV &", int_E_up, "eV the right integration boundaries? \n")
                plot_with_int_bounds(df, y_lin_bg, spectra_to_plot, fit_E_low, fit_E_up, fit_E_low, fit_E_up)
                correct_int_range_input = input("If yes: type 'yes'. If not 'no'\n")
                if correct_int_range_input == 'yes' or correct_int_range_input == 'y':
                    correct_int_range = True
                    break
                if correct_int_range_input == 'no' or correct_int_range_input == 'n':
                    lower_int_bound, int_E_low, i_low_int = choose_bound_fkt(df, Inputs, 2)
                    upper_int_bound, int_E_up, i_up_int = choose_bound_fkt(df, Inputs, 3)
                    correct_int_range = False
                else:
                    print("\nError, please type in 'yes' or 'no'\n")
                    correct_int_range = False
            continue

        else:
            print("\nError, please type in 'yes' or 'no'\n")
            int_range = False

    plot_or_calculation_continue = input(
        "do you want to continue? if yes: enter 'yes'. if you want to continue enter 'no'")

    if plot_or_calculation_continue == 'yes' or plot_or_calculation_continue == "y":
        plot_or_calc = 'no'  # to swap the result and continue with the script

        return plot_or_calc, fit_E_low, i_low_fit, fit_E_up, i_up_fit, int_E_low, i_low_int, int_E_up, i_up_int
    if plot_or_calculation_continue == 'no' or plot_or_calculation_continue == "n":  # to terminate the program
        # TODO: function: save inputs of bounds into loader file
        quit()
