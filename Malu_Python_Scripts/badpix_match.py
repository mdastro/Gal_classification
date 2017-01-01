from __future__ import division
import numpy as np
import pandas as pd

dn4000_txt = '/home/mldantas/Dropbox/STARLIGHT/dn4000_MALU.txt'
lines      = '/home/mldantas/Dropbox/STARLIGHT/lines.txt'

dn4000_table   = np.loadtxt(dn4000_txt, dtype=object)
lines_table    = np.loadtxt(lines, dtype=object)
bad_pix_info   = np.loadtxt('/home/mldantas/Dropbox/Clustering/Dataset/badpixels_class_WHAN_BPT_predictions.txt', dtype=str)
classification = np.loadtxt('/home/mldantas/Dropbox/Clustering/Dataset/class_WHAN_BPT.csv', delimiter=',', dtype=str)

dn4000_dictionary = {}
for k in range(len(dn4000_table[0, :])):
    dn4000_dictionary[dn4000_table[0, k]] = np.array(dn4000_table[0 + 1:, k], dtype=str)
print ("Dn4000 Table Dictionary read ok!")

lines_dictionary = {}
for j in range((lines_table[0, :]).size):
    lines_dictionary[lines_table[0, j]] = np.array(lines_table[0 + 1:, j], dtype=str)
print ("Lines' Table Dictionary read ok!")

classification_dictionary = {}
for k in range(len(classification[0, :])):
    classification_dictionary[classification[0, k]] = np.array(classification[0 + 1:, k], dtype=str)
print ("Classification Table Dictionary read ok!")


ids        = bad_pix_info[:, 0].astype(str)
bad_pix_hb = bad_pix_info[:, 1].astype(float)
bad_pix_o3 = bad_pix_info[:, 2].astype(float)
bad_pix_ha = bad_pix_info[:, 3].astype(float)
bad_pix_n2 = bad_pix_info[:, 4].astype(float)

index = np.where((bad_pix_hb < 0.25) * (bad_pix_hb >= 0.0) * (bad_pix_o3 < 0.25) * (bad_pix_o3 >= 0.0)
                    * (bad_pix_ha < 0.25) * (bad_pix_ha >= 0.0) * (bad_pix_n2 < 0.25) * (bad_pix_n2 >= 0.0))

dn4000_ids = dn4000_dictionary['SC5-output_file'].astype(str)
dn4000_obs_break = dn4000_dictionary['Dn4000(obs)'].astype(float)
dn4000_syn_break = dn4000_dictionary['Dn4000(syn)'].astype(float)

lines_plate   = lines_dictionary['plate'].astype(int)
lines_mjd     = lines_dictionary['mjd'].astype(int)
lines_fiberid = lines_dictionary['fiberID'].astype(int)
print("Line's table size is %d" % lines_plate.size)

ids_class = classification_dictionary['id'].astype(str)
plate_class   = []
mjd_class     = []
fiberid_class = []
for i in range(ids_class.size):
    plate_class.append(int(ids_class[i].split('.')[0]))
    mjd_class.append(int(ids_class[i].split('.')[1]))
    fiberid_class.append(int(ids_class[i].split('.')[2]))
plate_class   = np.array(plate_class)
mjd_class     = np.array(mjd_class)
fiberid_class = np.array(fiberid_class)

plate   = []
mjd     = []
fiberid = []
for i in range(ids.size):
    plate.append(int(ids[i].split('.')[0]))
    mjd.append(int(ids[i].split('.')[1]))
    fiberid.append(int(ids[i].split('.')[2]))
plate   = np.array(plate)[index]
mjd     = np.array(mjd)[index]
fiberid = np.array(fiberid)[index]


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

dn4000_indexes = np.arange(plate.size)
dn4000_data_index = []
for m in range(dn4000_plate.size):
    dn4000_data_index_m = dn4000_indexes[(plate == dn4000_plate[m]) * (mjd == dn4000_mjd[m]) *
                                         (fiberid == dn4000_fiberid[m])]
    if dn4000_data_index_m.size is 0:
        continue
    dn4000_data_index.append(m)

dn4000_synth = dn4000_syn_break[dn4000_data_index]
dn4000_obs = dn4000_obs_break[dn4000_data_index]
dn4000_plate = dn4000_plate[dn4000_data_index]
dn4000_mjd = dn4000_mjd[dn4000_data_index]
dn4000_fiberid = dn4000_fiberid[dn4000_data_index]

## Lines crossmatch ------------------------------------------------------------------------------------------------
indexes = np.arange(plate.size)
new_index = []
for i in range(lines_plate.size):
    index = indexes[(plate == lines_plate[i]) * (mjd == lines_mjd[i]) * (fiberid == lines_fiberid[i])]
    if index.size is 0:
        continue
    new_index.append(i)
h_alpha    = lines_dictionary['F_Halpha'].astype(float)[new_index]
ew_h_alpha = lines_dictionary['EW_Halpha'].astype(float)[new_index]
h_beta     = lines_dictionary['F_Hbeta'].astype(float)[new_index]
oiii       = lines_dictionary['F_oiii'].astype(float)[new_index]
nii        = lines_dictionary['F_nii'].astype(float)[new_index]

## Classification crossmatch -------------------------------------------------------------------------------------------

indexes_class = np.arange(plate_class.size)
index_class = []
for i in range(plate_class.size):
    index = indexes_class[(plate == plate_class[i]) * (mjd == mjd_class[i]) * (fiberid == fiberid_class[i])]
    if index.size is 0:
        continue
    index_class.append(i)
classification_bpt  = classification_dictionary['class_BPT'].astype(int)[index_class]
classification_whan = classification_dictionary['class_WHAN'].astype(int)[index_class]


np.savetxt('/home/mldantas/Dropbox/Clustering/Dataset/results_classification.csv',
           np.column_stack((plate, mjd, fiberid, dn4000_obs, dn4000_synth, h_alpha, ew_h_alpha, h_beta, oiii, nii,
                            classification_bpt, classification_whan)),
                           fmt="%d,%d,%d,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%d,%d", delimiter=',', newline='\n',
                           header='plate,mjd,fiber_id,dn4000_obs,dn4000_synth,H_alpha,EW_H_alpha,'
                                             'H_beta,OIII,NII,class_BPT,class_WHAN')

