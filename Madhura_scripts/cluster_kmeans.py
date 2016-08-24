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
n_clusters = 3
from sklearn.cluster import KMeans
km = KMeans(n_clusters=n_clusters, max_iter=300, n_init=12, init="random")
km.fit(data)
labels = km.predict(data)
print labels.astype(float)
colors = labels.astype(float)

xax = "4000 Angstrom break"
yax = "log10(EWidth H_alpha)"
plt.figure(1)
plt.scatter(data[xax], data[yax], c=labels.astype(float), s=2, edgecolors='none')
plt.title("K-means clustering on %i dimensions"%(len(subset)))
plt.xlabel(xax)
plt.ylabel(yax)
plt.savefig("cluster_KMeans_%i.png"%(n_clusters),format="png")
plt.show()
