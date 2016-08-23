#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Tables Match (my table with STARLIGHT SDSS DR7 tables) -- features needed for machine learning in order to classify
    galaxies
    @author:  Maria Luiza Linhares Dantas
    @date:    2016.22.08
    @version: 0.0.1
"""

from __future__ import division
import numpy as np
import datetime


# Main thread
if __name__ == '__main__':

    # Configuring the inputs -------------------------------------------------------------------------------------------
    my_data    = np.loadtxt('/home/mldantas/Dropbox/Clustering/dataset_clustering_abs.csv', delimiter=',', dtype=str)
    lines      = '/home/mldantas/Dropbox/STARLIGHT/lines.txt'
    # syn02      = '/home/mldantas/Dropbox/STARLIGHT/SYN02_MALU.txt'
    dn4000_txt = '/home/mldantas/Dropbox/STARLIGHT/dn4000_MALU.txt'

    # The program itself -----------------------------------------------------------------------------------------------
    # Creating a dictionary --------------------------------------------------------------------------------------------
    lines_table  = np.loadtxt(lines, dtype=object)
    dn4000_table = np.loadtxt(dn4000_txt, dtype=object)
    # syn02        = np.loadtxt(syn02, dtype=object)

    print ("Tables read ok!")

    my_dictionary = {}
    for i in range(len(my_data[0, :])):                                         # Converting numpy array into dictionary
        my_dictionary[my_data[0, i]] = np.array(my_data[0 + 1:, i], dtype=str)

    print ("My Table's Dictionary read ok!")

    # syn02_dictionary = {}
    # for j in range(len(syn02[0,:])):
    #     syn02_dictionary[syn02[0, j]] = np.array(syn02[0 + 1:, j], dtype=str)

    dn4000_dictionary = {}
    for k in range(len(dn4000_table[0, :])):
        dn4000_dictionary[dn4000_table[0, k]] = np.array(dn4000_table[0 + 1:, k], dtype=str)
    print ("Dn4000 Table Dictionary read ok!")

    lines_dictionary = {}
    for j in range((lines_table[0, :]).size):
        lines_dictionary[lines_table[0, j]] = np.array(lines_table[0 + 1:, j], dtype=str)
    print ("Lines' Table Dictionary read ok!")

    # Reading the data and performing the cross-match ------------------------------------------------------------------
    my_plate     = my_dictionary['plate'].astype(int)
    my_mjd       = my_dictionary['mjd'].astype(int)
    my_fiberid   = my_dictionary['fiberid'].astype(int)

    print ("My ids size is %d" % my_plate.size)

    # syn02_ids = syn02[:,0].astype(str)
    # stellar_mass_w_flux = syn02[:,3].astype(float)
    # stellar_mass_w_mass = syn02[:,4].astype(float)
    #
    # print ("The stellar mass sized is %d" % stellar_mass_w_mass.size)

    dn4000_ids       = dn4000_dictionary['SC5-output_file'].astype(str)
    dn4000_obs_break = dn4000_dictionary['Dn4000(obs)'].astype(float)
    dn4000_syn_break = dn4000_dictionary['Dn4000(syn)'].astype(float)

    print ("Dn4000 size is %d" % dn4000_obs_break.size)

    lines_plate   = lines_dictionary['plate'].astype(int)
    lines_mjd     = lines_dictionary['mjd'].astype(int)
    lines_fiberid = lines_dictionary['fiberID'].astype(int)

    print("Line's table size is %d" % lines_plate.size)

    print ("Parameters input ok!")

    # sy02 cross-match -------------------------------------------------------------------------------------------------
    # syn02_plate = []
    # syn02_mjd = []
    # syn02_fiberid = []
    # for g in range(stellar_mass_w_flux.size):
    #     syn02_plate_i   = int(syn02_ids[g].split('.')[0])
    #     syn02_mjd_i     = int(syn02_ids[g].split('.')[1])
    #     syn02_fiberid_i = int(syn02_ids[g].split('.')[2])
    #     syn02_plate.append(syn02_plate_i)
    #     syn02_mjd.append(syn02_mjd_i)
    #     syn02_fiberid.append(syn02_fiberid_i)
    # syn02_plate   = np.array(syn02_plate)
    # syn02_mjd     = np.array(syn02_mjd)
    # syn02_fiberid = np.array(syn02_fiberid)
    #
    # print ("SY02 size is %d" % syn02_plate.size)
    # print ("SYN02 ids read ok!")

    # indexes_syn02 = np.arange(my_plate.size)
    # syn02_index = []
    # for h in range(stellar_mass_w_flux.size):
    #     syn02_index_h = indexes_syn02[(my_plate == syn02_plate[h]) * (my_mjd == syn02_mjd[h])
    #                                   * (my_fiberid == syn02_fiberid[h])]
    #     if syn02_index_h.size is 0:
    #         continue
    #     syn02_index.append(syn02_index_h)
    # my_syn02_plate   = syn02_plate[syn02_index]
    # my_syn02_mjd     = syn02_mjd[syn02_index]
    # my_syn02_fiberid = syn02_fiberid[syn02_index]
    # my_stellar_mass_w_flux = stellar_mass_w_flux[syn02_index]
    # my_stellar_mass_w_mass = stellar_mass_w_mass[syn02_index]

    # print ("MY SYN02 size is %d" % my_syn02_plate.size)
    # print ("My SYN02 match ok!")

    ## Dn4000 crossmatch -----------------------------------------------------------------------------------------------
    dn4000_plate   = []
    dn4000_mjd     = []
    dn4000_fiberid = []
    for l in range(dn4000_ids.size):
        dn4000_plate_i   = dn4000_ids[l].split('.')[0]
        dn4000_mjd_i     = dn4000_ids[l].split('.')[1]
        dn4000_fiberid_i = dn4000_ids[l].split('.')[2]
        dn4000_plate.append(int(dn4000_plate_i))
        dn4000_mjd.append(int(dn4000_mjd_i))
        dn4000_fiberid.append(int(dn4000_fiberid_i))
    dn4000_plate   = np.array(dn4000_plate)
    dn4000_mjd     = np.array(dn4000_mjd)
    dn4000_fiberid = np.array(dn4000_fiberid)

    print ("Dn4000 size is %d" % dn4000_plate.size)
    datetime.datetime.now().time()

    dn4000_indexes = np.arange(my_plate.size)
    dn4000_data_index = []
    for m in range(dn4000_plate.size):
        dn4000_data_index_m = dn4000_indexes[(my_plate == dn4000_plate[m]) * (my_mjd == dn4000_mjd[m]) *
                                             (my_fiberid == dn4000_fiberid[m])]
        if dn4000_data_index_m.size is 0:
            continue
        dn4000_data_index.append(m)
    my_dn4000_synth   = dn4000_syn_break[dn4000_data_index]
    my_dn4000_obs     = dn4000_obs_break[dn4000_data_index]
    my_dn4000_plate   = dn4000_plate[dn4000_data_index]
    my_dn4000_mjd     = dn4000_mjd[dn4000_data_index]
    my_dn4000_fiberid = dn4000_fiberid[dn4000_data_index]

    print ("Dn4000 match ok!")
    datetime.datetime.now().time()

    ## Lines crossmatch ------------------------------------------------------------------------------------------------
    indexes = np.arange(my_plate.size)
    new_index = []
    for i in range(lines_plate.size):
        index = indexes[(my_plate == lines_plate[i]) * (my_mjd == lines_mjd[i]) * (my_fiberid == lines_fiberid[i])]
        if index.size is 0:
            continue
        new_index.append(i)
    my_h_alpha    = lines_dictionary['F_Halpha'].astype(float)[new_index]
    my_ew_h_alpha = lines_dictionary['EW_Halpha'].astype(float)[new_index]
    my_h_beta     = lines_dictionary['F_Hbeta'].astype(float)[new_index]
    my_oiii       = lines_dictionary['F_oiii'].astype(float)[new_index]
    my_nii        = lines_dictionary['F_nii'].astype(float)[new_index]
    my_vd_H_alpha = lines_dictionary['vd_Halpha'].astype(float)[new_index]
    my_vd_H_beta  = lines_dictionary['vd_Hbeta'].astype(float)[new_index]
    my_vd_nii     = lines_dictionary['vd_nii'].astype(float)[new_index]
    my_vd_oiii    = lines_dictionary['vd_oiii'].astype(float)[new_index]

    print ("Lines' match ok!")
    print ("Saving the dataset! YES!")

    # Saving the resulting dataset -------------------------------------------------------------------------------------
    np.savetxt('/home/mldantas/Dropbox/Clustering/learning_parameters.csv',
               np.column_stack((my_plate, my_mjd, my_fiberid, my_dn4000_obs, my_dn4000_synth, my_h_alpha, my_ew_h_alpha,
                                my_h_beta, my_oiii, my_nii, my_vd_H_alpha, my_vd_H_beta, my_vd_nii, my_vd_oiii)),
               fmt="%d,%d,%d,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f", delimiter=',', newline='\n',
               header='plate,mjd,fiber_id,dn4000_obs,dn4000_synth,H_alpha,EW_H_alpha,H_beta,OIII,NII,'
                      'vd_Halpha,vd_Hbeta,vd_nii,vd_oiii')

    print ("Done!")