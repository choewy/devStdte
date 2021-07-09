from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import json


JSON_PATH = "temp/client.json"


def getClient():
    with open(JSON_PATH, "r", encoding="utf-8") as file:
        return json.load(file)["userId"]


def setClient(userId):
    with open(JSON_PATH, "w", encoding="utf-8") as file:
        return json.dump({"userId": userId}, file, ensure_ascii=False, indent=4)


class AuthForm(QWidget):
    def __init__(self, central=None):
        QWidget.__init__(self, central)
        self.central = central

        self.inputId = QLineEdit()
        self.inputId.setObjectName("AuthInput")
        self.inputId.setText(getClient())
        self.inputId.setPlaceholderText("아이디")
        self.inputId.textChanged.connect(self.handleInputChange)

        self.labelId = QLabel(self.inputId)
        self.labelId.setObjectName("AuthLabel-icon")
        self.labelId.setPixmap(QPixmap("images/login-id.png").scaledToHeight(17))
        self.labelId.move(7, 13)

        self.inputPwd = QLineEdit()
        self.inputPwd.setObjectName("AuthInput")
        self.inputPwd.setEchoMode(QLineEdit.Password)
        self.inputPwd.setPlaceholderText("비밀번호")
        self.inputPwd.textChanged.connect(self.handleInputChange)

        self.labelPwd = QLabel(self.inputPwd)
        self.labelPwd.setObjectName("AuthLabel-icon")
        self.labelPwd.setPixmap(QPixmap("images/login-pwd.png").scaledToHeight(17))
        self.labelPwd.move(7, 13)

        self.labelError = QLabel()
        self.labelError.setObjectName("AuthLabel-error")
        self.labelError.setText(" ")

        self.buttonLogin = QPushButton()
        self.buttonLogin.setObjectName("AuthButton-login")
        self.buttonLogin.setText("로그인")
        self.buttonLogin.setCursor(Qt.PointingHandCursor)
        self.buttonLogin.clicked.connect(self.handleButtonLoginClick)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(" "), 10)
        layout.addWidget(self.inputId, alignment=Qt.AlignCenter)
        layout.addWidget(self.inputPwd, alignment=Qt.AlignCenter)
        layout.addWidget(self.labelError, alignment=Qt.AlignCenter)
        layout.addWidget(self.buttonLogin, alignment=Qt.AlignCenter)
        layout.addWidget(QLabel(" "), 10)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def handleInputChange(self, t):
        self.labelError.setText(" ")

    def handleButtonLoginClick(self):
        userId = self.inputId.text()
        userPwd = self.inputPwd.text()

        if not userId:
            self.labelError.setText("아이디를 입력하세요.")

        elif not userPwd:
            self.labelError.setText("비밀번호를 입력하세요.")

        else:
            userData = self.central.realtimeDB.getUserPwd(userId)

            if not userData:
                self.labelError.setText("계정이 존재하지 않습니다.\n회원가입은 시간관리 프로그램을 통해서만 가능ㄴ합니다.")

            elif userPwd != userData:
                self.labelError.setText("비밀번호가 일치하지 않습니다.")

            else:
                self.central.clientId = userId
                self.central.clientAuth = self.central.realtimeDB.getUserAuthor(userId)
                self.central.setLayoutMain()
                setClient(userId)
