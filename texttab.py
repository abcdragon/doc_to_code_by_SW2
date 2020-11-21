from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt

from classinfodialog import ClassInfoDialog


class TextTab(QWidget):
    def __init__(self):
        super().__init__()

        self.class_list = QTreeWidget()
        self.class_list.setColumnCount(5)
        self.class_list.setHeaderHidden(True)

        self.add_line = QPushButton('새로운 클래스 추가하기')
        self.add_line.clicked.connect(self.add_line_clicked)

        self.to_file = QPushButton('템플릿 코드 생성하기')

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_line)
        button_layout.addWidget(self.to_file)

        layout = QVBoxLayout()
        layout.addWidget(self.class_list)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def create_item(self, class_info):
        root = QTreeWidgetItem()
        root.setText(0, class_info['name'])

        item_roots = [('method', QTreeWidgetItem(root)),
                      ('variable', QTreeWidgetItem(root))]

        for key, item_root in item_roots:
            item_root.setText(0, key)

            if not class_info[key]:
                continue

            header = QTreeWidgetItem(item_root)
            for index, (header_text, _) in enumerate(class_info[key][0]):
                header.setText(index + 1, header_text)

            new_item = QTreeWidgetItem(item_root)
            for info in class_info[key]:
                for index, (_, content) in enumerate(info):
                    new_item.setText(index + 1, content)

        return root

    def add_line_clicked(self):
        info = ClassInfoDialog()
        info.exec_()

        if not info.data:
            return

        new_item = self.create_item(info.data)
        self.class_list.addTopLevelItem(new_item)
        self.class_list.scrollToBottom()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main = TextTab()
    main.show()
    sys.exit(app.exec_())
