import seaborn as sns
import numpy as np
import matplotlib.pylab as plt
from scipy.io import loadmat

# data = loadmat("./comm-Yang/SCADA_PII_coor_wrong.mat")
# data = loadmat("./comm-Yang/SCADA_PII_coor.mat")




def correlation_heatmap_analysis(SCADA_PIIO_coor, ytickname, xtickname, saving_name="", xlabel_name="", ylabel_name=""):
    f, ax = plt.subplots(figsize=(6, 5))
    h = sns.heatmap(data=SCADA_PIIO_coor, ax=ax, vmin=-0, vmax=1.0, cmap="RdBu", center=0, linewidths=0.3, square=True,
                    xticklabels=(
                        '$\mathtt{-0.9}$', '$\mathtt{-0.8}$', '$\mathtt{-0.7}$', '$\mathtt{-0.6}$',
                        '$\mathtt{-0.5}$', '$\mathtt{-0.4}$', '$\mathtt{-0.3}$', '$\mathtt{-0.2}$',
                        '$\mathtt{-0.1}$'), 
                    yticklabels=(
                        '$\mathtt{0.1}$', '$\mathtt{0.2}$', '$\mathtt{0.3}$',
                        '$\mathtt{0.4}$', '$\mathtt{0.5}$', '$\mathtt{0.6}$', '$\mathtt{0.7}$',
                        '$\mathtt{0.8}$', '$\mathtt{0.9}$'),
                    annot=True, fmt='.2f')
    

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=11)

    cbar.set_ticks([0, .5, 1.0 ])
    cbar.set_ticklabels(['0.0', '0.5', '1.0'])

    ax.set_xlabel('PII/PIO Tables', family='sans-serif', weight="normal")
    ax.set_ylabel('SCADA Logging Traffic', family='sans-serif', weight="normal")

    # ax.xaxis.tick_top()
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, weight="bold", fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, weight="bold", fontsize=11)

    if not (xlabel_name == ""):
        ax.set_xlabel(xlabel_name, family='sans-serif', weight="normal", fontsize=14)
        ax.set_ylabel(ylabel_name, family='sans-serif', weight="normal", fontsize=14)

    plt.tight_layout()
    if not (saving_name == ""):
        plt.savefig(saving_name + ".pdf")
    plt.show()



def correlation_heatmap_plot(SCADA_PIIO_coor, save_fig_path):
    f, ax = plt.subplots(figsize=(7, 6))
    # cbar_ax = f.add_axes([.87, .17, .03, .63])

    h = sns.heatmap(data=SCADA_PIIO_coor, ax=ax, vmin=-0, vmax=1.0, cmap="RdBu", center=0, linewidths=0.3, square=True,
                    # cbar=True, cbar_ax=cbar_ax,
                    xticklabels=(
                        '$\mathtt{I_{88}^2}$', '$\mathtt{I_{90}^2}$', '$\mathtt{I_{92}^2}$', '$\mathtt{I_{94}^2}$',
                        '$\mathtt{I_{96}^2}$', '$\mathtt{I_{98}^2}$', '$\mathtt{I_{100}^2}$', '$\mathtt{I_{102}^2}$',
                        '$\mathtt{I_{104}^2}$', '$\mathtt{I_{108}^2}$', '$\mathtt{I_{110}^2}$',
                        '$\mathtt{O_{70}^2}$', '$\mathtt{O_{74}^2}$'),
                    yticklabels=(
                        '$\mathtt{D_{20}^4}$', '$\mathtt{D_{24}^4}$', '$\mathtt{D_{32}^4}$', '$\mathtt{D_{36}^4}$',
                        '$\mathtt{D_{8}^4}$', '$\mathtt{D_{16}^4}$', '$\mathtt{D_{12}^4}$', '$\mathtt{D_{28}^4}$',
                        '$\mathtt{D_{4}^4}$', '$\mathtt{D_{0}^4}$', '$\mathtt{D_{40}^4}$',
                        '$\mathtt{D_{72}^4}$', '$\mathtt{D_{108}^4}$'))


    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=13)
    # cbar.set_ticks([0, .5, 1.0 ])
    # cbar.set_ticklabels(['0.0', '0.5', '1.0'])

    # plt.xlabel('PII/PIO tables', family='sans-serif', weight="normal")
    # plt.ylabel('SCADA logging traffic', family='sans-serif', weight="normal")

    # # 设置Axes的标题
    # ax.set_title('Correlation between features', fontsize=18, position=(0.5,1.05))

    # # 将y轴或x轴进行逆序
    # ax.invert_yaxis()
    # # ax.invert_xaxis()

    # 设置X轴标签的字体大小和字体颜色
    # ax.set_xlabel('X Label',fontsize=10)
    ax.set_xlabel('PII/PIO Tables', family='sans-serif', weight="normal", fontsize=15)

    # 设置Y轴标签的字体大小和字体颜色
    # ax.set_ylabel('Y Label',fontsize=15, color='r')
    ax.set_ylabel('SCADA Logging Traffic', family='sans-serif', weight="normal", fontsize=15)

    # # 设置坐标轴刻度的字体大小
    # ax.tick_params(axis='y', labelsize=8) # y轴

    # 将x轴刻度放置在top位置的几种方法
    # ax.xaxis.set_ticks_position('top')
    ax.xaxis.tick_top()
    # ax.tick_params(axis='x',labelsize=6, colors='b', labeltop=True, labelbottom=False) # x轴

    # 修改tick的字体颜色
    # ax.tick_params(axis='x', colors='b') # x轴

    # 单独设置y轴或x轴刻度的字体大小, 调整字体方向
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, weight="bold", fontsize=14)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, weight="bold", fontsize=14) # ha="left", 
    # ax.set_xticklabels(ax.get_xticklabels(), rotation=-90)

    f.tight_layout(rect=[0, 0, 1.04, 1])
    # plt.tight_layout()
    plt.savefig(save_fig_path + "SCADA_PIO_heatmap_20211116_wrong.pdf")
    plt.show()


if __name__ == '__main__':
    # data = loadmat("./comm-Yang/SCADA_PII_coor_20211116.mat")
    data = loadmat("./comm-Yang/SCADA_PII_coor_20211116_wrong.mat")
    SCADA_PIIO_coor = data["SCADA_PIIO_coor"]
    save_fig_path = "/Users/magnolia/Dropbox/Zeyu/Stealthy_Attack/figures/"
    correlation_heatmap_plot(SCADA_PIIO_coor, save_fig_path)