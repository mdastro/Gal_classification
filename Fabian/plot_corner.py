import numpy
from numpy import log10, float
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from brute import BruteNN
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('../Dataset/clean_data.csv')
subset = ["dn4000_obs", "dn4000_synth", "H_alpha", "EW_H_alpha", "H_beta", "OIII", "NII", "vd_Halpha", "vd_Hbeta", "vd_nii", "vd_oiii"]

# clean further
toclean = ["H_beta", "OIII"]
for feat in toclean:
    data = data[data[feat] > -900]

# ratios
data["log10([OIII]/H_beta)"] = log10(data["OIII"]/data["H_beta"])
data["log10([NII]/H_alpha)"] = log10(data["NII"]/data["H_alpha"])
data["log10(EW Halpha)"]     = log10(data["EW_H_alpha"])
subset = ["log10(EW Halpha)", "log10([OIII]/H_beta)", "dn4000_synth"]

data["log10(NII/EW Halpha)"]     = log10(data["NII"]/data["EW_H_alpha"])
subset += ["log10(NII/EW Halpha)"]

data["log10(NII)"]     = log10(data["NII"])
subset += ["log10(NII)"]

data["(NII)"]     = (data["NII"])
subset += ["(NII)"]

print("Selecting columns: %s" % str(subset))
data = data[subset]
print data.head(10).to_string()

X = data.values
X = StandardScaler().fit_transform(X)
print X[0]


# cluster
print("Clustering ...")
km = KMeans(n_clusters=3, max_iter=500, n_init=12, init="random")
km.fit(X)
labels = km.predict(X)

# get best low-dimensional space
print("Searching for best combination ...")
knn = BruteNN(n_neighbors=3, n_selected_features=2, n_top_combinations=1, verbose=1)
knn.fit(X, labels.astype(numpy.int32))
best = knn.get_top_combinations()[0]
print("Best combination: %s" % str(best))

print data.columns[best[0]]
print data.columns[best[1]]
# plot best combination
print("Plotting ...")
plt.figure(1)
plt.scatter(X[:,best[0]], X[:,best[1]], c=labels.astype(float), )
plt.title("KMeans clustering vis on two selected dimensions")
plt.xlabel(str(data.columns[best[0]]))
plt.ylabel(str(data.columns[best[1]]))
plt.savefig("cluster_KMeans.png",format="png")
plt.show()
