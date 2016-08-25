from numpy import log10, float, linspace
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.mixture import DPGMM

data = pd.read_csv('../Dataset/clean_data.csv')
print data

use_vdoiii = False

# clean further
#toclean = ["H_beta", "OIII"]
#for feat in toclean:
#    data = data[data[feat] > -900]
if use_vdoiii:
    data = data[data["vd_oiii"]>0]

# ratios
data["log10([OIII]/H_beta)"]  = log10(data["OIII"]/data["H_beta"])
data["log10([NII]/H_alpha)"]  = log10(data["NII"]/data["H_alpha"])
data["log10(EWidth H_alpha)"] = log10(data["EW_H_alpha"])
data.rename(columns={"dn4000_synth":"4000 Angstrom break"}, inplace=True)

# subset
if use_vdoiii:
    subset = ["log10(EWidth H_alpha)", "log10([OIII]/H_beta)", "log10([NII]/H_alpha)", "vd_oiii"]
else:
    subset = ["log10(EWidth H_alpha)", "log10([OIII]/H_beta)", "log10([NII]/H_alpha)"]
#subset = ["log10(EWidth H_alpha)", "log10([OIII]/H_beta)", "log10([NII]/H_alpha)", "4000 Angstrom break", "vd_oiii"]
n_dim = len(subset)
data = data[subset]

print data

# clustering
print "Beginning clustering ..."
dpgmm = DPGMM(n_components=4, covariance_type='full', alpha=100., tol=1.e-4, n_iter=20, verbose=2)
labels = dpgmm.fit_predict(data)
print "... finished clustering"

unique_labels = set(labels)
n_unique = len(unique_labels)
print('Estimated number of clusters: %d' % n_unique)

aic = dpgmm.aic(data)
print "AIC = %f"%aic
bic = dpgmm.bic(data)
print "BIC = %f"%bic

colors = plt.cm.viridis

# plot
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))
#f, (ax1, ax2, ax3) = plt.subplots(1, 3)
plt.suptitle("DPGMM clustering on %i dimensions"%(n_dim))

y_axis = "log10(EWidth H_alpha)"
x_axis = "log10([NII]/H_alpha)"
ax1.scatter(data[x_axis], data[y_axis], c=labels, cmap=colors, s=2, edgecolors='none')
ax1.set_xlabel(x_axis)
ax1.set_ylabel(y_axis)
ax1.set_title("WHAN")

y_axis = "log10([OIII]/H_beta)"
x_axis = "log10([NII]/H_alpha)"
ax2.scatter(data[x_axis], data[y_axis], c=labels, cmap=colors, s=2, edgecolors='none')
ax2.set_xlabel(x_axis)
ax2.set_ylabel(y_axis)
ax2.set_title("BPT")

[xleft, xright] = ax2.get_xlim()
kauffman_x = linspace(xleft, min(-0.2,xright), 20)
kauffman_y = 0.61 / (kauffman_x - 0.05) + 1.3
ax2.plot(kauffman_x, kauffman_y, 'k-')
kewley_x = linspace(xleft, min(0.2,xright), 20)
kewley_y = 0.61 / (kewley_x - 0.47) + 1.19
ax2.plot(kewley_x, kewley_y, 'k--')


"""
y_axis = "log10([OIII]/H_beta)"
x_axis = "vd_oiii"
#x_axis = "4000 Angstrom break"
ax3.scatter(data[x_axis], data[y_axis], c=labels, cmap=colors, s=2, edgecolors='none')
ax3.set_xlabel(x_axis)
ax3.set_ylabel(y_axis)
ax3.set_title("new")
"""

plt.savefig("cluster_DPGMM_%i.png"%(n_dim),format="png")
plt.show()
