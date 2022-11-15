from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtWidgets import QMainWindow, QMenuBar, QStatusBar, QCheckBox
from PyQt5.QtCore import QCoreApplication, QRect, QMetaObject, Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtMultimedia import QSound

from random import randint
import sys
import time
import datetime
import webbrowser
from sqlite3 import *


db = connect('database.db')
cur = db.cursor()


class My(QMainWindow):
    def __init__(self):
        super().__init__()
        My.setObjectName(self, 'FastMath')
        self.setFixedSize(700, 800)

        # --------------------------------------------------------------------------------------------------------------

        self.styleBubbles = '''background-color: rgb(134,232,239); border-style: outset; border-width: 2px; family: arial;
                border-radius: 10px; border-color: black; font: bold 26px; min-width: 3em; padding: 6px;'''
        self.styleDrop = '''background-color: rgb(90,200,45); border-style: outset; border-width: 2px; family: arial;
                border-radius: 10px; border-color: black; font: bold 26px; min-width: 3em; padding: 6px;'''
        self.styleFon1 = '''background-color: rgb(25,225,145); border-style: outset; border-width: 2px; family: arial;
                border-radius: 10px; border-color: black; font: bold 26px; min-width: 3em; padding: 6px;'''
        self.styleFon2 = '''background-color: rgb(40,130,230); border-style: outset; border-width: 2px; family: arial;
                border-radius: 10px; border-color: black; font: bold 26px; min-width: 3em; padding: 6px;'''
        self.styleFon3 = '''background-color: rgb(150,30,120); border-style: outset; border-width: 2px; family: arial;
                border-radius: 10px; border-color: black; font: bold 26px; min-width: 3em; padding: 6px;'''
        self.styleFon4 = '''background-color: rgb(135,165,240); border-style: outset; border-width: 2px; family: arial;
                border-radius: 10px; border-color: black; font: bold 26px; min-width: 3em; padding: 6px;'''

        self.styleLabel = '''background-color: rgb(255,255,255); border-style: outset; border-width: 2px;
                border-radius: 10px; border-color: black; font: bold 20px; min-width: 3em; padding: 6px;'''
        self.styleImages = '''border-style: outset; border-width: 2px;
                border-radius: 10px; border-color: black; font: bold 0px; min-width: 3em; padding: 6px;'''

        # --------------------------------------------------------------------------------------------------------------

        self.sound = QSound('sounds\\sound.wav')
        self.music = QSound('sounds\\music.wav')

        self.picture = 'background\\fon3.jpg'
        file = open('files\\config.txt', 'r')
        cfg = file.readlines()
        print(cfg)
        self.picture = f'background\\{cfg[0][:-1]}'
        self.styleNow = eval(f'{cfg[1][:-1]}')

        # --------------------------------------------------------------------------------------------------------------

        self.second = 0
        self.timer_ = QTimer()
        self.timer_.timeout.connect(self.again)

        self.count, self.success, self.error, self.timer, self.startGame, self.pInfo = 0, 0, 0, 0, False, []
        self.timePlaying = 30

        self.pInfo = []

        # --------------------------------------------------------------------------------------------------------------

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.background = QLabel(self.centralwidget)
        self.background.setGeometry(QRect(0, 0, 700, 800))

        self.my_font = QFont()
        self.my_font.setFamily('Trebuchet MS')
        self.my_font.setPointSize(22)

        self.background.setFont(self.my_font)
        self.background.setText('')
        self.background.setPixmap(QPixmap(self.picture))
        self.background.setObjectName("background")

        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 700, 26))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        # --------------------------------------------------------------------------------------------------------------

        self.buttonReg = QPushButton(self.centralwidget)
        self.buttonReg.setGeometry(QRect(200, 300, 300, 100))
        self.buttonReg.setFont(self.my_font)
        self.buttonReg.setStyleSheet(self.styleNow)
        self.buttonReg.setObjectName("buttonReg")
        self.buttonReg.clicked.connect(self.reg_account)

        self.buttonLog = QPushButton(self.centralwidget)
        self.buttonLog.setGeometry(QRect(200, 450, 300, 100))
        self.buttonLog.setFont(self.my_font)
        self.buttonLog.setStyleSheet(self.styleNow)
        self.buttonLog.setObjectName("buttonLog")
        self.buttonLog.clicked.connect(self.log_account)

        # --------------------------------------------------------------------------------------------------------------

        self.title = QLabel(self.centralwidget)
        self.title.setEnabled(True)
        self.title.setGeometry(QRect(180, 50, 350, 150))
        self.my_font.setPointSize(52)
        self.my_font.setWeight(50)
        self.title.setFont(self.my_font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setObjectName("title")

        # --------------------------------------------------------------------------------------------------------------

        self.my_font.setPointSize(16)
        self.regLabel1 = QLabel(self)
        self.regLabel1.resize(100, 30), self.regLabel1.move(150, 370), self.regLabel1.setText('Логин:')
        self.regLabel1.setFont(self.my_font), self.regLabel1.hide()
        self.regLabel2 = QLabel(self)
        self.regLabel2.resize(100, 30), self.regLabel2.move(150, 480), self.regLabel2.setText('Пароль:')
        self.regLabel2.setFont(self.my_font), self.regLabel2.hide()
        self.regLabel3 = QLabel(self)
        self.my_font.setPointSize(24)
        self.regLabel3.resize(250, 60), self.regLabel3.move(230, 250), self.regLabel3.setText('Регистрация')
        self.regLabel3.setFont(self.my_font), self.regLabel3.hide()

        self.regLogin = QLineEdit(self)
        self.regPassword = QLineEdit(self)
        self.le_font = self.regLogin.font()
        self.le_font.setPointSize(14)
        self.regLogin.resize(400, 50), self.regLogin.move(150, 400), self.regLogin.setFont(self.le_font)
        self.regLogin.setStyleSheet(self.styleLabel), self.regLogin.hide()
        self.regPassword.resize(400, 50), self.regPassword.move(150, 510), self.regPassword.setFont(self.le_font)
        self.regPassword.setStyleSheet(self.styleLabel), self.regPassword.hide()

        self.regButton = QPushButton(self.centralwidget)
        self.regButton.resize(300, 75), self.regButton.move(200, 650), self.regButton.setText('Далее')
        self.regButton.setFont(self.my_font), self.regButton.clicked.connect(self.register)
        self.regButton.setStyleSheet(self.styleNow), self.regButton.hide()

        self.regCheckBox = QCheckBox(self)
        self.regCheckBox.setStyleSheet('QCheckBox::indicator {width: 25px; height: 25px;}')
        self.regCheckBox.move(150, 580), self.regCheckBox.hide()

        self.my_font.setPointSize(10)
        self.regButton2 = QPushButton(self)
        self.regButton2.resize(350, 25), self.regButton2.move(185, 584), self.regButton2.setFont(self.my_font)
        self.regButton2.setText('Принять политику конфиденциальности'), self.regButton2.clicked.connect(self.browser2)
        self.regButton2.setStyleSheet('background-color: rgba(255,255,255,0);'), self.regButton2.hide()

        # --------------------------------------------------------------------------------------------------------------

        self.my_font.setPointSize(16)
        self.logLabel1 = QLabel(self)
        self.logLabel1.resize(100, 30), self.logLabel1.move(150, 370), self.logLabel1.setText('Логин:')
        self.logLabel1.setFont(self.my_font), self.logLabel1.hide()
        self.logLabel2 = QLabel(self)
        self.logLabel2.resize(100, 30), self.logLabel2.move(150, 480), self.logLabel2.setText('Пароль:')
        self.logLabel2.setFont(self.my_font), self.logLabel2.hide()
        self.logLabel3 = QLabel(self)
        self.my_font.setPointSize(24)
        self.logLabel3.resize(250, 60), self.logLabel3.move(230, 250), self.logLabel3.setText('Авторизация')
        self.logLabel3.setFont(self.my_font), self.logLabel3.hide()

        self.logLogin = QLineEdit(self)
        self.logPassword = QLineEdit(self)
        self.le_font = self.logLogin.font()
        self.le_font.setPointSize(14)
        self.logLogin.resize(400, 50), self.logLogin.move(150, 400), self.logLogin.setFont(self.le_font)
        self.logLogin.setStyleSheet(self.styleLabel), self.logLogin.hide()
        self.logPassword.resize(400, 50), self.logPassword.move(150, 510), self.logPassword.setFont(self.le_font)
        self.logPassword.setStyleSheet(self.styleLabel), self.logPassword.hide()

        self.logButton = QPushButton(self.centralwidget)
        self.logButton.resize(300, 75), self.logButton.move(200, 650), self.logButton.setText('Войти')
        self.logButton.setFont(self.my_font), self.logButton.clicked.connect(self.authorize)
        self.logButton.setStyleSheet(self.styleNow), self.logButton.hide()

        # --------------------------------------------------------------------------------------------------------------

        self.my_font.setPointSize(8)
        self.ButtonToAuth = QPushButton(self)
        self.ButtonToAuth.resize(50, 50), self.ButtonToAuth.move(30, 30), self.ButtonToAuth.setText('<<<')
        self.ButtonToAuth.setFont(self.my_font), self.ButtonToAuth.clicked.connect(self.initUI)
        self.ButtonToAuth.setStyleSheet(self.styleNow), self.ButtonToAuth.hide()

        self.ButtonToMenu = QPushButton(self)
        self.ButtonToMenu.resize(50, 50), self.ButtonToMenu.move(30, 30), self.ButtonToMenu.setText('<<<')
        self.ButtonToMenu.setFont(self.my_font), self.ButtonToMenu.clicked.connect(self.menu)
        self.ButtonToMenu.setStyleSheet(self.styleNow), self.ButtonToMenu.hide()

        # --------------------------------------------------------------------------------------------------------------

        self.my_font.setPointSize(26)
        self.profLabel1 = QLabel(self)
        self.profLabel1.resize(700, 100), self.profLabel1.move(0, 100), self.profLabel1.setText('Профиль')
        self.profLabel1.setFont(self.my_font), self.profLabel1.setAlignment(Qt.AlignCenter), self.profLabel1.hide()

        self.my_font.setPointSize(16)
        self.profLabel2 = QLabel(self)
        self.profLabel2.resize(700, 100), self.profLabel2.move(0, 200), self.profLabel2.setText('Профиль')
        self.profLabel2.setFont(self.my_font), self.profLabel2.setAlignment(Qt.AlignLeft), self.profLabel2.hide()

        self.profLabel3 = QLabel(self)
        self.profLabel3.resize(700, 100), self.profLabel3.move(0, 250), self.profLabel3.setText('Профиль')
        self.profLabel3.setFont(self.my_font), self.profLabel3.setAlignment(Qt.AlignLeft), self.profLabel3.hide()

        self.profLabel4 = QLabel(self)
        self.profLabel4.resize(700, 100), self.profLabel4.move(0, 300), self.profLabel4.setText('Профиль')
        self.profLabel4.setFont(self.my_font), self.profLabel4.setAlignment(Qt.AlignLeft), self.profLabel4.hide()

        self.profLabel5 = QLabel(self)
        self.profLabel5.resize(700, 100), self.profLabel5.move(0, 350), self.profLabel5.setText('Профиль')
        self.profLabel5.setFont(self.my_font), self.profLabel5.setAlignment(Qt.AlignLeft), self.profLabel5.hide()

        self.profLabel6 = QLabel(self)
        self.profLabel6.resize(700, 100), self.profLabel6.move(0, 400), self.profLabel6.setText('Профиль')
        self.profLabel6.setFont(self.my_font), self.profLabel6.setAlignment(Qt.AlignLeft), self.profLabel6.hide()

        self.profLabel7 = QLabel(self)
        self.profLabel7.resize(700, 100), self.profLabel7.move(0, 450), self.profLabel7.setText('Профиль')
        self.profLabel7.setFont(self.my_font), self.profLabel7.setAlignment(Qt.AlignLeft), self.profLabel7.hide()

        self.profLabel8 = QLabel(self)
        self.profLabel8.resize(700, 100), self.profLabel8.move(0, 500), self.profLabel8.setText('Профиль')
        self.profLabel8.setFont(self.my_font), self.profLabel8.setAlignment(Qt.AlignLeft), self.profLabel8.hide()

        self.profLabel9 = QLabel(self)
        self.profLabel9.resize(700, 100), self.profLabel9.move(0, 550), self.profLabel9.setText('Профиль')
        self.profLabel9.setFont(self.my_font), self.profLabel9.setAlignment(Qt.AlignLeft), self.profLabel9.hide()

        # --------------------------------------------------------------------------------------------------------------

        self.settHelp = QPushButton(self)
        self.settHelp.resize(150, 75), self.settHelp.move(62, 230), self.settHelp.clicked.connect(self.browser1)
        self.settHelp.setStyleSheet(self.styleNow), self.setFont(self.my_font)
        self.settHelp.setText('Помощь'), self.settHelp.hide()

        self.settMusic = QCheckBox(self)
        self.settMusic.resize(150, 75), self.settMusic.move(275, 230), self.settMusic.clicked.connect(self.changeMusic)
        self.setFont(self.my_font), self.settMusic.setStyleSheet(self.styleNow)
        self.settMusic.setText(' Музыка'), self.settMusic.hide()

        self.settSound = QCheckBox(self)
        self.settSound.resize(150, 75), self.settSound.move(487, 230), self.settSound.clicked.connect(self.changeMusic)
        self.settSound.setStyleSheet(self.styleNow), self.setFont(self.my_font)
        self.settSound.setText('   Звук'), self.settSound.hide()

        self.settSetFon1 = QPushButton(self)
        self.settSetFon1.resize(100, 100), self.settSetFon1.move(100, 400), self.settSetFon1.clicked.connect(
            self.changeFon)
        self.settSetFon1.setText('1'), self.settSetFon1.setStyleSheet(self.styleImages)
        self.settSetFon1.setIcon(QIcon('background\\bubbles.jpg')), self.settSetFon1.setIconSize(
            QSize(200, 200)), self.settSetFon1.hide()

        self.settSetFon2 = QPushButton(self)
        self.settSetFon2.resize(100, 100), self.settSetFon2.move(300, 400), self.settSetFon2.clicked.connect(
            self.changeFon)
        self.settSetFon2.setText('2'), self.settSetFon2.setStyleSheet(self.styleImages)
        self.settSetFon2.setIcon(QIcon('background\\drop.jpg')), self.settSetFon2.setIconSize(
            QSize(200, 200)), self.settSetFon2.hide()

        self.settSetFon3 = QPushButton(self)
        self.settSetFon3.resize(100, 100), self.settSetFon3.move(500, 400), self.settSetFon3.clicked.connect(
            self.changeFon)
        self.settSetFon3.setText('3'), self.settSetFon3.setStyleSheet(self.styleImages)
        self.settSetFon3.setIcon(QIcon('background\\fon1.jpg')), self.settSetFon3.setIconSize(
            QSize(200, 200)), self.settSetFon3.hide()

        self.settSetFon4 = QPushButton(self)
        self.settSetFon4.resize(100, 100), self.settSetFon4.move(100, 600), self.settSetFon4.clicked.connect(
            self.changeFon)
        self.settSetFon4.setText('4'), self.settSetFon4.setStyleSheet(self.styleImages)
        self.settSetFon4.setIcon(QIcon('background\\fon2.jpg')), self.settSetFon4.setIconSize(
            QSize(200, 200)), self.settSetFon4.hide()

        self.settSetFon5 = QPushButton(self)
        self.settSetFon5.resize(100, 100), self.settSetFon5.move(300, 600), self.settSetFon5.clicked.connect(
            self.changeFon)
        self.settSetFon5.setText('5'), self.settSetFon5.setStyleSheet(self.styleImages)
        self.settSetFon5.setIcon(QIcon('background\\fon3.jpg')), self.settSetFon5.setIconSize(
            QSize(200, 200)), self.settSetFon5.hide()

        self.settSetFon6 = QPushButton(self)
        self.settSetFon6.resize(100, 100), self.settSetFon6.move(500, 600), self.settSetFon6.clicked.connect(
            self.changeFon)
        self.settSetFon6.setText('6'), self.settSetFon6.setStyleSheet(self.styleImages)
        self.settSetFon6.setIcon(QIcon('background\\fon4.jpg')), self.settSetFon6.setIconSize(
            QSize(200, 200)), self.settSetFon6.hide()

        # --------------------------------------------------------------------------------------------------------------

        self.my_font.setPointSize(22)
        self.endLabel1 = QLabel(self)
        self.endLabel1.resize(700, 100), self.endLabel1.move(0, 100), self.endLabel1.setText('')
        self.endLabel1.setFont(self.my_font), self.endLabel1.setAlignment(Qt.AlignCenter), self.endLabel1.hide()

        self.endLabel2 = QLabel(self)
        self.endLabel2.resize(700, 100), self.endLabel2.move(0, 200), self.endLabel2.setText('')
        self.endLabel2.setFont(self.my_font), self.endLabel2.setAlignment(Qt.AlignCenter), self.endLabel2.hide()

        self.my_font.setPointSize(16)
        self.endLabel3 = QLabel(self)
        self.endLabel3.resize(700, 75), self.endLabel3.move(0, 300), self.endLabel3.setText('')
        self.endLabel3.setFont(self.my_font), self.endLabel3.setAlignment(Qt.AlignCenter), self.endLabel3.hide()

        self.endLabel4 = QLabel(self)
        self.endLabel4.resize(700, 75), self.endLabel4.move(0, 375), self.endLabel4.setText('')
        self.endLabel4.setFont(self.my_font), self.endLabel4.setAlignment(Qt.AlignCenter), self.endLabel4.hide()

        self.endLabel5 = QLabel(self)
        self.endLabel5.resize(700, 75), self.endLabel5.move(0, 450), self.endLabel5.setText('')
        self.endLabel5.setFont(self.my_font), self.endLabel5.setAlignment(Qt.AlignCenter), self.endLabel5.hide()

        self.endLabel6 = QLabel(self)
        self.endLabel6.resize(700, 75), self.endLabel6.move(0, 525), self.endLabel6.setText('')
        self.endLabel6.setFont(self.my_font), self.endLabel6.setAlignment(Qt.AlignCenter), self.endLabel6.hide()

        # --------------------------------------------------------------------------------------------------------------

        self.my_font.setPointSize(40)
        self.gameExample = QLabel(self)
        self.gameExample.resize(700, 100), self.gameExample.move(0, 200), self.gameExample.setText('')
        self.gameExample.setFont(self.my_font), self.gameExample.setAlignment(Qt.AlignCenter), self.gameExample.hide()

        self.my_font.setPointSize(8)
        self.gameCounter = QLabel(self)
        self.gameCounter.resize(700, 50), self.gameCounter.move(0, 320), self.gameCounter.setText('')
        self.gameCounter.setFont(self.my_font), self.gameCounter.setAlignment(Qt.AlignCenter), self.gameCounter.hide()

        self.my_font.setPointSize(30)
        self.gameAnswer1 = QPushButton(self)
        self.gameAnswer1.resize(250, 75), self.gameAnswer1.move(60, 400), self.gameAnswer1.setText('')
        self.gameAnswer1.setFont(self.my_font), self.gameAnswer1.clicked.connect(self.check_answer)
        self.gameAnswer1.setStyleSheet(self.styleNow), self.gameAnswer1.hide()

        self.gameAnswer2 = QPushButton(self)
        self.gameAnswer2.resize(250, 75), self.gameAnswer2.move(370, 400), self.gameAnswer2.setText('')
        self.gameAnswer2.setFont(self.my_font), self.gameAnswer2.clicked.connect(self.check_answer)
        self.gameAnswer2.setStyleSheet(self.styleNow), self.gameAnswer2.hide()

        self.gameAnswer3 = QPushButton(self)
        self.gameAnswer3.resize(250, 75), self.gameAnswer3.move(60, 500), self.gameAnswer3.setText('')
        self.gameAnswer3.setFont(self.my_font), self.gameAnswer3.clicked.connect(self.check_answer)
        self.gameAnswer3.setStyleSheet(self.styleNow), self.gameAnswer3.hide()

        self.gameAnswer4 = QPushButton(self)
        self.gameAnswer4.resize(250, 75), self.gameAnswer4.move(370, 500), self.gameAnswer4.setText('')
        self.gameAnswer4.setFont(self.my_font), self.gameAnswer4.clicked.connect(self.check_answer)
        self.gameAnswer4.setStyleSheet(self.styleNow), self.gameAnswer4.hide()

        self.my_font.setPointSize(8)
        self.gameRestart = QPushButton(self)
        self.gameRestart.resize(300, 75), self.gameRestart.move(200, 650), self.gameRestart.setText('Начать заново')
        self.gameRestart.setFont(self.my_font), self.gameRestart.clicked.connect(self.game)
        self.gameRestart.setStyleSheet(self.styleNow), self.gameRestart.hide()

        self.gameTimer = QLabel(self)
        self.gameTimer.resize(700, 100), self.gameTimer.move(0, 100), self.gameTimer.setText('Осталось секунд: 30')
        self.gameTimer.setFont(self.my_font), self.gameTimer.setAlignment(Qt.AlignCenter), self.gameTimer.hide()

        # --------------------------------------------------------------------------------------------------------------

        self.my_font.setPointSize(12)
        self.Error = QLabel(self)
        self.Error.resize(700, 100), self.Error.move(0, 570), self.Error.setFont(self.my_font)
        self.Error.setText(''), self.Error.setAlignment(Qt.AlignCenter), self.Error.hide()

        # --------------------------------------------------------------------------------------------------------------

        self.my_font.setPointSize(22)
        self.menuLabel1 = QLabel(self)
        self.menuLabel1.resize(200, 100), self.menuLabel1.move(250, 100), self.menuLabel1.setText('Главное меню')
        self.menuLabel1.setFont(self.my_font), self.menuLabel1.hide()

        self.my_font.setPointSize(18)
        self.menuButton1 = QPushButton(self)
        self.menuButton1.resize(350, 75), self.menuButton1.move(175, 300), self.menuButton1.setText('Играть')
        self.menuButton1.setFont(self.my_font), self.menuButton1.setStyleSheet(self.styleNow)
        self.menuButton1.clicked.connect(self.game), self.menuButton1.hide()

        self.menuButton2 = QPushButton(self)
        self.menuButton2.resize(350, 75), self.menuButton2.move(175, 400), self.menuButton2.setText('Профиль')
        self.menuButton2.setFont(self.my_font), self.menuButton2.setStyleSheet(self.styleNow)
        self.menuButton2.clicked.connect(self.profile), self.menuButton2.hide()

        self.menuButton3 = QPushButton(self)
        self.menuButton3.resize(350, 75), self.menuButton3.move(175, 500), self.menuButton3.setText('Настройки')
        self.menuButton3.setFont(self.my_font), self.menuButton3.clicked.connect(self.settings)
        self.menuButton3.setStyleSheet(self.styleNow), self.menuButton3.hide()

        self.menuButton4 = QPushButton(self)
        self.menuButton4.resize(350, 75), self.menuButton4.move(175, 600), self.menuButton4.setText('Выход')
        self.menuButton4.setFont(self.my_font), self.menuButton4.clicked.connect(self.initUI)
        self.menuButton4.setStyleSheet(self.styleNow), self.menuButton4.hide()

        # --------------------------------------------------------------------------------------------------------------

        self.my_font.setPointSize(12)
        self.authLabel1 = QLabel(self)
        self.authLabel1.resize(200, 50), self.authLabel1.move(0, 710), self.authLabel1.setText('FastMath © 2021')
        self.authLabel1.setAlignment(Qt.AlignCenter), self.authLabel1.setFont(self.my_font), self.authLabel1.show()

        self.authLabel2 = QLabel(self)
        self.authLabel2.resize(200, 50), self.authLabel2.move(220, 710), self.authLabel2.setText('Все права защищены.')
        self.authLabel2.setAlignment(Qt.AlignCenter), self.authLabel2.setFont(self.my_font), self.authLabel2.show()

        self.authLabel3 = QLabel(self)
        self.authLabel3.resize(250, 50), self.authLabel3.move(450, 710), self.authLabel3.setText(
            'leaderbomjganga@mail.ru')
        self.authLabel3.setAlignment(Qt.AlignCenter), self.authLabel3.setFont(self.my_font), self.authLabel3.show()

        # --------------------------------------------------------------------------------------------------------------

        if f'{cfg[2][:-1]}' == 'musicON':
            self.music.play(), self.music.setLoops(100), self.settMusic.toggle()
        if f'{cfg[3][:-1]}' == 'soundON':
            self.settSound.toggle()
        file.close()

        # --------------------------------------------------------------------------------------------------------------

        self.initUI()

        self.retranslateUI(self)
        QMetaObject.connectSlotsByName(self)

    def initUI(self):
        self.menuLabel1.hide(), self.menuButton1.hide(), self.menuButton2.hide(), self.menuButton3.hide(), self.menuButton4.hide()
        self.buttonReg.show(), self.buttonLog.show(), self.ButtonToAuth.hide(), self.authLabel1.show(), self.authLabel2.show(), self.authLabel3.show()
        self.regLabel1.hide(), self.regLabel2.hide(), self.regLabel3.hide(), self.regLogin.hide(), self.regPassword.hide()
        self.regButton.hide(), self.regButton2.hide(), self.regCheckBox.hide()

        self.logLabel1.hide(), self.logLabel2.hide(), self.logLabel3.hide(), self.logLogin.hide(), self.logPassword.hide()
        self.logButton.hide()

    def menu(self):
        if self.settSound.isChecked():
            self.sound.play()
        if self.timer_.isActive():
            self.timer_.stop()
            self.second = 0
        self.count, self.timer, self.success, self.error, self.startGame = 0, 0, 0, 0, False

        self.title.show(), self.ButtonToMenu.hide(), self.ButtonToAuth.hide(), self.Error.hide(), self.settHelp.hide()
        self.gameAnswer1.hide(), self.gameAnswer2.hide(), self.gameAnswer3.hide(), self.gameAnswer4.hide()
        self.gameCounter.hide(), self.gameTimer.hide(), self.gameRestart.hide(), self.gameExample.hide()
        self.endLabel1.hide(), self.endLabel2.hide(), self.endLabel3.hide()
        self.endLabel4.hide(), self.endLabel5.hide(), self.endLabel6.hide()
        self.settMusic.hide(), self.settSound.hide()
        self.settSetFon1.hide(), self.settSetFon2.hide(), self.settSetFon3.hide()
        self.settSetFon4.hide(), self.settSetFon5.hide(), self.settSetFon6.hide()
        self.profLabel1.hide(), self.profLabel2.hide(), self.profLabel3.hide(), self.profLabel4.hide()
        self.profLabel5.hide(), self.profLabel6.hide(), self.profLabel7.hide(), self.profLabel8.hide()
        self.profLabel9.hide()

        self.menuButton1.setStyleSheet(self.styleNow), self.menuButton2.setStyleSheet(self.styleNow)
        self.menuButton3.setStyleSheet(self.styleNow), self.menuButton4.setStyleSheet(self.styleNow)
        self.menuLabel1.hide(), self.menuButton1.show(), self.menuButton2.show(), self.menuButton3.show(), self.menuButton4.show()

    def game(self):
        if self.settSound.isChecked():
            self.sound.play()
        if self.startGame is False or self.sender().text() == '':
            self.startGame = True
            self.second = 0
            self.timer = time.time()
            self.timer_.start(1000)

        self.ButtonToMenu.setStyleSheet(self.styleNow)
        self.menuLabel1.hide(), self.menuButton1.hide(), self.menuButton2.hide(), self.menuButton3.hide(), self.menuButton4.hide()
        self.title.hide(), self.gameRestart.hide(), self.ButtonToMenu.show()
        self.endLabel1.hide(), self.endLabel2.hide(), self.endLabel3.hide()
        self.endLabel4.hide(), self.endLabel5.hide(), self.endLabel6.hide()

        self.answers = list(self.generator())
        indexes = []

        while len(indexes) < 4:
            r = randint(1, 4)
            if r not in indexes:
                indexes.append(r)

        self.my_font.setPointSize(20)
        self.gameTimer.setFont(self.my_font), self.gameTimer.show()
        self.gameExample.setText(str(self.answers[0])), self.gameExample.show()
        self.gameCounter.setText(f'правильно: {self.success} из {self.count}'), self.gameCounter.setFont(self.my_font), self.gameCounter.show()
        self.gameAnswer1.setText(str(self.answers[indexes[0]]))
        self.gameAnswer1.setStyleSheet(self.styleNow), self.gameAnswer1.show()
        self.gameAnswer2.setText(str(self.answers[indexes[1]]))
        self.gameAnswer2.setStyleSheet(self.styleNow), self.gameAnswer2.show()
        self.gameAnswer3.setText(str(self.answers[indexes[2]]))
        self.gameAnswer3.setStyleSheet(self.styleNow), self.gameAnswer3.show()
        self.gameAnswer4.setText(str(self.answers[indexes[3]]))
        self.gameAnswer4.setStyleSheet(self.styleNow), self.gameAnswer4.show()
        self.gameRestart.setStyleSheet(self.styleNow)

    def settingsGame(self):
        pass

    def profile(self):
        if self.settSound.isChecked():
            self.sound.play()
        self.menuLabel1.hide(), self.menuButton1.hide(), self.menuButton2.hide(), self.menuButton3.hide()
        self.menuButton4.hide(), self.title.hide()

        self.profLabel2.setText(f'      Ник аккаунта: {self.pInfo[0][1]}')
        self.profLabel3.setText(f'      Пароль: {self.pInfo[0][2]}')
        self.profLabel4.setText(f'      Игр сыграно: {self.pInfo[1][6]}')
        self.profLabel5.setText(f'      Максимально правильно решено за 1 игру: {self.pInfo[1][1]}')
        self.profLabel6.setText(f'      Решено всего примеров: {self.pInfo[1][2]}')
        self.profLabel7.setText(f'      Решено правильно примеров всего: {self.pInfo[1][3]}')
        self.profLabel8.setText(f'      Решено неправильно примеров всего: {self.pInfo[1][4]}')
        self.profLabel9.setText(f'      Процент правильности решения: {self.pInfo[1][5]}')

        self.ButtonToMenu.show(), self.profLabel1.show(), self.profLabel2.show()
        self.profLabel3.show(), self.profLabel4.show(), self.profLabel5.show(), self.profLabel6.show()
        self.profLabel7.show(), self.profLabel8.show(), self.profLabel9.show()

    def settings(self):
        if self.settSound.isChecked():
            self.sound.play()
        self.ButtonToMenu.setStyleSheet(self.styleNow), self.settHelp.setStyleSheet(self.styleNow)
        self.settMusic.setStyleSheet(self.styleNow), self.settSound.setStyleSheet(self.styleNow)
        self.menuLabel1.hide(), self.menuButton1.hide(), self.menuButton2.hide(), self.menuButton3.hide(), self.menuButton4.hide()
        self.ButtonToMenu.show(), self.settHelp.show()
        self.settMusic.show(), self.settSound.show()
        self.settSetFon1.show(), self.settSetFon2.show(), self.settSetFon3.show()
        self.settSetFon4.show(), self.settSetFon5.show(), self.settSetFon6.show()

    def reg_account(self):
        if self.settSound.isChecked():
            self.sound.play()

        self.buttonReg.hide(), self.buttonLog.hide(), self.ButtonToAuth.show(), self.title.show()
        self.authLabel1.hide(), self.authLabel2.hide(), self.authLabel3.hide()

        self.regLabel1.show(), self.regLabel2.show(), self.regLabel3.show()
        self.regButton.show(), self.regCheckBox.show(), self.regButton2.show()
        self.regLogin.show(), self.regPassword.show(), self.ButtonToAuth.show()

    def log_account(self):
        if self.settSound.isChecked():
            self.sound.play()

        self.buttonReg.hide(), self.buttonLog.hide(), self.ButtonToAuth.hide(), self.title.show()
        self.authLabel1.hide(), self.authLabel2.hide(), self.authLabel3.hide()

        self.logLabel1.show(), self.logLabel2.show(), self.logLabel3.show()
        self.logLogin.show(), self.logPassword.show(), self.logButton.show(), self.ButtonToAuth.show()

    def register(self):
        log = self.regLogin.text()
        pas = self.regPassword.text()

        if len(log) == 0:
            self.Error.setText('Ошибка! Введите Ваш логин!'), self.Error.show()
        elif len(pas) == 0:
            self.Error.setText('Ошибка! Введите Ваш пароль!'), self.Error.show()
        elif not self.regCheckBox.isChecked():
            self.my_font.setPointSize(9)
            self.Error.setFont(self.my_font)
            self.Error.setText('Ошибка! Примите правила конфиденциальности!'), self.Error.show()
        else:
            self.regButton.hide(), self.regButton2.hide(), self.regLogin.hide(), self.regPassword.hide()
            self.regCheckBox.hide(), self.regLabel1.hide(), self.regLabel2.hide(), self.regLabel3.hide()
            self.Error.hide(), self.ButtonToAuth.hide()

            query = f"SELECT * FROM `accounts` WHERE `Nick` = '{log}'"
            result = cur.execute(query).fetchall()
            if result:
                self.Error.setText('Аккаунт с таким ником уже есть!'), self.Error.show(), self.reg_account()
            else:
                query = f"INSERT INTO accounts (Nick, Password) VALUES ('{log}', '{pas}')"
                cur.execute(query), db.commit()

                query = f"SELECT * FROM `accounts` WHERE `Nick` = '{log}'"
                self.pInfo = cur.execute(query).fetchall()

                query = "INSERT INTO `info` DEFAULT VALUES"
                cur.execute(query), db.commit()

                self.logi(f'\n[{datetime.datetime.now()}] Новый пользователь: Nick - {log}, Password - {pas}')

                self.get_info()
                self.menu()

    def authorize(self):
        log = self.logLogin.text()
        pas = self.logPassword.text()
        if len(log) == 0:
            self.Error.setText('Ошибка! Введите Ваш логин!'), self.Error.show()
        elif len(pas) == 0:
            self.Error.setText('Ошибка! Введите Ваш пароль!'), self.Error.show()
        else:
            self.logLabel1.hide(), self.logLabel2.hide(), self.logLabel3.hide(), self.title.hide()
            self.logLogin.hide(), self.logPassword.hide(), self.logButton.hide()
            if log == 'root' and pas != '09122004':
                self.logi(f'\n[{datetime.datetime.now()}] БЕЗОПАСНОСТЬ: Замечена попытка входа в аккаунт ROOT! Введённый пароль - {pas}')
            query = f"SELECT * FROM `accounts` WHERE `Nick` = '{log}'"
            self.pInfo = cur.execute(query).fetchall()
            if self.pInfo:
                if pas == self.pInfo[0][2]:
                    self.logi(f'\n[{datetime.datetime.now()}] Вход в аккаунт: Nick - {log}, Password - {pas}')
                    self.get_info()
                    self.menu()
                else:
                    self.Error.setText('Неверный пароль!'), self.Error.show(), self.log_account()
            else:
                self.Error.setText('Аккаунт не найден!'), self.Error.show(), self.log_account()

    def again(self):
        self.timer_.start(1000)
        self.second += 1
        if self.timePlaying - self.second >= 0:
            self.gameTimer.setText(f'Осталось секунд: {self.timePlaying - self.second}')
        else:
            self.timer_.stop()
            self.gameCounter.hide()
            self.end_game()

    def get_info(self):
        query = f"SELECT * FROM `accounts` WHERE `ID` = {self.pInfo[0][0]}"
        self.pInfo = list(cur.execute(query).fetchall())

        query = f"SELECT * FROM `info` WHERE `ID` = {self.pInfo[0][0]}"
        result = list(cur.execute(query).fetchall())
        self.pInfo.extend(result)

        print(self.pInfo)

    def browser1(self):
        if self.settSound.isChecked():
            self.sound.play()
        webbrowser.open('https://www.gosuslugi.ru/', new=2)

    def browser2(self):
        if self.settSound.isChecked():
            self.sound.play()
        webbrowser.open('http://kremlin.ru/', new=2)

    def generator(self):
        figures = '+-*/'
        num1 = randint(-10, 10)
        num2 = randint(-10, 10)
        figure = figures[randint(0, 3)]
        if figure == '/' and num2 == 0:
            num2 = randint(1, 10)
        return f'{num1} {figure} {num2}', str(int(eval(f'{num1} {figure} {num2}'))), int(randint(-50, 50)), int(randint(-50, 50)), int(randint(-50, 50))

    def check_answer(self):
        if str(self.sender().text()) == str(self.answers[1]):
            self.success += 1
        self.count += 1
        self.gameExample.setText(''), self.gameCounter.setText('')#, self.gameTimer.setText('')
        if time.time() - self.timer < self.timePlaying:
            self.game()
        else:
            self.end_game()

    def end_game(self):
        print('+++')
        self.gameExample.hide(), self.gameTimer.hide(), self.gameAnswer1.hide(), self.gameAnswer2.hide()
        self.gameAnswer3.hide(), self.gameAnswer4.hide(), self.gameRestart.show()

        self.endLabel1.setText('Время вышло!'), self.endLabel1.show()
        self.endLabel2.setText('Итог'), self.endLabel2.show()
        self.endLabel3.setText(f'Решено всего примеров: {self.count}'), self.endLabel3.show()
        self.endLabel4.setText(f'Решено правильно примеров: {self.success}'), self.endLabel4.show()
        self.endLabel5.setText(f'Решено неправильно примеров: {self.count - self.success}'), self.endLabel5.show()
        self.endLabel6.setText(f'Процент правильности решения: {round((self.success / self.count) * 100, 2)}'), self.endLabel6.show()

        query = f"SELECT * FROM `info` WHERE `ID` = {self.pInfo[0][0]}"
        result = list(cur.execute(query).fetchall())

        if self.success > result[0][1]:
            query = f"UPDATE `info` SET `Record` = {self.success} WHERE `ID` = {self.pInfo[0][0]}"
            cur.execute(query), db.commit()

        query = f"UPDATE `info` SET `Count` = `Count` + {self.count}, `RightTotal` = `RightTotal` + {self.success}, " \
                f"`WrongTotal` = `WrongTotal` + {self.count - self.success} WHERE `ID` = {self.pInfo[0][0]}"

        cur.execute(query), db.commit()

        query = f"UPDATE `info` SET `KF` = {round(float(result[0][3] / result[0][2]), 4)} WHERE `ID` = {self.pInfo[0][0]}"
        cur.execute(query), db.commit()

        query = f"UPDATE `info` SET `CountGames` = `CountGames` + 1 WHERE `ID` = {self.pInfo[0][0]}"
        cur.execute(query), db.commit()

        self.count, self.timer, self.success, self.error, self.startGame = 0, 0, 0, 0, False

    def changeFon(self):
        if self.settSound.isChecked():
            self.sound.play()
        num = self.sender().text()
        if num == '1':
            self.background.setPixmap(QPixmap("background\\bubbles.jpg"))
            self.picture = 'background\\bubbles.jpg'
            self.styleNow = self.styleBubbles
            o = 'self.styleBubbles'
        elif num == '2':
            self.background.setPixmap(QPixmap("background\\drop.jpg"))
            self.picture = 'background\\drop.jpg'
            self.styleNow = self.styleDrop
            o = 'self.styleDrop'
        elif num == '3':
            self.background.setPixmap(QPixmap("background\\fon1.jpg"))
            self.picture = 'background\\fon1.jpg'
            self.styleNow = self.styleFon1
            o = 'self.styleFon1'
        elif num == '4':
            self.background.setPixmap(QPixmap('background\\fon2.jpg'))
            self.picture = 'background\\fon2.jpg'
            self.styleNow = self.styleFon2
            o = 'self.styleFon2'
        elif num == '5':
            self.background.setPixmap(QPixmap("background\\fon3.jpg"))
            self.picture = 'background\\fon3.jpg'
            self.styleNow = self.styleFon3
            o = 'self.styleFon3'
        elif num == '6':
            self.background.setPixmap(QPixmap("background\\fon4.jpg"))
            self.picture = 'background\\fon4.jpg'
            self.styleNow = self.styleFon4
            o = 'self.styleFon4'
        else:
            o = 'self.styleBubbles'
        self.settHelp.setStyleSheet(self.styleNow), self.settMusic.setStyleSheet(self.styleNow)
        self.settSound.setStyleSheet(self.styleNow), self.ButtonToMenu.setStyleSheet(self.styleNow)

        file = open('files\\config.txt', 'w')
        file.write(f'{self.picture}\n{o}')
        file.close()

    def changeMusic(self):
        what = self.sender().text()
        print(what)

        if what == ' Музыка':
            file = open('files\\config.txt', 'r')
            txt = file.read()
            if self.settMusic.isChecked():
                txt = txt.replace('musicOFF', 'musicON')
                self.music.play(), self.music.setLoops(100)
            else:
                txt = txt.replace('musicON', 'musicOFF')
                self.music.stop()
            file.close()

            file = open('files\\config.txt', 'w')
            file.write(txt)
            file.close()

        if what == '   Звук':
            file = open('files\\config.txt', 'r')
            txt = file.read()
            if self.settSound.isChecked():
                txt = txt.replace('soundOFF', 'soundON')
            else:
                txt = txt.replace('soundON', 'soundOFF')
            file.close()

            file = open('files\\config.txt', 'w')
            file.write(txt)
            file.close()

        print(txt)

    def logi(self, line):
        file = open('files\\logs.txt', 'a', encoding='cp1251')
        file.write(line)
        file.close()

    def retranslateUI(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'FastMath'))
        self.buttonLog.setText(_translate('MainWindow', 'Авторизация'))
        self.buttonReg.setText(_translate('MainWindow', 'Регистрация'))
        self.title.setText(_translate('MainWindow', 'FastMath'))


class Second(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        My.setObjectName(self, 'FastMath')
        self.showFullScreen()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # sec = Second()
    # sec.show()

    mw = My()
    mw.setWindowIcon(QIcon('title.png'))
    mw.show()

    sys.exit(app.exec())
