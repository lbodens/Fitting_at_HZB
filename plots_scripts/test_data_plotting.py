"""
Script to plot data with multiple parameters at once.

Inputs:
 - Files with
     - Fitted Areas
     - Time / other x-axis
     - THin, Thickness of the spots
     - Measurement order

Output:
 - plot of chosen parameters

"""

import lmfit.models
import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np
import pandas as pd

# import matplotlib
# matplotlib.use('ps')
# from matplotlib import rc

# rc('text', usetex=True)
# rc('text.latex', preamble=r"\usepackage{color}")

"""
Import the different files

"""


class meta_data:

    def __init__(self, area, time, thickness, meausrement_order):
        self.area = area
        self.time = time
        self.thickness = thickness
        self.meausrement_order = meausrement_order


def dataload_fkt():
    """
    taking the params from the files into a class
    """
    element_list = ["Cu/(Cu+Ni)", "Cu(I)/(Cu(I)+Cu(II)", "Ni(II)/(Ni(II)+Ni(III)", "Pb4f_tot", "Pb4f_Pb0", "Pb4f_PbOx",
                    "I", "N", "Cs", "I:Pb", "Pb4f_shift", "Pb0+Pbox"]
    param_list = ["time(h)", "time(min)", "thickness", "measurement_order"]
    col_list = element_list.copy()
    col_list.extend(param_list)
    file_path = [
        "d:\\Profile\\ogd\\Desktop\\PhD\\Measurements\\Analysis\\210605_CuNiO_200p_ni_terminated\\Ni_term_BIU.dat",
        "d:\\Profile\\ogd\\Desktop\\PhD\\Measurements\\Analysis\\210605_CuNiO_200p_ni_terminated\\Ni_term_HZB.dat",
        "d:\\Profile\\ogd\\Desktop\\PhD\\Measurements\\Analysis\\210605_CuNiO_200p_ni_terminated\\Orig_BIU.dat"]
    df_1 = pd.read_csv(file_path[0], skiprows=0, usecols=col_list, delim_whitespace=True)
    df_2 = pd.read_csv(file_path[1], skiprows=0, usecols=col_list, delim_whitespace=True)
    df_3 = pd.read_csv(file_path[2], skiprows=0, usecols=col_list, delim_whitespace=True)

    color_list_blue = ["dodgerblue", "royalblue", "mediumblue", "midnightblue"]
    color_list_red = ["tomato", "red", "firebrick", "maroon"]
    color_list_green = ["springgreen", "limegreen", "green", "darkgreen"]
    color_list = [color_list_blue, color_list_red, color_list_green]
    colors_list = ["green", "#19FF00", "#33FF00", "#4DFF00", "#66FF00", "#80FF00", "#99FF00", "#B3FF00", "#CCFF00",
                   "#E6FF00", "yellow", "#FFE600", "#FFCC00", "#FFB300", "#FF9900", "Orange", "#FF6600", "#FF4D00",
                   "#FF3300", "#FF1900", "Red", "#FF001C", "#FF0039", "#FF0055", "#FF0071", "#FF008E", "#FF00AA",
                   "#FF00C6", "#FF00E3", "magenta", "#E600FF", "#CC00FF", "#B300FF", "#9900FF", "violet", "#6600FF",
                   "#4D00FF", "#3300FF", "#1900FF", "blue"]

    el_ratio_list = [0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3, 0.325, 0.35, 0.375, 0.4,
                     0.425, 0.45, 0.475, 0.5, 0.525, 0.55, 0.575, 0.6, 0.625, 0.65, 0.675, 0.7, 0.725, 0.75, 0.775, 0.8,
                     0.825, 0.85, 0.875, 0.9, 0.925, 0.95, 0.975, 1]
    color_ratio_to_plot = 0  # selects from CU/(Cu+Ni), Cu(I)/Cu, Ni(II)/Ni) ratios

    marker_shape_list = ["^", "o", "p", "s"]
    thickness_list = ["thinnest", "thinner", "thicker", "thickest"]
    for i in range(len(element_list)):
        fig, axs = plt.subplots()
        plotting_relations_fkt(fig, axs, df_1, 1, col_list, param_list, color_list[0], marker_shape_list,
                               thickness_list, 0, i)
        plotting_relations_fkt(fig, axs, df_2, 2, col_list, param_list, color_list[1], marker_shape_list,
                               thickness_list, 0, i)
        plotting_relations_fkt(fig, axs, df_3, 3, col_list, param_list, color_list[2], marker_shape_list,
                               thickness_list, 0, i)
        plt.show()
    for i in range(len(element_list)):
        fig, axs = plt.subplots(3)
        plotting_relations_new_fkt(fig, axs[0], df_1, 1, col_list, param_list, marker_shape_list, thickness_list, 0, i,
                                   colors_list, el_ratio_list, color_ratio_to_plot)
        plotting_relations_new_fkt(fig, axs[1], df_2, 2, col_list, param_list, marker_shape_list, thickness_list, 0, i,
                                   colors_list, el_ratio_list, color_ratio_to_plot)
        plotting_relations_new_fkt(fig, axs[2], df_3, 3, col_list, param_list, marker_shape_list, thickness_list, 0, i,
                                   colors_list, el_ratio_list, color_ratio_to_plot)
        plt.show()


