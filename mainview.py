from PyQt5.QtWidgets import QWidget, QTabWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel

from texttab import TextTab


class MainView(QWidget):
    def __init__(self):
        super().__init__()

        tab = QTabWidget()
        tab.addTab(TextTab(), '텍스트')
        tab.addTab(QLabel('UML'), 'UML')

        layout = QHBoxLayout()
        layout.addWidget(tab)
        self.setLayout(layout)

        self.setFixedSize(600, 400)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main = MainView()
    main.show()
    sys.exit(app.exec_())
