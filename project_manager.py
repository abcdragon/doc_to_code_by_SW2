from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox
from PyQt5.QtWidgets import QPushButton, QStackedWidget, QListWidget, QInputDialog, QMessageBox

from class_treeview import ClassTreeView
from filecontrol import save_data


class ProjectManager(QWidget):
    def __init__(self, project_path, pre_data=None):
        super().__init__()

        self.project_name = project_path[project_path.rfind('/')+1:]
        self.project_path = project_path

        self.project = {
            'file': [],
            'info_view': []
        } if not pre_data else pre_data

        self.init_ui()

    def init_ui(self):
        btn_layout = QHBoxLayout()

        file_add_button = QPushButton('파일 추가')
        file_add_button.clicked.connect(self.file_add)
        btn_layout.addWidget(file_add_button)

        file_del_button = QPushButton('파일 삭제')
        file_del_button.clicked.connect(self.file_del)
        btn_layout.addWidget(file_del_button)

        self.file_list = QListWidget()
        self.file_list.clicked.connect(self.change_view)

        file_layout = QVBoxLayout()
        file_layout.addWidget(self.file_list)
        file_layout.addLayout(btn_layout)

        file_group = QGroupBox(self.project_name)
        file_group.setLayout(file_layout)

        self.class_view = QStackedWidget()

        main_layout = QGridLayout()
        main_layout.addWidget(file_group, 0, 0, 0, 2)
        main_layout.addWidget(self.class_view, 0, 2)
        self.setLayout(main_layout)

        self.setFixedSize(800, 500)

    def change_view(self):
        self.class_view.setCurrentIndex(self.file_list.selectedIndexes()[0].row())

    def file_add(self):
        while True:
            file_name, success = QInputDialog.getText(self, '파일 이름', '파일 이름을 입력해주세요')
            if file_name not in self.project['file']:
                break

            box = QMessageBox()
            box.setWindowTitle('경고')
            box.setText('이미 존재하는 파일입니다.')
            box.setModal(True)
            box.exec_()

        if file_name and success:
            self.file_list.addItem(file_name)
            self.project['file'].append(file_name)

            self.project['info_view'].append(ClassTreeView())
            self.class_view.addWidget(self.project['info_view'][-1])

    def file_del(self):
        selected_item = self.file_list.selectedItems()
        if not selected_item:
            return

        selected_item = selected_item[0]
        confirm, success = QInputDialog.getText(self, '확인', '정말로 삭제하길 원하면 선택한 파일의 이름을 적으세요')

        if success and confirm and confirm == selected_item.text():
            row = self.file_list.selectedIndexes()[0].row()

            self.class_view.removeWidget(self.project['info_view'][row])
            self.project['info_view'].pop(row)

            self.file_list.takeItem(self.file_list.row(selected_item))
            self.project['file'].pop(row)

    def closeEvent(self, event):
        save_data(self.project, self.project_path)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main = ProjectManager('.')
    main.show()
    sys.exit(app.exec_())
