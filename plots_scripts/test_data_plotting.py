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
from matplotlib.cbook import get_sample_data
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


def param_lists():
    """
    just a bunch of lists which are used later all the time. if someting is changed in the txt file, also add it here
    """
    element_list = ["Cu/(Cu+Ni)", "Cu(I)/(Cu(I)+Cu(II)", "Ni(II)/(Ni(II)+Ni(III)", "Pb4f_tot", "Pb4f_Pb0", "Pb4f_PbOx",
                    "I", "N", "Cs", "I:Pb", "Pb4f_shift", "Pb0+Pbox", "N:I", "N:Pb", "N:Cs", "Cs:Pb", "N/(Pb+I)"]
    param_list = ["time(h)", "time(min)", "thickness", "measurement_order", "exp_time(min)", "exp_time(h)"]
        # if you want to use either time or exposure time, change param_list[x] to either 0 or 5 in the whole code
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
    marker_shape_list = ["^", "o", "p", "s"]
    thickness_list = ["thinnest", "thinner", "thicker", "thickest"]
    sample_list = ["Ni-term_HZB", "Ni-term_BIU", "Orig_BIU"]

    return element_list, param_list, color_list, colors_list, el_ratio_list, marker_shape_list, thickness_list, sample_list


def data_to_load(col_list):
    """
    fkt to call the three txt files with all the data stored (in the way as written in param_list[element_list]
    """
    file_path = [
        "d:\\Profile\\ogd\\Desktop\\PhD\\Measurements\\Analysis\\210605_CuNiO_200p_ni_terminated\\Ni_term_HZB.dat",
        "d:\\Profile\\ogd\\Desktop\\PhD\\Measurements\\Analysis\\210605_CuNiO_200p_ni_terminated\\Ni_term_BIU.dat",
        "d:\\Profile\\ogd\\Desktop\\PhD\\Measurements\\Analysis\\210605_CuNiO_200p_ni_terminated\\Orig_BIU.dat"]
    df_1 = pd.read_csv(file_path[0], skiprows=0, usecols=col_list, delim_whitespace=True)
    df_2 = pd.read_csv(file_path[1], skiprows=0, usecols=col_list, delim_whitespace=True)
    df_3 = pd.read_csv(file_path[2], skiprows=0, usecols=col_list, delim_whitespace=True)

    color_arrow = plt.imread(get_sample_data("d:\\Profile\\ogd\\Desktop\\PhD\\Talks & Reports\\Pictures & Schematics\\colorarrow.png"))
    return df_1, df_2, df_3, color_arrow


def plot_seperate(df_1, df_2, df_3, col_list, param_list, colors_list, marker_shape_list, thickness_list, el_ratio_list,
                  color_ratio_to_plot, sample_list, color_arrow, a, b):
    """
    fkt to create the plot of the data against each other (separatet in the the three substrates)
    """
    for i in range(3 + int(a), 4 + int(b)):

        fig, axs = plt.subplots(3, 1, sharex=True, sharey=True, constrained_layout=True)
        fig.suptitle(str(col_list[color_ratio_to_plot]), fontsize=16)
        fig.supylabel(col_list[i])
        plt.xlabel(param_list[5])

        plotting_relations_new_fkt(axs[0], df_1, 1, col_list, param_list, marker_shape_list, thickness_list, 5, i,
                                   colors_list, el_ratio_list, color_ratio_to_plot, sample_list[0])

        plotting_relations_new_fkt(axs[1], df_2, 2, col_list, param_list, marker_shape_list, thickness_list, 5, i,
                                   colors_list, el_ratio_list, color_ratio_to_plot, sample_list[1])
        plotting_relations_new_fkt(axs[2], df_3, 3, col_list, param_list, marker_shape_list, thickness_list, 5, i,
                                   colors_list, el_ratio_list, color_ratio_to_plot, sample_list[2])

        plt.legend(loc='lower left', bbox_to_anchor=(1.04, 0))
        newax = fig.add_axes([0.85, 0.8, 0.2, 0.2], anchor='NE', zorder=-1)
        newax.imshow(color_arrow)
        newax.axis('off')
        plt.show()


