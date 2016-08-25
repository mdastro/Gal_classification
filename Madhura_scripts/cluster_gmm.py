from numpy import log10, float, linspace
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.mixture import GMM

data = pd.read_csv('../Dataset/clean_data.csv')

use_vdoiii = False
use_4000A  = False # otherwise NII/H_alpha

# clean further
if use_vdoiii:
    data = data[data["vd_oiii"]>0]

# ratios
data["log10([OIII]/H_beta)"]  = log10(data["OIII"]/data["H_beta"])
data["log10(EWidth H_alpha)"] = log10(data["EW_H_alpha"])
if use_4000A:
    data.rename(columns={"dn4000_synth":"4000 Angstrom break"}, inplace=True)
else:
    data["log10([NII]/H_alpha)"]  = log10(data["NII"]/data["H_alpha"])

# subset
if use_vdoiii:
    if use_4000A:
        subset = ["log10(EWidth H_alpha)", "log10([OIII]/H_beta)", "4000 Angstrom break", "vd_oiii"]
    else:
        subset = ["log10(EWidth H_alpha)", "log10([OIII]/H_beta)", "log10([NII]/H_alpha)", "vd_oiii"]
elif use_4000A:
    subset = ["log10(EWidth H_alpha)", "log10([OIII]/H_beta)", "4000 Angstrom break"]
else:
    subset = ["log10(EWidth H_alpha)", "log10([OIII]/H_beta)", "log10([NII]/H_alpha)"]
n_dim = len(subset)
data = data[subset]

print data

# clustering
for n_comp in range(2,4):
    print "Beginning clustering into %i components ..."%n_comp
    gmm = GMM(n_components=n_comp, covariance_type='full', n_init=2, verbose=2)
    labels = gmm.fit_predict(data)
    print "... finished clustering"

    unique_labels = set(labels)
    n_unique = len(unique_labels)
    print('Estimated number of clusters: %d' % n_unique)

    aic = gmm.aic(data)
    print "AIC = %f"%aic
    bic = gmm.bic(data)
    print "BIC = %f"%bic

    #colors = plt.cm.rainbow
    colors = plt.cm.viridis

    # plot
    f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15,5))
    #f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))
    plt.suptitle("GMM clustering on %i dimensions"%(n_dim))

    ax1.set_title("WHAN")
    y_axis = "log10(EWidth H_alpha)"
    if use_4000A:
        x_axis = "4000 Angstrom break"
    else:
        x_axis = "log10([NII]/H_alpha)"
    ax1.set_xlabel(x_axis)
    ax1.set_ylabel(y_axis)
    for i in unique_labels:
        data_plot = data[labels==i]
        start = float(i)*2.95/(n_unique)
        cmap = sns.cubehelix_palette(8, start=start, as_cmap=True)
        sns.kdeplot(data_plot[x_axis], data_plot[y_axis], cmap=cmap, shade=True, shade_lowest=False, ax=ax1)
    #ax1.scatter(data[x_axis], data[y_axis], c=labels, cmap=colors, s=2, edgecolors='none')


    if use_4000A:
        ax2.set_title("not-quite BPT")
        x_axis = "4000 Angstrom break"
    else:
        ax2.set_title("BPT")
        x_axis = "log10([NII]/H_alpha)"
    y_axis = "log10([OIII]/H_beta)"
    ax2.set_xlabel(x_axis)
    ax2.set_ylabel(y_axis)
    for i in unique_labels:
        data_plot = data[labels==i]
        start = float(i)*2.9/(n_unique)
        cmap = sns.cubehelix_palette(8, start=start, as_cmap=True)
        sns.kdeplot(data_plot[x_axis], data_plot[y_axis], cmap=cmap, shade=True, shade_lowest=False, ax=ax2)
    #ax2.scatter(data[x_axis], data[y_axis], c=labels, cmap=colors, s=2, edgecolors='none')
    if not use_4000A:
        [xleft, xright] = ax2.get_xlim()
        kauffman_x = linspace(xleft, min(-0.2,xright), 20)
        kauffman_y = 0.61 / (kauffman_x - 0.05) + 1.3
        ax2.plot(kauffman_x, kauffman_y, 'k-')
        kewley_x = linspace(xleft, min(0.2,xright), 20)
        kewley_y = 0.61 / (kewley_x - 0.47) + 1.19
        ax2.plot(kewley_x, kewley_y, 'k--')


    ax3.set_title("new")
    y_axis = "log10([OIII]/H_beta)"
    if use_vdoiii:
        x_axis = "vd_oiii"
    else:
        x_axis = "log10(EWidth H_alpha)"
    ax3.set_xlabel(x_axis)
    ax3.set_ylabel(y_axis)
    for i in unique_labels:
        data_plot = data[labels==i]
        start = float(i)*2.9/(n_unique)
        cmap = sns.cubehelix_palette(8, start=start, as_cmap=True)
        sns.kdeplot(data_plot[x_axis], data_plot[y_axis], cmap=cmap, shade=True, shade_lowest=False, ax=ax3)
    #ax3.scatter(data[x_axis], data[y_axis], c=labels, cmap=colors, s=2, edgecolors='none')


    plt.savefig("cluster_GMM_nc%i_nd%i.pdf"%(n_comp,n_dim),format="pdf")
    plt.show()
    
