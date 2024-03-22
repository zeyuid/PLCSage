import seaborn as sns
import numpy as np
import matplotlib.pylab as plt
from scipy.io import loadmat
import math




# data = loadmat("./comm-Yang/comm_wincc_snap_20211116_MSB0_1.mat")
data = loadmat("./comm-Yang/comm_wincc_snap_20211116_MSB0_0.mat")
# data = loadmat("./comm-Yang/comm_wincc_snap_20211223_MSB0_1.mat")
# data = loadmat("./comm-Yang/comm_wincc_snap_20211223_MSB0_0.mat")



PII = data["I_1"]
PIO = data["Q_1"]
# SCADA_1 = data["SCADA_1"]
# SCADA_2 = data["SCADA_2"]

SCADA = np.hstack((data["SCADA_1"], data["SCADA_2"], data["SCADA_3"], data["SCADA_4"], data["SCADA_5"]))

# % omit the tower pressure measurement
PII[0, 848:863] = 0
# %  omit the useless feedback,
PII[0, 896:] = 0
PIO[0, 608:] = 0
SCADA[0, 352:383] = 0




save_fig_path = "/Users/magnolia/Dropbox/Zeyu/Stealthy_Attack/figures/"



col_num = 64

PIImemory_size = math.ceil(PII.size/col_num)*col_num
PII_arrange = np.zeros((1, PIImemory_size))
PIOmemory_size = math.ceil(PIO.size/col_num)*col_num
PIOmemory_size = PIImemory_size
PIO_arrange = np.zeros((1, PIOmemory_size))

SCADAmemory_size = math.ceil(SCADA.size/col_num)*col_num
SCADA_arrange = np.zeros((1, SCADAmemory_size))


PII_arrange[0, 0:PII.size] = PII[0,:]
PIO_arrange[0, 0:PIO.size] = PIO[0,:]
SCADA_arrange[0, 0:SCADA.size] = SCADA[0,:]


PIIsizea,PIIsizeb = PII_arrange.shape
PIOsizea,PIOsizeb = PIO_arrange.shape
SCADAsizea,SCADAsizeb = SCADA_arrange.shape





PII_arrange = np.reshape(PII_arrange, (int(PIIsizea*PIIsizeb/col_num), col_num))
PIO_arrange = np.reshape(PIO_arrange, (int(PIOsizea*PIOsizeb/col_num), col_num))
SCADA_arrange = np.reshape(SCADA_arrange, (int(SCADAsizea*SCADAsizeb/col_num), col_num))



# f, ax = plt.subplots(figsize=(6, 5))
# h = sns.heatmap(data=PII_arrange[0:14, :], ax=ax, vmin=0, vmax=1, cmap="RdBu", center=0., linewidths=0.3, cbar=False,
#                 xticklabels=(),
#                 yticklabels=('$\mathtt{I(0,8)}$', '$\mathtt{I(8,8)}$', '$\mathtt{I(16,8)}$', '$\mathtt{I(24,8)}$',
#                              '$\mathtt{I(32,8)}$', '$\mathtt{I(40,8)}$', '$\mathtt{I(48,8)}$', '$\mathtt{I(56,8)}$',
#                              '$\mathtt{I(64,8)}$', '$\mathtt{I(72,8)}$', '$\mathtt{I(80,8)}$', '$\mathtt{I(88,8)}$',
#                              '$\mathtt{I(96,8)}$', '$\mathtt{I(104,8)}$'))
f, ax = plt.subplots(figsize=(6, 2))
h = sns.heatmap(data=PII_arrange[10:15, :], ax=ax, vmin=0, vmax=1, cmap="RdBu", center=0., linewidths=0.3, cbar=False,
                annot=False, fmt='.3f',annot_kws={'rotation':90,"fontsize":4},
                xticklabels=('$\mathtt{0}$', '$\mathtt{8}$', '$\mathtt{16}$', '$\mathtt{24}$',
                             '$\mathtt{32}$', '$\mathtt{40}$', '$\mathtt{48}$', '$\mathtt{56}$','$\mathtt{64}$' ),
                yticklabels=('$\mathtt{I_{80}^8}$', '$\mathtt{I_{88}^8}$', '$\mathtt{I_{96}^8}$', '$\mathtt{I_{104}^8}$',
                             '$\mathtt{I_{112}^8}$'))


plt.xticks(range(0,65,8),rotation=0)  # X轴范围0-400，刻度间隔为15，标签旋转45°

# 单独设置y轴或x轴刻度的字体大小, 调整字体方向
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, weight="bold")
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, weight="bold")


# # 设置X轴标签的字体大小和字体颜色
# # ax.set_xlabel('X Label',fontsize=10)
# ax.set_xlabel('PII/PIO Tables', family='sans-serif', weight="normal")
#
# # 设置Y轴标签的字体大小和字体颜色
# # ax.set_ylabel('Y Label',fontsize=15, color='r')
# ax.set_ylabel('SCADA Logging Traffic', family='sans-serif', weight="normal")


plt.tight_layout()
plt.savefig(save_fig_path + "PII_bit_entropy_LSB0.pdf")
plt.show()


