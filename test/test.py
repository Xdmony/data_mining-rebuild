# author:Xdmony
# contact: jerkyadmon@gmail.com
# datetime:2020/4/22 11:12 下午
# software: PyCharm
# description:

"""
文件说明：
"""
import sys

from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QHBoxLayout

class Window(QWidget):
    def __init__(self):
        super(Window,self).__init__()
        btn = QPushButton("find")
        btn.clicked.connect(self.click)
        btn_child = QPushButton("child")
        btn_child.setObjectName("children")
        lay = QHBoxLayout()
        lay.addWidget(btn)
        lay.addWidget(btn_child)
        self.setLayout(lay)

    def click(self):
        btn = self.findChild(QPushButton,"child")
        bt = self.findChild(QPushButton,"find")
        b = self.findChild(QPushButton,"children")
        pas = QPushButton()
        s = QPushButton()

if __name__ == '__main__':
        app = QApplication(sys.argv)
        win = Window()
        win.resize(800,600)
        win.show()
        sys.exit(app.exec_())