from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QComboBox, QCheckBox, QPushButton, QTreeWidget, QTreeWidgetItem, QLineEdit, \
    QHBoxLayout, QVBoxLayout, QLabel, QHeaderView

USER_KEYS = {
    "position": {
        "type": "select",
        "header": "직위",
        "widget": QComboBox,
        "items": ["이사", "부장", "차장", "과장", "대리", "사원", "인턴"]
    },
    "birth": {
        "type": "text",
        "header": "생년월일",
        "widget": QLineEdit,
        "items": "ex) 950302-1"
    },
    "phone": {
        "type": "text",
        "header": "연락처",
        "widget": QLineEdit,
        "items": "ex) 010-1234-5678"
    },
    "science": {
        "type": "text",
        "header": "과학기술인번호",
        "widget": QLineEdit,
        "items": ""
    },
    "degree": {
        "type": "select",
        "header": "최종학력",
        "widget": QComboBox,
        "items": ["박사", "석사", "학사", "전문학사", "고졸", "기타"]
    },
    "school": {
        "type": "text",
        "header": "출신학교",
        "widget": QLineEdit,
        "items": ""
    },
    "major": {
        "type": "text",
        "header": "전공",
        "widget": QLineEdit,
        "items": ""
    },
    "carType": {
        "type": "text",
        "header": "차종",
        "widget": QLineEdit,
        "items": ""
    },
    "carNumber": {
        "type": "text",
        "header": "차량번호",
        "widget": QLineEdit,
        "items": ""
    },
    "author": {
        "type": "select",
        "header": "접근권한",
        "widget": QComboBox,
        "items": ["관리", "일반"]
    },
    "status": {
        "type": "select",
        "header": "재직상태",
        "widget": QComboBox,
        "items": ["재직", "휴직", "퇴직"]
    }
}

USER_AUTHOR = {
    "일반": False,
    "관리": True,
    "개발자": True
}


