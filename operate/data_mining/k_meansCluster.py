# author:Xdmony
# contact: jerkyadmon@gmail.com
# datetime:2020/4/22 1:25 下午
# software: PyCharm
# description:

"""
文件说明：K-means聚类
"""
from PyQt5.QtWidgets import QWidget
from sklearn.cluster import KMeans


class ClusterEdit(QWidget):
    def __init__(self):
        super(ClusterEdit, self).__init__()


class ClusterOut(QWidget):
    def __init__(self):
        super(ClusterOut, self).__init__()


def k_means_cluster(taskData):
    """
    聚类
    :param taskData:
    :return:
    """
