import numpy as np
import os

my_data = np.loadtxt('/home/mldantas/Dropbox/Clustering/dataset_clustering_abs.csv', delimiter=',', dtype=str)

mjd     = my_data[:, 0].astype(int)
plate   = my_data[:, 1].astype(int)
fiberid = my_data[:, 2].astype(int)

filelist_path       = '/media/mldantas/SAMSUNG/LinuxBackupIAG/Documentos/Clustering/filelist_incomplete.txt'
spec_file_path      = '/media/mldantas/SAMSUNG/LinuxBackupIAG/Documentos/Clustering/DATABASE'
spec_file_selection = '/home/mldantas/Documents/Clustering/DATASET_selected'


filelist = np.loadtxt(filelist_path, dtype=str)

indexes  = np.arange(plate.size)

for spec_file in filelist:
        basename = os.path.split(spec_file)[-1]     # Get filename
        basename = os.path.splitext(basename)[0]    # Remove file extension

        plates   = basename.split('.')[0]
        mjds     = basename.split('.')[1]
        fiberids = basename.split('.')[2]

        plates   = int(plates)
        mjds     = int(mjds)
        fiberids = int(fiberids)

        index = indexes[(plate == plates) * (mjd == mjds) * (fiberid == fiberids)]

        if index.size is 0:
                continue

        selected_object = np.loadtxt(os.path.join(spec_file_path, spec_file))

        np.savetxt(os.path.join(spec_file_selection, basename+'.csv'), selected_object, fmt="%d,%.4f,%.4f,%d")