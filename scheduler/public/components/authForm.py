from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox
import json


LOGO_PATH = "images/logo.png"
JSON_PATH = "temp/client.json"


def getClientId():
    with open(JSON_PATH, "r", encoding="utf-8") as file:
        return json.load(file)["userId"]


def setClientId(userId):
    with open(JSON_PATH, "w", encoding="utf-8") as file:
        json.dump({"userId": userId}, file, ensure_ascii=False, indent=4)


class AuthForm(QWidget):
    def __init__(self, central=None):
        QWidget.__init__(self)
        self.central = central

        self.signupFlag = False

        # Login Form
        self.labelLogo = QLabel()
        self.labelLogo.setObjectName("AuthLogo")
        self.labelLogo.setPixmap(QPixmap(LOGO_PATH).scaledToWidth(400))
        self.labelLogo.setAlignment(Qt.AlignCenter)

        self.inputLoginId = QLineEdit()
        self.inputLoginId.setObjectName("AuthInput-login")
        self.inputLoginId.setPlaceholderText("아이디")
        self.inputLoginId.setText(getClientId())
        self.inputLoginId.textChanged.connect(self.inputLoginTextChange)

        labelIdIcon = QLabel(self.inputLoginId)
        labelIdIcon.setObjectName("AuthIcon")
        labelIdIcon.setPixmap(QPixmap("images/login-id.png").scaledToHeight(17))
        labelIdIcon.move(14, 13)

        self.inputLoginPwd = QLineEdit()
        self.inputLoginPwd.setObjectName("AuthInput-login")
        self.inputLoginPwd.setEchoMode(QLineEdit.Password)
        self.inputLoginPwd.setPlaceholderText("비밀번호")
        self.inputLoginPwd.textChanged.connect(self.inputLoginTextChange)

        labelPwdIcon = QLabel(self.inputLoginPwd)
        labelPwdIcon.setObjectName("AuthIcon")
        labelPwdIcon.setPixmap(QPixmap("images/login-pwd.png").scaledToHeight(17))
        labelPwdIcon.move(14, 13)

        self.labelLoginError = QLabel()
        self.labelLoginError.setObjectName("labelError")
        self.labelLoginError.setText(" ")
        self.labelLoginError.setAlignment(Qt.AlignCenter)

        self.btnLogin = QPushButton()
        self.btnLogin.setObjectName("AuthButton-login")
        self.btnLogin.setText("로그인")
        self.btnLogin.setCursor(Qt.PointingHandCursor)
        self.btnLogin.setShortcut("return")
        self.btnLogin.clicked.connect(self.handlerBtnLoginClick)

        self.labelLoginNew = QLabel("계정이 없으신가요?")
        self.labelLoginNew.setObjectName("AuthLabel-signup")

        self.btnLoginNew = QPushButton()
        self.btnLoginNew.setObjectName("AuthButton-new")
        self.btnLoginNew.setText("회원가입")
        self.btnLoginNew.setCursor(Qt.PointingHandCursor)
        self.btnLoginNew.clicked.connect(self.handlerBtnNewClick)

        layoutLoginNew = QHBoxLayout()
        layoutLoginNew.addWidget(QLabel(" "), 10)
        layoutLoginNew.addWidget(self.labelLoginNew, alignment=Qt.AlignRight)
        layoutLoginNew.addWidget(self.btnLoginNew, alignment=Qt.AlignLeft)
        layoutLoginNew.addWidget(QLabel(" "), 10)
        layoutLoginNew.setContentsMargins(0, 0, 0, 0)

        layoutLogin = QVBoxLayout()
        layoutLogin.addWidget(QLabel(" "), 10)
        layoutLogin.addWidget(self.labelLogo, alignment=Qt.AlignCenter)
        layoutLogin.addWidget(self.inputLoginId, alignment=Qt.AlignCenter)
        layoutLogin.addWidget(self.inputLoginPwd, alignment=Qt.AlignCenter)
        layoutLogin.addWidget(self.labelLoginError, alignment=Qt.AlignCenter)
        layoutLogin.addWidget(self.btnLogin, alignment=Qt.AlignCenter)
        layoutLogin.addLayout(layoutLoginNew)
        layoutLogin.addWidget(QLabel(" "), 10)

        self.authBoxLogin = QGroupBox()
        self.authBoxLogin.setObjectName("AuthBox")
        self.authBoxLogin.setLayout(layoutLogin)

        # Signup Form
        self.inputSignupId = QLineEdit()
        self.inputSignupId.setObjectName("AuthInput-signup-check")
        self.inputSignupId.setPlaceholderText("아이디")
        self.inputSignupId.textChanged.connect(self.inputSignupTextChange)
        self.inputSignupId.textChanged.connect(self.inputSignupIdTextChange)

        self.btnCheckId = QPushButton()
        self.btnCheckId.setObjectName("AuthButton-check")
        self.btnCheckId.setText("중복확인")
        self.btnCheckId.setCursor(Qt.PointingHandCursor)
        self.btnCheckId.clicked.connect(self.handlerBtnCheckClick)

        self.inputSignupInitPwd = QLineEdit()
        self.inputSignupInitPwd.setObjectName("AuthInput-signup")
        self.inputSignupInitPwd.setEchoMode(QLineEdit.Password)
        self.inputSignupInitPwd.setPlaceholderText("비밀번호")
        self.inputSignupInitPwd.textChanged.connect(self.inputSignupTextChange)

        self.inputSignupAgainPwd = QLineEdit()
        self.inputSignupAgainPwd.setObjectName("AuthInput-signup")
        self.inputSignupAgainPwd.setEchoMode(QLineEdit.Password)
        self.inputSignupAgainPwd.setPlaceholderText("비밀번호 다시 입력")
        self.inputSignupAgainPwd.textChanged.connect(self.inputSignupTextChange)

        self.inputSignupName = QLineEdit()
        self.inputSignupName.setObjectName("AuthInput-signup")
        self.inputSignupName.setPlaceholderText("성명")
        self.inputSignupName.textChanged.connect(self.inputSignupTextChange)

        self.labelSignupError = QLabel()
        self.labelSignupError.setObjectName("labelError")
        self.labelSignupError.setText(" ")
        self.labelSignupError.setAlignment(Qt.AlignCenter)

        self.btnSignup = QPushButton()
        self.btnSignup.setObjectName("AuthButton-signup")
        self.btnSignup.setText("회원가입")
        self.btnSignup.setCursor(Qt.PointingHandCursor)
        self.btnSignup.clicked.connect(self.handlerBtnSignupClick)

        self.btnCancel = QPushButton()
        self.btnCancel.setObjectName("AuthButton-cancel")
        self.btnCancel.setText("취소")
        self.btnCancel.setCursor(Qt.PointingHandCursor)
        self.btnCancel.clicked.connect(self.handlerBtnCancelClick)

        layoutSignupId = QHBoxLayout()
        layoutSignupId.addWidget(QLabel(" "), 10)
        layoutSignupId.addWidget(self.inputSignupId, alignment=Qt.AlignRight)
        layoutSignupId.addWidget(self.btnCheckId, alignment=Qt.AlignLeft)
        layoutSignupId.addWidget(QLabel(" "), 10)
        layoutSignupId.setContentsMargins(0, 0, 0, 0)

        layoutSignup = QVBoxLayout()
        layoutSignup.addWidget(QLabel(" "), 10)
        layoutSignup.addLayout(layoutSignupId)
        layoutSignup.addWidget(self.inputSignupInitPwd, alignment=Qt.AlignCenter)
        layoutSignup.addWidget(self.inputSignupAgainPwd, alignment=Qt.AlignCenter)
        layoutSignup.addWidget(self.inputSignupName, alignment=Qt.AlignCenter)
        layoutSignup.addWidget(self.labelSignupError, alignment=Qt.AlignCenter)
        layoutSignup.addWidget(self.btnSignup, alignment=Qt.AlignCenter)
        layoutSignup.addWidget(self.btnCancel, alignment=Qt.AlignCenter)
        layoutSignup.addWidget(QLabel(" "), 10)
        layoutSignup.setContentsMargins(0, 0, 0, 0)

        self.authBoxSignup = QGroupBox()
        self.authBoxSignup.setObjectName("AuthBox")
        self.authBoxSignup.setLayout(layoutSignup)
        self.authBoxSignup.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.authBoxLogin)
        layout.addWidget(self.authBoxSignup)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def inputLoginTextChange(self):
        self.labelLoginError.setText(" ")

    def inputSignupTextChange(self):
        self.labelSignupError.setText(" ")

    def inputSignupIdTextChange(self):
        self.signupFlag = False

    def handlerBtnLoginClick(self):
        userId = self.inputLoginId.text()
        userPwd = self.inputLoginPwd.text()

        if not userId:
            self.labelLoginError.setText("아이디를 입력하세요.")

        elif not userPwd:
            self.labelLoginError.setText("비밀번호를 입력하세요.")

        else:
            userData = self.central.realTimeDB.getUserPwd(userId)

            if not userData:
                self.labelLoginError.setText("계정이 존재하지 않습니다.")

            elif userPwd != userData:
                self.labelLoginError.setText("비밀번호가 일치하지 않습니다.")

            else:
                self.central.clientId = userId
                self.central.clientAuthor = self.central.realTimeDB.getUserAuthor(userId)
                self.central.setLayoutMain()
                setClientId(userId)

    def handlerBtnNewClick(self):
        self.authBoxLogin.setVisible(False)
        self.authBoxSignup.setVisible(True)

    def handlerBtnCheckClick(self):
        userId = self.inputSignupId.text()

        if not userId:
            self.labelSignupError.setText("아이디를 입력하세요.")
            self.signupFlag = False

        elif self.central.realTimeDB.getUserPwd(userId):
            self.labelSignupError.setText("이미 존재하는 계정입니다.")
            self.signupFlag = False

        else:
            self.central.window.showMessage("사용 가능한 아이디입니다.")
            self.signupFlag = True

    def handlerBtnSignupClick(self):
        if self.signupFlag:

            userId = self.inputSignupId.text()
            userPwdInit = self.inputSignupInitPwd.text()
            userPwdAgain = self.inputSignupAgainPwd.text()
            userName = self.inputSignupName.text()

            if not userPwdInit:
                self.labelSignupError.setText("비밀번호를 입력하세요.")

            elif not userPwdAgain:
                self.labelSignupError.setText("비밀번호 확인을 위해 한번 더 입력하세요.")

            elif userPwdInit != userPwdAgain:
                self.labelSignupError.setText("비밀번호가 일치하지 않습니다.")

            elif not userName:
                self.labelSignupError.setText("성명을 입력하세요.")

            else:
                self.central.realTimeDB.newUser(userId, userName, userPwdInit)
                self.central.window.showMessage("회원가입이 완료되었습니다.")
                self.handlerBtnCancelClick()

        else:
            self.labelSignupError.setText("아이디 중복 확인이 필요합니다.")

    def handlerBtnCancelClick(self):
        self.authBoxSignup.setVisible(False)
        self.authBoxLogin.setVisible(True)
