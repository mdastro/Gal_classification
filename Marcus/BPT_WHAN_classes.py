def class_whan(xx,yy,EW_NII,SN,SN_min):
    """

      This routine classifies emission line galaxies in the
      WHAN diagram (CF+11) according to their boundaries, where
      xx = N2/Ha and yy = EW(Ha). The signal-to-noise of emission lines
      are also an input. It is necessary to be higher than a certain 
      threshold (SN_min).        


                              12/07/2014 - Marcus Costa-Duarte
    """
    #
    class_gal = 0.
    if SN[0] > SN_min and SN[1] >= SN_min: # Signal-to-noise criteria 
        # SF
        if xx <= -0.4 and yy > np.log10(3.):
            class_gal = 1.
        # sAGN
        if xx > -0.4 and yy > np.log10(6.):
            class_gal = 2.
        # wAGN
        if xx > -0.4 and yy >= np.log10(3.) and yy <= np.log10(6.):
            class_gal = 3.
        # retired
        if yy < np.log10(3.):
            class_gal = 4.
        # passive
        if yy <= np.log10(0.5) and EW_NII <= np.log10(0.5):
            class_gal = 5.
        # Any problem? NO classification?
        if class_gal == 0.:
            print 'PROBLEM - NO CLASSIFICATION'
            exit()
    return class_gal

def class_BPT_kauffmann_kewley(x, y):

    """

      This routine classifies emission line galaxies in the
      BPT diagram according to Kewley+03 and Kauffmann+01 boundaries, 
      where x = N2/Ha and y = O3/Hb. (No SN condiction here!)

      https://sites.google.com/site/agndiagnostics/home/bpt

                              12/07/2014 - Marcus Costa-Duarte
    """
    y_kauffmann = 0.61 / (x - 0.05) + 1.3
    y_kewley = 0.61 / (x - 0.47) + 1.19
    #
    class_BPT = 0
    if y <= y_kauffmann and y < y_kewley and x < 0.47: class_BPT = 1 # SF
    if y <= y_kauffmann and x < 0.05: class_BPT = 1 # SF
    if y >= y_kauffmann and y < y_kewley: class_BPT = 2 # Composite
    if y < y_kewley and x > 0.05 and x < 0.47: class_BPT = 2 # Composite
    if y > y_kewley and y >= y_kauffmann: class_BPT = 3 # AGN
    if x > 0.47: class_BPT = 3 # AGN

    # At the extreme left of the diagram, these curves cross each other, then...(rarely!)
    if y > y_kewley: class_BPT = 3 # AGN
    #
    if class_BPT == 0:
         print 'PROBLEM BPT_kauffmann_kewley CLASSIFICATION!'
         exit()
    return class_BPT
