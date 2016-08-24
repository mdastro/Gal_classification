
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
  ind_5 = data[5] < threshold
  ind_6 = data[6] < threshold
  ind_7 = data[7] < threshold
  ind_8 = data[8] < threshold
  ind_9 = data[9] < threshold
  
  failed_5 = ind_5.sum()
  failed_6 = ind_6.sum()
  failed_7 = ind_7.sum()
  failed_8 = ind_8.sum()
  failed_9 = ind_9.sum()
  
  ind = ind_5 + ind_6 + ind_7 + ind_8 + ind_9
  
  print('Number of samples in raw data   = %6d' % N_tot)
  print('Number of samples in clean data = %6d' % N_tot_2)
  print('Difference                      = %6d' % (N_tot - N_tot_2))
  print('Difference computed from raw    = %6d' % (ind.sum()))
  print()
  print('  Feature    Failed samples    Ratio')
  print('---------------------------------------')
  print('   H_alpha     %7d        ' % failed_5 + '{:6.2%}'.format(failed_5/N_tot))
  print('EW_H_alpha     %7d        ' % failed_6 + '{:6.2%}'.format(failed_6/N_tot))
  print('    H_beta     %7d        ' % failed_7 + '{:6.2%}'.format(failed_7/N_tot))
  print('      OIII     %7d        ' % failed_8 + '{:6.2%}'.format(failed_8/N_tot))
  print('       NII     %7d        ' % failed_9 + '{:6.2%}'.format(failed_9/N_tot))
  print()
  return
  
  
count()
