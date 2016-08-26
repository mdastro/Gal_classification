#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Tables Match (my table with STARLIGHT SDSS DR7 tables) -- features needed for machine learning in order to classify
    galaxies
    This version: added equivalent width of NII for the WHAN classification (see last column)
    @author:  Maria Luiza Linhares Dantas
    @date:    2016.26.08
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
    print ("My Data Loaded!")

    lines_all = '/home/mldantas/Documents/STARLIGHT/Tabelas/Lines_all.txt'
    print ("Tables read ok!")

    # The program itself -----------------------------------------------------------------------------------------------
    # Creating a dictionary --------------------------------------------------------------------------------------------

    my_dictionary = {}
    for i in range(len(my_data[0, :])):                                         # Converting numpy array into dictionary
        my_dictionary[my_data[0, i]] = np.array(my_data[0 + 1:, i], dtype=str)

    print ("My Table's Dictionary read ok!")

    # Reading the data and performing the cross-match ------------------------------------------------------------------
    my_plate     = my_dictionary['plate'].astype(int)
    my_mjd       = my_dictionary['mjd'].astype(int)
    my_fiberid   = my_dictionary['fiber_id'].astype(int)

    print ("My ids size is %d" % my_plate.size)

    lines_all_ids = np.loadtxt(lines_all, usecols=[0], skiprows=1, dtype=str)
    print ("Teste: Lines ALL table works? Print object %s" % lines_all_ids[1])

    lines_all_ew_nii = np.loadtxt(lines_all, usecols=[124], skiprows=1, dtype=float)
    print ("EW NII read successfully!")


    print ("Parameters input ok!")

    lines_all_plate   = []
    lines_all_mjd     = []
    lines_all_fiberid = []
    for l in range(lines_all_ids.size):
        lines_all_plate_i   = lines_all_ids[l].split('.')[0]
        print (lines_all_plate_i)
        lines_all_mjd_i     = lines_all_ids[l].split('.')[1]
        print (lines_all_mjd_i)
        lines_all_fiberid_i = lines_all_ids[l].split('.')[2]
        print (lines_all_fiberid_i)
        lines_all_plate.append(int(lines_all_plate_i))
        lines_all_mjd.append(int(lines_all_mjd_i))
        lines_all_fiberid.append(int(lines_all_fiberid_i))
    lines_all_plate   = np.array(lines_all_plate)
    lines_all_mjd     = np.array(lines_all_mjd)
    lines_all_fiberid = np.array(lines_all_fiberid)

    print ("Lines ALL read with ids ok!")

    lines_all_indexes = np.arange(my_plate.size)
    lines_all_data_index = []
    for m in range(lines_all_plate.size):
        lines_all_data_index_m = lines_all_indexes[(my_plate == lines_all_plate[m]) * (my_mjd == lines_all_mjd[m]) *
                                             (my_fiberid == lines_all_fiberid[m])]
        if lines_all_data_index_m.size is 0:
            continue
        lines_all_data_index.append(m)

    my_lines_all_ew_nii   = ['ew_nii']
    my_lines_all_plate    = lines_all_plate[lines_all_data_index]
    my_lines_all_mjd      = lines_all_mjd[lines_all_data_index]
    my_lines_all_fiberid  = lines_all_fiberid[lines_all_data_index]
    my_lines_all_ew_nii   = lines_all_ew_nii[lines_all_data_index]

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


    np.savetxt('/home/mldantas/Dropbox/Clustering/learning_parameters_b.csv',
               np.column_stack((my_plate, my_mjd, my_fiberid, my_dn4000_obs, my_dn4000_synth, my_h_alpha, my_ew_h_alpha,
                            my_h_beta, my_oiii, my_nii, my_vd_h_alpha, my_vd_h_beta, my_vd_nii, my_vd_oiii, my_oi_6300,
                                my_oii_3727, my_sii_6717, my_sii_6731, my_lines_all_ew_nii)),
                       fmt = "%d,%d,%d,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f",
               delimiter=',', newline='\n', header='plate,mjd,fiber_id,dn4000_obs,dn4000_synth,H_alpha,EW_H_alpha,'
                                                   'H_beta,OIII,NII,vd_Halpha,vd_Hbeta,vd_nii,vd_oiii,oi_6300,oii_3727,'
                                                   'sii_6717,sii_6731,ew_nii')

    

    print ("Lines ALL match ok!")
