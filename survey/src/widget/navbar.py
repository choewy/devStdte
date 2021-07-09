from PyQt5.QtWidgets import *
from src.dialog.manual import Manual
from src.widget.home import Home
from src.widget.list import List
from src.widget.survey import Survey

ITEMS = {
    "    홈": {
        "type": "widget",
        "object": Home
    },
    "    운영방안": {
        "type": "dialog",
        "object": Manual
    },
    "    목록": {
        "type": "widget",
        "object": List
    },
    "    로그아웃": {
        "type": "function",
        "object": None
    }
}


class NavBar(QWidget):
    def __init__(self, central):
        QWidget.__init__(self)
        self.central = central

        self.widget = None

        self.navBar = QListWidget()
        self.navBar.setObjectName("NavBarList")
        self.navBar.addItems(ITEMS.keys())
        self.navBar.setFixedWidth(180)
        self.navBar.itemClicked.connect(self.handleItemClick)

        layout = QVBoxLayout()
        layout.addWidget(self.navBar)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def handleItemClick(self, item):
        try:
            itemText = item.text()

            widgetType = ITEMS[itemText]["type"]
            if widgetType == "widget":
                self.widget = ITEMS[itemText]["object"](self.central)
                self.central.mainForm.layout().itemAt(2).widget().deleteLater()
                self.central.mainForm.layout().addWidget(self.widget, 10)

            elif widgetType == "dialog":
                ITEMS[itemText]["object"](self.central).exec_()

            else:
                self.central.setLayoutAuth()

        except Exception as e:
            print(e)

    def setSurveyWidget(self, uuid):
        self.widget = Survey(self.central, uuid)
        self.central.mainForm.layout().itemAt(2).widget().deleteLater()
        self.central.mainForm.layout().addWidget(self.widget, 10)
