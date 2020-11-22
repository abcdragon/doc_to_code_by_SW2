from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QTreeWidget, QTreeWidgetItem

from classinfodialog import ClassInfoDialog


class TextTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        self.all_data = []

    def init_ui(self):
        self.class_list = QTreeWidget()
        self.class_list.setColumnCount(5)
        self.class_list.setHeaderHidden(True)
        self.class_list.itemDoubleClicked.connect(self.change_item_content)

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

    def add_line_clicked(self):
        info = ClassInfoDialog()
        info.exec_()

        if not info.data:
            return

        self.all_data.append(info.data)
        new_item = self.create_item(info.data)
        self.class_list.addTopLevelItem(new_item)
        self.class_list.scrollToBottom()

    def change_item_content(self):
        item = self.class_list.selectedItems()[0]
        index = self.class_list.indexOfTopLevelItem(item)

        while index == -1:
            item = item.parent()
            index = self.class_list.indexOfTopLevelItem(item)

        info = ClassInfoDialog(self.all_data[index])
        info.exec_()

        if not info.data:
            return

        self.all_data[index] = info.data

        new_item = self.create_item(info.data)

        self.class_list.takeTopLevelItem(index)
        self.class_list.insertTopLevelItem(index, new_item)

        self.class_list.scrollToBottom()

    def create_item(self, info):
        root = QTreeWidgetItem()
        root.setText(0, info['class']['name'])
        if info['class']['parent'] != '':
            root.setText(1, '->')
            root.setText(2, info['class']['parent'])

        item_roots = [('method', QTreeWidgetItem(root)),
                      ('variable', QTreeWidgetItem(root))]

        for key, item_root in item_roots:
            item_root.setText(0, key)

            if not info[key]:
                continue

            header_item = QTreeWidgetItem(item_root)
            new_item = QTreeWidgetItem(item_root)

            for index, header in enumerate(info[key]['header']):
                header_item.setText(index + 1, header)
                new_item.setText(index + 1, info[key][header])

        return root


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main = TextTab()
    main.show()
    sys.exit(app.exec_())
