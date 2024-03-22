import seaborn as sns
import numpy as np
import matplotlib.pylab as plt
from scipy.io import loadmat

# data = loadmat("./comm-Yang/SCADA_PII_coor_wrong.mat")
# data = loadmat("./comm-Yang/SCADA_PII_coor.mat")
data = loadmat("./comm-Yang/SCADA_PII_coor_20211116.mat")
# data = loadmat("./comm-Yang/SCADA_PII_coor_20211116_wrong.mat")


SCADA_PIIO_coor = data["SCADA_PIIO_coor"]

save_fig_path = "/Users/magnolia/Dropbox/Stealthy_Attack/figures/"


a = [[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]]
bit_significate = np.array(a)/15
f, ax = plt.subplots(figsize=(8, 2))
h = sns.heatmap(data=bit_significate, ax=ax, vmin=0, vmax=1, cmap="RdBu_r", center=0., linewidths=0.3, xticklabels=(),yticklabels=(),cbar=False)
plt.tight_layout()
# plt.savefig(save_fig_path + "bit_significance4.pdf")
plt.show()





bit_significate[0] = bit_significate[0][::-1]
f, ax = plt.subplots(figsize=(8, 2))
h = sns.heatmap(data=bit_significate, ax=ax, vmin=0, vmax=1, cmap="RdBu_r", center=0., linewidths=0.3, xticklabels=(),yticklabels=(),cbar=False)
plt.tight_layout()
# plt.savefig(save_fig_path + "bit_significance1.pdf")
plt.show()




a = [[8,9,10,11,12,13,14,15, 0,1,2,3,4,5,6,7]]
bit_significate = np.array(a)/15
f, ax = plt.subplots(figsize=(8, 2))
h = sns.heatmap(data=bit_significate, ax=ax, vmin=0, vmax=1, cmap="RdBu_r", center=0., linewidths=0.3, xticklabels=(),yticklabels=(),cbar=False)
plt.tight_layout()
# plt.savefig(save_fig_path + "bit_significance2.pdf")
plt.show()


bit_significate[0] = bit_significate[0][::-1]
# a = [[8,9,10,11,12,13,14,15, 0,1,2,3,4,5,6,7]]
# bit_significate = np.array(a)/15
f, ax = plt.subplots(figsize=(8, 2))
h = sns.heatmap(data=bit_significate, ax=ax, vmin=0, vmax=1, cmap="RdBu_r", center=0., linewidths=0.3, xticklabels=(),yticklabels=(),cbar=False)
plt.tight_layout()
# plt.savefig(save_fig_path + "bit_significance3.pdf")
plt.show()



f, ax = plt.subplots(figsize=(6, 5))
h = sns.heatmap(data=bit_significate, ax=ax, vmin=0, vmax=1, cmap="RdBu_r", center=0., linewidths=0.3, xticklabels=(),yticklabels=())
plt.tight_layout()
# plt.savefig(save_fig_path + "bit_significance.pdf")
plt.show()
