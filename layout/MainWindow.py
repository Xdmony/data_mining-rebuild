# author:Xdmony
# contact: jerkyadmon@gmail.com
# datetime:2020/4/22 1:03 下午
# software: PyCharm
# description:

"""
文件说明：程序主窗口
"""

import sys

from PyQt5 import Qt, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QDialog, \
    QLineEdit
import pandas as pd

import global_var
import operate.taskController as controller
from layout.widgets.taskProgress import TaskProgress
from layout.widgets.dataList import List
from layout.widgets.opearateTabs import OperateTab
from layout.widgets.operateList import OperateList
from layout.widgets.dataTail import DataTail
from operate.data_mining import linearRegression, decideTreeClassifier, k_meansCluster, associationApriori


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1080, 720)

        # 布局
        layout = QVBoxLayout()  # 总体布局为上下两个布局
        up = QHBoxLayout()
        up_l = QVBoxLayout()  # 左侧两个按钮上下排列
        down = QHBoxLayout()
        down_l = QVBoxLayout()  # 左侧列表框上下排列

        # 控件
        self.btn_local = QPushButton("从本地导入")  # 文件导入按钮
        self.btn_local.clicked.connect(self.on_btn_local_click)
        self.btn_db = QPushButton("从数据库导入")
        self.btn_run = QPushButton("运行")
        self.btn_run.clicked.connect(self.task_run)
        self.btn_quit = QPushButton("退出")

        # 布局设置
        up_l.addWidget(self.btn_local)
        up_l.addWidget(self.btn_db)
        up_l.setStretch(0, 1)
        up_l.setStretch(1, 1)

        # 左下数据集显示
        self.taskProgress = TaskProgress()  # 任务列表
        self.data_in_label = QLabel("输入数据： ")
        self.dataList_in = List()  # 输入数据显示
        self.dataList_in.update_.connect(self.showDataTail)
        # global_var.read()         # 加载数据集
        # self.dataList_in.refresh()
        self.data_out_label = QLabel("输出数据： ")
        self.dataList_out = List()  # 输出数据显示
        down_l.addWidget(self.data_in_label)
        down_l.addWidget(self.dataList_in)
        down_l.addWidget(self.data_out_label)
        down_l.addWidget(self.dataList_out)
        down_l.setStretch(0, 1)
        down_l.setStretch(1, 4)
        down_l.setStretch(2, 1)
        down_l.setStretch(3, 4)

        # 中下
        self.operateEdit = OperateTab()  # 显示数据信息以及操作编辑区
        self.operateBoard = OperateList()  # 任务选择
        self.operateBoard.clickBtn_.connect(self.showOperate)

        # 上方布局
        up.addLayout(up_l)
        up.addWidget(self.taskProgress)
        up.addWidget(self.btn_run)
        up.addWidget(self.btn_quit)
        up.setStretch(0, 2)
        up.setStretch(1, 6)
        up.setStretch(2, 1)
        up.setStretch(3, 1)

        # 下方布局
        down.addLayout(down_l)
        down.addWidget(self.operateEdit)
        down.addWidget(self.operateBoard)
        down.setStretch(0, 2)
        down.setStretch(1, 6)
        down.setStretch(2, 2)

        # 总体布局
        layout.addLayout(up)
        layout.addLayout(down)
        layout.setStretch(0, 1)
        layout.setStretch(1, 6)
        self.setLayout(layout)

    def on_btn_local_click(self):
        """
        从本地文件导入数据集
        :return:
        """
        fileName, fileType = QFileDialog.getOpenFileName(self, '选择文件', '', '*.csv')
        if fileName is not None and fileName != "":
            global_var.currentData.type = global_var.DataSetType.IN
            global_var.filePath = fileName
            self.dialog = QDialog()
            self.dialog.resize(400, 40)
            hbox_u = QHBoxLayout()
            hbox_d = QHBoxLayout()
            vbox = QVBoxLayout()
            label = QLabel("数据集命名：")
            self.lineText = QLineEdit()
            self.btn_ok = QPushButton("确定")
            self.btn_cancel = QPushButton("取消")
            self.btn_ok.clicked.connect(self.on_ok_click)
            self.btn_cancel.clicked.connect(self.on_cancel_click)
            hbox_u.addWidget(label)
            hbox_u.addWidget(self.lineText)
            hbox_u.setStretch(0, 1)
            hbox_u.setStretch(1, 2)
            hbox_d.addStretch(2)
            hbox_d.addWidget(self.btn_ok)
            hbox_d.addWidget(self.btn_cancel)
            vbox.addLayout(hbox_u)
            vbox.addLayout(hbox_d)
            self.dialog.setLayout(vbox)
            self.dialog.exec_()

    @QtCore.pyqtSlot()
    def on_ok_click(self):
        """
        添加数据集
        :return:
        """
        global_var.currentData.dataName = self.lineText.text()
        path = global_var.filePath
        data = pd.read_csv(path)
        global_var.currentData.data = data
        global_var.currentData.dataColumns = data.columns.tolist()
        global_var.currentData.length = len(data)
        global_var.allDataSet.data_in[global_var.currentData.dataName] = global_var.currentData
        global_var.currentData = global_var.DataSet()
        # global_var.save()
        self.dataList_in.refresh()  # 刷新输入数据
        self.dialog.close()

    @QtCore.pyqtSlot()
    def on_cancel_click(self):
        global_var.currentData = global_var.DataSet()
        self.dialog.close()

    def on_btn_db_click(self):
        """
        从数据库导入文件
        :return:
        """
        pass

    def showDataTail(self, dataName):
        """
        显示数据集详情
        :param dataName:
        :return:
        """
        data = global_var.allDataSet.data_in[dataName]
        dataTail = DataTail(data)
        dataTail.setObjectName(dataName)
        global_var.currentData = data
        dataTail.add_.connect(self.add_data)
        show = self.operateEdit.find_tab(dataName)
        if not show:
            self.operateEdit.add_Tab(dataTail, dataName)

    def add_data(self, dataName):
        self.taskProgress.add_data(dataName)

    def showOperate(self, operate):
        operateList = global_var.allOperateList
        if operate == operateList[0][0]:  # 数据清洗
            pass
        elif operate == operateList[0][1]:  # 数据集成
            pass
        elif operate == operateList[0][2]:  # 数据变换
            pass
        elif operate == operateList[0][3]:  # 特征选择
            pass
        elif operate == operateList[0][4]:  # 特征提取
            pass
        elif operate == operateList[1][0]:  # 关联分析
            tab = associationApriori.AprioriAssociationEdit()
            tab.addTask_.connect(self.add_task)
        elif operate == operateList[2][0]:  # 聚类分析
            tab = k_meansCluster.ClusterEdit()
            tab.addTask_.connect(self.add_task)
        elif operate == operateList[3][0]:  # 分类分析
            tab = decideTreeClassifier.DTC_Edit()
            tab.addTask_.connect(self.add_task)
        elif operate == operateList[4][0]:  # 回归分析
            tab = linearRegression.LinearEdit()
            tab.addTask_.connect(self.add_task)
        elif operate == operateList[5][0]:  # 可视化
            pass
        self.operateEdit.add_Tab(tab, operate)

    def add_task(self, task):
        """
        添加任务到任务列表
        :param task:
        :return:
        """
        self.taskProgress.add_task(task)

    def task_run(self):
        """
        执行任务事件，任务存储在变量currentTask
        :return:
        """
        task = global_var.currentTask
        for operate in task.operateList:
            if operate is not None and operate != "":
                controller.execute(operate)
        # 显示结果tab
        if global_var.currentTask.resultType == global_var.DataMiningType.ASSOCIATION:
            result_tab = associationApriori.AprioriAssociationOut(global_var.currentTask.result)
            self.operateEdit.add_Tab(result_tab, "result-apriori关联规则")
        if global_var.currentTask.resultType == global_var.DataMiningType.CLUSTER:
            result_tab = k_meansCluster.ClusterOut(global_var.currentTask.result)
            self.operateEdit.add_Tab(result_tab, "result-Kmeans聚类")
        if global_var.currentTask.resultType == global_var.DataMiningType.CLASSIFY:
            result_tab = decideTreeClassifier.DTC_Out(global_var.currentTask.result)
            self.operateEdit.add_Tab(result_tab, "result-决策树分类")
        if global_var.currentTask.resultType == global_var.DataMiningType.REGRESSION:
            result_tab = linearRegression.LinearOut(global_var.currentTask.result)
            self.operateEdit.add_Tab(result_tab, "result-线性回归")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
