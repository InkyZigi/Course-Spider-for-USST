# -*- coding: utf-8 -*-
"""
@Time ： 2023/12/10
@Auth ： Schwaze Katze
@File ：UI_main.py
@IDE ：Pycharm(CE)
@Motto：ABC(Always Be Coding)
"""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
import sys

from UI_ops import Dialog
from CourseSpider2 import Spider_Dean_Office


class DataManager(QWidget):
    def __init__(self):
        super(DataManager, self).__init__()
        self.data_list = []
        self.init_ui()

    def init_ui(self):
        """全局设置"""

        self.setWindowIcon(QIcon('crash.ico'))
        self.setWindowTitle('课程管理器')
        self.resize(650, 500)
        grid = QGridLayout()

        """菜单设置"""

        self.add_btn = QPushButton()
        self.add_btn.setText('添加课程')
        self.add_btn.clicked.connect(self.add_btn_click)

        self.del_btn = QPushButton()
        self.del_btn.setText('删除课程')
        self.del_btn.clicked.connect(self.del_data_row)

        self.submit_btn = QPushButton()
        self.submit_btn.setText('执行挂载')
        self.submit_btn.clicked.connect(self.submit_data)

        self.tips = QLabel()
        self.tips.setText("请确保你输入的课程信息准确无误!")

        self.ulabel = QLabel()
        self.ulabel.setText("用户")
        self.uname = QLineEdit()

        self.pwdlabel = QLabel()
        self.pwdlabel.setText("密码")
        self.password = QLineEdit()

        """数据列表设置"""
        self.cource_table = QTableWidget()
        COLUMN = 2
        ROW = 0
        self.cource_table.setColumnCount(COLUMN)
        self.cource_table.setRowCount(ROW)
        h_table_header = ['教师名', '课程名']
        self.cource_table.setHorizontalHeaderLabels(h_table_header)
        self.cource_table.verticalHeader().setVisible(False)
        self.cource_table.setShowGrid(True)
        self.cource_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.cource_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.cource_table.setSelectionMode(QTableWidget.SingleSelection)

        for index in range(self.cource_table.columnCount()):
            headItem = self.cource_table.horizontalHeaderItem(index)
            if headItem:
                headItem.setTextAlignment(Qt.AlignVCenter)

        '''加入布局'''
        self.user_widget = QWidget()
        user_layer = QHBoxLayout()
        user_layer.addWidget(self.ulabel)
        user_layer.addWidget(self.uname)
        self.user_widget.setLayout(user_layer)

        self.pwd_widget = QWidget()
        pwd_layer = QHBoxLayout()
        pwd_layer.addWidget(self.pwdlabel)
        pwd_layer.addWidget(self.password)
        self.pwd_widget.setLayout(pwd_layer)

        self.person_widget = QWidget()
        person_layer = QVBoxLayout()
        person_layer.addWidget(self.user_widget)
        person_layer.addWidget(self.pwd_widget)
        self.person_widget.setLayout(person_layer)

        grid.addWidget(self.person_widget, 0, 0, 1, 1)
        grid.addWidget(self.add_btn, 1, 0, 1, 1)
        grid.addWidget(self.del_btn, 2, 0, 1, 1)
        grid.addWidget(self.submit_btn, 3, 0, 1, 1)
        grid.addWidget(self.tips, 4, 0, 1, 1)
        grid.addWidget(self.cource_table, 0, 2, 5, 5)

        self.setLayout(grid)

    # 将新增数据的按钮绑定到该槽函数
    def add_btn_click(self):
        """
        打开新增数据的弹框模块
        :return:
        """
        Dialog.get_add_dialog(self)

    # 将查询数据的按钮绑定到该槽函数
    def query_data(self):
        """
        查询数据、并将数据展示到主窗口的数据列表中
        :return:
        """
        data = self.data_list
        if len(data) != 0 and len(data[0]) != 0:
            self.cource_table.setRowCount(len(data))
            self.cource_table.setColumnCount(len(data[0]))
            for i in range(len(data)):
                for j in range(len(data[0])):
                    self.cource_table.setItem(i, j, QTableWidgetItem(str(data[i][j])))

    # 将删除数据按钮绑定到该槽函数
    def del_data_row(self):
        """
        删除某一行的数据信息
        :return:
        """
        row_select = self.cource_table.selectedItems()
        print(row_select)
        if len(row_select) != 0:
            row = row_select[0].row()
            print(row)
            self.cource_table.removeRow(row)
            del self.data_list[row]
        print(self.cource_table)

    def submit_data(self):
        """
        提交数据
        :return:
        """
        if self.uname.text().strip() != '' and self.password.text().strip() != '':
            user = self.uname.text().strip()
            pwd = self.password.text().strip()
            try:
                spider = Spider_Dean_Office(user_id=user, user_password=pwd, course=self.data_list)
                spider.visitUrl()
                spider.quit()
                Dialog.show_success(self)
            except Exception as error:
                Dialog.show_error(self, error=error)
        else:
            pass

    def closeEvent(self, event):  # 关闭窗口触发以下事件
        a = QMessageBox.question(self, '关闭', '你确定要退出吗?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if a == QMessageBox.Yes:
            event.accept()  # 接受关闭事件
        else:
            event.ignore()  # 忽略关闭事件


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = DataManager()
    main.show()
    sys.exit(app.exec_())