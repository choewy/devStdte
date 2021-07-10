from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from src.widget.answer import Answer


STATUS = {
    0: "종료",
    1: "진행"
}


class Survey(QWidget):
    def __init__(self, central, uuid):
        QWidget.__init__(self)
        self.central = central
        self.uuid = uuid

        self.surveySource = None

        self.comboStatus = QComboBox()
        self.comboStatus.setObjectName("SurveyCombo-status")
        self.comboStatus.addItems(STATUS.values())
        self.comboStatus.setEnabled(False)

        self.buttonEdit = QPushButton()
        self.buttonEdit.setObjectName("SurveyButton-edit")
        self.buttonEdit.setText("수정")
        self.buttonEdit.clicked.connect(self.handleButtonEditClick)

        self.buttonRemove = QPushButton()
        self.buttonRemove.setObjectName("SurveyButton-remove")
        self.buttonRemove.setText("삭제")
        self.buttonRemove.setVisible(False)
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

        self.textAnswer = QTextEdit()
        self.textAnswer.setObjectName("SurveyText-answer")
        self.textAnswer.setPlaceholderText("답글을 입력하세요.")

        self.buttonUpload = QPushButton()
        self.buttonUpload.setObjectName("SurveyButton-upload")
        self.buttonUpload.setText("등록")

        layoutAnswer = QHBoxLayout()
        layoutAnswer.addWidget(self.textAnswer, 10)
        layoutAnswer.addWidget(self.buttonUpload, 0)
        layoutAnswer.setContentsMargins(0, 0, 0, 0)

        layoutRight = QVBoxLayout()
        layoutRight.addWidget(self.tableAnswers, 10)
        layoutRight.addLayout(layoutAnswer, 0)

        layout = QHBoxLayout()
        layout.addLayout(layoutLeft)
        layout.addLayout(layoutRight)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

        self.setSurveySource()
        self.setAnswerTable()

    def setSurveySource(self):
        try:
            self.surveySource = self.central.realtimeDB.getSurveySource(self.uuid)
            status = self.surveySource["status"]
            self.textAnswer.setVisible(status)
            self.buttonUpload.setVisible(status)
            self.comboStatus.setCurrentText(STATUS[status])

            admin = self.surveySource["admin"]
            adminFlag = (self.central.clientId == admin) or (self.central.clientAuth in ["관리자", "개발자"])
            self.buttonEdit.setVisible(adminFlag)

        except Exception as e:
            print(e)

    def setAnswerTable(self):
        self.textTitle.setText(self.surveySource["title"])
        self.textContents.setPlainText(self.surveySource["contents"])

        self.tableAnswers.clear()
        self.tableAnswers.setRowCount(0)
        self.tableAnswers.setColumnCount(1)

        if "answers" in self.surveySource.keys():
            for row, key in enumerate(self.surveySource["answers"].keys()):
                answerSource = self.surveySource["answers"][key]
                answerWidget = Answer(self, answerSource)
                self.tableAnswers.insertRow(row)
                self.tableAnswers.setCellWidget(row, 0, answerWidget)

            self.tableAnswers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tableAnswers.resizeRowsToContents()

    def handleButtonEditClick(self):
        if self.buttonEdit.text() == "수정":
            self.buttonEdit.setText("완료")
            self.buttonRemove.setVisible(True)
            self.comboStatus.setEnabled(True)
            self.textTitle.setReadOnly(False)
            self.textContents.setReadOnly(False)

        else:
            self.buttonEdit.setText("수정")

            title = self.textTitle.text()
            contents = self.textContents.toPlainText()
            status = self.comboStatus.currentText()
            # 저장

            self.buttonRemove.setVisible(False)
            self.comboStatus.setEnabled(False)
            self.textTitle.setReadOnly(True)
            self.textContents.setReadOnly(True)

    def handleButtonRemoveClick(self):
        pass    # 삭제