class User(QWidget):
    def __init__(self, central=None):
        QWidget.__init__(self)
        self.central = central

        self.userAuthFlag = USER_AUTHOR[self.central.clientAuthor]
        self.usersSource = None

        self.btnDelete = QPushButton()
        self.btnDelete.setObjectName("UserButton-delete")
        self.btnDelete.setText("선택 항목 삭제")
        self.btnDelete.setCursor(Qt.PointingHandCursor)

        if not self.userAuthFlag:
            self.btnDelete.setVisible(False)

        self.btnDelete.clicked.connect(self.handleBtnDeleteClick)

        self.checkHideUser = QCheckBox()
        self.checkHideUser.setObjectName("UserCheck")
        self.checkHideUser.setText("재직자만 보기")
        self.checkHideUser.setChecked(True)
        self.checkHideUser.clicked.connect(self.handleCheckHideUserClick)

        self.treeUser = QTreeWidget()
        self.treeUser.setObjectName("UserTree")
        self.treeUser.setColumnCount(4)
        self.treeUser.setHeaderLabels(["아이디", "", "항목", "값"])

        layoutTop = QHBoxLayout()
        layoutTop.addWidget(self.btnDelete)
        layoutTop.addWidget(QLabel(" "), 10)
        layoutTop.addWidget(self.checkHideUser)
        layoutTop.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.addLayout(layoutTop, 0)
        layout.addWidget(self.treeUser, 10)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

        self.setTreeUser()

    def setTreeUser(self):
        tempSource = self.central.realTimeDB.getUserSource()

        self.usersSource = {}

        # FILTER
        for userId, userSource in tempSource.items():

            if self.checkHideUser.isChecked():
                if userSource["status"] == "재직":
                    self.usersSource[userId] = userSource

            else:
                self.usersSource[userId] = userSource

        # RENDER
        self.treeUser.clear()

        for userId, userSource in self.usersSource.items():

            editFlag = self.userAuthFlag or self.central.clientId == userId

            itemParent = QTreeWidgetItem(self.treeUser)
            itemParent.userId = userId
            itemParent.setText(0, userId)
            itemParent.setText(2, "이름")

            buttonSave = QPushButton()
            buttonSave.setObjectName("UserButton-table-save")
            buttonSave.setText("저장")
            buttonSave.setStyleSheet("QPushButton#UserButton-table-save{min-width: 80px; max-width: 80px;}")
            buttonSave.setEnabled(False)
            buttonSave.setCursor(Qt.PointingHandCursor)
            buttonSave.clicked.connect(self.handleBtnSaveClick)

            buttonSave.userId = userId
            buttonSave.updateSource = {}
            buttonSave.oldUserSource = {}

            for key, value in userSource.items():
                buttonSave.oldUserSource[key] = value

            buttonSave.newUserSource = {}

            for key, value in userSource.items():
                buttonSave.newUserSource[key] = value

            if self.userAuthFlag:
                itemParent.setCheckState(0, Qt.Unchecked)

            self.treeUser.setItemWidget(itemParent, 1, buttonSave)

            widgetName = QLineEdit()
            widgetName.setObjectName("UserInput-item")
            widgetName.buttonSave = buttonSave
            widgetName.key = "name"
            widgetName.setText(userSource["name"])
            widgetName.setEnabled(editFlag)
            widgetName.textChanged.connect(self.handleDataChange)

            self.treeUser.setItemWidget(itemParent, 3, widgetName)

            # CHILD ITEM
            for key in USER_KEYS.keys():
                item = QTreeWidgetItem(itemParent)
                item.setText(2, USER_KEYS[key]["header"])
                item.setFlags(Qt.ItemIsSelectable)

                widget = USER_KEYS[key]["widget"]()
                widget.key = key
                widget.buttonSave = buttonSave
                widget.setEnabled(editFlag)

                if USER_KEYS[key]["type"] == "select":
                    if key == "author":
                        widget.addItems(["개발자"] if userSource[key] == "개발자" else USER_KEYS[key]["items"])
                    else:
                        widget.addItems(USER_KEYS[key]["items"])
                    widget.setObjectName("UserCombo-item")
                    widget.setCurrentText(userSource[key])
                    widget.currentTextChanged.connect(self.handleDataChange)
                    widget.wheelEvent = self.handleWheel

                else:
                    widget.setObjectName("UserInput-item")
                    widget.setText(userSource[key])
                    widget.setPlaceholderText(USER_KEYS[key]["items"])
                    widget.textChanged.connect(self.handleDataChange)

                self.treeUser.setItemWidget(item, 3, widget)

        for col in range(len(self.treeUser.header())):
            self.treeUser.resizeColumnToContents(col)

        self.treeUser.setColumnWidth(1, 100)
        self.treeUser.setColumnWidth(2, 105)

        self.treeUser.header().setSectionResizeMode(QHeaderView.Fixed)

    def accessByProfile(self):
        for row in range(self.treeUser.topLevelItemCount()):
            itemParent = self.treeUser.topLevelItem(row)
            if itemParent.userId == self.central.clientId:
                self.treeUser.expandItem(itemParent)
                self.treeUser.setCurrentItem(itemParent)

    def handleDataChange(self, value):
        widget = self.sender()
        buttonSave = widget.buttonSave
        key = widget.key
        buttonSave.newUserSource[key] = value

        if buttonSave.newUserSource[key] != buttonSave.oldUserSource[key]:
            buttonSave.updateSource[key] = buttonSave.newUserSource[key]

        else:
            del buttonSave.updateSource[key]

        if buttonSave.updateSource.keys():
            buttonSave.setEnabled(True)

        else:
            buttonSave.setEnabled(False)

    def handleBtnSaveClick(self):
        buttonSave = self.sender()
        userId = buttonSave.userId
        updateSource = buttonSave.updateSource

        if updateSource.keys():
            self.central.realTimeDB.setUserSource(userId, updateSource)

            for key, value in buttonSave.updateSource.items():
                buttonSave.oldUserSource[key] = value

            buttonSave.setEnabled(False)

    def handleCheckHideUserClick(self):
        self.setTreeUser()
    
    def handleBtnDeleteClick(self):
        deleteTargets = []

        for row in range(self.treeUser.topLevelItemCount()):
            item = self.treeUser.topLevelItem(row)
            if item.checkState(0):
                deleteTargets.append(item.text(0))

        if deleteTargets:
            answer = self.central.window.showQuestion(
                question=f"{len(deleteTargets)} 명의 계정을 삭제하시겠습니까?",
                btnYes="삭제",
                btnNo="취소"
            )

            if answer:
                for userId in deleteTargets:
                    self.central.realTimeDB.delUserSource(userId)

                self.setTreeUser()

    def handleWheel(self, e):
        pass