def plotting_relations_fkt(fig, axs, df, counter, col_list, param_list, color_list, shape, label_list, x_to_plot,
                           y_to_plot):
    for i in range(len(df)):
        if counter == 1:
            if i < 4:
                axs.scatter(df[param_list[x_to_plot]][i], df[col_list[y_to_plot]][i],
                            marker=shape[(df[param_list[3]][i] - 1) % 4],
                            s=100, c=color_list[df[param_list[3]][i] - 1], label=label_list[df[param_list[2]][i] - 1])
            else:
                axs.scatter(df[param_list[x_to_plot]][i], df[col_list[y_to_plot]][i],
                            marker=shape[(df[param_list[3]][i] - 1) % 4], s=100,
                            c=color_list[(df[param_list[3]][i] - 1) % 4])
        else:
            axs.scatter(df[param_list[x_to_plot]][i], df[col_list[y_to_plot]][i],
                        marker=shape[(df[param_list[3]][i] - 1) % 4], s=100,
                        c=color_list[(df[param_list[3]][i] - 1) % 4])
    plt.legend(loc='best')
    plt.ylabel(col_list[y_to_plot])
    plt.xlabel(param_list[x_to_plot])

    bla = ["Ni-term, BIU", "Ni-term, HZB", "Orig, BIU"]
    for i in range(len(bla)):
        axs.text(-0.5, i * 0.1, r'\textcolor{color_list[0][i]}{bla[i]}')


def plotting_relations_new_fkt(fig, axs, df, counter, col_list, param_list, marker_shape_list, thickness_list, x, y,
                               colors_list, el_ratio_list, color_ratio_to_plot):
    elemental_ratio = df[col_list[color_ratio_to_plot]]
    for i in range(len(df)):
        position = df[param_list[3]][i] - 1
        marker_shape = marker_shape_list[df[param_list[2]][i] - 1]

        # getting the right color for the point
        ratio_limit = 1000  # necessary since floats have to big errors when subtracted
        while elemental_ratio[i] * 1000 < ratio_limit:
            ratio_limit -= 25
        ratio_limit = ratio_limit / 1000

        for j in range(len(colors_list)):
            if el_ratio_list[j] == ratio_limit:
                marker_color = colors_list[j]

        if counter == 3:
            if i < 4:
                axs.scatter(df[param_list[x]][position], df[col_list[y]][position], marker=marker_shape, s=100,
                            c=marker_color, label=thickness_list[df[param_list[2]][i] - 1])
            else:
                axs.scatter(df[param_list[x]][position], df[col_list[y]][position], marker=marker_shape, s=100,
                            c=marker_color)
        else:
            axs.scatter(df[param_list[x]][position], df[col_list[y]][position], marker=marker_shape, s=100,
                        c=marker_color)

    plt.legend(loc='best')
    plt.ylabel(col_list[y])
    plt.xlabel(param_list[x])
