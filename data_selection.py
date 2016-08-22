import numpy as np

starlight_params = '/home/mldantas/Documents/STARLIGHT/Tabelas/parameters_MALU.txt'

identifiers = np.loadtxt(starlight_params, usecols=[0], dtype=object)
mjd         = np.loadtxt(starlight_params, usecols=[1], dtype=object)
plate       = np.loadtxt(starlight_params, usecols=[2], dtype=object)
fiberid     = np.loadtxt(starlight_params, usecols=[3], dtype=object)
mag_apa_r   = np.loadtxt(starlight_params, usecols=[10])      # Observed Petrosian magnitude in r band
mag_abs_r   = np.loadtxt(starlight_params, usecols=[20])      # Absolute Petrosian magnitude in r band
redshift    = np.loadtxt(starlight_params, usecols=[6])

index = [(redshift <= 0.075) * (redshift >= 0.015) * (mag_abs_r <=-19.88)]

print identifiers[index].size

new_identifiers = identifiers[index]
new_mjd         = mjd[index]
new_plate       = plate[index]
new_fiberid     = fiberid[index]
new_mag_apa_r   = mag_apa_r[index]
new_mag_abs_r   = mag_abs_r[index]
new_redshift    = redshift[index]

np.savetxt('/home/mldantas/Dropbox/Clustering/dataset_clustering_abs.csv',
               np.column_stack((new_mjd, new_plate, new_fiberid, new_redshift, new_mag_abs_r, new_mag_apa_r)),
               fmt="%d,%d,%d,%.4f,%.4f,%.4f", delimiter=',', newline='\n',
               header='mjd,plate,fiberid,redshift,mag_absolute_petro_r, mag_obs_petro_r')
