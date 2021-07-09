from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QWidget, QCheckBox, QListWidget, QTabWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QHBoxLayout, QLabel, QComboBox, QPushButton, QListWidgetItem, QHeaderView, QFileDialog
from datetime import date

from src.dialog.memo import DialogMemo
from src.dialog.time import DialogTime


WEEKDAYS = ["(월)", "(화)", "(수)", "(목)", "(금)", "(토)", "(일)"]
TASK_COLUMNS = ["사업명", "사업코드", "구분"]
TASK_OPTIONS = {
    "회의": "0",
    "교육/훈련": "1",
    "기타업무": "2",
    "사업관리": "3",
    "기술업무": "4"
}


class Schedule(QWidget):
    def __init__(self, central=None) -> None:
        QWidget.__init__(self)
        self.central = central

        self.timeColumns = None
        self.userSource = None
        self.memoSource = None
        self.taskSource = None
        self.rowSource = None
        self.timeSource = None
        self.totalSource = None

        self.oldUserFlag = True

        self.currentYear = f"{date.today().year}"
        self.currentUserId = self.central.clientId

        self.checkHideUser = QCheckBox()
        self.checkHideUser.setObjectName("ScheduleCheck-hidden")
        self.checkHideUser.setText("재직자만 보기")
        self.checkHideUser.setChecked(True)
        self.checkHideUser.clicked.connect(self.handleCheckHideUserClick)

        self.listUser = QListWidget()
        self.listUser.setObjectName("ScheduleList")
        self.listUser.verticalScrollBar().setVisible(False)
        self.listUser.horizontalScrollBar().setVisible(False)
        self.listUser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listUser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listUser.itemClicked.connect(self.handleListUserItemClick)

        self.listMemo = QListWidget()
        self.listMemo.setObjectName("ScheduleList")
        self.listMemo.verticalScrollBar().setVisible(False)
        self.listMemo.horizontalScrollBar().setVisible(False)
        self.listMemo.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listMemo.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listMemo.itemClicked.connect(self.handleListMemoItemClick)

        self.tabList = QTabWidget()
        self.tabList.setObjectName("ScheduleTab")
        self.tabList.addTab(self.listUser, "현황")
        self.tabList.addTab(self.listMemo, "메모")

        layoutList = QVBoxLayout()
        layoutList.addWidget(self.checkHideUser, 0)
        layoutList.addWidget(self.tabList, 10)
        layoutList.setContentsMargins(0, 0, 0, 0)

        # 메모 테이블 헤더
        self.tableMemoHeader = QTableWidget()
        self.tableMemoHeader.setObjectName("ScheduleTableHeader")
        self.tableMemoHeader.setRowCount(1)
        self.tableMemoHeader.setColumnCount(1)
        self.tableMemoHeader.horizontalHeader().setVisible(False)
        self.tableMemoHeader.verticalHeader().setVisible(False)
        self.tableMemoHeader.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableMemoHeader.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        memoHeaderItem = QTableWidgetItem()
        memoHeaderItem.setText("메모")
        memoHeaderItem.setTextAlignment(Qt.AlignCenter)
        memoHeaderItem.setFlags(Qt.ItemIsEditable)

        self.tableMemoHeader.setItem(0, 0, memoHeaderItem)
        self.tableMemoHeader.setFixedHeight(self.tableMemoHeader.rowHeight(0))
        
        # 메모 테이블
        self.tableMemo = QTableWidget()
        self.tableMemo.setObjectName("ScheduleTableHeader")
        self.tableMemo.setRowCount(1)
        self.tableMemo.horizontalHeader().setVisible(False)
        self.tableMemo.verticalHeader().setVisible(False)
        self.tableMemo.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableMemo.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableMemo.setFixedHeight(self.tableMemo.rowHeight(0))
        self.tableMemo.cellClicked.connect(self.handleTableMemoCellClick)
        self.tableMemo.horizontalScrollBar().valueChanged.connect(self.handleTableMemoHorizontalScrollChange)

        layoutTblMemo = QHBoxLayout()
        layoutTblMemo.addWidget(self.tableMemoHeader)
        layoutTblMemo.addWidget(self.tableMemo)
        layoutTblMemo.setContentsMargins(0, 0, 0, 0)

        # 일간합계 테이블 헤더
        self.tableTotalHeader = QTableWidget()
        self.tableTotalHeader.setObjectName("ScheduleTableHeader")
        self.tableTotalHeader.setRowCount(1)
        self.tableTotalHeader.setColumnCount(1)
        self.tableTotalHeader.horizontalHeader().setVisible(False)
        self.tableTotalHeader.verticalHeader().setVisible(False)
        self.tableTotalHeader.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableTotalHeader.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        totalHeaderItem = QTableWidgetItem()
        totalHeaderItem.setText("일간합계")
        totalHeaderItem.setTextAlignment(Qt.AlignCenter)
        totalHeaderItem.setFlags(Qt.ItemIsEditable)

        self.tableTotalHeader.setItem(0, 0, totalHeaderItem)
        self.tableTotalHeader.setFixedHeight(self.tableTotalHeader.rowHeight(0))
        
        # 일일합계 테이블
        self.tableTotal = QTableWidget()
        self.tableTotal.setObjectName("ScheduleTable")
        self.tableTotal.setRowCount(1)
        self.tableTotal.horizontalHeader().setVisible(False)
        self.tableTotal.verticalHeader().setVisible(False)
        self.tableTotal.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableTotal.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableTotal.setFixedHeight(self.tableTotal.rowHeight(0))

        layoutTblTotal = QHBoxLayout()
        layoutTblTotal.addWidget(self.tableTotalHeader)
        layoutTblTotal.addWidget(self.tableTotal)
        layoutTblTotal.setContentsMargins(0, 0, 0, 0)
        
        # 사업 테이블
        self.tableTask = QTableWidget()
        self.tableTask.setObjectName("ScheduleTable")
        self.tableTask.verticalHeader().setVisible(False)
        self.tableTask.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableTask.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.tableTask.verticalScrollBar().valueChanged.connect(self.handleTableTaskVerticalScrollChange)

        # 시간 테이블
        self.tableTime = QTableWidget()
        self.tableTime.setObjectName("ScheduleTable")
        self.tableTime.verticalHeader().setVisible(False)
        self.tableTime.horizontalScrollBar().valueChanged.connect(self.handleTableTimeHorizontalScrollChange)
        self.tableTime.verticalScrollBar().valueChanged.connect(self.handleTableTimeVerticalScrollChange)
        self.tableTime.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableTime.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableTime.cellClicked.connect(self.handleTableTimeCellClick)

        layoutTblTime = QHBoxLayout()
        layoutTblTime.addWidget(self.tableTask)
        layoutTblTime.addWidget(self.tableTime)
        layoutTblTime.setContentsMargins(0, 0, 0, 0)

        self.labelYear = QLabel()
        self.labelYear.setObjectName("ScheduleLabel")
        self.labelYear.setText("기준연도 : ")

        self.comboYear = QComboBox()
        self.comboYear.setObjectName("ScheduleCombo")
        self.comboYear.currentTextChanged.connect(self.handleComboYearChange)

        self.buttonExcel = QPushButton()
        self.buttonExcel.setObjectName("ScheduleButton")
        self.buttonExcel.setText("엑셀 저장")
        self.buttonExcel.setCursor(Qt.PointingHandCursor)
        self.buttonExcel.clicked.connect(self.handleButtonExcelClick)

        layoutYear = QHBoxLayout()
        layoutYear.addWidget(self.labelYear, 0)
        layoutYear.addWidget(self.comboYear, 10)
        layoutYear.addWidget(self.buttonExcel, 0)
        layoutYear.setContentsMargins(0, 0, 0, 0)

        layoutTable = QVBoxLayout()
        layoutTable.addLayout(layoutYear)
        layoutTable.addLayout(layoutTblMemo)
        layoutTable.addLayout(layoutTblTotal)
        layoutTable.addLayout(layoutTblTime)
        layoutTable.addWidget(self.tableTime.horizontalScrollBar())
        layoutTable.setContentsMargins(0, 0, 0, 0)

        layout = QHBoxLayout()
        layout.addLayout(layoutList,0)
        layout.addLayout(layoutTable, 10)
        layout.addWidget(self.tableTime.verticalScrollBar())
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

        self.setListUser()
        self.setComboYear()
        self.setListMemo()
        self.setTableMemo()
        self.setTableTask()
        self.setTableTimeAndTotal()
        self.resizeTables()
        self.setToday()

    def setListUser(self) -> None:
        self.listUser.clear()

        hideRows = []
        self.userSource = self.central.realTimeDB.getScheduleUserListSource()

        currentRow = 0

        for row, [userId, userName, userStatus, editTime] in enumerate(self.userSource):
            item = QListWidgetItem()
            item.userId = userId
            item.userStatus = userStatus
            item.setText(f"{userName}\t{editTime}")

            self.listUser.addItem(item)

            if userId == self.currentUserId:
                currentRow = row

            if userStatus != "재직":
                hideRows.append(row)

        self.listUser.setCurrentRow(currentRow)

        if self.oldUserFlag:
            for row in hideRows:
                self.listUser.setRowHidden(row, self.oldUserFlag)

    def setListMemo(self) -> None:
        self.memoSource = self.central.realTimeDB.getScheduleMemoSource(self.currentYear, self.currentUserId, self.timeColumns)
        self.listMemo.clear()

        for memoSource in self.memoSource:
            if memoSource[1]:
                item = QListWidgetItem()
                item.memoSource = memoSource
                item.setText(' - '.join(memoSource))
                self.listMemo.addItem(item)

    def setComboYear(self) -> None:
        userYears = self.central.realTimeDB.getUserTimeYears(self.currentUserId)
        self.comboYear.clear()
        self.comboYear.addItems(userYears)

    def setTableTask(self) -> None:
        self.taskSource, self.rowSource = self.central.realTimeDB.getScheduleTaskSource()
        self.tableTask.clear()
        self.tableTask.setRowCount(0)
        self.tableTask.setColumnCount(len(TASK_COLUMNS))
        self.tableTask.setHorizontalHeaderLabels(TASK_COLUMNS)

        whiteRow1 = 3
        whiteRow2 = 4

        for row, taskValues in enumerate(self.taskSource):
            self.tableTask.insertRow(row)

            for col, taskValue in enumerate(taskValues[1:]):
                if col == 2:
                    taskItem = QTableWidgetItem()
                    taskItem.setText(taskValue)
                    taskItem.taskValues = taskValues
                else:
                    if (row != 0 and row % 2 == 0) or row == 1:
                        taskItem = QTableWidgetItem()

                    else:
                        taskItem = QTableWidgetItem(taskValue)

                        if col == 1:
                            taskItem.setTextAlignment(Qt.AlignCenter)

                taskItem.setFlags(Qt.ItemIsEditable)
                if row not in [whiteRow1, whiteRow2]:
                    taskItem.setBackground(QBrush(QColor(245, 245, 255)))

                self.tableTask.setItem(row, col, taskItem)

            if row == whiteRow2:
                whiteRow1 += 4
                whiteRow2 += 4

        self.tableTask.resizeColumnsToContents()

    def setTableMemo(self) -> None:
        self.tableMemo.clear()
        self.tableMemo.setColumnCount(len(self.timeColumns))

        for col, memoSource in enumerate(self.memoSource):
            item = QTableWidgetItem()
            item.memoSource = memoSource
            item.setText("■" if memoSource[1] else "")
            item.setTextAlignment(Qt.AlignCenter)
            self.tableMemo.setItem(0, col, item)

        self.tableMemo.setEditTriggers(QTableWidget.NoEditTriggers)

    def setTableTimeAndTotal(self) -> None:
        self.timeSource = self.central.realTimeDB.getScheduleTimeSource(self.currentYear, self.currentUserId, self.timeColumns, self.taskSource, self.rowSource)
        self.totalSource = [f"{sum(self.timeSource[column].tolist())}" for column in self.timeColumns]

        self.tableTotal.clear()
        self.tableTotal.setColumnCount(len(self.timeColumns))

        for col, total in enumerate(self.totalSource):
            item = QTableWidgetItem()
            item.setText(total)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsEditable)
            self.tableTotal.setItem(0, col, item)

        self.tableTime.clear()
        self.tableTime.setRowCount(0)
        self.tableTime.setColumnCount(len(self.timeColumns))
        self.tableTime.setHorizontalHeaderLabels(self.timeColumns)

        whiteRow1 = 3
        whiteRow2 = 4

        for row, timeValues in enumerate(self.timeSource.values):
            self.tableTime.insertRow(row)
            timeValues = [f"{value}" if value else "" for value in timeValues]

            for col, timeValue in enumerate(timeValues):

                timeItem = QTableWidgetItem()
                timeItem.setText(timeValue)
                timeItem.setTextAlignment(Qt.AlignCenter)

                if row not in [whiteRow1, whiteRow2]:
                    timeItem.setBackground(QBrush(QColor(245, 245, 255)))

                self.tableTime.setItem(row, col, timeItem)

            if row == whiteRow2:
                whiteRow1 += 4
                whiteRow2 += 4

        self.tableTime.resizeColumnsToContents()
        self.tableTime.setEditTriggers(QTableWidget.NoEditTriggers)

    def resizeTables(self) -> None:
        taskWidth = sum([self.tableTask.columnWidth(col) for col in range(len(TASK_COLUMNS))])

        self.tableMemoHeader.setColumnWidth(0, taskWidth)
        self.tableMemoHeader.setFixedWidth(taskWidth)
        self.tableTotalHeader.setColumnWidth(0, taskWidth)
        self.tableTotalHeader.setFixedWidth(taskWidth)
        self.tableTask.setFixedWidth(taskWidth)

        timeWidth = self.tableTime.columnWidth(0)
        for col in range(len(self.timeColumns)):
            self.tableMemo.setColumnWidth(col, timeWidth)
            self.tableTotal.setColumnWidth(col, timeWidth)

        self.tableTask.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableTime.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

    def setToday(self) -> None:
        today = date.today()
        year = int(self.currentYear)
        month = today.month
        day = today.day
        today = date(year, month, day)
        weekday = WEEKDAYS[today.weekday()]
        todayColumn = f"{today.strftime('%m/%d')}{weekday}"
        self.tableTime.setCurrentCell(0, self.timeColumns.index(todayColumn))

    def handleComboYearChange(self, year) -> None:
        if year:
            self.currentYear = year
            self.timeColumns = self.central.realTimeDB.getScheduleTimeColumns(self.currentYear)

            if self.taskSource:
                self.setListMemo()
                self.setTableMemo()
                self.setTableTimeAndTotal()
                self.resizeTables()

    def handleButtonExcelClick(self) -> None:
        if self.taskSource and self.timeColumns:
            userNames = {userId: userName for userId, userName, _, _ in self.userSource}
            currentUserName = userNames[self.currentUserId]
            savePath = QFileDialog.getSaveFileName(self, "파일 저장", f"시간관리-{self.currentYear}-{currentUserName}", "*.xlsx")[0]

            if savePath:
                self.central.realTimeDB.toExcelSchedule(savePath, currentUserName, self.currentYear, self.taskSource, self.timeColumns, self.timeSource)

    def handleCheckHideUserClick(self, checked) -> None:
        self.oldUserFlag = checked
        self.setListUser()

    def handleListUserItemClick(self, item) -> None:
        self.currentUserId = item.userId
        self.setComboYear()

    def handleTableMemoHorizontalScrollChange(self, value) -> None:
        self.tableTotal.horizontalScrollBar().setValue(value)
        self.tableTime.horizontalScrollBar().setValue(value)

    def handleTableTaskVerticalScrollChange(self, value) -> None:
        self.tableTime.verticalScrollBar().setValue(value)

    def handleTableTimeVerticalScrollChange(self, value) -> None:
        self.tableTask.verticalScrollBar().setValue(value)

    def handleTableTimeHorizontalScrollChange(self, value) -> None:
        self.tableMemo.horizontalScrollBar().setValue(value)
        self.tableTotal.horizontalScrollBar().setValue(value)

    def handleListMemoItemClick(self, item) -> None:
        userFlag = self.currentUserId == self.central.clientId
        yearFlag = self.currentYear == date.today().strftime("%Y")
        flag = userFlag and yearFlag
        DialogMemo(self, flag, item).exec_()

    def handleTableTimeCellClick(self, row, col) -> None:
        userFlag = self.currentUserId == self.central.clientId
        yearFlag = self.currentYear == date.today().strftime("%Y")
        if userFlag and yearFlag:
            DialogTime(self, row, col).exec_()

    def handleTableMemoCellClick(self, row, col) -> None:
        userFlag = self.currentUserId == self.central.clientId
        yearFlag = self.currentYear == date.today().strftime("%Y")
        flag = userFlag and yearFlag
        item = self.tableMemo.item(row, col)
        DialogMemo(self, flag, item).exec_()

    def keyPressEvent(self, event) -> None:
        userFlag = self.currentUserId == self.central.clientId
        yearFlag = self.currentYear == date.today().strftime("%Y")
        flag = userFlag and yearFlag

        if flag:
            if event.key() in [Qt.Key_Return, Qt.Key_Enter]:
                row = self.tableTime.currentRow()
                col = self.tableTime.currentColumn()
                self.handleTableTimeCellClick(row, col)

            elif event.key() == Qt.Key_Delete:
                row = self.tableTime.currentRow()
                col = self.tableTime.currentColumn()
                if self.tableTime.item(row, col).text():
                    timeDate = self.tableTime.horizontalHeaderItem(col).text()

                    answer = self.central.window.showQuestion(question=f"{timeDate} 시간을 삭제하시겠습니까?", btnYes="삭제", btnNo="취소")

                    if answer:
                        taskValues = self.tableTask.item(row, 2).taskValues
                        taskOptionKey = TASK_OPTIONS[taskValues[3]]
                        timeSource = [timeDate[:5].replace("/", "-"), taskValues[0], taskOptionKey]
                        key = '-'.join(timeSource)
                        self.central.realTimeDB.setTime(self.currentYear, key, 0.0)
                        self.setListUser()
                        self.setTableTimeAndTotal()
                        self.tableTime.setCurrentCell(row, col)