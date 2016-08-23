from numpy import log
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#data_full = pd.read_csv('../data/learning_parameters.csv')
data = pd.read_csv('Dataset/clean_data.csv')
print data

#clean
toclean = ["H_beta", "OIII"]
for feat in toclean:
    data = data[data[feat] > -900]
print data

#ratios
data["log([OIII]/H_beta)"] = log(data["OIII"]/data["H_beta"])
data["log([NII]/H_alpha)"] = log(data["NII"]/data["H_alpha"])
print data

# subset
subset = ["EW_H_alpha", "log([OIII]/H_beta)", "log([NII]/H_alpha)"]
data = data[subset]
print data

#plot
data = data[data["EW_H_alpha"]<60] # just for plotting
g = sns.PairGrid(data)
#g = g.map(sns.kdeplot)
g.map_offdiag(sns.kdeplot, n_levels=6)
g.map_diag(sns.kdeplot, legend=False, shade=True)
#ax = sns.pairplot(data, diag_kind="kde", diag_kws=dict(shade=True))
plt.savefig("agn_cornerplot.png",format="png")
#plt.show()


# clustering for BPT


# clustering for WHAN


# clustering for 3


# clustering for more
