#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    This script cleans missing data from SDSS (-999)
    @author:  Maria Luiza Linhares Dantas
    @date:    2016.25.08
    @version: 0.0.1
"""

from __future__ import division
import numpy as np
import csv

# Main thread
if __name__ == '__main__':

    print ("Hey yo, let's go!")

    # Configuring the inputs -------------------------------------------------------------------------------------------
    my_data = np.loadtxt('/home/mldantas/Dropbox/Clustering/learning_parameters_a.csv', delimiter=',', dtype=str)

    my_header = my_data[0,:].astype(str)

    my_dictionary = {}
    for i in range(len(my_data[0, :])):                                         # Converting numpy array into dictionary
        my_dictionary[my_data[0, i]] = np.array(my_data[0 + 1:, i], dtype=str)

    my_plate        = my_dictionary['plate'].astype(int)
    my_mjd          = my_dictionary['mjd'].astype(int)
    my_fiberid      = my_dictionary['fiber_id'].astype(int)
    my_dn4000_obs   = my_dictionary['dn4000_obs'].astype(float)
    my_dn4000_synth = my_dictionary['dn4000_synth'].astype(float)
    my_h_alpha      = my_dictionary['H_alpha'].astype(float)
    my_ew_h_alpha   = my_dictionary['EW_H_alpha'].astype(float)
    my_h_beta       = my_dictionary['H_beta'].astype(float)
    my_oiii         = my_dictionary['OIII'].astype(float)
    my_nii          = my_dictionary['NII'].astype(float)
    my_vd_h_alpha   = my_dictionary['vd_Halpha'].astype(float)
    my_vd_h_beta    = my_dictionary['vd_Hbeta'].astype(float)
    my_vd_nii       = my_dictionary['vd_nii'].astype(float)
    my_vd_oiii      = my_dictionary['vd_oiii'].astype(float)
    my_oi_6300      = my_dictionary['oi_6300'].astype(float)
    my_oii_3727     = my_dictionary['oii_3727'].astype(float)
    my_sii_6717     = my_dictionary['sii_6717'].astype(float)
    my_sii_6731     = my_dictionary['sii_6731'].astype(float)

    indexes = np.arange(my_plate.size)

    my_clean_data = []
    for i in range(my_plate.size):
        index = indexes[(my_dn4000_obs[i] >= 0.) & (my_dn4000_synth[i] >= 0.) & (my_h_alpha[i] >= 0.)
                        & (my_ew_h_alpha[i] >= 0) & (my_h_beta[i] >= 0.) & (my_oiii[i] >= 0.) & (my_nii[i] >= 0.)
                        & (my_vd_h_alpha[i] >= 0.) & (my_vd_h_beta[i] >= 0.) & (my_vd_nii[i] >= 0.)
                        & (my_vd_oiii[i] >= 0.) & (my_oi_6300[i] >= 0.) & (my_oii_3727[i] >= 0.)
                        & (my_sii_6717[i] >= 0.) & (my_sii_6731[i] >= 0.) & (my_dn4000_obs[i] != -999) & (my_dn4000_synth[i] != -999) & (my_h_alpha[i] != -999)
                        & (my_ew_h_alpha[i] >= 0) & (my_h_beta[i] != -999) & (my_oiii[i] != -999) & (my_nii[i] != -999)
                        & (my_vd_h_alpha[i] != -999) & (my_vd_h_beta[i] != -999) & (my_vd_nii[i] != -999)
                        & (my_vd_oiii[i] != -999) & (my_oi_6300[i] != -999) & (my_oii_3727[i] != -999)
                        & (my_sii_6717[i] != -999) & (my_sii_6731[i] != -999) & (my_dn4000_obs[i] !=-994) & (my_dn4000_synth[i] !=-994) & (my_h_alpha[i] !=-994)
                        & (my_ew_h_alpha[i] >= 0) & (my_h_beta[i] !=-994) & (my_oiii[i] !=-994) & (my_nii[i] !=-994)
                        & (my_vd_h_alpha[i] !=-994) & (my_vd_h_beta[i] !=-994) & (my_vd_nii[i] !=-994)
                        & (my_vd_oiii[i] !=-994) & (my_oi_6300[i] !=-994) & (my_oii_3727[i] !=-994)
                        & (my_sii_6717[i] !=-994) & (my_sii_6731[i] !=-994)]
        if index.size is 0:
            continue
        my_clean_data.append(my_data[i])
    my_clean_data = np.array(my_clean_data)

    np.savetxt('/home/mldantas/Dropbox/Clustering/learning_parameters_clean.csv', my_clean_data,
               fmt = "%s", delimiter=',', header='plate,mjd,fiber_id,dn4000_obs,dn4000_synth,H_alpha,EW_H_alpha,H_beta,'
                                                 'OIII,NII,vd_Halpha,vd_Hbeta,vd_nii,vd_oiii,oi_6300,oii_3727,sii_6717,'
                                                 'sii_6731')