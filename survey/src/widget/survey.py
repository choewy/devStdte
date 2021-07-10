from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from src.dialog.question import Question
from src.widget.answer import Answer


ENCODE_STATUS = {
    0: "종료",
    1: "진행"
}

DECODE_STATUS = {
    "종료": 0,
    "진행": 1
}


class Survey(QWidget):
    def __init__(self, central, uuid):
        QWidget.__init__(self)
        self.central = central
        self.uuid = uuid

        self.surveySource = None

        self.comboStatus = QComboBox()
        self.comboStatus.setObjectName("SurveyCombo-status")
        self.comboStatus.addItems(ENCODE_STATUS.values())
        self.comboStatus.setEnabled(False)

        self.buttonEdit = QPushButton()
        self.buttonEdit.setObjectName("SurveyButton-edit")
        self.buttonEdit.setText("수정")
        self.buttonEdit.setCursor(Qt.PointingHandCursor)
        self.buttonEdit.clicked.connect(self.handleButtonEditClick)

        self.buttonRemove = QPushButton()
        self.buttonRemove.setObjectName("SurveyButton-remove")
        self.buttonRemove.setText("삭제")
        self.buttonRemove.setVisible(False)
        self.buttonRemove.setCursor(Qt.PointingHandCursor)
        self.buttonRemove.clicked.connect(self.handleButtonRemoveClick)

        layoutSetting = QHBoxLayout()
        layoutSetting.addWidget(self.comboStatus, alignment=Qt.AlignLeft)
        layoutSetting.addWidget(QLabel(" "), 10)
        layoutSetting.addWidget(self.buttonRemove, alignment=Qt.AlignRight)
        layoutSetting.addWidget(self.buttonEdit, alignment=Qt.AlignRight)
        layoutSetting.setContentsMargins(0, 0, 0, 0)

        self.textTitle = QLineEdit()
        self.textTitle.setObjectName("SurveyText-title")
        self.textTitle.setReadOnly(True)

        self.textContents = QTextEdit()
        self.textContents.setObjectName("SurveyText-contents")
        self.textContents.setReadOnly(True)

        layoutLeft = QVBoxLayout()
        layoutLeft.addLayout(layoutSetting, 0)
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
        self.labelAnswers.setText("답글이 존재하지 않습니다.")
        self.labelAnswers.setAlignment(Qt.AlignCenter)
        self.labelAnswers.setVisible(False)

        self.textAnswer = QTextEdit()
        self.textAnswer.setObjectName("SurveyText-answer")
        self.textAnswer.setPlaceholderText("답글을 입력하세요.")

        self.buttonUpload = QPushButton()
        self.buttonUpload.setObjectName("SurveyButton-upload")
        self.buttonUpload.setText("등록")
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

        layout = QHBoxLayout()
        layout.addLayout(layoutLeft)
        layout.addLayout(layoutRight)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

        self.setSurveySource()
        self.setAnswerTable()

    def setSurveySource(self):
        self.surveySource = self.central.realtimeDB.getSurveySource(self.uuid)
        status = self.surveySource["status"]
        self.textAnswer.setVisible(status)
        self.buttonUpload.setVisible(status)
        self.comboStatus.setCurrentText(ENCODE_STATUS[status])

        admin = self.surveySource["admin"]
        adminFlag = (self.central.clientId == admin) or (self.central.clientAuth in ["관리자", "개발자"])
        self.buttonEdit.setVisible(adminFlag)

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

    def handleButtonEditClick(self):
        if self.buttonEdit.text() == "수정":
            self.buttonEdit.setText("완료")
            self.buttonRemove.setVisible(True)
            self.comboStatus.setEnabled(True)
            self.textTitle.setReadOnly(False)
            self.textContents.setReadOnly(False)

        else:
            oldSurveySource = {
                "title": self.surveySource["title"],
                "contents": self.surveySource["contents"],
                "status": self.surveySource["status"]
            }

            newSurveySource = {
                "title": self.textTitle.text(),
                "contents": self.textContents.toPlainText(),
                "status": DECODE_STATUS[self.comboStatus.currentText()]
            }

            if oldSurveySource != newSurveySource:
                self.central.realtimeDB.setSurveySource(self.uuid, newSurveySource)
                self.setSurveySource()
                self.setAnswerTable()

            self.buttonEdit.setText("수정")
            self.buttonRemove.setVisible(False)
            self.comboStatus.setEnabled(False)
            self.textTitle.setReadOnly(True)
            self.textContents.setReadOnly(True)
    
    def handleButtonRemoveClick(self):
        question = Question(self.central, "설문을 삭제하시겠습니까?", "삭제", "취소")
        question.exec_()

        if question.answer:
            self.central.realtimeDB.removeSurveySource(self.uuid)
            self.central.mainForm.navBar.setSurveyList()

    def handleButtonUploadClick(self):
        answer = self.textAnswer.toPlainText()
        self.central.realtimeDB.setAnswer(self.uuid, answer)
        self.textAnswer.clear()
        self.setSurveySource()
        self.setAnswerTable()