# f, ax = plt.subplots(figsize=(6, 5))
# h = sns.heatmap(data=PIO_arrange[0:14, :], ax=ax, vmin=0, vmax=1, cmap="RdBu", center=0., linewidths=0.3, cbar=False,
#                 xticklabels=(),
#                 yticklabels=('$\mathtt{O(0,8)}$', '$\mathtt{O(8,8)}$', '$\mathtt{O(16,8)}$', '$\mathtt{O(24,8)}$',
#                              '$\mathtt{O(32,8)}$', '$\mathtt{O(40,8)}$', '$\mathtt{O(48,8)}$', '$\mathtt{O(56,8)}$',
#                              '$\mathtt{O(64,8)}$', '$\mathtt{O(72,8)}$', '$\mathtt{O(80,8)}$', '$\mathtt{O(88,8)}$',
#                              '$\mathtt{O(96,8)}$', '$\mathtt{O(104,8)}$'))
f, ax = plt.subplots(figsize=(6, 1.7))
h = sns.heatmap(data=PIO_arrange[7:11, :], ax=ax, vmin=0, vmax=1, cmap="RdBu", center=0., linewidths=0.3, cbar=False,
                annot=False, fmt='.3f',annot_kws={'rotation':90,"fontsize":4},
                xticklabels=('$\mathtt{0}$', '$\mathtt{8}$', '$\mathtt{16}$', '$\mathtt{24}$',
                             '$\mathtt{32}$', '$\mathtt{40}$', '$\mathtt{48}$', '$\mathtt{56}$', '$\mathtt{64}$'),
                yticklabels=('$\mathtt{O_{56}^8}$', '$\mathtt{O_{64}^8}$', '$\mathtt{O_{72}^8}$', '$\mathtt{O_{80}^8}$',))

plt.xticks(range(0,65,8),rotation=0)  # X轴范围0-400，刻度间隔为15，标签旋转45°

# 单独设置y轴或x轴刻度的字体大小, 调整字体方向
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, weight="bold")
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, weight="bold")


# # 设置X轴标签的字体大小和字体颜色
# # ax.set_xlabel('X Label',fontsize=10)
# ax.set_xlabel('PII/PIO Tables', family='sans-serif', weight="normal")
#
# # 设置Y轴标签的字体大小和字体颜色
# # ax.set_ylabel('Y Label',fontsize=15, color='r')
# ax.set_ylabel('SCADA Logging Traffic', family='sans-serif', weight="normal")



plt.tight_layout()
plt.savefig(save_fig_path + "PIO_bit_entropy_LSB0.pdf")
plt.show()



f, ax = plt.subplots(figsize=(6, 4))
h = sns.heatmap(data=SCADA_arrange[[0,1,2,3,4,5,6,7,8,9,13], :], ax=ax, vmin=0, vmax=1, cmap="RdBu", center=0., linewidths=0.3, cbar=False,
                annot=False, fmt='.3f',annot_kws={'rotation':90,"fontsize":4},
                xticklabels=('$\mathtt{0}$', '$\mathtt{8}$', '$\mathtt{16}$', '$\mathtt{24}$',
                             '$\mathtt{32}$', '$\mathtt{40}$', '$\mathtt{48}$', '$\mathtt{56}$', '$\mathtt{64}$'),
                # yticklabels=('$\mathtt{D(0,8)}$', '$\mathtt{D(8,8)}$', '$\mathtt{D(16,8)}$', '$\mathtt{D(24,8)}$',
                #              '$\mathtt{D(32,8)}$', '$\mathtt{D(40,8)}$', '$\mathtt{D(48,8)}$', '$\mathtt{D(56,8)}$',
                #              '$\mathtt{D(64,8)}$', '$\mathtt{D(72,8)}$', '$\mathtt{D(80,8)}$', '$\mathtt{D(88,8)}$',
                #              '$\mathtt{D(96,8)}$', '$\mathtt{D(104,8)}$')
                yticklabels=('$\mathtt{D_0^8}$', '$\mathtt{D_8^8}$', '$\mathtt{D_{16}^8}$', '$\mathtt{D_{24}^8}$',
                             '$\mathtt{D_{32}^8}$', '$\mathtt{D_{40}^8}$', '$\mathtt{D_{72}^8}$', '$\mathtt{D_{80}^8}$', 
                             '$\mathtt{D_{88}^8}$', '$\mathtt{D_{96}^8}$', '$\mathtt{D_{104}^8}$'))

plt.xticks(range(0,65,8),rotation=0)  # X轴范围0-400，刻度间隔为15，标签旋转45°

# 单独设置y轴或x轴刻度的字体大小, 调整字体方向
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, weight="bold")
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, weight="bold")


# # 设置X轴标签的字体大小和字体颜色
# # ax.set_xlabel('X Label',fontsize=10)
# ax.set_xlabel('PII/PIO Tables', family='sans-serif', weight="normal")
#
# # 设置Y轴标签的字体大小和字体颜色
# # ax.set_ylabel('Y Label',fontsize=15, color='r')
# ax.set_ylabel('SCADA Logging Traffic', family='sans-serif', weight="normal")

plt.tight_layout()
plt.savefig(save_fig_path + "SCADA_bit_entropy_LSB0.pdf")
plt.show()

