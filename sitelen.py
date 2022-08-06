# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sitelen.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

import random
import string
import flask
from flask import Flask
from flask import request
import threading
import requests

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)

acces_code = ""
token = ""
client_id = "472f565b135d44e5bc5d40d36e1c26ed"
client_secret = "80b1fd56efd343edb9187ba211bee072"
redirect_uri = "http://localhost:8080"

from werkzeug.serving import make_server

class ServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('localhost', 8080, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print('starting server')
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()



def start_server(killme):
    global server
    app = flask.Flask('myapp')
    # App routes defined here
    @app.route('/',methods=['GET','POST','PUT'])
    def home():
        print("got here")
        args = request.args
        print(args)
        print(args.get("code"))
        acces_code = args.get("code")
        form = {
        'code': acces_code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
        }
        import base64
        headers = {
        'Authorization': 'Basic ' + str(base64.b64encode(((client_id+':'+client_secret).encode('ascii'))))[2:-1]
        }
        r = requests.post('https://accounts.spotify.com/api/token',data=form,headers=headers)
        res = r.json()
        print(res)
        token = res.get('access_token')
        print(token)
        f = open("token.txt",'w')
        f.write(token)
        f.close()
        stop_thread = threading.Thread(target=stop_server,args=('absolutely nothing',))
        stop_thread.start()
        return "yay! seems to work. you can close this tab now (your token: " + token + " )"

    server = ServerThread(app)
    server.start()
    print('server started')

def stop_server(shit):
    global server
    from time import sleep
    sleep(5)
    server.shutdown()




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(814, 609)
        font = QFont()
        font.setFamilies([u"Noto Mono"])
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(180, 10, 384, 47))
        font1 = QFont()
        font1.setFamilies([u"Noto Mono"])
        font1.setPointSize(30)
        self.label.setFont(font1)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(260, 230, 211, 31))
        font2 = QFont()
        font2.setFamilies([u"Noto Mono"])
        font2.setPointSize(13)
        self.pushButton.setFont(font2)
        self.pushButton.pressed.connect(self.logic)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 814, 20))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"First time setup", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"connect spotify", None))
    # retranslateUi
    def logic(self):
        import webbrowser
        from urllib.parse import urlencode
        state = get_random_string(16)
        scope = "user-read-email"
        mydict = {
        'response_type': 'code',
        'client_id': client_id,
        'scope': scope,
        'redirect_uri': redirect_uri,
        'state': state,
        'show_dialog': 'true'
        }
        self.new_thread = threading.Thread(target=start_server,args=('shiut',))
        self.new_thread.start()
        webbrowser.open('https://accounts.spotify.com/authorize?'+urlencode(mydict), new=0)
