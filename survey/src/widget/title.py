from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *


NEW_ICON_PATH = "images/survey-new.png"
ICON_PATHS = {
    0: "images/status-false.png",
    1: "images/status-true.png"
}


class Title(QWidget):
    def __init__(self, central, uuid, status, title, isView):
        QWidget.__init__(self, central)
        self.central = central
        self.uuid = uuid

        self.setFixedHeight(50)

        self.labelStatus = QLabel()
        self.labelStatus.setObjectName("TitleLabel-status")
        self.labelStatus.setPixmap(QPixmap())
        self.labelStatus.setPixmap(QPixmap(ICON_PATHS[status]).scaledToHeight(20))
        self.labelStatus.setAlignment(Qt.AlignCenter)

        self.buttonTitle = QPushButton()
        self.buttonTitle.setObjectName("TitleButton-item-title")
        self.buttonTitle.setText(title)
        self.buttonTitle.setCursor(Qt.PointingHandCursor)
        self.buttonTitle.setFocusPolicy(Qt.NoFocus)
        self.buttonTitle.clicked.connect(self.handleButtonTitleClick)

        self.labelVisible = QLabel(self.buttonTitle)
        self.labelVisible.setObjectName("TitleLabel-visible")

        if not isView and status:
            self.labelVisible.setPixmap(QPixmap(NEW_ICON_PATH).scaledToHeight(30))

        layout = QHBoxLayout()
        layout.addWidget(self.labelStatus, 0)
        layout.addWidget(self.buttonTitle, 10)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def handleButtonTitleClick(self):
        try:
            self.central.realtimeDB.setSurveyView(self.central.clientId, self.uuid)
            self.central.mainForm.navBar.setSurveyWidget(self.uuid)
        except Exception as e:
            print(e)