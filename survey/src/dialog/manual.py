from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetricsF
from PyQt5.QtWidgets import *


class Manual(QDialog):
    def __init__(self, central):
        QDialog.__init__(self, central)
        self.central = central

        self.setWindowFlag(Qt.FramelessWindowHint)

        self.manualSource = None
        self.editFlag = self.central.clientAuth in ["관리자", "개발자"]

        self.buttonEdit = QPushButton()
        self.buttonEdit.setObjectName("ManualButton-edit")
        self.buttonEdit.setText("수정")

        if not self.editFlag:
            self.buttonEdit.setVisible(False)

        self.buttonEdit.setCursor(Qt.PointingHandCursor)
        self.buttonEdit.clicked.connect(self.handleButtonEditClick)

        self.inputManual = QTextEdit()
        self.inputManual.setObjectName("ManualText-contents")

        font = self.inputManual.font()
        fontMetrics = QFontMetricsF(font)
        spaceWidth = fontMetrics.width(' ')

        self.inputManual.setTabStopDistance(spaceWidth * 4)
        self.inputManual.setReadOnly(True)

        self.buttonClose = QPushButton()
        self.buttonClose.setObjectName("ManualButton-close")
        self.buttonClose.setText("닫기")
        self.buttonClose.setCursor(Qt.PointingHandCursor)
        self.buttonClose.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.buttonEdit, alignment=Qt.AlignLeft)
        layout.addWidget(self.inputManual, stretch=10)
        layout.addWidget(self.buttonClose)

        self.setLayout(layout)
        self.setManual()

    def setManual(self):
        self.manualSource = self.central.realtimeDB.getManualSource()
        self.inputManual.setPlainText(self.manualSource.replace("\t", " "*4))

    def handleButtonEditClick(self):
        if self.buttonEdit.text() == "수정":
            self.buttonEdit.setText("완료")
            self.inputManual.setReadOnly(False)

        else:
            oldManualSource = self.manualSource
            newManualSource = self.inputManual.toPlainText()

            if oldManualSource != newManualSource:
                self.central.realtimeDB.setManualSource(newManualSource)
                self.setManual()

            self.buttonEdit.setText("수정")
            self.inputManual.setReadOnly(True)