#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    This code was originally created by Madhura Killedar and Pierre-Yves Lablanche.
    This version has personal modifications to the original code.
    @author:  Maria Luiza Linhares Dantas
    @date:    2016.10.12
    @version: 0.0.1
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sklearn.mixture as skm
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

# Main thread
if __name__ == '__main__':

    # Configuring the inputs -------------------------------------------------------------------------------------------
    my_data = '/home/mldantas/Dropbox/Clustering/Dataset/class_WHAN_BPT.csv'
    my_data = pd.read_csv(my_data)

    nii_halpha = my_data["xx_BPT"]        # log([NII]/Halpha) - BPT and WHAN x axis'
    oiii_hbeta = my_data["yy_BPT"]        # log([OIII]/Hbeta) - BPT y axis
    ew_halpha  = my_data["yy_WHAN"]       # log(EW(Halpha))   - WHAN y axis
    ew_nii     = my_data["EW_NII_WHAN"]   # log(EW(NII))      - WHAN passive-retired galaxies sep. requirement

    # My training set --------------------------------------------------------------------------------------------------
    training_set = np.c_[nii_halpha, oiii_hbeta, ew_halpha]

    # GMM with 4 clusters ----------------------------------------------------------------------------------------------
    n_components  = 3
    gmm_4clusters = skm.GMM(n_components=n_components, covariance_type='full')
    y_gmm4        = gmm_4clusters.fit_predict(training_set)
    probability   = gmm_4clusters.predict_proba(training_set)
    mean          = gmm_4clusters.means_

    # Plots ------------------------------------------------------------------------------------------------------------

    plot_order = [1, 0, 2]  # Run GMM, decide preferred order
    color_order = ["BuPu", "Oranges", "Greens"]
    plt.figure(figsize=(15, 5))

    # WHAN -------------------------------------------------------------------------------------------------------------
    index = np.where(probability)

    ax3a = plt.subplot(131)
    for j in np.arange(n_components):
        i = plot_order[j]
        select = probability[:, i] > 0.8
        # select = y_gmm3==i
        x_plot = nii_halpha[select]
        y_plot = ew_halpha[select]
        cmap = color_order[j]
        sns.kdeplot(x_plot, y_plot, cmap=cmap, shade=True, shade_lowest=False, ax=ax3a)
        plt.plot(mean[i][1], mean[i][0], 'k*', ms=6)
    # plt.scatter(np.log10(rna),np.log10(tmp['EW_H_alpha']),c=y_gmm3,alpha=0.3,edgecolors='None',cmap='viridis')
    plt.xlabel(r'$\log([$NII$]/$H$\alpha)$')
    plt.ylabel(r'$\log W_{H\alpha}$')
    plt.xlim(-1.5, 1.0)
    plt.ylim(-1.0, 2.5)
    # theoretical and empirical curves
    [xleft, xright] = ax3a.get_xlim()
    ax3a.plot((xleft, xright), (0.5, 0.5), 'k--')
    plt.grid()

    # BPT
    ax3b = plt.subplot(132)
    for j in np.arange(n_components):
        i = plot_order[j]
        select = probability[:, i] > 0.8
        # select = y_gmm3==i
        x_plot = nii_halpha[select]
        y_plot = oiii_hbeta[select]
        cmap = color_order[j]
        sns.kdeplot(x_plot, y_plot, cmap=cmap, shade=True, shade_lowest=False, ax=ax3b)
        plt.plot(mean[i][1], mean[i][2], 'k*', ms=6)
    # plt.scatter(np.log10(rna),np.log10(rob),c=y_gmm3,alpha=0.3,edgecolors='None',cmap='viridis')
    plt.xlabel(r'$\log([$NII$]/$H$\alpha)$')
    plt.ylabel(r'$\log([$OIII$]/$H$\beta)$')
    plt.xlim(-1.5, 1.0)
    plt.ylim(-1.5, 1.5)
    # theoretical and empirical curves
    [xleft, xright] = ax3b.get_xlim()
    kauffman_x = np.linspace(xleft, min(-0.2, xright), 20)
    kauffman_y = 0.61 / (kauffman_x - 0.05) + 1.3
    ax3b.plot(kauffman_x, kauffman_y, 'k-')
    kewley_x = np.linspace(xleft, min(0.2, xright), 20)
    kewley_y = 0.61 / (kewley_x - 0.47) + 1.19
    ax3b.plot(kewley_x, kewley_y, 'k--')
    plt.grid()

    # Third projection
    ax3c = plt.subplot(133)
    for j in np.arange(n_components):
        i = plot_order[j]
        select = probability[:, i] > 0.8
        x_plot = oiii_hbeta[select]
        y_plot = ew_halpha[select]
        cmap = color_order[j]
        sns.kdeplot(x_plot, y_plot, cmap=cmap, shade=True, shade_lowest=False, ax=ax3c)
        plt.plot(mean[i][2], mean[i][0], 'k*', ms=6)
    plt.xlabel(r'$\log([$OIII$]/$H$\beta)$')
    plt.ylabel(r'$\log W_{H\alpha}$')
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.0, 2.5)
    plt.grid()

    plt.show()