def plotting_relations_new_fkt(ax, df, counter, col_list, param_list, marker_shape_list, thickness_list, x, y,
                               colors_list, el_ratio_list, color_ratio_to_plot, sample_name):
    """
    plotting fkt for the plot_separate fkt
    """
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
                ax.scatter(df[param_list[x]][position], df[col_list[y]][i], marker=marker_shape, s=100,
                            c=marker_color, label=thickness_list[df[param_list[2]][i] - 1])
            else:
                ax.scatter(df[param_list[x]][position], df[col_list[y]][i], marker=marker_shape, s=100,
                            c=marker_color)
        else:
            ax.scatter(df[param_list[x]][position], df[col_list[y]][i], marker=marker_shape, s=100,
                        c=marker_color)
    ax.set_title(sample_name)


def plot_3x3(df_1, df_2, df_3, col_list, param_list, colors_list, marker_shape_list, thickness_list, el_ratio_list,
             sample_list, color_arrow, a, b):
    """
    fkt to create the plot of the selected element in a 3x3 schema. In the columns its the same HTL property
    (Cu/(CU+Ni), Cu(I)/Cu, etc) the rows are the different HTL´s with the different cleaning methods
    """
    for i in range(3 + int(a), 4 + int(b)):
        counter = 0
        fig, axs = plt.subplots(3, 3, sharex=True, sharey=True, constrained_layout=True)
        fig.supylabel(col_list[i])

        axs[0, 0].set_title(col_list[0])
        axs[0, 1].set_title(col_list[1])
        axs[0, 2].set_title(col_list[2])
        axs[0, 2].text(1.1, 0.5, sample_list[0], horizontalalignment='center', verticalalignment='center', rotation=90,
                 transform=axs[0, 2].transAxes)
        axs[1, 2].text(1.1, 0.5, sample_list[1], horizontalalignment='center', verticalalignment='center', rotation=90,
                 transform=axs[1, 2].transAxes)
        axs[2, 2].text(1.1, 0.5, sample_list[2], horizontalalignment='center', verticalalignment='center', rotation=90,
                 transform=axs[2, 2].transAxes)
        axs[2, 0].set_xlabel(param_list[5])
        axs[2, 1].set_xlabel(param_list[5])
        axs[2, 2].set_xlabel(param_list[5])
        for j in range(9):
            color_ratio_to_plot = j % 3
            if color_ratio_to_plot == 0:
                plotting_relations_3x3_fkt(axs[0, counter], df_1, 1, col_list, param_list, marker_shape_list,
                                           thickness_list, 5, i, colors_list, el_ratio_list, counter)
            if color_ratio_to_plot == 1:
                plotting_relations_3x3_fkt(axs[1, counter], df_2, 2, col_list, param_list, marker_shape_list,
                                           thickness_list, 5, i, colors_list, el_ratio_list, counter)
            if color_ratio_to_plot == 2:
                plotting_relations_3x3_fkt(axs[2, counter], df_3, (counter + 1), col_list, param_list, marker_shape_list
                                           , thickness_list, 5, i, colors_list, el_ratio_list, counter)
                counter += 1
        plt.legend(loc='lower left', bbox_to_anchor=(1.04, 0))
        newax = fig.add_axes([0.85, 0.8, 0.2, 0.2], anchor='NE', zorder=-1)
        newax.imshow(color_arrow)
        newax.axis('off')
        plt.show()


