from numpy import log10
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('../Dataset/clean_data.csv')
print data

# clean further
toclean = ["H_beta", "OIII"]
for feat in toclean:
    data = data[data[feat] > -900]
data = data[data["vd_oiii"]>0]
data = data[data["vd_nii"]>0]

# ratios
data["log10([OIII]/H_beta)"] = log10(data["OIII"]/data["H_beta"])
data["log10([NII]/H_alpha)"] = log10(data["NII"]/data["H_alpha"])
data["log10(EW Halpha)"]     = log10(data["EW_H_alpha"])
data.rename(columns={"dn4000_synth":"4000 Angstrom break"}, inplace=True)

# subset
#subset = ["log10(EW Halpha)", "log10([OIII]/H_beta)", "log10([NII]/H_alpha)", "4000 Angstrom break", "vd_Halpha", "vd_Hbeta", "vd_nii", "vd_oiii"]
subset = ["log10(EW Halpha)", "log10([OIII]/H_beta)", "log10([NII]/H_alpha)", "4000 Angstrom break", "vd_oiii", "vd_nii"]
data = data[subset]
print data

# plot
g = sns.PairGrid(data)
g.map_offdiag(sns.kdeplot, n_levels=6)
g.map_diag(sns.kdeplot, legend=False, shade=True)
plt.savefig("agn_cornerplot.png",format="png")

