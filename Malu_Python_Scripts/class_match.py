from __future__ import division
import numpy as np

my_data = np.loadtxt('/home/mldantas/Dropbox/Clustering/Dataset/results_d4000.csv', delimiter=',', dtype=str)
classification = np.loadtxt('/home/mldantas/Dropbox/Clustering/Dataset/class_WHAN_BPT.csv', delimiter=',', dtype=str)

classification_dictionary = {}
for k in range(len(classification[0, :])):
    classification_dictionary[classification[0, k]] = np.array(classification[0 + 1:, k], dtype=str)
print ("Classification Table Dictionary read ok!")

ids = my_data[:, 0].astype(str)
plate   = []
mjd     = []
fiberid = []
for i in range(ids.size):
    plate.append(int(ids[i].split('.')[0]))
    mjd.append(int(ids[i].split('.')[1]))
    fiberid.append(int(ids[i].split('.')[2]))
plate   = np.array(plate)
mjd     = np.array(mjd)
fiberid = np.array(fiberid)

ids_class = classification_dictionary['id'].astype(str)
plate_class   = []
mjd_class     = []
fiberid_class = []
for i in range(ids_class.size):
    plate_class.append(int(ids_class[i].split('.')[0]))
    mjd_class.append(int(ids_class[i].split('.')[1]))
    fiberid_class.append(int(ids_class[i].split('.')[2]))
plate_class   = np.array(plate_class)[index]
mjd_class     = np.array(mjd_class)[index]
fiberid_class = np.array(fiberid_class)[index]