from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton


class ClassInfoDialog(QDialog):
    def __init__(self, **pre_information):
        super().__init__()
        self.data = pre_information
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('클래스 정보입력')

        class_layout = QHBoxLayout()
        class_layout.addWidget(QLabel('클래스 이름'))

        self.class_name_edit = QLineEdit()
        class_layout.addWidget(self.class_name_edit)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        ok_button = QPushButton('확인')
        ok_button.clicked.connect(self.save_class_info)
        button_layout.addWidget(ok_button)

        cancel_button = QPushButton('취소')
        cancel_button.clicked.connect(self.cancel)
        button_layout.addWidget(cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(class_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.show()

    def save_class_info(self):
        name = self.class_name_edit.text().strip()

        if len(name) == 0 or (name[0].isnumeric() and name[0] != '_'):
            msg = QMessageBox()
            msg.setWindowTitle('에러')
            msg.setText('이름의 형식이 올바르지 않습니다.')
            msg.exec_()
            return

        self.data['name'] = self.class_name_edit.text().strip()
        self.data['method'] = [[('name', 'test_method1'), ('input(type)', 'self'), ('output(type)', 'self')],
                               [('name', 'test_method2'), ('input(type)', 'self'), ('output(type)', 'self')]]
        self.data['variable'] = [[('name', 'test_variable'), ('type', 'int'), ('initial value', '0')]]
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
