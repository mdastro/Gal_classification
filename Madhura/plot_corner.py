from numpy import log10, float
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
data["log10([OIII]/H_beta)"] = log10(data["OIII"]/data["H_beta"])
data["log10([NII]/H_alpha)"] = log10(data["NII"]/data["H_alpha"])
data["log10(EW Halpha)"]     = log10(data["EW_H_alpha"])

# subset
#subset = ["EW_H_alpha", "log10([OIII]/H_beta)", "log10([NII]/H_alpha)", "dn4000_synth"]
#subset = ["EW_H_alpha", "log10([OIII]/H_beta)", "dn4000_synth"]
subset = ["log10(EW Halpha)", "log10([OIII]/H_beta)", "dn4000_synth"]
#subset = ["EW_H_alpha", "log10([OIII]/H_beta)", "log10([NII]/H_alpha)"]
data = data[subset]
#data = data[data["EW_H_alpha"]<60] # just for cleaner plotting
print data

# plot
"""
g = sns.PairGrid(data)
g.map_offdiag(sns.kdeplot, n_levels=6)
g.map_diag(sns.kdeplot, legend=False, shade=True)
plt.savefig("agn_cornerplot.png",format="png")
"""

# clustering for 4
from sklearn.cluster import KMeans
km = KMeans(n_clusters=3, max_iter=300, n_init=12, init="random")
km.fit(data)
labels = km.predict(data)
print labels.astype(float)
xax = "dn4000_synth"
yax = "log10(EW Halpha)"
plt.figure(1)
plt.scatter(data[xax], data[yax], c=labels.astype(float), )
plt.title("KMeans clustering on %i dimensions"%(len(subset)))
plt.xlabel(xax)
plt.ylabel(yax)
plt.savefig("cluster_KMeans.png",format="png")
plt.show()