def plotting_relations_3x3_fkt(ax, df, counter, col_list, param_list, marker_shape_list, thickness_list, x, y,
                               colors_list, el_ratio_list, color_ratio_to_plot):
    """
    plotting fkt for the plot_3x3 fkt. All points are colorcoded (depending on the column property).
    The shapes are the different thicknesses of the sample. THe order is from time, but since the measurement order is
    not the same as the order on the sample there is an extra loop to calc the position in the graph
    """
    elemental_ratio = df[col_list[color_ratio_to_plot]] #choosing right column from df
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
                ax.scatter(df[param_list[x]][position], df[col_list[y]][i], marker=marker_shape, s=100, c=marker_color,
                           label=thickness_list[df[param_list[2]][i] - 1])
            else:
                ax.scatter(df[param_list[x]][position], df[col_list[y]][i], marker=marker_shape, s=100, c=marker_color)
        else:
            ax.scatter(df[param_list[x]][position], df[col_list[y]][i], marker=marker_shape, s=100, c=marker_color)


def plot_3x3_element(df_1, df_2, df_3, col_list, param_list, colors_list, marker_shape_list, el_ratio_list, sample_list,
                     color_arrow):
    """
    fkt to call the fkt to create the plot of the selected element in a 3x3 schema.
    Once for the Pb elements/params and one for the elements only
    """
    pb_list_int = [3, 4, 5, 10, 11]
    el_list_int = [3, 6, 7, 8]
    ratio_list_int = [9, 12, 13, 14, 15, 16]
    for choosen_element in range(12, 15):  # <-----------------------------------------------iterate over that later
        pb_list_len, pb_list = get_elements_list_params(col_list, choosen_element, pb_list_int)
        el_list_len, el_list = get_elements_list_params(col_list, choosen_element, el_list_int)
        ratio_list_len, ratio_list = get_elements_list_params(col_list, choosen_element, ratio_list_int)

        # plotting the Pb_list
        plotting_elements_fkt_call(df_1, df_2, df_3, col_list, param_list, colors_list, marker_shape_list,
               el_ratio_list, sample_list, color_arrow, pb_list_len, pb_list, choosen_element)
        plotting_elements_2_fkt_call(df_1, df_2, df_3, col_list, param_list, colors_list, marker_shape_list,
               el_ratio_list, sample_list, color_arrow, pb_list_len, pb_list, choosen_element)

        # plotting the el_list
        plotting_elements_fkt_call(df_1, df_2, df_3, col_list, param_list, colors_list, marker_shape_list,
                                   el_ratio_list, sample_list, color_arrow, el_list_len, el_list, choosen_element)
        plotting_elements_2_fkt_call(df_1, df_2, df_3, col_list, param_list, colors_list, marker_shape_list,
                                     el_ratio_list, sample_list, color_arrow, el_list_len, el_list, choosen_element)

        # plotting the ratio_list
        plotting_elements_fkt_call(df_1, df_2, df_3, col_list, param_list, colors_list, marker_shape_list,
                                   el_ratio_list, sample_list, color_arrow, ratio_list_len, ratio_list, choosen_element)
        plotting_elements_2_fkt_call(df_1, df_2, df_3, col_list, param_list, colors_list, marker_shape_list,
                                   el_ratio_list, sample_list, color_arrow, ratio_list_len, ratio_list, choosen_element)


def get_elements_list_params(col_list, choosen_element, list_int):
    """
    fkt to get the right params/lists/positions of the choosen element configuration
    """
    list_len = len(list_int)
    pos = 100

    if choosen_element in list_int:
        list_len = len(list_int) - 1
        pos = list_int.index(choosen_element)
    list = [0] * list_len

    for o in range(list_len):
        if o < pos:
            j = list_int[o]
        elif o >= pos:
            j = list_int[o + 1]
        else:
            print("error at preparing the pb list to plot")
        list[o] = col_list[j]

    return list_len, list


