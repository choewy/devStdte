from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from src.widget.answer import Answer


class Survey(QWidget):
    def __init__(self, central, uuid):
        QWidget.__init__(self)
        self.central = central
        self.uuid = uuid

        self.surveySource = None

        # self.buttonEdit = QPushButton()
        # self.buttonEdit.setText("수정")

        self.textTitle = QLineEdit()
        self.textTitle.setObjectName("SurveyText-title")
        self.textTitle.setEnabled(False)

        self.textContents = QTextBrowser()
        self.textContents.setObjectName("SurveyTextBrowser")

        layoutLeft = QVBoxLayout()
        layoutLeft.addWidget(self.textTitle, 0)
        layoutLeft.addWidget(self.textContents, 10)

        # self.groupAnswer = QGroupBox()
        # self.groupAnswer.setObjectName("SurveyGroup-answers")

        self.tableAnswers = QTableWidget()
        self.tableAnswers.setObjectName("SurveyTable-answers")
        self.tableAnswers.horizontalHeader().setVisible(False)
        self.tableAnswers.verticalHeader().setVisible(False)

        self.textAnswer = QTextEdit()
        self.textAnswer.setObjectName("SurveyText-answer")

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

    def setSurveySource(self):
        try:
            self.surveySource = self.central.realtimeDB.getSurveySource(self.uuid)

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
        except Exception as e:
            print(e)

    def setSurveySource_1(self):
        self.surveySource = self.central.realtimeDB.getSurveySource(self.uuid)

        self.textTitle.setText(self.surveySource["title"])
        self.textContents.setPlainText(self.surveySource["contents"])

        layout = QVBoxLayout()
        
        # 여기 수정 필요함 :: string indices must be integers
        try:
            if "answers" in self.surveySource.keys():
                for key in self.surveySource["answers"].keys():
                    answerSource = self.surveySource["answers"][key]
                    layout.addWidget(Answer(self, answerSource), stretch=0, alignment=Qt.AlignTop)
        except Exception as e:
            print(e)
        layout.setContentsMargins(0, 0, 0, 0)

        self.groupAnswer.setLayout(layout)
