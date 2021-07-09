from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QComboBox, QDateEdit, QWidget, QPushButton, QCheckBox, QTreeWidget, \
    QHBoxLayout, QLabel, QVBoxLayout, QTreeWidgetItem, QHeaderView

TASK_KEYS = {
    "code": {
        "type": "text",
        "header": "사업코드",
        "widget": QLineEdit,
        "items": None
    },
    "type": {
        "type": "select",
        "header": "사업구분",
        "widget": QComboBox,
        "items": ["일반", "기술", "연구", "국책", "기타"]
    },
    "summary": {
        "type": "text",
        "header": "사업개요",
        "widget": QTextEdit,
        "items": None
    },
    "order": {
        "type": "text",
        "header": "발주처",
        "widget": QLineEdit,
        "items": None
    },
    "start": {
        "type": "date",
        "header": "시작일",
        "widget": QDateEdit,
        "items": None
    },
    "end": {
        "type": "date",
        "header": "종료일",
        "widget": QDateEdit,
        "items": None
    },
    "totalMonth": {
        "type": "text",
        "header": "개월수",
        "widget": QLineEdit,
        "items": None
    },
    "keep": {
        "type": "date",
        "header": "보존기한",
        "widget": QDateEdit,
        "items": None
    },
    "revenue": {
        "type": "text",
        "header": "사업비",
        "widget": QLineEdit,
        "items": None
    },
    "admin": {
        "type": "text",
        "header": "책임자",
        "widget": QLineEdit,
        "items": None
    },
    "whole": {
        "type": "text",
        "header": "PL-총괄",
        "widget": QLineEdit,
        "items": None
    },
    "part": {
        "type": "text",
        "header": "PL-분야",
        "widget": QLineEdit,
        "items": None
    },
    "status": {
        "type": "select",
        "header": "진행상태",
        "widget": QComboBox,
        "items": ["진행", "수주", "준공", "중지", "A/S"]
    }
}


USER_AUTHOR = {
    "일반": False,
    "관리": True,
    "개발자": True
}