def plotting_elements_fkt_call(df_1, df_2, df_3, col_list, param_list, colors_list, marker_shape_list, el_ratio_list,
                               sample_list, color_arrow, list_len, el_list, choosen_element):
    """
    fkt to create the plot of the selected element in a 3xX schema. THe columns are the different
    elements, while they use the same x_axis. they area also split between the 3 substrates (in the rows)
    """
    counter = 0
    fig, axs = plt.subplots(3, list_len, sharex=True, sharey="col", constrained_layout=True)
    axs[0, list_len - 1].text(1.1, 0.5, sample_list[0], horizontalalignment='center', verticalalignment='center',
                                 rotation=90, transform=axs[0, list_len - 1].transAxes)
    axs[1, list_len - 1].text(1.1, 0.5, sample_list[1], horizontalalignment='center', verticalalignment='center',
                                 rotation=90, transform=axs[1, list_len - 1].transAxes)
    axs[2, list_len - 1].text(1.1, 0.5, sample_list[2], horizontalalignment='center', verticalalignment='center',
                                 rotation=90, transform=axs[2, list_len - 1].transAxes)
    for o in range(list_len):
        axs[2, o].set_xlabel(col_list[choosen_element])
        axs[1, o].set_ylabel(el_list[o])

    for j in range(list_len * 3):
        color_ratio_to_plot = j % 3
        #            print(j, color_ratio_to_plot, counter)
        #            print(list[counter])
        if color_ratio_to_plot == 0:
            #               axs[0, counter].set_title(col_list[pb_list_int[counter]])
            plotting_relations_el_fkt(axs[0, counter], df_1, col_list, param_list, marker_shape_list, choosen_element,
                                      el_list[counter], colors_list, el_ratio_list, 0)
        if color_ratio_to_plot == 1:
            plotting_relations_el_fkt(axs[1, counter], df_2, col_list, param_list, marker_shape_list, choosen_element,
                                      el_list[counter], colors_list, el_ratio_list, 0)
        if color_ratio_to_plot == 2:
            plotting_relations_el_fkt(axs[2, counter], df_3, col_list, param_list, marker_shape_list, choosen_element,
                                      el_list[counter], colors_list, el_ratio_list, 0)
            counter += 1

    plt.legend(loc='lower left', bbox_to_anchor=(1.04, 0))
    newax = fig.add_axes([0.85, 0.8, 0.2, 0.2], anchor='NE', zorder=-1)
    newax.imshow(color_arrow)
    newax.axis('off')
    plt.show()


def plotting_relations_el_fkt(ax, df,  col_list, param_list, marker_shape_list,  x, y, colors_list, el_ratio_list,
                              color_ratio_to_plot):
    """
    plotting fkt for the plot_3x3 fkt. All points are colorcoded (depending on the column property).
    The shapes are the different thicknesses of the sample. THe order is from time, but since the measurement order is
    not the same as the order on the sample there is an extra loop to calc the position in the graph
    """
    elemental_ratio = df[col_list[color_ratio_to_plot]]
    for i in range(len(df)):
        marker_shape = marker_shape_list[df[param_list[2]][i] - 1]

        # getting the right color for the point
        ratio_limit = 1000  # necessary since floats have to big errors when subtracted
        while elemental_ratio[i] * 1000 < ratio_limit:
            ratio_limit -= 25
        ratio_limit = ratio_limit / 1000
        for j in range(len(colors_list)):
            if el_ratio_list[j] == ratio_limit:
                marker_color = colors_list[j]

        ax.scatter(df[col_list[x]][i], df[y][i], marker=marker_shape, s=100, c=marker_color)

    #    ax.set_title(col_list[y])


def plotting_elements_2_fkt_call(df_1, df_2, df_3, col_list, param_list, colors_list, marker_shape_list, el_ratio_list,
                                 sample_list, color_arrow, list_len, el_list, choosen_element):
    """
    fkt to create the plot of the selected element in a 3xX schema. THe columns are the different
    elements, while they use the same x_axis. they area also split between the 3 substrates (in the rows)
    fkt to plot the data with the lists the x-axis and the choosen element on y axis
    """
    counter = 0
    fig, axs = plt.subplots(3, list_len, sharex="col", sharey=True, constrained_layout=True)

    fig.supylabel(col_list[choosen_element])
    axs[0, list_len - 1].text(1.1, 0.5, sample_list[0], horizontalalignment='center', verticalalignment='center',
                                 rotation=90, transform=axs[0, list_len - 1].transAxes)
    axs[1, list_len - 1].text(1.1, 0.5, sample_list[1], horizontalalignment='center', verticalalignment='center',
                                 rotation=90, transform=axs[1, list_len - 1].transAxes)
    axs[2, list_len - 1].text(1.1, 0.5, sample_list[2], horizontalalignment='center', verticalalignment='center',
                                 rotation=90, transform=axs[2, list_len - 1].transAxes)

    for o in range(list_len):
        axs[2, o].set_xlabel(el_list[o])
