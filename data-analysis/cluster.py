import numpy as np

import matplotlib.pyplot as plt
import pandas as pd
from keras.layers.core import Activation, Dense
from keras.models import Sequential
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression as LR
from sklearn.linear_model import RandomizedLogisticRegression as RLR
from sklearn.manifold import TSNE
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.tree import export_graphviz
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller as ADF


def programmer_4():
    inputfile = 'data-pred.csv'
    outputfile = 'data_type.csv'
    """
    k: 聚类类别
    iteration: 聚类循环次数
    model.labels_： 聚类类别
    model.cluster_centers_： 聚类中心
    """
    k = 3
    iteration = 500
    df = pd.read_csv(inputfile)

    # 构建聚类数组
    df_with_dummy = pd.concat([df['月工资'], df['经验'], df['公司人数']], axis=1)
    data_zs = 1.0 * (df - df.mean()) / df.std()

    model = KMeans(n_clusters=k, n_jobs=4, max_iter=iteration)
    model.fit(data_zs)

    # 统计各个类别的数目
    r1 = pd.Series(model.labels_).value_counts()
    r2 = pd.DataFrame(model.cluster_centers_)
    r = pd.concat([r2, r1], axis=1)
    r.columns = list(df.columns) + [u'类别数目']
    print(r)

    # 详细输出每个样本对应的类别
    r = pd.concat([df, pd.Series(model.labels_, index=df.index)], axis=1)
    r.columns = list(df.columns) + [u'聚类类别']
    r.to_excel(outputfile)

    def density_plot(data, k):
        p = data.plot(kind='kde', linewidth=2, subplots=True, sharex=False)
        [p[i].set_ylabel(u'密度') for i in range(k)]
        plt.legend()
        return plt

    # 保存概率密度图
    pic_output = 'tmp/pd_'
    for i in range(k):
        density_plot(df[r[u'聚类类别'] == i],
                     k).savefig(u'%s%s.png' % (pic_output, i))

    return data_zs, r