class Task(QWidget):
    def __init__(self, central=None):
        QWidget.__init__(self, central)
        self.central = central

        self.userAuthFlag = USER_AUTHOR[self.central.clientAuthor]
        self.tasksSource = None

        self.btnNew = QPushButton()
        self.btnNew.setObjectName("TaskButton-new")
        self.btnNew.setText("신규 사업 등록")
        self.btnNew.setCursor(Qt.PointingHandCursor)

        if not self.userAuthFlag:
            self.btnNew.setVisible(False)

        self.btnNew.clicked.connect(self.handleBtnNewClick)

        self.btnDelete = QPushButton()
        self.btnDelete.setObjectName("TaskButton-delete")
        self.btnDelete.setText("선택 항목 삭제")
        self.btnDelete.setCursor(Qt.PointingHandCursor)

        if not self.userAuthFlag:
            self.btnDelete.setVisible(False)

        self.btnDelete.clicked.connect(self.handleBtnDeleteClick)

        self.checkHideTask = QCheckBox()
        self.checkHideTask.setObjectName("TaskCheck")
        self.checkHideTask.setText("적용 중인 사업만 보기")
        self.checkHideTask.setChecked(True)
        self.checkHideTask.clicked.connect(self.handleCheckHideTaskClick)

        self.treeTask = QTreeWidget()
        self.treeTask.setObjectName("TaskTree")
        self.treeTask.setColumnCount(4)
        self.treeTask.setHeaderLabels(["선택", "", "적용여부", "항목", "값"] if self.userAuthFlag else ["", "", "적용여부", "항목", "값"])

        layoutTop = QHBoxLayout()
        layoutTop.addWidget(self.btnNew)
        layoutTop.addWidget(self.btnDelete)
        layoutTop.addWidget(QLabel(" "), 10)
        layoutTop.addWidget(self.checkHideTask)
        layoutTop.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.addLayout(layoutTop, 0)
        layout.addWidget(self.treeTask, 10)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

        self.setTreeTask()

    def setTreeTask(self):
        tempSource = self.central.realTimeDB.getTaskSource()

        self.tasksSource = {}

        # FILTER
        for uuid, taskSource in tempSource.items():

            if self.checkHideTask.isChecked():
                if taskSource["visible"]:
                    self.tasksSource[uuid] = taskSource

            else:
                self.tasksSource[uuid] = taskSource

        # RENDER
        self.treeTask.clear()

        for uuid, taskSource in self.tasksSource.items():

            itemParent = QTreeWidgetItem(self.treeTask)
            itemParent.uuid = uuid
            itemParent.setText(3, "사업명")

            buttonSave = QPushButton()
            buttonSave.setObjectName("TaskButton-table-save")
            buttonSave.setText("저장")
            buttonSave.setStyleSheet("QPushButton#TaskButton-table-save{min-width: 80px; max-width: 80px;}")
            buttonSave.setEnabled(False)
            buttonSave.setCursor(Qt.PointingHandCursor)
            buttonSave.clicked.connect(self.handleBtnSaveClick)

            buttonSave.uuid = uuid
            buttonSave.updateSource = {}
            buttonSave.oldTaskSource = {}

            for key, value in taskSource.items():
                buttonSave.oldTaskSource[key] = value

            buttonSave.newTaskSource = {}

            for key, value in taskSource.items():
                buttonSave.newTaskSource[key] = value

            if self.userAuthFlag:
                itemParent.setCheckState(0, Qt.Unchecked)

            self.treeTask.setItemWidget(itemParent, 1, buttonSave)

            widgetVisible = QCheckBox()
            widgetVisible.setObjectName("TaskCheck-item")
            widgetVisible.buttonSave = buttonSave
            widgetVisible.key = "visible"
            widgetVisible.setText("적용" if taskSource["visible"] else "제외")
            widgetVisible.setChecked(taskSource["visible"])
            widgetVisible.setEnabled(self.userAuthFlag)
            widgetVisible.clicked.connect(self.handleCheckVisibleChange)

            self.treeTask.setItemWidget(itemParent, 2, widgetVisible)

            widgetName = QLineEdit()
            widgetName.setObjectName("TaskInput-item")
            widgetName.buttonSave = buttonSave
            widgetName.key = "name"
            widgetName.setText(taskSource["name"])
            widgetName.setEnabled(self.userAuthFlag)
            widgetName.textChanged.connect(self.handleDataChange)

            self.treeTask.setItemWidget(itemParent, 4, widgetName)

            del taskSource["name"]

            # CHILD ITEM
            for key in TASK_KEYS.keys():
                item = QTreeWidgetItem(itemParent)
                item.setText(3, TASK_KEYS[key]["header"])
                item.setFlags(Qt.ItemIsSelectable)

                widget = TASK_KEYS[key]["widget"]()
                widget.key = key
                widget.buttonSave = buttonSave
                widget.setEnabled(self.userAuthFlag)

                if TASK_KEYS[key]["type"] == "select":
                    widget.setObjectName("TaskCombo-item")
                    widget.addItems(TASK_KEYS[key]["items"])
                    widget.setCurrentText(taskSource[key])
                    widget.currentTextChanged.connect(self.handleDataChange)
                    widget.wheelEvent = self.handleWheel

                elif TASK_KEYS[key]["type"] == "check":
                    widget.setObjectName("TaskCheck-item")
                    widget.setChecked(taskSource[key])
                    widget.setEnabled(self.userAuthFlag)
                    widget.clicked.connect(self.handleDataChange)

                elif TASK_KEYS[key]["type"] == "date":
                    date = QDate.fromString(taskSource[key], "yyyy-MM-dd")
                    widget.setObjectName("TaskDate-item")
                    widget.setDate(QDate(date.year(), date.month(), date.day()))
                    widget.dateChanged.connect(self.handleDateChange)
                    widget.wheelEvent = self.handleWheel

                    if key == "start":
                        buttonSave.start = widget
                    elif key == "end":
                        buttonSave.end = widget

                else:
                    widget.setObjectName("TaskInput-item")

                    if key == "revenue":
                        widget.setText(format(taskSource[key], ","))
                        widget.textChanged.connect(self.handleRevenueChange)

                    elif key == "totalMonth":
                        buttonSave.totalMonth = widget
                        widget.setText(f"{taskSource[key]}")
                        widget.setEnabled(False)
                        widget.textChanged.connect(self.handleDataChange)

                    elif key == "summary":
                        widget.setText(f"{taskSource[key]}")
                        widget.textChanged.connect(self.handleTextChange)

                    else:
                        widget.setText(f"{taskSource[key]}")
                        widget.textChanged.connect(self.handleDataChange)

                self.treeTask.setItemWidget(item, 4, widget)

        for col in range(len(self.treeTask.header())):
            self.treeTask.resizeColumnToContents(col)

        self.treeTask.setColumnWidth(1, 100)
        self.treeTask.setColumnWidth(2, 80)
        self.treeTask.setColumnWidth(3, 105)

        self.treeTask.header().setSectionResizeMode(QHeaderView.Fixed)

        if not self.userAuthFlag:
            self.treeTask.hideColumn(1)

    def handleCheckHideTaskClick(self):
        self.setTreeTask()

    def handleBtnDeleteClick(self):
        deleteTargets = []

        for row in range(self.treeTask.topLevelItemCount()):
            item = self.treeTask.topLevelItem(row)
            if item.checkState(0):
                deleteTargets.append(item.uuid)

        if deleteTargets:
            answer = self.central.window.showQuestion(
                question=f"{len(deleteTargets)} 개의 사업을 삭제하시겠습니까?",
                btnYes="삭제",
                btnNo="취소"
            )

            if answer:
                for uuid in deleteTargets:
                    self.central.realTimeDB.delTaskSource(uuid)

                self.setTreeTask()

    def handleBtnNewClick(self):
        self.central.realTimeDB.newTask()
        self.setTreeTask()
        row = self.treeTask.topLevelItemCount()-1
        itemParent = self.treeTask.topLevelItem(row)
        self.treeTask.expandItem(itemParent)

    def handleRevenueChange(self, value):
        lineEdit = self.sender()

        value = value.replace(",", "")

        try:
            value = format(int(value), ",")
            lineEdit.setText(value)

        except:
            if value[:-1]:
                value = format(int(value[:-1]), ",")
                lineEdit.setText(value)
            else:
                value = "0"

        try:
            lineEdit.setText(value)
            self.handleDataChange(value)
        except:
            pass

    def handleTextChange(self):
        widget = self.sender()
        buttonSave = widget.buttonSave
        key = widget.key
        value = widget.toPlainText()

        buttonSave.newTaskSource[key] = value

        if buttonSave.newTaskSource[key] != buttonSave.oldTaskSource[key]:
            buttonSave.updateSource[key] = buttonSave.newTaskSource[key]

        else:
            del buttonSave.updateSource[key]

        if buttonSave.updateSource.keys():
            buttonSave.setEnabled(True)

        else:
            buttonSave.setEnabled(False)

    def handleDataChange(self, value):
        widget = self.sender()
        buttonSave = widget.buttonSave
        key = widget.key

        if key == "totalMonth":
            value = int(value)

        elif key == "revenue":
            value = int(value.replace(",", ""))

        buttonSave.newTaskSource[key] = value

        if buttonSave.newTaskSource[key] != buttonSave.oldTaskSource[key]:
            buttonSave.updateSource[key] = buttonSave.newTaskSource[key]

        else:
            del buttonSave.updateSource[key]

        if buttonSave.updateSource.keys():
            buttonSave.setEnabled(True)

        else:
            buttonSave.setEnabled(False)

    def handleCheckVisibleChange(self, checked):
        check = self.sender()
        check.setText("적용" if checked else "제외")
        buttonSave = check.buttonSave
        value = 1 if checked else 0
        key = check.key
        buttonSave.newTaskSource[key] = value

        if buttonSave.newTaskSource[key] != buttonSave.oldTaskSource[key]:
            buttonSave.updateSource[key] = buttonSave.newTaskSource[key]

        else:
            del buttonSave.updateSource[key]

        if buttonSave.updateSource.keys():
            buttonSave.setEnabled(True)

        else:
            buttonSave.setEnabled(False)

    def handleDateChange(self, date):
        dateEdit = self.sender()
        buttonSave = dateEdit.buttonSave
        value = date.toString("yyyy-MM-dd")
        key = dateEdit.key

        if key == "start":
            buttonSave.end.setMinimumDate(date)

        startDate = buttonSave.start.date().toPyDate()
        endDate = buttonSave.end.date().toPyDate()
        delta = endDate - startDate
        buttonSave.totalMonth.setText(f"{round(delta.days // 30, 1)}")
        buttonSave.newTaskSource[key] = value

        if buttonSave.newTaskSource[key] != buttonSave.oldTaskSource[key]:
            buttonSave.updateSource[key] = buttonSave.newTaskSource[key]

        else:
            del buttonSave.updateSource[key]

        if buttonSave.updateSource.keys():
            buttonSave.setEnabled(True)

        else:
            buttonSave.setEnabled(False)

    def handleBtnSaveClick(self):
        buttonSave = self.sender()
        uuid = buttonSave.uuid
        updateSource = buttonSave.updateSource

        if updateSource:
            self.central.realTimeDB.setTaskSource(uuid, updateSource)

            for key, value in buttonSave.updateSource.items():
                buttonSave.oldTaskSource[key] = value

            buttonSave.setEnabled(False)

    def handleExpandItem(self):
        self.treeTask.resizeColumnToContents(0)
        self.treeTask.resizeColumnToContents(1)
        self.treeTask.resizeColumnToContents(2)
        self.treeTask.resizeColumnToContents(3)
        self.treeTask.resizeColumnToContents(4)

    def handleWheel(self, e):
        pass