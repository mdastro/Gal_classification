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
import csv

# Main thread
if __name__ == '__main__':

    print ("Hey yo, let's go!")

    # Configuring the inputs -------------------------------------------------------------------------------------------
    my_data = np.loadtxt('/home/mldantas/Dropbox/Clustering/learning_parameters.csv', delimiter=',', dtype=str)
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
    lines_all_sii_6717 = np.loadtxt(lines_all, usecols=[144], skiprows=1, dtype=float)
    print ("Line 6717 read successfully!")
    lines_all_sii_6731 = np.loadtxt(lines_all, usecols=[155], skiprows=1, dtype=float)
    print ("Line 6731 read successfully!")
    lines_all_oi_6300  = np.loadtxt(lines_all, usecols=[100], skiprows=1, dtype=float)
    print ("Line 6300 read successfully!")
    lines_all_oii_3727 = np.loadtxt(lines_all, usecols=[1], skiprows=1, dtype=float)
    print ("Line 3727 read successfully!")

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

    my_lines_all_oi_6300  = ["oi_6300"]
    my_lines_all_oii_3727 = ["oii_3727"]
    my_lines_all_sii_6717 = ["sii_6717"]
    my_lines_all_sii_6731 = ["sii_6731"]
    my_lines_all_plate    = lines_all_plate[lines_all_data_index]
    my_lines_all_mjd      = lines_all_mjd[lines_all_data_index]
    my_lines_all_fiberid  = lines_all_fiberid[lines_all_data_index]
    my_lines_all_oi_6300  = lines_all_oi_6300[lines_all_data_index]
    my_lines_all_oii_3727 = lines_all_oii_3727[lines_all_data_index]
    my_lines_all_sii_6717 = lines_all_sii_6717[lines_all_data_index]
    my_lines_all_sii_6731 = lines_all_sii_6731[lines_all_data_index]

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


    np.savetxt('/home/mldantas/Dropbox/Clustering/learning_parameters_a.csv',
               np.column_stack((my_plate, my_mjd, my_fiberid, my_dn4000_obs, my_dn4000_synth, my_h_alpha, my_ew_h_alpha,
                            my_h_beta, my_oiii, my_nii, my_vd_h_alpha, my_vd_h_beta, my_vd_nii, my_vd_oiii,
                                my_lines_all_oi_6300, my_lines_all_oii_3727, my_lines_all_sii_6717,
                                my_lines_all_sii_6731)),
                       fmt = "%d,%d,%d,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f",
               delimiter=',', newline='\n', header='plate,mjd,fiber_id,dn4000_obs,dn4000_synth,H_alpha,EW_H_alpha,'
                                                   'H_beta,OIII,NII,vd_Halpha,vd_Hbeta,vd_nii,vd_oiii,oi_6300,oii_3727,'
                                                   'sii_6717,sii_6731')

    # input_file  = open('/home/mldantas/Dropbox/Clustering/learning_parameters.csv')
    # reader_file = csv.reader(input_file)
    #
    # with open('/home/mldantas/Dropbox/Clustering/learning_parameters_a.csv', 'w') as file_out:
    #     with input_file as in_file:
    #         i = 0
    #         for line in in_file:
    #             s = ''
    #             s = line.replace('\n', '') + ',' + my_lines_all_oi_6300[i] + my_lines_all_oii_3727[i] + \
    #                 my_lines_all_sii_6717[i] + my_lines_all_sii_6731[i] + '\n'
    #             i+=1
    #             file_out.write(s)

    # my_data = my_data.T
    # column_list = [c for c in my_data]
    # column_list += [my_lines_all_oi_6300, my_lines_all_oii_3727, my_lines_all_sii_6717, my_lines_all_sii_6731]
    #
    # my_new_data = np.array(column_list).T

    # col_plate = my_new_data[:,0].astype(int)    #1
    # col_mjd   = my_new_data[:,1].astype(int)    #2
    # col_fid   = my_new_data[:,2].astype(int)    #3
    # col_d4K_o = my_new_data[:,3].astype(float)  #4
    # col_d4K_s = my_new_data[:,4].astype(float)  #5
    # col_ha    = my_new_data[:,5].astype(float)  #6
    # col_ew_ha = my_new_data[:,6].astype(float)  #7
    # col_hb    = my_new_data[:,7].astype(float)  #8
    # col_oiii  = my_new_data[:,8].astype(float)  #9
    # col_nii   = my_new_data[:,9].astype(float)  #10
    # col_vd_ha = my_new_data[:,10].astype(float) #11
    # col_vd_hb = my_new_data[:,11].astype(float) #12
    # col_vd_n2 = my_new_data[:,12].astype(float)
    # col_vd_o3 = my_new_data[:,13].astype(float)
    # col_6300  = my_new_data[:,14].astype(float)
    # col_3727  = my_new_data[:,15].astype(float)
    # col_6717  = my_new_data[:,16].astype(float)
    # col_6731  = my_new_data[:,17].astype(float)

    # np.savetxt('/home/mldantas/Dropbox/Clustering/learning_parameters_a.csv',
    #            np.column_stack((col_plate,col_mjd,col_fid,col_d4K_o,col_d4K_s,col_ha,col_ew_ha,col_hb,col_oiii,col_nii,
    #                             col_vd_ha,col_vd_hb,col_vd_n2,col_vd_o3,col_6300,col_3727,col_6717,col_6731)),
    #            fmt="%d,%d,%d,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f",
    #            delimiter=',', newline='\n', header='plate,mjd,fiber_id,dn4000_obs,dn4000_synth,H_alpha,EW_H_alpha,'
    #                                               'H_beta,OIII,NII,vd_Halpha,vd_Hbeta,vd_nii,vd_oiii,oi_6300,oii_3727,'
    #                                               'sii_6717,sii_6731')

    print ("Lines ALL match ok!")