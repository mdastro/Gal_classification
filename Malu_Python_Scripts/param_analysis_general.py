#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Summaries of the parameters 
    @author:  Maria Luiza L. Dantas
    @date:    2017.01.23
    @version: 0.0.2
"""

import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import pandas as pd
from statsmodels import robust

# ======================================================================================================================
# Main thread
if __name__ == '__main__':

    # Reading the files which contain the data -------------------------------------------------------------------------
    my_data = pd.read_csv('/home/mldantas/Dropbox/Clustering/clustering_starlight_analysis.csv')

    # Variables Attribution --------------------------------------------------------------------------------------------

    metallicity_w_flux = my_data['metallicity_flux']
    metallicity_w_mass = my_data['metallicity_mass']
    age_w_flux         = my_data['stellar_age_mass']
    age_w_mass         = my_data['stellar_age_mass']
    dn4000             = my_data['dn4000_synth']
    class_whan         = my_data['class_whan']
    class_bpt          = my_data['class_bpt']
    gmm_class          = my_data['gmm_class']

    print (metallicity_w_flux[gmm_class == 1].describe())
    print ("Median=%f" % np.median(metallicity_w_flux[gmm_class == 1]))
    print ("MAD=%f" % robust.mad(metallicity_w_flux[gmm_class == 1]))
    exit()
    print (metallicity_w_flux[gmm_class == 2].describe())
    print (metallicity_w_flux[gmm_class == 3].describe())
    print (metallicity_w_flux[gmm_class == 4].describe())

    print (age_w_flux[gmm_class == 1].describe())
    print (age_w_flux[gmm_class == 1].describe())
    print (age_w_flux[gmm_class == 1].describe())
    print (age_w_flux[gmm_class == 1].describe())
