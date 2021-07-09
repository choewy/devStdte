from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QTextEdit, QPushButton, QVBoxLayout


class DialogMemo(QDialog):
    def __init__(self, schedule, flag, item):
        QDialog.__init__(self, schedule.central.window)

        self.setObjectName("MemoDialog")
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.schedule = schedule
        self.flag = flag

        memoSource = item.memoSource
        self.key = memoSource[0][5:]
        self.oldMemo = memoSource[1]

        self.labelDate = QLabel()
        self.labelDate.setObjectName("MemoLabel-date")
        self.labelDate.setAlignment(Qt.AlignCenter)
        self.labelDate.setText(f"{memoSource[0]}")

        self.inputMemo = QTextEdit()
        self.inputMemo.setObjectName("MemoInput")
        self.inputMemo.setText(self.oldMemo)
        self.inputMemo.setEnabled(flag)

        self.btnOk = QPushButton()
        self.btnOk.setObjectName("MemoButton")
        self.btnOk.setText("저장" if flag else "닫기")
        self.btnOk.setCursor(Qt.PointingHandCursor)
        self.btnOk.clicked.connect(self.handleBtnOkClick)

        layout = QVBoxLayout()
        layout.addWidget(self.labelDate)
        layout.addWidget(self.inputMemo)
        layout.addWidget(self.btnOk, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def handleBtnOkClick(self):
        newMemo = self.inputMemo.toPlainText()
        if newMemo != self.oldMemo:
            self.schedule.central.realTimeDB.setMemo(self.schedule.currentYear, self.key, newMemo)
            self.schedule.setListMemo()
            self.schedule.setTableMemo()
        self.close()



