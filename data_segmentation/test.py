

import numpy as np
import struct,pickle
import seaborn as sns
import matplotlib.pylab as plt
from scipy.io import loadmat
import math
import re
from utils import *


def test_entropy(PLCbins_I):

    # obtain the entropy of each bit
    bins_item_num = PLCbins_I
    bins_entropy_I = np.zeros([1, bins_item_num.shape[1]])
    for bin_id in range(bins_item_num.shape[1]):
        bins_entropy_I[0, bin_id] = non_zeros_ratio(bins_item_num[0:, bin_id:bin_id + 1])
    
    return bins_entropy_I




x = np.arange(0, 20, 0.1)
y = np.zeros([1, len(x)])

bins_total = []

for i in range(0, len(x)):
    y[0][i] = 1000 * (math.sin(x[i])+1)
    # y[0][i] =  (x[i]*x[i]+1)
    
    # hex_num = struct.pack('!h', int(y[0][i]))
    # pattern = re.compile("x([0-9a-f]+)")
    # hexvalues = pattern.findall(str(hex_num))
    # hex_y.append(hexvalues)
    
    bin_y = []
    # for j in range(2):
    byte2binaries = bin(int(y[0][i]))[2:]
    byte2binaries = format(byte2binaries, '0>{}'.format(16))  # append the higher bits
    for bin_id in range(len(byte2binaries)):
        bin_y.append(int(byte2binaries[bin_id]))
    bins_total.append(bin_y)

binaries = np.array(bins_total)

binaries_diff = np.zeros([binaries.shape[0]-1, binaries.shape[1]])
for i in range(1, binaries.shape[0]):
    binaries_diff[i-1] = abs(binaries[i, :] - binaries[i-1, :]) 

bins_entropy_I = test_entropy(np.array(bins_total))
bins_entropy_I_diff = test_entropy(np.array(binaries_diff))


# a = [[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]]
# bit_significate = np.array(a)/15
f, ax = plt.subplots(figsize=(6, 2))
h = sns.heatmap(data=bins_entropy_I_diff, ax=ax, vmin=0, vmax=1, cmap="RdBu", 
                annot=True, fmt='.3f',annot_kws={'rotation':90,"fontsize":12},
                center=0., linewidths=0.3, xticklabels=(),yticklabels=(),cbar=False)
plt.tight_layout()
# plt.savefig(save_fig_path + "bit_significance4.pdf")
plt.show()

