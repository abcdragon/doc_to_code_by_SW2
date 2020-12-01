from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QGroupBox

from classinfomodel import DataModel

import keyword
import re


def nameing_rule(name):
    return re.fullmatch('[_|A-Za-z]+[\\d|_]*', name)


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

        self.layout = {element: QVBoxLayout() for element in ['class', 'method', 'variable']}
        self.groupbox = {element: QGroupBox() for element in ['class', 'method', 'variable']}

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('클래스 정보입력')

        main_layout = QVBoxLayout()
        for element in ['class', 'method', 'variable']:
            groupbox, ele_layout = self.groupbox[element], self.layout[element]

            for row, texts in enumerate(self.data.data[element]):
                layout = QHBoxLayout()
                for index in range(len(texts)):
                    layout.addWidget(QLabel(self.data.header[element][index]))
                    layout.addWidget(QLineEdit(texts[index]))

                if element != 'class':
                    layout.addWidget(RemoveButton(element, row, self.remove_button_clicked))

                ele_layout.addLayout(layout)

            groupbox.setLayout(ele_layout)
            main_layout.addWidget(groupbox)

            if element != 'class':
                add_button = QPushButton('%s 추가하기' % element)
                add_button.clicked.connect(self.add_button_clicked)
                main_layout.addWidget(add_button)

        self.groupbox['class'].setFixedHeight(self.groupbox['class'].sizeHint().height())

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

        self.setFixedWidth(700)
        self.setModal(True)
        self.show()

    def get_item(self, element, row, col=-1):
        return self.layout[element].itemAt(row).layout().itemAt(col).widget() if col >= 0 else self.layout[element].itemAt(row)

    def add_button_clicked(self):
        btn_name = self.sender().text()
        ele = 'method' if 'method' in btn_name else 'variable'

        self.data.add(ele)

        h_layout = QHBoxLayout()
        for index in range(len(self.data.data[ele][-1])):
            h_layout.addWidget(QLabel(self.data.header[ele][index]))
            h_layout.addWidget(QLineEdit(self.data.data[ele][-1][index]))

        h_layout.addWidget(RemoveButton(ele, self.layout[ele].count(), self.remove_button_clicked))

        self.layout[ele].addLayout(h_layout)

        self.groupbox[ele].setFixedHeight(self.groupbox[ele].height() + 25)
        self.setFixedHeight(self.height() + 25)

    def remove_button_clicked(self):
        ele, row = self.sender().element, self.sender().row

        self.data.remove(ele, row)
        for col in range(2 * len(self.data.header)):
            self.get_item(ele, row, col).deleteLater()

        for i in range(row, self.layout[ele].count()):
            self.get_item(ele, i, 6).row -= 1

        self.layout[ele].removeItem(self.get_item(ele, row))
        self.sender().deleteLater()

        self.groupbox[ele].setFixedHeight(self.groupbox[ele].sizeHint().height())
        self.setFixedHeight(max(self.height() - 25, 250))

    def chk_class_info(self):
        # class 체크
        class_name = self.get_item('class', 0, 1).text().strip()
        if not nameing_rule(class_name):
            return '클래스 이름에', False

        class_parent = self.get_item('class', 0, 3).text().strip()
        if class_parent and not nameing_rule(class_parent):
            return '상위 클래스 이름에', False
    
        # method 체크
        method_list = []
        for row in range(self.layout['method'].count()):
            method_name = self.get_item('method', row, 1).text().strip()
            method_list += [method_name]
            method_input = self.get_item('method', row, 3).text().strip()
            try:
                exec('def %s(%s):pass' % (method_name, method_input))

            except SyntaxError:
                return '%d번 메서드에 문제가 있습니다.' % (row + 1), False

        # method 중복 체크
        if len(method_list) != len(set(method_list)):
            return '메서드 이름은 중복', False

        # variable 체크
        variable_list = []
        for row in range(self.layout['variable'].count()):
            variable_name = self.get_item('variable', row, 1).text().strip()
            variable_list += [variable_name]
            if not variable_name or not nameing_rule(variable_name):
                return '%d번 변수 이름에' % (row + 1), False

            variable_type = self.get_item('variable', row, 3).text().strip()
            if not nameing_rule(variable_type):
                return '%d번 변수 타입에' % (row + 1), False
        
            # 타입 체크 str, int, float 등 built-in 타입만 체크
            variable_initial_value = self.get_item('variable', row, 5).text().strip()
            if variable_type in keyword.kwlist and variable_type != 'str':
                try:
                    eval('%s(%s)' % (variable_type, variable_initial_value))

                except ValueError:
                    return '%d번 변수 초기값에' % (row + 1), False

        if len(variable_list) != len(set(variable_list)):
            return '변수 이름에 중복', False

        return None, True

    def save_class_info(self):
        msg, success = self.chk_class_info()

        if not success:
            box = QMessageBox()
            box.setWindowTitle('경고')
            box.setText(msg + ' 문제가 있습니다.\n확인해주세요')
            box.setModal(True)
            box.exec_()
            return

        for ele in ['class', 'method', 'variable']:
            for row in range(self.layout[ele].count()):
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
