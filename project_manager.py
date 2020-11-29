from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox
from PyQt5.QtWidgets import QPushButton, QStackedWidget, QListWidget, QInputDialog, QMessageBox

from class_treeview import ClassTreeView

import os


class ProjectManager(QWidget):
    def __init__(self, project_path, pre_data=None):
        super().__init__()
        self.project_path = project_path
        self.project = {
            'name': project_path[project_path.rfind('/')+1:],
            'files': [],
            'infos': []
        }

        self.class_view = QStackedWidget()
        self.file_list = QListWidget()
        self.file_list.doubleClicked.connect(self.file_name_change)
        self.file_group = QGroupBox(self.project['name'])

        if pre_data:
            self.project['files'] = pre_data['files']
            for file, info in zip(self.project['files'], pre_data['infos']):
                self.file_list.addItem(file)
                self.project['infos'].append(ClassTreeView(self.project_path + '/' + file, pre_data=info))
                self.class_view.addWidget(self.project['infos'][-1])

        self.init_ui()

    def init_ui(self):
        btn_layout = QHBoxLayout()

        file_add_button = QPushButton('파일 추가')
        file_add_button.clicked.connect(self.file_add)
        btn_layout.addWidget(file_add_button)

        file_del_button = QPushButton('파일 삭제')
        file_del_button.clicked.connect(self.file_del)
        btn_layout.addWidget(file_del_button)

        self.file_list.clicked.connect(self.change_view)

        file_layout = QVBoxLayout()
        file_layout.addWidget(self.file_list)
        file_layout.addLayout(btn_layout)

        self.file_group.mouseDoubleClickEvent = self.get_project_name
        self.file_group.setLayout(file_layout)

        main_layout = QGridLayout()
        main_layout.addWidget(self.file_group, 0, 0, 0, 2)
        main_layout.addWidget(self.class_view, 0, 2)
        self.setLayout(main_layout)

        self.setFixedSize(800, 500)

    def change_view(self):
        self.class_view.setCurrentIndex(self.file_list.selectedIndexes()[0].row())

    def get_project_name(self, event):
        while True:
            project_name, success = QInputDialog.getText(self, '프로젝트 이름', '프로젝트 이름을 입력해주세요')
            new_path = self.project_path[:self.project_path.rfind('/')] + '/' + project_name
            if not os.path.exists(new_path) or not success:
                break

            box = QMessageBox()
            box.setWindowTitle('경고')
            box.setText('이미 존재하는 폴더입니다.')
            box.setModal(True)
            box.exec_()

        if success and project_name:
            self.file_group.setTitle(new_path[new_path.rfind('/')+1:])
            self.project['name'] = new_path[new_path.rfind('/')+1:]
            os.rename(self.project_path, new_path)
            self.project_path = new_path

    def get_file_name(self):
        while True:
            file_name, success = QInputDialog.getText(self, '파일 이름', '파일 이름을 입력해주세요')
            if file_name.lower() not in [s.lower() for s in self.project['files']]:
                break

            box = QMessageBox()
            box.setWindowTitle('경고')
            box.setText('이미 존재하는 파일입니다.')
            box.setModal(True)
            box.exec_()

        return file_name, success

    def file_name_change(self):
        file_name, success = self.get_file_name()

        if file_name and success:
            index = self.file_list.selectedIndexes()[0].row()
            self.project['files'][index] = file_name
            if os.path.exists(self.project['infos'][index].file_full_path + '.py'):
                os.remove(self.project['infos'][index].file_full_path + '.py')

            self.project['infos'][index].file_full_path = self.project_path + '/' + file_name
            self.file_list.selectedItems()[0].setText(file_name)

    def file_add(self):
        file_name, success = self.get_file_name()

        if file_name and success:
            self.project['files'].append(file_name)
            self.file_list.addItem(self.project['files'][-1])

            self.project['infos'].append(ClassTreeView(self.project_path + '/' + self.project['files'][-1]))
            self.class_view.addWidget(self.project['infos'][-1])

    def file_del(self):
        selected_item = self.file_list.selectedItems()
        if not selected_item:
            return

        selected_item = selected_item[0]
        confirm, success = QInputDialog.getText(self, '확인', '정말로 삭제하길 원하면 선택한 파일의 이름을 적으세요')

        if success and confirm and confirm == selected_item.text():
            row = self.file_list.selectedIndexes()[0].row()

            self.class_view.removeWidget(self.project['infos'][row])
            self.project['infos'].pop(row)

            self.file_list.takeItem(self.file_list.row(selected_item))
            self.project['files'].pop(row)

            if os.path.exists('%s/%s.py' % (self.project_path, confirm)):
                os.remove('%s/%s.py' % (self.project_path, confirm))


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main = ProjectManager('.')
    main.show()
    sys.exit(app.exec_())
