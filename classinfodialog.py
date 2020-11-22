from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QGroupBox


class ClassInfoDialog(QDialog):
    def __init__(self, pre_information=None):
        super().__init__()
        self.data = pre_information if pre_information else dict()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('클래스 정보입력')

        self.component = dict()
        if self.data:
            for key1 in self.data:
                self.component[key1] = []
                for key2 in self.data[key1]['header']:
                    line_edit = QLineEdit()
                    line_edit.setText(self.data[key1][key2])
                    self.component[key1].append((key2, line_edit))

        else:
            self.component['class'] = [('name', QLineEdit()), ('parent', QLineEdit())]
            self.component['method'] = [('name', QLineEdit()), ('input(type)', QLineEdit()), ('output(type)', QLineEdit())]
            self.component['variable'] = [('name', QLineEdit()), ('type', QLineEdit()), ('inital value', QLineEdit())]

        main_layout = QVBoxLayout()
        for key in ['class', 'method', 'variable']:
            groupbox, layout = QGroupBox(key), QHBoxLayout()

            for label, edit in self.component[key]:
                layout.addWidget(QLabel(label))
                layout.addWidget(edit)

            groupbox.setLayout(layout)
            main_layout.addWidget(groupbox)

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

    def save_class_info(self):
        for key, info in self.component.items():
            self.data[key] = {'header': []}
            for label, edit in info:
                self.data[key]['header'].append(label)
                self.data[key][label] = edit.text()

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
