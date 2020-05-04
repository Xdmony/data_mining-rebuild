# author:Xdmony
# contact: jerkyadmon@gmail.com
# datetime:2020/4/22 10:31 下午
# software: PyCharm
# description:

"""
文件说明：任务控制器，执行选择的任务，输出数据为operateData
"""
import global_var
from operate.data_mining import linearRegression, decideTreeClassifier, k_meansCluster, associationApriori


def execute(operate):
    operates = global_var.allOperateList
    if operate == operates[0][0]:       # "数据清洗", "数据集成", "数据变换", "特征选择", "特征提取"
        pass
    elif operate == operates[0][1]:     # 数据集成
        pass
    elif operate == operates[0][2]:     # 数据变换
        pass
    elif operate == operates[0][3]:     # 特征选择
        pass
    elif operate == operates[0][4]:     # 特征提取
        pass
    elif operate == operates[1][0]:     # 关联分析
        taskData = global_var.currentTask
        associationApriori.apriori_association(taskData)
    elif operate == operates[2][0]:     # 聚类分析
        taskData = global_var.currentTask
        k_meansCluster.k_means_cluster(taskData)
    elif operate == operates[3][0]:     # 分类分析
        taskData = global_var.currentTask
        decideTreeClassifier.decision_tree_classify(taskData)
    elif operate == operates[4][0]:     # 回归分析
        taskData = global_var.currentTask
        linearRegression.linear_regression(taskData)
    elif operate == operates[5][0]:     # 可视化
        pass



