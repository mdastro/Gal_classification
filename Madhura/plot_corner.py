from numpy import log
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
data["log([OIII]/H_beta)"] = log(data["OIII"]/data["H_beta"])
data["log([NII]/H_alpha)"] = log(data["NII"]/data["H_alpha"])
print data

# subset
subset = ["EW_H_alpha", "log([OIII]/H_beta)", "log([NII]/H_alpha)", "dn4000_synth"]
#subset = ["EW_H_alpha", "log([OIII]/H_beta)", "log([NII]/H_alpha)"]
data = data[subset]
data = data[data["EW_H_alpha"]<60] # just for cleaner plotting
print data

# plot
g = sns.PairGrid(data)
g.map_offdiag(sns.kdeplot, n_levels=6)
g.map_diag(sns.kdeplot, legend=False, shade=True)
plt.savefig("agn_cornerplot.png",format="png")


# clustering for BPT


# clustering for WHAN


# clustering for 3


# clustering for more
