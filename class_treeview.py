from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QTreeWidget, QTreeWidgetItem

from classinfodialog import ClassInfoDialog
from doctocode import DocToCode


class ClassTreeView(QWidget):
    def __init__(self, file_full_path, pre_data=None):
        super().__init__()

        self.all_data = pre_data if pre_data else []
        self.file_full_path = file_full_path

        self.init_ui()

    def init_ui(self):
        self.class_list = QTreeWidget()
        self.class_list.setColumnCount(5)
        self.class_list.setHeaderHidden(True)
        self.class_list.itemDoubleClicked.connect(self.change_item)
        for data in self.all_data:
            self.class_list.addTopLevelItem(self.create_item(data))
            self.class_list.scrollToBottom()

        add_item_button = QPushButton('새로운 클래스 추가하기')
        add_item_button.clicked.connect(self.add_item)

        del_item_button = QPushButton('클래스 삭제하기')
        del_item_button.clicked.connect(self.del_item)

        to_file_button = QPushButton('템플릿 코드 생성하기')
        to_file_button.clicked.connect(self.to_file)

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_item_button)
        button_layout.addWidget(del_item_button)
        button_layout.addWidget(to_file_button)

        layout = QVBoxLayout()
        layout.addWidget(self.class_list)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    # 아이템 생성
    def create_item(self, info):
        root = QTreeWidgetItem()
        root.setText(0, info.data['class'][0][0])
        if info.data['class'][0][1] != '':
            root.setText(1, '->')
            root.setText(2, info.data['class'][0][1])

        item_roots = [('method', QTreeWidgetItem(root)),
                      ('variable', QTreeWidgetItem(root))]

        for ele, item_root in item_roots:
            item_root.setText(0, ele)

            header_item = QTreeWidgetItem(item_root)
            for idx, header in enumerate(info.header[ele]):
                header_item.setText(idx + 1, header)

            new_items = [QTreeWidgetItem(item_root) for _ in range(len(info.data[ele]))]
            for row, texts in enumerate(info.data[ele]):
                for col, text in enumerate(texts):
                    new_items[row].setText(col + 1, text)

        return root
    
    # 아이템 추가
    def add_item(self):
        info = None
        while True:
            info = ClassInfoDialog(info.data if info else None)
            info.exec_()

            if not info.success:
                break

            # 클래스 이름이 같은게 있으면 continue
            if not [0 for data in self.all_data if data.data['class'][0][0] == info.data.data['class'][0][0]]:
                break

            box = QMessageBox()
            box.setWindowTitle('경고')
            box.setModal(True)
            box.setText('클래스의 이름이 겹쳤습니다.')
            box.exec_()

        if info.success:
            self.all_data.append(info.data)
            self.class_list.addTopLevelItem(self.create_item(info.data))
            self.class_list.scrollToBottom()

    # 아이템 변경
    def change_item(self):
        item = self.class_list.selectedItems()[0]
        index = self.class_list.indexOfTopLevelItem(item)

        while index == -1:
            item = item.parent()
            index = self.class_list.indexOfTopLevelItem(item)

        info = None
        while True:
            info = ClassInfoDialog(pre_info=info.data if info else self.all_data[index])
            info.exec_()

            if not info.success:
                break

            if not [0 for i, data in enumerate(self.all_data) if i != index and data.data['class'][0][0] == info.data.data['class'][0][0]]:
                break

            box = QMessageBox()
            box.setWindowTitle('경고')
            box.setModal(True)
            box.setText('클래스의 이름이 겹쳤습니다.')
            box.exec_()

        if info.success:
            self.all_data[index] = info.data

            new_item = self.create_item(info.data)

            self.class_list.takeTopLevelItem(index)
            self.class_list.insertTopLevelItem(index, new_item)

            self.class_list.scrollToBottom()

    def del_item(self):
        item = self.class_list.selectedItems()[0]
        index = self.class_list.indexOfTopLevelItem(item)

        while index == -1:
            item = item.parent()
            index = self.class_list.indexOfTopLevelItem(item)

        self.class_list.takeTopLevelItem(index)
        del self.all_data[index]

    def to_file(self):
        DocToCode(self.file_full_path, self.all_data)
