import seaborn as sns
import numpy as np
import matplotlib.pylab as plt
from scipy.io import loadmat

# Using the Conditional Mutual Information
data = loadmat('/Users/magnolia/Documents/MATLAB/StealthyAttack/command_sensor_coor.mat')
# Using the Mutual Information
# data = loadmat('/Users/magnolia/Documents/MATLAB/StealthyAttack/command_sensor_coor_MI.mat')

command_sensor_coor = data["command_sensor_coor"]


save_fig_path = "/Users/magnolia/Dropbox/Zeyu/Stealthy_Attack/figures/"

# plt.rc('font', family='Times New Roman')
# plt.rcParams["font.weight"] = "bold"
# plt.rcParams["axes.labelweight"] = "bold"




f, ax = plt.subplots(figsize=(10, 2))

# cbar_ax = f.add_axes([1.22, .15, .03, .38])
cbar_ax = f.add_axes([.87, .17, .03, .63])

h = sns.heatmap(data=command_sensor_coor, ax=ax, vmin=-0, vmax=1, cmap="RdBu", center=0, linewidths=0.3, square=True,
                cbar=True, cbar_ax=cbar_ax,
                # xticklabels=(
                # '$\mathtt{I(88,2)}$', '$\mathtt{I(90,2)}$', '$\mathtt{I(92,2)}$', '$\mathtt{I(94,2)}$',
                # '$\mathtt{I(96,2)}$', '$\mathtt{I(98,2)}$', '$\mathtt{I(100,2)}$', '$\mathtt{I(102,2)}$',
                # '$\mathtt{I(104,2)}$', '$\mathtt{I(108,2)}$', '$\mathtt{I(110,2)}$'),
                # xticklabels=(
                # '$y_{4}$', '$y_{5}$', '$y_{11}$', '$y_{2}$',
                # '$y_{6}$', '$y_{8}$', '$y_{9}$', '$y_{10}$',
                # '$y_{7}$', '$y_{1}$', '$y_{3}$'),
                xticklabels=(
                '$y_{1}$', '$y_{2}$', '$y_{3}$', '$y_{4}$',
                '$y_{5}$', '$y_{6}$', '$y_{7}$', '$y_{8}$',
                '$y_{9}$', '$y_{10}$', '$y_{11}$'),
                yticklabels=(
                '$u_{2}$', '$u_{3}$'),
                annot=True, fmt='.1f',annot_kws={"size":15})

cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=15)

cbar.set_ticks([0, .5, 1.0 ])
cbar.set_ticklabels(['0.0', '0.5', '1.0'])




# plt.xlabel('PII/PIO tables', family='sans-serif', weight="normal")
# plt.ylabel('SCADA logging traffic', family='sans-serif', weight="normal")


# # 设置Axes的标题
# ax.set_title('Correlation between features', fontsize=18, position=(0.5,1.05))

# # 将y轴或x轴进行逆序
# ax.invert_yaxis()
# # ax.invert_xaxis()

# 设置X轴标签的字体大小和字体颜色
# ax.set_xlabel('X Label',fontsize=10)
ax.set_xlabel('Sensor readings', family='sans-serif', weight="normal", fontsize=18)

# 设置Y轴标签的字体大小和字体颜色
# ax.set_ylabel('Y Label',fontsize=15, color='r')
ax.set_ylabel('Commands', family='sans-serif', weight="normal", fontsize=18)

# # 设置坐标轴刻度的字体大小
# ax.tick_params(axis='y', labelsize=8) # y轴


# 将x轴刻度放置在top位置的几种方法
# ax.xaxis.set_ticks_position('top')
ax.xaxis.tick_top()
# ax.tick_params(axis='x',labelsize=6, colors='b', labeltop=True, labelbottom=False) # x轴

# 修改tick的字体颜色
ax.tick_params(axis='x', colors='k') # x轴


# 单独设置y轴或x轴刻度的字体大小, 调整字体方向
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, weight="bold", fontsize=18)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha="left",  weight="bold", fontsize=18)
# ax.set_xticklabels(ax.get_xticklabels(), rotation=-90)


plt.xticks(range(11), )

# plt.tight_layout()
f.tight_layout(rect=[0, 0, .94, 1])
plt.savefig(save_fig_path + "command_sensor_heatmap_CMI.pdf")
plt.show()
