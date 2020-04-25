# author:Xdmony
# contact: jerkyadmon@gmail.com
# datetime:2020/4/22 1:23 下午
# software: PyCharm
# description:

"""
文件说明：关联规则
"""
from PyQt5.QtWidgets import QWidget


class AprioriAssociationEdit(QWidget):
    def __init__(self):
        super(AprioriAssociationEdit, self).__init__()


class AprioriAssociationOut(QWidget):
    def __init__(self):
        super(AprioriAssociationOut, self).__init__()


def apriori_association(taskData):
    """
    Apriori关联分析
    :param taskData:
    :return:
    """