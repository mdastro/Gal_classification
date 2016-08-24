from numpy import log10, float
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

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
print "Beginning clustering ..."
db = DBSCAN(eps=0.2, min_samples=100).fit(data)
print "... finished clustering"
labels = db.labels_
print labels.astype(float)
unique_labels = set(labels)
# number of clusters in labels, ignoring noise if present.
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
print('Estimated number of clusters: %d' % n_clusters)

# plot
xax = "4000 Angstrom break"
yax = "log10(EWidth H_alpha)"
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
#colors = labels.astype(float)
plt.figure(1)
plt.scatter(data[xax], data[yax], c=colors, s=2, edgecolors='none')
plt.title("DBSCAN clustering on %i dimensions"%(len(subset)))
plt.xlabel(xax)
plt.ylabel(yax)
plt.savefig("cluster_DBSCAN_%i.png"%(n_clusters),format="png")
plt.show()