#        axs[1, o].set_ylabel(col_list[choosen_element])

    for j in range(list_len * 3):
        color_ratio_to_plot = j % 3
        if color_ratio_to_plot == 0:
            #               axs[0, counter].set_title(col_list[pb_list_int[counter]])
            plotting_relations_el_2_fkt(axs[0, counter], df_1, col_list, param_list, marker_shape_list, choosen_element,
                                      el_list[counter], colors_list, el_ratio_list, 0)
        if color_ratio_to_plot == 1:
            plotting_relations_el_2_fkt(axs[1, counter], df_2, col_list, param_list, marker_shape_list, choosen_element,
                                      el_list[counter], colors_list, el_ratio_list, 0)
        if color_ratio_to_plot == 2:
            plotting_relations_el_2_fkt(axs[2, counter], df_3, col_list, param_list, marker_shape_list, choosen_element,
                                      el_list[counter], colors_list, el_ratio_list, 0)
            counter += 1

    plt.legend(loc='lower left', bbox_to_anchor=(1.04, 0))
    newax = fig.add_axes([0.85, 0.8, 0.2, 0.2], anchor='NE', zorder=-1)
    newax.imshow(color_arrow)
    newax.axis('off')
    plt.show()


def plotting_relations_el_2_fkt(ax, df,  col_list, param_list, marker_shape_list,  x, y,
                               colors_list, el_ratio_list, color_ratio_to_plot):
    """plotting the data with the params given from plotting_elements_2_fkt"""
    elemental_ratio = df[col_list[color_ratio_to_plot]]
    for i in range(len(df)):
        marker_shape = marker_shape_list[df[param_list[2]][i] - 1]

        # getting the right color for the point
        ratio_limit = 1000  # necessary since floats have to big errors when subtracted
        while elemental_ratio[i] * 1000 < ratio_limit:
            ratio_limit -= 25
        ratio_limit = ratio_limit / 1000
        for j in range(len(colors_list)):
            if el_ratio_list[j] == ratio_limit:
                marker_color = colors_list[j]

        ax.scatter(df[y][i], df[col_list[x]][i], marker=marker_shape, s=100, c=marker_color)



def dataload_fkt():
    """
    taking the params from the files into a class
    """
    element_list, param_list, color_list, colors_list, el_ratio_list, marker_shape_list, thickness_list, sample_list = param_lists()

    col_list = element_list.copy()
    col_list.extend(param_list)

    df_1, df_2, df_3, color_arrow = data_to_load(col_list)

    color_ratio_to_plot = 0  # selects from CU/(Cu+Ni), Cu(I)/Cu, Ni(II)/Ni) ratios

    a = 0#input("please select the 1st element you want to plot according to:" + str(element_list))
    b = 13#input("please select the last element you want to plot according to:" + str(element_list))
    #plot_fkt(df_1, df_2, df_3, col_list, param_list, color_list, marker_shape_list, thickness_list, a, b)

    plot_seperate(df_1, df_2, df_3, col_list, param_list, colors_list, marker_shape_list, thickness_list, el_ratio_list,
                  color_ratio_to_plot, sample_list, color_arrow, a, b)
    plot_3x3(df_1, df_2, df_3, col_list, param_list, colors_list, marker_shape_list, thickness_list,el_ratio_list,
             sample_list, color_arrow, a, b)








