#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    This python program plots the BPT and WHAN diagrams using the SEABORN package.
    @author:  Maria Luiza Linhares Dantas
    @date:    2016.23.08
    @version: 0.0.1
"""

from __future__ import division
import numpy as np
import statsmodels as stats
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Main thread
if __name__ == '__main__':

    # Configuring the inputs -------------------------------------------------------------------------------------------
    my_data = np.loadtxt('/home/mldantas/Dropbox/Clustering/clean_data.csv', delimiter=',', dtype=str)

    my_dictionary = {}
    for i in range(len(my_data[0, :])):                                         # Converting numpy array into dictionary
        my_dictionary[my_data[0, i]] = np.array(my_data[0 + 1:, i], dtype=str)

    my_nii        = my_dictionary['NII'].astype(float)
    my_oiii       = my_dictionary['OIII'].astype(float)
    my_h_alpha    = my_dictionary['H_alpha'].astype(float)
    my_h_beta     = my_dictionary['H_beta'].astype(float)
    my_ew_h_alpha = my_dictionary['EW_H_alpha'].astype(float)

    ## BPT -------------------------------------------------------------------------------------------------------------
    xbpt_01 = np.linspace(-1.8, -0.1, 1000)
    xbpt_02 = np.linspace(-1.8, 0.4, 1000)
    xbpt_03 = np.linspace(-1.8, 0.3, 1000)
    schawinski_x = np.linspace(-0.182, 2.0, 1000)

    ybpt_01 = []
    for j in range(len(xbpt_01)):
        ybpt_01j = 0.61 / (xbpt_01[j] - 0.05) + 1.3  # Kauffman03
        ybpt_01.append(ybpt_01j)
    ybpt_01 = np.array(ybpt_01)

    ybpt_02 = []
    for k in range(len(xbpt_02)):
        ybpt_02k = 0.61 / (xbpt_02[k] - 0.47) + 1.19  # Kewley01
        ybpt_02.append(ybpt_02k)
    ybpt_02 = np.array(ybpt_02)

    ybpt_03 = []
    for n in range(len(xbpt_03)):
        ybpt_03n = (-30.787 + (1.1358 * xbpt_03[n]) + 0.27297) * np.tanh(5.7409 * xbpt_03[n]) - 31.093  # Stasinska
        ybpt_03.append(ybpt_03n)
    ybpt_03 = np.array(ybpt_03)

    schawinski_y = []
    for l in range(len(schawinski_x)):
        schawinski_yl = 1.05 * schawinski_x[l] + 0.45
        schawinski_y.append(schawinski_yl)
    schawinski_y = np.array(schawinski_y)

    # Plots ------------------------------------------------------------------------------------------------------------
    index = np.where(np.log10(my_nii / my_h_alpha) != 0)

    # my_cool_palette = ['#00CED1', '#191970', '#FFA500', '#A020F0']
    # sns.palplot(sns.color_palette(my_cool_palette))
    plt.subplot(1, 2, 1)
    sns.set_style("darkgrid")
    # sns.palplot(sns.color_palette(my_cool_palette))
    # plot01  = plt.scatter(np.log10(my_nii/my_h_alpha)[index], np.log10(my_oiii/my_h_beta)[index], c='gray', alpha=0.2)
    cmap = sns.cubehelix_palette(8, rot=-.75, as_cmap=True)
    sns.kdeplot(np.log10(my_nii/my_h_alpha)[index], np.log10(my_oiii/my_h_beta)[index], cmap=cmap, shade=True, cut=5)
    plot02, = plt.plot(xbpt_01, ybpt_01, '--', color='#FF4500', linewidth=3.)
    plot03, = plt.plot(xbpt_02, ybpt_02, '-', color='#1E90FF', linewidth=3.)
    plot04, = plt.plot(schawinski_x, schawinski_y, '-', color='#FF1493', linewidth=3.)
    plot05, = plt.plot(xbpt_03, ybpt_03, '--', color='#6B8E23', linewidth=3.)
    plt.legend([plot02, plot03, plot04, plot05], [r"""$\rmKauffman+03$""", r"""$\rmKewley+01$""",
                                                  r"""$\rmSchawinski+07$""", r"""$\rm Stasi\' nska+06$"""], numpoints=1,
               loc='lower left', fontsize=20)
    plt.xlabel(r"$\log ([NII]/H{\alpha})$", fontweight='bold', fontsize=30)
    plt.ylabel(r"$\log (\left[OIII\right]/H \beta) $", fontweight='bold', fontsize=30)
    plt.text(-1.3, -0.4, r"Star Forming", fontsize=20)
    plt.text(-0.8, 1.0, r"AGN", fontsize=20)
    plt.text(-0.8, 0.9, r"Seyfert", fontsize=20)
    plt.text(0.3, 0.5, r"AGN(?)", fontsize=20)
    plt.text(0.3, 0.4, r"LI(N)ER", fontsize=17)
    plt.text(-0.25, -1.1, r"Composite", fontsize=20)
    plt.xlim([-1.8, 1.2])
    plt.ylim([-1.3, 1.55])
    plt.minorticks_on()
    plt.tick_params('both', labelsize='30')
    plt.grid(alpha=0.5)
    plt.subplots_adjust(top=0.95, bottom=0.15, left=0.10, right=0.60)
    # plt.show()

    plt.subplot(1, 2, 2)
    # sns.set_style("darkgrid")
    # sns.palplot(sns.color_palette(my_cool_palette))
    # plot01  = plt.scatter(np.log10(my_nii / my_h_alpha)[index], np.log10(my_ew_h_alpha)[index], c='gray', alpha=0.2)
    plot02, = plt.plot([-0.4, -0.4], [3.5, 0.5], '-', color='#FF1493', linewidth=3.)
    plot03, = plt.plot([-0.4, 3.5], [0.78, 0.78], '-', color='#FF1493', linewidth=3.)
    cmap = sns.cubehelix_palette(8, rot=-.75, as_cmap=True)
    sns.kdeplot(np.log10(my_nii / my_h_alpha)[index], np.log10(my_ew_h_alpha)[index], cmap=cmap, shade=True, cut=5)
    # plt.legend([plot01], [r"$\propto \, D_{n}4000_{synth}$ break"], numpoints=1, loc='lower left', fontsize=20)
    plt.axhline(y=+0.5, color='#FF1493', linewidth=2.)
    plt.xlabel(r"$\log ([NII]/H{\alpha})$", fontweight='bold', fontsize=30)
    plt.ylabel(r"$\log EW(H{\alpha})$", fontweight='bold', fontsize=30)
    plt.text(-1.0, 0., r"Retired/Passive", fontsize=20)
    plt.text(0.35, 1.0, r"sAGN", fontsize=20)
    plt.text(0.35, 0.6, r"wAGN", fontsize=20)
    plt.text(-1.5, 0.6, r"Star Forming", fontsize=20)
    plt.xlim([-1.8, 1.2])
    plt.ylim([-1.1, 2.5])
    plt.minorticks_on()
    plt.tick_params('both', labelsize='30')
    plt.grid(alpha=0.5)
    plt.subplots_adjust(top=0.95, bottom=0.15, left=0.10, right=0.60)

    plt.show()