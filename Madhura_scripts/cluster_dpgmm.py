from numpy import log10, float, linspace
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('../Dataset/clean_data.csv')
print data

# clean further
toclean = ["H_beta", "OIII"]
for feat in toclean:
    data = data[data[feat] > -900]

# ratios
data["log10([OIII]/H_beta)"]  = log10(data["OIII"]/data["H_beta"])
data["log10([NII]/H_alpha)"]  = log10(data["NII"]/data["H_alpha"])
data["log10(EWidth H_alpha)"] = log10(data["EW_H_alpha"])
data.rename(columns={"dn4000_synth":"4000 Angstrom break"}, inplace=True)

# subset
#subset = ["EW_H_alpha", "log10([OIII]/H_beta)", "log10([NII]/H_alpha)", "dn4000_synth"]
subset = ["log10(EWidth H_alpha)", "log10([OIII]/H_beta)", "4000 Angstrom break"]
data = data[subset]
print data

# clustering
n_components = 3
print "Beginning clustering ..."
from sklearn.mixture import DPGMM
dpgmm = DPGMM(n_components=n_components)
dpgmm.fit(data)
labels = dpgmm.predict(data)
print labels

print "... finished clustering"
aic = dpgmm.aic(data)
print "AIC = %f"%aic
bic = dpgmm.bic(data)
print "BIC = %f"%bic

#colors = plt.cm.Spectral(linspace(0, 1, n_components))
colors = labels.astype(float)
#print('Estimated number of clusters: %d' % n_clusters)

# plot
xax = "4000 Angstrom break"
yax = "log10(EWidth H_alpha)"
plt.figure(1)
plt.scatter(data[xax], data[yax], c=colors, s=2, edgecolors='none')
plt.title("DPGMM clustering on %i dimensions"%(len(subset)))
plt.xlabel(xax)
plt.ylabel(yax)
plt.savefig("cluster_DPGMM_%i.png"%(n_components),format="png")
plt.show()
