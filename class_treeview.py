from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QPushButton, QTreeWidget, QTreeWidgetItem

from classinfodialog import ClassInfoDialog
from doctocode import DocToCode


class ClassTreeView(QWidget):
    def __init__(self, pre_data=None):
        super().__init__()

        self.all_data = pre_data if pre_data else []

        self.init_ui()

    def init_ui(self):
        self.class_list = QTreeWidget()
        self.class_list.setColumnCount(5)
        self.class_list.setHeaderHidden(True)
        self.class_list.itemDoubleClicked.connect(self.change_item_content)
        for data in self.all_data:
            self.class_list.addTopLevelItem(self.create_item(data))
            self.class_list.scrollToBottom()

        self.add_item = QPushButton('새로운 클래스 추가하기')
        self.add_item.clicked.connect(self.add_item_clicked)

        self.del_item = QPushButton('클래스 삭제하기')
        self.del_item.clicked.connect(self.del_item_clicked)

        self.to_file = QPushButton('템플릿 코드 생성하기')
        self.to_file.clicked.connect(self.to_file_clicked)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_item)
        button_layout.addWidget(self.del_item)
        button_layout.addWidget(self.to_file)

        layout = QVBoxLayout()
        layout.addWidget(self.class_list)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def add_item_clicked(self):
        info = None
        while True:
            info = ClassInfoDialog(info.data if info else None)
            info.exec_()

            if not info.success:
                break

            box = QMessageBox()
            box.setWindowTitle('경고')
            box.setModal(True)

            # 클래스 이름이 같은게 있으면 continue
            if [0 for data in self.all_data if data.data['class'][0][0] == info.data.data['class'][0][0]]:
                box.setText('클래스의 이름이 겹쳤습니다.')
                box.exec_()

                continue

            # 메서드 이름이 같은게 있으면 강제 종료해서 while 처음으로 돌아가고,
            for info_name, info_para, _ in info.data.data['method']:
                if [0 for data in self.all_data for name, _, _ in data.data['method'] if name == info_name]:
                    box.setText('메서드의 이름이 겹치는 요소가 있습니다.')
                    box.exec_()
                    break

                tmp = [c for c in info_para.replace(',', ' ').split(' ') if c]
                if len(tmp) != len(set(tmp)):
                    box.setText('매개변수 중 겹치는 것이 있습니다.')
                    box.exec_()
                    break

            # 메서드 이름이 겹치지 않고, 매개변수도 안 겹친다면 변수에 대해 검색
            else:
                # 변수 이름이 같은게 있으면 강제 종료해서 while 처음으로 돌아가고
                for info_name, _, _ in info.data.data['variable']:
                    if [0 for data in self.all_data for name, _, _ in data.data['variable'] if name == info_name]:
                        box.setText('변수의 이름이 겹치는 요소가 있습니다.')
                        box.exec_()

                        break

                # 변수 이름까지 같은게 없으면 break으로 while문 탈출
                else:
                    break

        if info.success:
            self.all_data.append(info.data)
            self.class_list.addTopLevelItem(self.create_item(info.data))
            self.class_list.scrollToBottom()

    def del_item_clicked(self):
        item = self.class_list.selectedItems()[0]
        index = self.class_list.indexOfTopLevelItem(item)

        while index == -1:
            item = item.parent()
            index = self.class_list.indexOfTopLevelItem(item)

        self.class_list.takeTopLevelItem(index)
        del self.all_data[index]

    def change_item_content(self):
        item = self.class_list.selectedItems()[0]
        index = self.class_list.indexOfTopLevelItem(item)

        while index == -1:
            item = item.parent()
            index = self.class_list.indexOfTopLevelItem(item)

        info = ClassInfoDialog(self.all_data[index])
        info.exec_()

        if not info.success:
            return

        self.all_data[index] = info.data

        new_item = self.create_item(info.data)

        self.class_list.takeTopLevelItem(index)
        self.class_list.insertTopLevelItem(index, new_item)

        self.class_list.scrollToBottom()

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
            new_items = [QTreeWidgetItem(item_root) for _ in range(len(info.data[ele]))]

            for idx, header in enumerate(info.header[ele]):
                header_item.setText(idx + 1, header)

            for row, texts in enumerate(info.data[ele]):
                for col, text in enumerate(texts):
                    new_items[row].setText(col + 1, text)

        return root

    def to_file_clicked(self):
        DocToCode(self.all_data)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main = ClassTreeView()
    main.show()
    sys.exit(app.exec_())
