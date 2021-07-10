from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QVBoxLayout, QTableWidget, \
    QAbstractItemView, QHeaderView
from src.widget.answer import Answer
from src.widget.header import Header

ENCODE_STATUS = {
    0: "종료",
    1: "진행"
}

DECODE_STATUS = {
    "종료": 0,
    "진행": 1
}

UPLOAD_ICON_PATH = "images/answer-upload.png"


class Survey(QWidget):
    def __init__(self, central, uuid):
        QWidget.__init__(self)
        self.central = central
        self.uuid = uuid

        self.surveySource = None

        self.header = Header(self)

        self.textTitle = QLineEdit()
        self.textTitle.setObjectName("SurveyText-title")
        self.textTitle.setVisible(False)

        self.textContents = QTextEdit()
        self.textContents.setObjectName("SurveyText-contents")
        self.textContents.setReadOnly(True)

        layoutLeft = QVBoxLayout()
        layoutLeft.addWidget(self.textTitle, 0)
        layoutLeft.addWidget(self.textContents, 10)

        self.tableAnswers = QTableWidget()
        self.tableAnswers.setObjectName("SurveyTable-answers")
        self.tableAnswers.horizontalHeader().setVisible(False)
        self.tableAnswers.verticalHeader().setVisible(False)
        self.tableAnswers.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableAnswers.setFocusPolicy(Qt.NoFocus)
        self.tableAnswers.setShowGrid(False)
        self.tableAnswers.setVisible(False)

        self.labelAnswers = QLabel()
        self.labelAnswers.setObjectName("SurveyLabel")
        self.labelAnswers.setText("※ 답글이 존재하지 않습니다.")
        self.labelAnswers.setAlignment(Qt.AlignCenter)
        self.labelAnswers.setVisible(False)

        self.textAnswer = QTextEdit()
        self.textAnswer.setObjectName("SurveyText-answer")
        self.textAnswer.setPlaceholderText("답글을 입력하세요.")
        self.textAnswer.textChanged.connect(self.handleTextAnswerChange)

        self.buttonUpload = QPushButton()
        self.buttonUpload.setObjectName("SurveyButton-upload")
        self.buttonUpload.setIcon(QIcon(QPixmap(UPLOAD_ICON_PATH)))
        self.buttonUpload.setIconSize(QSize(40, 30))
        self.buttonUpload.setEnabled(False)
        self.buttonUpload.setCursor(Qt.PointingHandCursor)
        self.buttonUpload.clicked.connect(self.handleButtonUploadClick)

        layoutAnswer = QHBoxLayout()
        layoutAnswer.addWidget(self.textAnswer, 10)
        layoutAnswer.addWidget(self.buttonUpload, 0)
        layoutAnswer.setContentsMargins(0, 0, 0, 0)

        layoutRight = QVBoxLayout()
        layoutRight.addWidget(self.tableAnswers, 10)
        layoutRight.addWidget(self.labelAnswers, 10)
        layoutRight.addLayout(layoutAnswer, 0)
        layoutRight.setContentsMargins(0, 0, 0, 0)

        layoutBottom = QHBoxLayout()
        layoutBottom.addLayout(layoutLeft, 5)
        layoutBottom.addLayout(layoutRight, 5)
        layoutBottom.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.addWidget(self.header, 0)
        layout.addLayout(layoutBottom, 10)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

        self.setSurveySource()
        self.setAnswerTable()

    def setSurveySource(self):
        self.surveySource = self.central.realtimeDB.getSurveySource(self.uuid)
        status = self.surveySource["status"]
        self.textAnswer.setVisible(status)
        self.buttonUpload.setVisible(status)

        self.header.setHeader()

        self.textTitle.setText(self.surveySource["title"].replace("\t", " "*4))
        self.textContents.setPlainText(self.surveySource["contents"].replace("\t", " "*4))

    def setAnswerTable(self):

        if "answers" in self.surveySource.keys():
            self.tableAnswers.clear()
            self.tableAnswers.setRowCount(0)
            self.tableAnswers.setColumnCount(1)

            for row, key in enumerate(self.surveySource["answers"].keys()):
                answerSource = self.surveySource["answers"][key]
                answerWidget = Answer(self, key, answerSource)
                self.tableAnswers.insertRow(row)
                self.tableAnswers.setCellWidget(row, 0, answerWidget)

            self.tableAnswers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tableAnswers.resizeRowsToContents()

            self.labelAnswers.setVisible(False)
            self.tableAnswers.setVisible(True)

        else:
            self.tableAnswers.setVisible(False)
            self.labelAnswers.setVisible(True)

    def handleButtonUploadClick(self):
        answer = self.textAnswer.toPlainText()
        self.central.realtimeDB.setAnswer(self.uuid, answer)
        self.textAnswer.clear()
        self.setSurveySource()
        self.setAnswerTable()

    def handleTextAnswerChange(self):
        text = self.textAnswer.toPlainText()

        if text:
            self.buttonUpload.setEnabled(True)
        else:
            self.buttonUpload.setEnabled(False)
