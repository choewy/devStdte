from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QFontMetricsF, QPixmap, QIcon


class New(QDialog):
    def __init__(self, central):
        QDialog.__init__(self, central)
        self.central = central

        self.setObjectName("NewDialog")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(600)
        self.setFixedHeight(800)

        self.buttonSave = QPushButton()
        self.buttonSave.setObjectName("NewButton-save")
        self.buttonSave.setIcon(QIcon(QPixmap("images/survey-save.png").scaledToHeight(30)))
        self.buttonSave.setEnabled(False)
        self.buttonSave.setFocusPolicy(Qt.NoFocus)
        self.buttonSave.setCursor(Qt.PointingHandCursor)
        self.buttonSave.clicked.connect(self.handleButtonSave)

        self.buttonClose = QPushButton()
        self.buttonClose.setObjectName("NewButton-close")
        self.buttonClose.setIcon(QIcon(QPixmap("images/close.png").scaledToHeight(12)))
        self.buttonClose.setFocusPolicy(Qt.NoFocus)
        self.buttonClose.setCursor(Qt.PointingHandCursor)
        self.buttonClose.clicked.connect(self.close)

        layoutButtons = QHBoxLayout()
        layoutButtons.addWidget(QLabel(" "), 10)
        layoutButtons.addWidget(self.buttonSave)
        layoutButtons.addWidget(self.buttonClose)
        layoutButtons.setContentsMargins(0, 0, 0, 0)

        self.inputTitle = QLineEdit()
        self.inputTitle.setObjectName("NewText-title")
        self.inputTitle.setPlaceholderText("제목")
        self.inputTitle.textChanged.connect(self.handleInputChange)

        self.inputContents = QTextEdit()
        self.inputContents.setObjectName("NewText-contents")
        self.inputContents.setPlaceholderText("내용")
        self.inputContents.textChanged.connect(self.handleInputChange)

        font = self.inputContents.font()
        fontMetrics = QFontMetricsF(font)
        spaceWidth = fontMetrics.width(' ')

        self.inputContents.setTabStopDistance(spaceWidth * 4)

        layout = QVBoxLayout()
        layout.addLayout(layoutButtons, 0)
        layout.addWidget(self.inputTitle, 0)
        layout.addWidget(self.inputContents, 10)

        self.setLayout(layout)

    def handleButtonSave(self):
        title = self.inputTitle.text()
        contents = self.inputContents.toPlainText()
        uuid = self.central.realtimeDB.newSurveySource(self.central.clientId, title, contents)
        self.central.mainForm.navBar.setSurveyWidget(uuid)
        self.close()

    def handleInputChange(self):
        title = self.inputTitle.text()
        contents = self.inputContents.toPlainText()

        if title and contents:
            self.buttonSave.setEnabled(True)

        else:
            self.buttonSave.setEnabled(False)
