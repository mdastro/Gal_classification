#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Boxplot Plot Using Seaborn Package in Python
    @author:  Maria Luiza L. Dantas
    @date:    2017.01.13
    @version: 0.0.2
"""

import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import pandas as pd
import seaborn as sns


def standardization(variable):
    """
    :param variable: the array with the variables you wish to standardize
    :return: standardized array
    """
    var_average = np.average(variable)
    var_std     = np.std(variable)
    new_variable = []
    for i in range(variable.size):
        new_variable_i = (variable[i] - var_average)/var_std
        new_variable.append(new_variable_i)
    new_variable = np.array(new_variable)
    return new_variable

# ======================================================================================================================
# Main thread
if __name__ == '__main__':

    # Reading the files which contain the data -------------------------------------------------------------------------
    my_data = np.loadtxt('/home/mldantas/Dropbox/Clustering/clustering_starlight_analysis.csv', delimiter=',',
                         dtype=str)

    my_dictionary = {}
    for i in range(len(my_data[0, :])):                                         # Converting numpy array into dictionary
        my_dictionary[my_data[0, i]] = np.array(my_data[0 + 1:, i], dtype=str)
    print ("My Table Table Dictionary read ok!")

    # Variables Attribution --------------------------------------------------------------------------------------------
    gmm_class = my_dictionary['gmm_class'].astype(int)

    indexes = np.arange(gmm_class.size)
    hue = []
    index = []
    for i in range(gmm_class.size):
        if (gmm_class[i] == 1):
            index.append(i)
            hue.append('G1')
        elif (gmm_class[i] == 4):
            index.append(i)
            hue.append('G4')
        else:
            continue
    hue = np.array(hue)

    metallicity_w_flux = my_dictionary['metallicity_flux'].astype(float)
    metallicity_w_mass = my_dictionary['metallicity_mass'].astype(float)
    age_w_flux         = my_dictionary['stellar_age_mass'].astype(float)
    age_w_mass         = my_dictionary['stellar_age_mass'].astype(float)
    dn4000             = my_dictionary['dn4000_synth'].astype(float)
    class_whan         = my_dictionary['class_whan'].astype(int)
    class_bpt          = my_dictionary['class_bpt'].astype(int)

    std_metallicity_flux = standardization(metallicity_w_flux)
    std_metallicity_mass = standardization(metallicity_w_mass)
    std_age_flux         = standardization(age_w_flux)
    std_age_mass         = standardization(age_w_mass)
    std_dn4000           = standardization(dn4000)

    # dictionary = {'Metallicity (wFlux)': std_metallicity_flux, 'Metallicity (wMass)': std_metallicity_mass,
    #               'Age (wFlux)': std_age_flux, 'Age (wMass)': std_age_mass, 'Dn4000': std_dn4000}
    plot_data01 = [std_metallicity_flux, std_age_flux, std_dn4000]
    plot_data02 = [std_metallicity_flux[index], std_age_flux[index], std_dn4000[index]]

    # # Plot01 -------------------------------------------------------------------------------------------------------
    # sns.set_style("white")
    # plot01 = sns.violinplot(data = plot_data01)
    # plt.setp(plot01.artists, alpha=1.)
    # plt.ylabel(r"Distribution", fontsize=17)
    # plt.xticks([0, 1, 2], ['Average Stellar Metallicity', 'Average Stellar Age', 'Dn4000'])
    # plt.tick_params('both', labelsize='15')
    # # plt.ylim([-0.2, 1.5])
    # # plt.xlim([-1, 2])
    # # plt.subplots_adjust(left=0.25, bottom=0.2, right=0.9, top=0.75)
    # # plot01.set_yscale("log", nonposy='clip')
    # # sns.despine(left=True)
    # # plt.savefig('color_e.pdf', format='pdf')
    # sns.axes_style({'legend.frameon': True})
    # plot01.get_yaxis().set_label_coords(-0.05, 0.5)
    #
    # plt.show()

    with sns.axes_style('white', {'axes.grid': False}):
        #
        # fig = plt.figure()
        # gs = gridspec.GridSpec(3, 1, height_ratios=[1, 1, 1])

        # Plot01 -------------------------------------------------------------------------------------------------------

        # ax0 = plt.subplot(gs[0])
        plt.subplot(3, 1, 1)
        sns.set_style("white")
        plot01 = sns.boxplot(x=gmm_class, y=metallicity_w_mass, order=[4,1,3,2],
                             palette={1: "#e78ac3", 2: "#66c2a5", 3: "#8da0cb", 4: "#fc8d62"}, notch=True)
        plt.setp(plot01.artists, alpha=1.)
        plt.setp(plot01.get_xticklabels(), visible=True)
        plt.xticks([0, 1, 2, 3], ['Group 4', 'Group 1', 'Group 3', 'Group 2'],  fontweight='bold')
        plt.tick_params('both', labelsize='15')
        plt.text(3.6, 1.4, "GMM", rotation=-90, horizontalalignment='center', fontsize = 15, fontweight='bold')
        sns.axes_style({'legend.frameon': True})
        plot01.get_yaxis().set_label_coords(-0.05, 0.5)

        # Plot02 -------------------------------------------------------------------------------------------------------
        # ax1 = plt.subplot(gs[1], sharex = plot01)
        plt.subplot(3, 1, 2)
        sns.set_style("white")
        plot02 = sns.boxplot(x=class_bpt, y=metallicity_w_mass, order=[1,2,3],
                             palette={1: "gray", 2: "gray", 3: "gray", 4: "gray"}, notch=True)
        plt.setp(plot02.artists, alpha=.8)
        plt.xticks([0, 1, 2], ['SF', 'Composite', 'AGN'],  fontweight='bold')
        plt.setp(plot01.get_xticklabels(), visible=True)
        plt.ylabel(r"$\rm <Z>$", fontsize=30, fontweight='bold')
        plt.tick_params('both', labelsize='15')
        plt.text(2.58, 1.4, r"BPT", rotation=-90, horizontalalignment='center', fontsize = 15, fontweight='bold')
        sns.axes_style({'legend.frameon': True})
        plot02.get_yaxis().set_label_coords(-0.05, 0.5)

        # Plot03 -------------------------------------------------------------------------------------------------------
        # ax2 = plt.subplot(gs[2], sharex = plot01)
        plt.subplot(3, 1, 3)
        sns.set_style("white")
        plot03 = sns.boxplot(x=class_whan, y=metallicity_w_mass, order=[1,2,3,4],
                             palette={1: "gray", 2: "gray", 3: "gray", 4: "gray"}, notch=True)
        plt.setp(plot03.artists, alpha=.8)
        plt.xticks([0, 1, 2, 3], ['SF', 'sAGN', 'wAGN', 'Retired/Passive'],  fontweight='bold')
        plt.tick_params('y', labelsize='15')
        plt.tick_params('x', labelsize='15')
        plt.text(3.6, 1.4, r"WHAN", rotation=-90, horizontalalignment='center', fontsize = 15, fontweight='bold')
        plt.subplots_adjust(left=0.24, bottom=0.10, right=0.61, top=0.82, hspace=0.20)
        # plt.savefig('/home/mldantas/Dropbox/Clustering/metallicity.pdf', format='pdf')
        sns.axes_style({'legend.frameon': True})
        plot02.get_yaxis().set_label_coords(-0.08, 0.5)


    plt.show()

    with sns.axes_style('white', {'axes.grid': False}):
        #
        # fig = plt.figure()
        # gs = gridspec.GridSpec(3, 1, height_ratios=[1, 1, 1])

        # Plot01 -------------------------------------------------------------------------------------------------------

        # ax0 = plt.subplot(gs[0])
        plt.subplot(3, 1, 1)
        sns.set_style("white")
        plot01 = sns.boxplot(x=gmm_class, y=age_w_mass, order=[4,1,3,2],
                             palette={1: "#e78ac3", 2: "#66c2a5", 3: "#8da0cb", 4: "#fc8d62"}, notch=True)
        plt.setp(plot01.artists, alpha=1.)
        plt.setp(plot01.get_xticklabels(), visible=True)
        plt.xticks([0, 1, 2, 3], ['Group 4', 'Group 1', 'Group 3', 'Group 2'],  fontweight='bold')
        plt.tick_params('both', labelsize='15')
        plt.text(3.6, 9.8, "GMM", rotation=-90, horizontalalignment='center', fontsize = 15, fontweight='bold')
        sns.axes_style({'legend.frameon': True})
        plot01.get_yaxis().set_label_coords(-0.05, 0.5)
        plt.ylim([9.0, 10.5])

        # Plot02 -------------------------------------------------------------------------------------------------------
        # ax1 = plt.subplot(gs[1], sharex = plot01)
        plt.subplot(3, 1, 2)
        sns.set_style("white")
        plot02 = sns.boxplot(x=class_bpt, y=age_w_mass, order=[1,2,3],
                             palette={1: "gray", 2: "gray", 3: "gray", 4: "gray"}, notch=True)
        plt.setp(plot02.artists, alpha=.8)
        plt.xticks([0, 1, 2], ['SF', 'Composite', 'AGN'],  fontweight='bold')
        plt.setp(plot01.get_xticklabels(), visible=True)
        plt.ylabel(r"Age", fontsize=25)
        plt.tick_params('both', labelsize='15')
        plt.text(2.58, 9.8, r"BPT", rotation=-90, horizontalalignment='center', fontsize = 15, fontweight='bold')
        sns.axes_style({'legend.frameon': True})
        # plot02.set_yscale("log", nonposy='clip')
        plt.ylim([9.0, 10.5])

        # Plot03 -------------------------------------------------------------------------------------------------------
        # ax2 = plt.subplot(gs[2], sharex = plot01)
        plt.subplot(3, 1, 3)
        sns.set_style("white")
        plot03 = sns.boxplot(x=class_whan, y=age_w_mass, order=[1,2,3,4],
                             palette={1: "gray", 2: "gray", 3: "gray", 4: "gray"}, notch=True)
        plt.setp(plot03.artists, alpha=.8)
        plt.xticks([0, 1, 2, 3], ['SF', 'sAGN', 'wAGN', 'Retired/Passive'],  fontweight='bold')
        plt.tick_params('y', labelsize='15')
        plt.tick_params('x', labelsize='15')
        plt.text(3.6, 9.8, r"WHAN", rotation=-90, horizontalalignment='center', fontsize = 15, fontweight='bold')
        plt.subplots_adjust(left=0.24, bottom=0.10, right=0.61, top=0.82, hspace=0.20)
        # plt.savefig('/home/mldantas/Dropbox/Clustering/age.pdf', format='pdf')
        sns.axes_style({'legend.frameon': True})
        plot02.get_yaxis().set_label_coords(-0.1, 0.5)
        plt.ylim([9., 10.5])


    plt.show()

    with sns.axes_style('white', {'axes.grid': False}):
        #
        # fig = plt.figure()
        # gs = gridspec.GridSpec(3, 1, height_ratios=[1, 1, 1])

        # Plot01 -------------------------------------------------------------------------------------------------------

        # ax0 = plt.subplot(gs[0])
        plt.subplot(3, 1, 1)
        sns.set_style("white")
        plot01 = sns.boxplot(x=gmm_class, y=dn4000, order=[4,1,3,2],
                             palette={1: "#e78ac3", 2: "#66c2a5", 3: "#8da0cb", 4: "#fc8d62"}, notch=True)
        plt.setp(plot01.artists, alpha=1.)
        plt.setp(plot01.get_xticklabels(), visible=True)
        plt.xticks([0, 1, 2, 3], ['Group 4', 'Group 1', 'Group 3', 'Group 2'],  fontweight='bold')
        plt.tick_params('both', labelsize='15')
        plt.text(3.6, 1.8, "GMM", rotation=-90, horizontalalignment='center', fontsize = 15, fontweight='bold')
        sns.axes_style({'legend.frameon': True})
        plot01.get_yaxis().set_label_coords(-0.05, 0.5)
        # plt.ylim([9.0, 10.5])

        # Plot02 -------------------------------------------------------------------------------------------------------
        # ax1 = plt.subplot(gs[1], sharex = plot01)
        plt.subplot(3, 1, 2)
        sns.set_style("white")
        plot02 = sns.boxplot(x=class_bpt, y=dn4000, order=[1,2,3],
                             palette={1: "gray", 2: "gray", 3: "gray", 4: "gray"}, notch=True)
        plt.setp(plot02.artists, alpha=.8)
        plt.xticks([0, 1, 2], ['SF', 'Composite', 'AGN'],  fontweight='bold')
        plt.setp(plot01.get_xticklabels(), visible=True)
        plt.ylabel(r"$\rm D_n 4000$", fontsize=25)
        plt.tick_params('both', labelsize='15')
        plt.text(2.58, 1.8, r"BPT", rotation=-90, horizontalalignment='center', fontsize = 15, fontweight='bold')
        sns.axes_style({'legend.frameon': True})
        # plot02.set_yscale("log", nonposy='clip')
        # plt.ylim([9.0, 10.5])

        # Plot03 -------------------------------------------------------------------------------------------------------
        # ax2 = plt.subplot(gs[2], sharex = plot01)
        plt.subplot(3, 1, 3)
        sns.set_style("white")
        plot03 = sns.boxplot(x=class_whan, y=dn4000, order=[1,2,3,4],
                             palette={1: "gray", 2: "gray", 3: "gray", 4: "gray"}, notch=True)
        plt.setp(plot03.artists, alpha=.8)
        plt.xticks([0, 1, 2, 3], ['SF', 'sAGN', 'wAGN', 'Retired/Passive'],  fontweight='bold')
        plt.tick_params('y', labelsize='15')
        plt.tick_params('x', labelsize='15')
        plt.text(3.6, 1.8, r"WHAN", rotation=-90, horizontalalignment='center', fontsize = 15, fontweight='bold')
        plt.subplots_adjust(left=0.24, bottom=0.10, right=0.61, top=0.82, hspace=0.20)
        # plt.savefig('/home/mldantas/Dropbox/Clustering/age.pdf', format='pdf')
        sns.axes_style({'legend.frameon': True})
        plot02.get_yaxis().set_label_coords(-0.07, 0.5)
        # plt.ylim([9., 10.5])


    plt.show()
