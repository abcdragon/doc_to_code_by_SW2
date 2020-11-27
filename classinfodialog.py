from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QGroupBox

from classinfomodel import DataModel

import keyword
import re


def nameing_rule(name):
    return name not in keyword.kwlist and re.fullmatch('[_|A-Za-z]+[\\d|_]*', name)


class RemoveButton(QPushButton):
    def __init__(self, element, row, func):
        super().__init__('삭제')
        self.row = row
        self.element = element
        self.clicked.connect(func)


class ClassInfoDialog(QDialog):
    def __init__(self, pre_info=None):
        super().__init__()
        self.data = pre_info if pre_info else DataModel()
        self.success = False
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('클래스 정보입력')

        self.layout = {
            'class': QGridLayout(),
            'method': QGridLayout(),
            'variable': QGridLayout()
        }

        main_layout = QVBoxLayout()
        for ele in ['class', 'method', 'variable']:
            groupbox, layout = QGroupBox(ele), self.layout[ele]

            row = 0
            for texts in self.data.data[ele]:
                col = 0
                for index in range(len(texts)):
                    layout.addWidget(QLabel(self.data.header[ele][index]), row, col)
                    layout.addWidget(QLineEdit(texts[index]), row, col + 1)
                    col += 2

                if ele != 'class':
                    layout.addWidget(RemoveButton(ele, row, self.remove_button_clicked), row, col)

                row += 1

            groupbox.setLayout(layout)
            main_layout.addWidget(groupbox)

            if ele != 'class':
                add_button = QPushButton('%s 추가하기' % ele)
                add_button.clicked.connect(self.add_button_clicked)
                main_layout.addWidget(add_button)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        ok_button = QPushButton('확인')
        ok_button.clicked.connect(self.save_class_info)
        button_layout.addWidget(ok_button)

        cancel_button = QPushButton('취소')
        cancel_button.clicked.connect(self.cancel)
        button_layout.addWidget(cancel_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.setModal(True)
        self.show()

    def get_item(self, element, row, col):
        return self.layout[element].itemAtPosition(row, col).widget()

    def add_button_clicked(self):
        btn_name = self.sender().text()
        ele = 'method' if 'method' in btn_name else 'variable'

        self.data.add(ele)
        row, col = self.layout[ele].rowCount(), 0

        for index in range(len(self.data.data[ele][-1])):
            self.layout[ele].addWidget(QLabel(self.data.header[ele][index]), row, col)
            self.layout[ele].addWidget(QLineEdit(self.data.data[ele][-1][index]), row, col + 1)
            col += 2

        self.layout[ele].addWidget(RemoveButton(ele, row, self.remove_button_clicked), row, col)

    def remove_button_clicked(self):
        ele, row = self.sender().element, self.sender().row
        if self.layout[ele].rowCount() == 1:
            return

        for idx in range(2 * len(self.data.header[ele])):
            self.get_item(ele, row, idx).deleteLater()

        self.sender().deleteLater()

    def chk_class_info(self):
    #   class 체크
        class_name = self.get_item('class', 0, 1).text().strip()
        if not nameing_rule(class_name):
            return False

        class_parent = self.get_item('class', 0, 3).text().strip()
        if class_parent and not nameing_rule(class_parent):
            return False
    
    #   method 체크
        for row in range(self.layout['method'].rowCount()):
            method_name = self.get_item('method', row, 1).text().strip()
            if method_name and not nameing_rule(method_name):
                return False

            method_input = self.get_item('method', row, 3).text().strip()
            if method_input and not nameing_rule(method_input):
                return False

    #   variable 체크
        for row in range(self.layout['variable'].rowCount()):
            variable_name = self.get_item('variable', row, 1).text().strip()
            if variable_name and not nameing_rule(variable_name):
                return False

            variable_type = self.get_item('variable', row, 3).text().strip()
            if not nameing_rule(variable_type):
                return False

            variable_initial_value = self.get_item('variable', row, 5).text().strip()
            if variable_type != 'str':
                try:
                    eval('%s(%s)' % (variable_type, variable_initial_value))

                except ValueError:
                    return False

        return True

    def save_class_info(self):
        if not self.chk_class_info():
            box = QMessageBox()
            box.setWindowTitle('경고')
            box.setText('입력에 문제가 있습니다. 확인해주세요')
            box.setModal(True)
            box.exec_()
            return

        for ele in ['class', 'method', 'variable']:
            for row in range(self.layout[ele].rowCount()):
                for col in range(len(self.data.header[ele])):
                    self.data.data[ele][row][col] = self.get_item(ele, row, 2 * col + 1).text().strip()

        self.success = True
        self.close()

    def cancel(self):
        self.close()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main = ClassInfoDialog()
    main.show()
    sys.exit(app.exec_())
