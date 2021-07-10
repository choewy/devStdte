from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QTableWidget, QAbstractItemView, QLabel, QVBoxLayout, QLineEdit, QPushButton, \
    QTableWidgetItem, QHeaderView

from src.widget.title import Title

NEW_ICON_PATH = "images/survey-new.png"
ICON_PATHS = {
    0: "images/status-false.png",
    1: "images/status-true.png"
}


class List(QWidget):
    def __init__(self, central):
        QWidget.__init__(self)

        self.central = central

        self.surveySources = None

        self.tableSurvey = QTableWidget()
        self.tableSurvey.setObjectName("ListTable")
        self.tableSurvey.verticalHeader().setVisible(False)
        self.tableSurvey.horizontalHeader().setVisible(False)
        self.tableSurvey.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableSurvey.setFocusPolicy(Qt.NoFocus)
        self.tableSurvey.setVisible(False)

        self.labelSurvey = QLabel()
        self.labelSurvey.setObjectName("ListLabel")
        self.labelSurvey.setText("※ 이슈사항이 없습니다.")
        self.labelSurvey.setAlignment(Qt.AlignCenter)
        self.labelSurvey.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.tableSurvey)
        layout.addWidget(self.labelSurvey)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
        self.setTableSurvey()

    def setTableSurvey(self):
        self.surveySources = self.central.realtimeDB.getSurveySources(self.central.clientId)

        if self.surveySources:
            self.tableSurvey.clear()
            self.tableSurvey.setRowCount(0)
            self.tableSurvey.setColumnCount(3)

            for row, (uuid, status, title, isView, createTime, answerCounts) in enumerate(self.surveySources):
                self.tableSurvey.insertRow(row)

                widgetTitle = Title(self.central, uuid, status, title, isView)

                self.tableSurvey.setCellWidget(row, 0, widgetTitle)

                itemCreateTime = QTableWidgetItem()
                itemCreateTime.setText(f"  최초게시일 : {createTime}  ")
                itemCreateTime.setFlags(Qt.ItemIsEditable)

                self.tableSurvey.setItem(row, 1, itemCreateTime)

                itemAnswerCounts = QTableWidgetItem()
                itemAnswerCounts.setText(f"  답글 수 : {answerCounts}  ")
                itemAnswerCounts.setFlags(Qt.ItemIsEditable)

                self.tableSurvey.setItem(row, 2, itemAnswerCounts)
                self.tableSurvey.setRowHeight(row, 50)

            self.tableSurvey.resizeColumnsToContents()
            self.tableSurvey.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.tableSurvey.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
            self.tableSurvey.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)

            self.labelSurvey.setVisible(False)
            self.tableSurvey.setVisible(True)

        else:
            self.tableSurvey.setVisible(False)
            self.labelSurvey.setVisible(True)
