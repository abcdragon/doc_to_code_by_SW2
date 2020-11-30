from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QDialog, QFileDialog
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton

from project_manager import ProjectManager
from filecontrol import load_data, save_data

import os


class ProjectMenu(QWidget):
    def __init__(self):
        super().__init__()

        project_button_layout = QHBoxLayout()
        self.new_project = QPushButton('새 프로젝트 만들기')
        project_button_layout.addWidget(self.new_project)

        self.open_project = QPushButton('프로젝트 열기')
        project_button_layout.addWidget(self.open_project)

        self.setLayout(project_button_layout)


class NewProjectDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.success = False
        self.path = 'C:/'

        self.project_name = QLineEdit()
        self.project_name.textChanged.connect(self.update_path)

        self.full_path = QLineEdit(self.path)
        self.full_path.setReadOnly(True)

        load_path = QPushButton('열기')
        load_path.clicked.connect(self.load)

        self.ok_button = QPushButton('확인')
        self.ok_button.clicked.connect(self.ok)

        self.cancel_button = QPushButton('취소')
        self.cancel_button.clicked.connect(self.cancel)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        all_layout = QGridLayout()
        all_layout.addWidget(QLabel('프로젝트 이름'), 0, 0)
        all_layout.addWidget(self.project_name, 0, 1, 1, 2)

        all_layout.addWidget(QLabel('프로젝트 경로'), 1, 0)
        all_layout.addWidget(self.full_path, 1, 1)
        all_layout.addWidget(load_path, 1, 2)

        all_layout.addLayout(button_layout, 2, 0)

        self.setLayout(all_layout)
        self.setModal(True)
        self.show()

    def update_path(self):
        self.full_path.setText(self.path + self.project_name.text())
        self.ok_button.setEnabled(not os.path.exists(self.full_path.text()))

    def load(self):
        path = str(QFileDialog.getExistingDirectory(self, '경로'))

        if path:
            self.path = path + '/'
            self.full_path.setText(self.path + self.project_name.text())

    def ok(self):
        self.success = True
        self.close()

    def cancel(self):
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Doc to Code')
        menu = ProjectMenu()
        menu.new_project.clicked.connect(self.new_project)
        menu.open_project.clicked.connect(self.open_project)
        self.setCentralWidget(menu)
        self.setFixedSize(400, 250)
        self.show()

    def new_project(self):
        dialog = NewProjectDialog()
        dialog.exec_()

        if dialog.success:
            os.mkdir(dialog.full_path.text())

            pm = ProjectManager(dialog.full_path.text())
            self.setCentralWidget(pm)
            self.setFixedSize(pm.size())

    def open_project(self):
        path = str(QFileDialog.getExistingDirectory(self, '경로'))

        if path:
            data = load_data(path)
            if data:
                pm = ProjectManager(path, pre_data=data)
                self.setCentralWidget(pm)
                self.setFixedSize(pm.size())
    
    def closeEvent(self, event):
        if isinstance(self.centralWidget(), ProjectManager):
            widget = self.centralWidget()
            widget.project['infos'] = [infos.all_data for infos in widget.project['infos']]
            save_data(widget.project, widget.project_path)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
