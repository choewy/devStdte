from PyQt5.QtWidgets import QWidget, QListWidget, QVBoxLayout
from src.widget.schedule import Schedule
from src.widget.total import Total
from src.widget.user import User
from src.widget.task import Task

ITEMS = {
    " 시간 관리": Schedule,
    " 시간 집계": Total,
    " 부서원 정보": User,
    " 사업 정보": Task
}


class NavBar(QWidget):
    def __init__(self, central=None):
        QWidget.__init__(self)
        self.central = central

        self.widget = None

        self.navBar = QListWidget()
        self.navBar.setObjectName("NavBar")
        self.navBar.addItems(ITEMS.keys())
        self.navBar.setFixedWidth(180)
        self.navBar.itemClicked.connect(self.handlerItemClick)

        layout = QVBoxLayout()
        layout.addWidget(self.navBar)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def handlerItemClick(self, item, text=""):
        if item:
            self.widget = ITEMS[item.text()](self.central)
            self.central.mainForm.header.labelContents.setText(item.text())
        else:
            self.widget = ITEMS[text](self.central)
            self.central.mainForm.header.labelContents.setText(text)

        self.central.mainForm.layoutContents.itemAt(2).widget().deleteLater()
        self.central.mainForm.layoutContents.addWidget(self.widget, 10)
