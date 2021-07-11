from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QListWidget
from src.dialog.manual import Manual
from src.dialog.new import New
from src.widget.home import Home
from src.widget.list import List
from src.widget.survey import Survey

ITEMS = {
    "    홈": {
        "type": "widget",
        "object": Home
    },
    "    이슈현황": {
        "type": "widget",
        "object": List
    },
    "    이슈등록": {
        "type": "dialog",
        "object": New
    },
    "    운영방안": {
        "type": "dialog",
        "object": Manual
    },
    "    로그아웃": {
        "type": "function",
        "object": None
    }
}


class NavBar(QListWidget):
    def __init__(self, central):
        QWidget.__init__(self)
        self.central = central

        self.widget = None
        self.setObjectName("NavBarList")
        self.addItems(ITEMS.keys())
        self.setFixedWidth(180)
        self.setFocusPolicy(Qt.NoFocus)
        self.itemClicked.connect(self.handleItemClick)

    def handleItemClick(self, item):
        itemText = item.text()

        widgetType = ITEMS[itemText]["type"]
        if widgetType == "widget":
            self.widget = ITEMS[itemText]["object"](self.central)
            self.central.mainForm.layoutContents.itemAt(0).widget().deleteLater()
            self.central.mainForm.layoutContents.insertWidget(0, self.widget, 10)

        elif widgetType == "dialog":
            ITEMS[itemText]["object"](self.central).exec_()

        else:
            self.central.setLayoutAuth()

    def setHomeWidget(self):
        self.widget = ITEMS["    홈"]["object"](self.central)
        self.central.mainForm.layoutContents.itemAt(0).widget().deleteLater()
        self.central.mainForm.layoutContents.insertWidget(0, self.widget, 10)

    def setSurveyList(self):
        self.widget = ITEMS["    이슈현황"]["object"](self.central)
        self.central.mainForm.layoutContents.itemAt(0).widget().deleteLater()
        self.central.mainForm.layoutContents.insertWidget(0, self.widget, 10)

    def setSurveyWidget(self, uuid):
        self.widget = Survey(self.central, uuid)
        self.central.mainForm.layoutContents.itemAt(0).widget().deleteLater()
        self.central.mainForm.layoutContents.insertWidget(0, self.widget, 10)
