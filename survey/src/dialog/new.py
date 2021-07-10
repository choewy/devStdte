from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFontMetricsF


class New(QDialog):
    def __init__(self, central):
        QDialog.__init__(self, central)
        self.central = central

        self.setWindowFlag(Qt.FramelessWindowHint)

        self.inputTitle = QLineEdit()
        self.inputTitle.setObjectName("NewText-title")
        self.inputTitle.setPlaceholderText("제목")

        self.inputContents = QTextEdit()
        self.inputContents.setObjectName("NewText-contents")
        self.inputContents.setPlaceholderText("내용")

        font = self.inputContents.font()
        fontMetrics = QFontMetricsF(font)
        spaceWidth = fontMetrics.width(' ')

        self.inputContents.setTabStopDistance(spaceWidth * 4)

        self.labelError = QLabel()
        self.labelError.setObjectName("NewLabel-error")
        self.labelError.setText(" ")
        self.labelError.setAlignment(Qt.AlignCenter)

        self.buttonCreate = QPushButton()
        self.buttonCreate.setObjectName("NewButton-create")
        self.buttonCreate.setText("등록")
        self.buttonCreate.setCursor(Qt.PointingHandCursor)
        self.buttonCreate.clicked.connect(self.handleButtonCreate)

        self.buttonCancel = QPushButton()
        self.buttonCancel.setObjectName("NewButton-cancel")
        self.buttonCancel.setText("취소")
        self.buttonCancel.setCursor(Qt.PointingHandCursor)
        self.buttonCancel.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.inputTitle, 0)
        layout.addWidget(self.inputContents, 10)
        layout.addWidget(self.labelError, 0)
        layout.addWidget(self.buttonCreate, 0)
        layout.addWidget(self.buttonCancel, 0)

        self.setLayout(layout)

    def handleButtonCreate(self):
        title = self.inputTitle.text()
        contents = self.inputContents.toPlainText()

        if not title:
            self.labelError.setText("제목을 입력하세요.")

        elif not contents:
            self.labelError.setText("내용을 입력하세요.")

        else:
            uuid = self.central.realtimeDB.newSurveySource(self.central.clientId, title, contents)
            self.central.mainForm.navBar.setSurveyWidget(uuid)
            self.close()
