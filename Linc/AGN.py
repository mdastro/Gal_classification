
def readCsv(name):
  f = open(name, 'r')
  stock = [line for line in f if line[0] != '#']
  stock = [[float(split) for split in line.split(',')] for line in stock]
  f.close()
  stock = np.array(stock).T
  return stock
    
def count():
  name  = 'data/raw_data.csv'
  name2 = 'data/clean_data.csv'
  data  = readCsv(name)
  data2 = readCsv(name2)
  N_tot = data.shape[1]
  N_tot = float(N_tot)
  N_tot_2 = data2.shape[1]
  
  threshold = -900.0
  ind_5  = data[5] < threshold
  ind_6  = data[6] < threshold
  ind_7  = data[7] < threshold
  ind_8  = data[8] < threshold
  ind_9  = data[9] < threshold
  ind_14 = data[14] < threshold
  ind_15 = data[15] < threshold
  ind_16 = data[16] < threshold
  ind_17 = data[17] < threshold
  
  failed_5  = ind_5.sum()
  failed_6  = ind_6.sum()
  failed_7  = ind_7.sum()
  failed_8  = ind_8.sum()
  failed_9  = ind_9.sum()
  failed_14 = ind_14.sum()
  failed_15 = ind_15.sum()
  failed_16 = ind_16.sum()
  failed_17 = ind_17.sum()
  
  ind = ind_5 + ind_6 + ind_7 + ind_8 + ind_9 + ind_14 + ind_15 + ind_16 + ind_17
  
  print 'Number of samples in raw data   = %6d' % N_tot
  print 'Number of samples in clean data = %6d' % N_tot_2
  print 'Difference                      = %6d' % (N_tot - N_tot_2)
  print 'Difference computed from raw    = %6d' % (ind.sum())
  print 
  print '  Feature    Failed samples    Ratio'
  print '---------------------------------------'
  print '   H_alpha     %7d        ' % failed_5 + '{:6.2%}'.format(failed_5/N_tot)
  print 'EW_H_alpha     %7d        ' % failed_6 + '{:6.2%}'.format(failed_6/N_tot)
  print '    H_beta     %7d        ' % failed_7 + '{:6.2%}'.format(failed_7/N_tot)
  print '      OIII     %7d        ' % failed_8 + '{:6.2%}'.format(failed_8/N_tot)
  print '       NII     %7d        ' % failed_9 + '{:6.2%}'.format(failed_9/N_tot)
  print '   OI_6300     %7d        ' % failed_14 + '{:6.2%}'.format(failed_14/N_tot)
  print '  OII_3727     %7d        ' % failed_15 + '{:6.2%}'.format(failed_15/N_tot)
  print '  SII_6717     %7d        ' % failed_16 + '{:6.2%}'.format(failed_16/N_tot)
  print '  SII_6731     %7d        ' % failed_17 + '{:6.2%}'.format(failed_17/N_tot)
  return

def clean(data):
  ind = data < -900.0
  ind = ind.sum(axis=0, dtype=bool)
  data = data.T[True - ind]
  print ind.sum()
  return data

def outClean():
  name1 = 'data/raw_data.csv'
  name2 = 'data/clean_data.csv'
  data = readCsv(name1)
  data = clean(data)
  f = open(name2, 'w')
  f.write('# plate,mjd,fiber_id,dn4000_obs,dn4000_synth,H_alpha,EW_H_alpha,H_beta,OIII,NII,vd_Halpha,vd_Hbeta,vd_nii,vd_oiii,oi_6300,oii_3727,sii_6717,sii_6731\n')
  for i in range(len(data)):
    line = data[i]
    f.write('%d,%d,%d,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n'\
      % (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], 
	 line[9], line[10], line[11], line[12], line[13], line[14], line[15], line[16], line[17]))
  f.close()
  return 
  

#count()
#outClean()
