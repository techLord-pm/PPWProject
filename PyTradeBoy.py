import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import websocket
import requests
from time import time
from time import mktime
from datetime import datetime
import asyncio
import threading
from threading import Thread
from datetime import datetime
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
import json
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsItem, QGraphicsTextItem, QLabel, QTableWidget, QBoxLayout, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QFormLayout, QButtonGroup, QScrollArea, QGroupBox,QGridLayout, QFormLayout,QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon
import PyQt5.QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui, uic, QtCore
from PyQt5.QtCore import Qt, pyqtSlot, QObject, QThread
import os.path
from os import path
import random
import pymysql
import pymysql.cursors
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg


data=[]
newData=[]#testing
data1=dict()


start_time = time()
max_runtime = 15  # 15 seconds,
runtime = 0  # accounts for aiding in tracking estimated time
#dataStore = []

#Factory class design
class Trade:
        #below does nothing as of yet
        print("Trade called.")
        buy = []
        sell = []

        # intitialize lists
        counter = 0
        # dictionary to store all these as key value pairs?
        fifteenLowLog = []
        fifteenHighLog = []

        # will be updated
        shortLog = []  # to hold all values from 15 second data pull
        shortStore = []  # counter to match plot shortLog
        trendStore = []
        store = []
        #dataStore = []
        fifteenLog = []
        minute = []
        fiveMinute = []
        fifteenMinute = []
        thirtyMinute = []
        hour = []  # by 15 second intervals
        day = []  # by 5 min intervals

        wallet = 200

        def calcAverage(self, list):
            totalSum = 0
            count = 0
            min = 1000000
            max = 0
            print("type of list is:", type(list))

            for item in list:
                pyObject = json.loads(item)
                if pyObject['type'] == "ping":
                    print("ping!")
                    continue
                print("type of object is:", type(pyObject['data'][0]['p']))
                print(pyObject['data'][0]['p'])
                if pyObject['data'][0]['p'] < min:
                    min = pyObject['data'][0]['p']
                if pyObject['data'][0]['p'] > max:
                    max = pyObject['data'][0]['p']
                # print(item[1]['p']) #enumerated number
                # print(item[1]) #data set in json form
                totalSum = totalSum + pyObject['data'][0]['p']
                self.shortLog.append(pyObject['data'][0]['p'])
                count += 1
                self.shortStore.append(count)
            self.fifteenLog.append((totalSum / count))
            self.fifteenLowLog.append(min)
            self.fifteenHighLog.append(max)
            self.store.append(self.counter)

            return (totalSum / count)

        def calcMinute(self, list):
            try:
                i = 0
                size = len(list)
                total = 0
                while i < 4:
                    total += list[size - 1 - i]
                    i += 1
            except Exception as e:
                print("error in calcMinute...", e)
            return (total / 4)

        def calcFiveMinute(self, list):
            try:
                i = 0
                size = len(list)
                total = 0
                while i < 5:
                    total += list[size - 1 - i]
                    i += 1
            except Exception as e:
                print("error in calcFiveMinute...", e)
            return (total / 5)

        # plots every average 15 second log low, average, and high price over time. Includes linear and polynomial regression
        def plot_regression_line(self, x, y, b, a, c, d, k):
            # plotting the actual points as scatter plot
            plt.scatter(x, y, color="b",
                        marker="o", s=30)
            plt.scatter(x, a, color="g", marker="o", s=30)
            plt.scatter(x, d, color="r", marker="o", s=30)

            polyModel = np.poly1d(np.polyfit(x, y, 3))
            polyLine = np.linspace(0, len(x), 1000)

            # predicted response vector
            y_pred = b[0] + b[1] * x
            a_pred = c[0] + c[1] * x
            d_pred = k[0] + k[1] * x

            # plotting the regression line
            plt.plot(x, y_pred, color="b")
            plt.plot(x, a_pred, color="g")
            plt.plot(x, d_pred, color="r")
            plt.plot(polyLine, polyModel(polyLine))
            # putting labels
            plt.legend(['average', 'high', 'low'], loc='upper left')

            plt.xlabel('ETH / USD')
            plt.ylabel('# of 15 Second Intervals')

            # function to show plot
            plt.show()

        # a quick trend plot changing every 15 second log
        def trend(self, x, y, b):
            plt.scatter(x, y, color="b",
                        marker="o", s=30)
            polyModel = np.poly1d(np.polyfit(x, y, 3))
            polyLine = np.linspace(0, len(x), 1000)

            y_pred = b[0] + b[1] * x

            plt.plot(x, y_pred, color="b")
            if b[1] > 0:  # positive trend
                self.trendStore.append("+")
            else:
                self.trendStore.append("-")
            plt.plot(polyLine, polyModel(polyLine))
            plt.show()

        def isNear(self, price, price2):
            return (abs(price - price2) <= 0.15)

        def __init__(self, symbol, price):
            self.symbol = symbol
            self.price = price

        #create based on class name
        def factory(type):
            #return eval(type+"()")
            if type == "Stock": return Stock()
            if type == "Crypto": return Crypto()
            assert 0, "Bad shape creation: " + type
        factory = staticmethod(factory)

class Stock(Trade):
    ticker = 'stock'
    print("STOCK")
class Crypto(Trade):
    symbol = 'eth'
    print("CRYPTO")
# testing

def on_message(ws, message):
    print(message)
    data.append(message) #testing
    newData.append(message) #might be the one that matters
    #dataStore.append(message)
    #print("message type is offff:", type(message))

def on_error(ws, error):
    print(error)
def on_close(self, ws):
    print("### closed ###")
def on_open(ws):

    ws.send('{"type":"subscribe","symbol":"BINANCE:ETHUSDT"}') #just one crpto currency for now

def end_loop():
    if time()-start_time > max_runtime:
        return True
    else:
        return False

async def timer(ws):
    start_time = time()
    while time() - start_time < max_runtime:
        # do some stuff
        if ws.keep_running == True:
            #print("is on")
            pass
        else:
            print("isoff")
            thread = Thread(target=ws.run_forever)
            thread.start()
        #print(time())
        if end_loop():
            print("end")
            break
    return ws

class Account():
    def __init__(self, apiKey, mysqlPassword, email, phone):
        self.apiKey = apiKey
        self.mysqlPassword = mysqlPassword
        self.email = email
        self.phone = phone

# widget for configuration view part 1/2
class IntroductionWidget(QtWidgets.QWidget):
    def __init__(self, mysqlPassword):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("Configuration Part 1/2")
        self.setGeometry(0,0,600,500)
        screen_center = lambda \
            widget: app.desktop().screen().rect().center() - widget.rect().center()  # determines center of view
        self.move(screen_center(self))  # move to center

        # sets background color
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.darkCyan)  # set background color of widget to green
        self.setPalette(p)

        self.mysqlPassword = mysqlPassword
        # sets title label and alignment
        self.label1 = QLabel("PyTradeBot")
        self.label1.setFont(QtGui.QFont("Courier", 72, QtGui.QFont.Bold))
        self.label1.setAlignment(QtCore.Qt.AlignCenter)

        self.emptyLabel = QLabel(" ")  # to add an empty line
        self.instructionLabel = QLabel("- Please visit " +  '<a href=\"https://finnhub.io/\" style =\"color: yellow;\">FinnHub.io</a>' + " and select 'Get free API key'")
        #self.instructionLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)  # to enable selecting, copying, and pasting of web link
        self.instructionLabel.setOpenExternalLinks(True)

        self.instructionLabel2 = QLabel("- Complete registration")
        self.instructionLabel3 = QLabel("- Enter your API key below")

        self.instructionLabel.setFont(QtGui.QFont("Courier", 14, QtGui.QFont.Bold))
        self.instructionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.instructionLabel2.setFont(QtGui.QFont("Courier", 14, QtGui.QFont.Bold))
        self.instructionLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.instructionLabel3.setFont(QtGui.QFont("Courier", 14, QtGui.QFont.Bold))
        self.instructionLabel3.setAlignment(QtCore.Qt.AlignCenter)

        self.box1 = QLineEdit()
        self.box1.setPlaceholderText("API key")

        self.nextbtn = QPushButton("Next")
        self.nextbtn.setMaximumWidth(150)
        self.nextbtn.setMinimumWidth(150)
        self.nextbtn.clicked.connect(self.nextbtn_clicked)

        self.newbox = QVBoxLayout()
        self.newbox.addWidget(self.box1)

        self.layout3 = QButtonGroup()
        self.layout3.addButton(self.nextbtn)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label1)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.instructionLabel)
        self.vbox.addWidget(self.instructionLabel2)
        self.vbox.addWidget(self.instructionLabel3)
        self.vbox.addWidget(self.emptyLabel)
        # vbox.addWidget(box)

        self.vbox.addLayout(self.newbox)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.nextbtn, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(self.vbox)
        self.vbox.setAlignment(Qt.AlignTop | Qt.AlignCenter)

    def nextbtn_clicked(self):
        print("Next clicked!")
        print(self.box1.text())

        self.key = self.box1.text()

        if self.box1.text() != "" and self.box1.text() != "API key":
            self.w = SecondIntroductionWidget(self.mysqlPassword, self.key)
            self.w.show() #show new widget window
            self.hide() #hide old widget window

# widget for configuration view part 2/2
class SecondIntroductionWidget(QtWidgets.QWidget):
    def __init__(self,mysqlPassword,key):
        '''
        self.setWindowTitle("Python Trading Bot")
        self.setGeometry(0, 0, 600, 500)
        screen_center = lambda \
                widget: app.desktop().screen().rect().center() - widget.rect().center()  # determines center of view
        self.move(screen_center(self))  # move to center
        '''
        super().__init__()
        self.mysqlPassword = mysqlPassword
        self.key = key
        self.setWindowTitle("Configuration Part 2/2")
        self.setGeometry(0, 0, 600, 500)
        screen_center = lambda \
                widget: app.desktop().screen().rect().center() - widget.rect().center()  # determines center of view
        self.move(screen_center(self))  # move to center

        # sets background color
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.darkCyan)  # set background color of widget to green
        self.setPalette(p)

        self.label1 = QLabel("PyTradeBot")
        self.label1.setFont(QtGui.QFont("Courier", 72, QtGui.QFont.Bold))
        self.label1.setAlignment(QtCore.Qt.AlignCenter)

        self.instructionLabel2 = QLabel("- Enter your Email below")

        self.instructionLabel3 = QLabel("- Enter your Phone Number below")

        self.instructionLabel2.setFont(QtGui.QFont("Courier", 14, QtGui.QFont.Bold))
        self.instructionLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.instructionLabel3.setFont(QtGui.QFont("Courier", 14, QtGui.QFont.Bold))
        self.instructionLabel3.setAlignment(QtCore.Qt.AlignCenter)


        self.emailBox = QLineEdit()
        self.emailBox.setPlaceholderText("Email")

        self.phoneBox = QLineEdit()
        self.phoneBox.setPlaceholderText("Phone Number as XXXXXXXXXX")

        self.emptyLabel = QLabel(" ")  # to add an empty line

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label1)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.instructionLabel2)
        self.vbox.addWidget(self.emailBox)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.instructionLabel3)
        self.vbox.addWidget(self.phoneBox)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.emptyLabel)

        self.confirmbtn = QPushButton("Confirm")
        self.confirmbtn.setMaximumWidth(150)
        self.confirmbtn.setMinimumWidth(150)
        self.confirmbtn.clicked.connect(self.confirmbtn_clicked)

        print("2nd page inputs...")
        print("phone",self.phoneBox.text())
        print("email", self.emailBox.text())

        self.buttonLayout = QButtonGroup()
        self.buttonLayout.addButton(self.confirmbtn)

        self.vbox.addWidget(self.confirmbtn, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(self.vbox)
        self.vbox.setAlignment(Qt.AlignTop | Qt.AlignCenter)

    def confirmbtn_clicked(self):
        print("Confirm clicked!")

        if self.emailBox.text() != "" and self.phoneBox.text() != "":

            textFile = open("PyTradeBot.txt","w+")
            textFile.write(self.mysqlPassword)
            textFile.close() #testing

            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password=self.mysqlPassword,
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor,
                                         #database = 'PyTradeBot'
                                         )
            #where working connection is made
            cursor = connection.cursor()

            cursor.execute("CREATE DATABASE IF NOT EXISTS PyTradeBot")

            connection.select_db("PyTradeBot") # switch to the newly created database

            #table creation commands for PyTradeBot database
            cursor.execute("CREATE TABLE account(account_id INT NOT NULL AUTO_INCREMENT, phone VARCHAR(11) NOT NULL, email VARCHAR(100) NOT NULL, wallet INT(9) NOT NULL, apiKey VARCHAR(100) NOT NULL, PRIMARY KEY (account_id))")
            cursor.execute("CREATE TABLE buy_trades(buy_id INT NOT NULL AUTO_INCREMENT, price DOUBLE NOT NULL, quantity INT(9) NOT NULL, time VARCHAR(50), PRIMARY KEY (buy_id))")
            cursor.execute("CREATE TABLE PyTradeBot.sell_trades(sell_id INT NOT NULL AUTO_INCREMENT, price DOUBLE NOT NULL, quantity INT(9) NOT NULL, time VARCHAR(50), PRIMARY KEY (sell_id))")

            #insert account information
            sqlInsert ="INSERT INTO `account` (`phone`,`email`,`wallet`,`apiKey`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sqlInsert,(self.phoneBox.text(), self.emailBox.text(), int(100000), self.key))

            connection.commit()
            cursor.close()

            self.h = HomeWidget()
            self.h.show() #show new widget window
            self.hide() #hide old widget window


#home widget for home view
class HomeWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__() #testing



        self.liveTrades = {}
        self.buyList = []
        self.sellList = []
        self.change = 0 #difference gained or loss from trades


        self.high = 0
        self.low = 10000000
        self.price = 0
        self.currentPrice = 0
        self.tempPrice = 0 #to hold value every 19th iterations used to determine short term trend
        self.counter = 0 # to count 19th iterations and reset
        self.tradeCount = 0

        #for temp highs and lows
        self.tempHigh = 0
        self.tempLow = 10000000
        #self.rootPassword=""


        #QtWidgets.QMainWindow.__init__(self)
        #super(HomeWidget, self).__init__()
        self.initUI()
        self.scrollSize = 100 #should update to count of live datas
        self.setWindowTitle("PyTradeBot")
        #self.setGeometry(0, 0, 800, 650)
        #self.setGeometry(0, 0, 1000, 750)
        self.showMaximized() # maximizes screen without going into full screen mode

        #for the minimized screen, to center it
        #screen_center = lambda \
                #widget: app.desktop().screen().rect().center() - widget.rect().center()  # determines center of view
        #self.move(screen_center(self))  # move to center

        # sets background color
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)  # set background color of widget to green
        self.setPalette(p)

        #title label
        self.label1 = QLabel("PyTradeBot")
        self.label1.setFont(QtGui.QFont("Courier", 72, QtGui.QFont.Bold))
        self.label1.setAlignment(QtCore.Qt.AlignCenter)

        #Right column labels
        #1/2
        self.priceLabel = QLabel("Price: ")
        self.priceLabel.setFont(QtGui.QFont("Courier", 12, QtGui.QFont.Bold))
        self.highPriceLabel = QLabel("High: " + str(self.high))
        self.highPriceLabel.setFont(QtGui.QFont("Courier", 12, QtGui.QFont.Bold))
        self.lowPriceLabel = QLabel("Low: " + str(self.low))
        self.lowPriceLabel.setFont(QtGui.QFont("Courier", 12, QtGui.QFont.Bold))
        #2/2
        self.trendLabel = QLabel("Trend: ")
        self.trendLabel.setFont(QtGui.QFont("Courier", 12, QtGui.QFont.Bold))
        self.tradeCountLabel = QLabel("Buy Trades: ")
        self.tradeCountLabel.setFont(QtGui.QFont("Courier", 12, QtGui.QFont.Bold))
        self.returnLabel = QLabel("Sell Trades: ")
        self.returnLabel.setFont(QtGui.QFont("Courier", 12, QtGui.QFont.Bold))

        self.accountValueSQL = "SELECT `wallet` FROM `account` WHERE `account_id`>0"  # to retrieve wallet value, set to arbitrary 100,000 upon creation
        self.walletReturn = self.connectDB(self.accountValueSQL)
        #print(self.walletReturn)
        #print(self.walletReturn[0]['wallet'])

        self.nowPrice = self.walletReturn[0]['wallet']  # price to update wallet upon trades

        #Horizontal labels
        self.labelH = QLabel("  Price     Quantity      Time")
        self.labelH.setFont(QtGui.QFont("Courier", 12, QtGui.QFont.Bold))

        self.labelH2 = QLabel("$" + str(self.walletReturn[0]['wallet']))
        self.labelH2.setFont(QtGui.QFont("Courier", 36, QtGui.QFont.Bold))

        self.emptyLabel = QLabel(" ")  # to add an empty line

        self.graphWidget = pg.PlotWidget()
        self.x = []
        self.xLow = []
        self.xHigh = []
        self.y = []
        self.yLow = []
        self.yHigh = []

        #adjusting main plot view size

        self.graphWidget.setMaximumHeight(492)


        self.graphWidget.setBackground('w')
        self.graphWidget.addLegend()#to add graph legend 'name="Ethereum/USDT"'
        #self.pen = pg.mkPen(color=(100, 100, 0)) #ugly puke color
        self.pen = pg.mkPen(color=(0, 100, 100), width=6)
        self.graphWidget.plot(self.x, self.y, pen=self.pen, name="Ethereum USD / Trade")




        #vertical box for layout
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label1)

        self.hbox3 = QHBoxLayout()
        self.hbox3.addWidget(self.labelH)
        self.hbox3.addWidget(self.labelH2)

        self.vbox.addLayout(self.hbox3)


        #vertical box 2 for layout
        self.vbox2 = QVBoxLayout()

        self.vbox3 = QVBoxLayout()
        self.vbox3.addWidget(self.highPriceLabel)
        self.vbox3.addWidget(self.priceLabel)
        self.vbox3.addWidget(self.lowPriceLabel)

        self.vbox4 = QVBoxLayout()
        self.vbox4.addWidget(self.trendLabel)
        self.vbox4.addWidget(self.tradeCountLabel)
        self.vbox4.addWidget(self.returnLabel)



        # new for testing
        self.formLayout2 = QFormLayout()
        self.groupBox2 = QGroupBox("Incoming Data Stream")#2


        self.scrollBox2 = QScrollArea()
        self.scrollBox2.setWidget(self.groupBox2)
        self.scrollBox2.setWidgetResizable(True)
        self.scrollBox2.setFixedHeight(492)
        self.scrollBox2.setFixedWidth(300)



        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.scrollBox2)
        self.hbox.addWidget(self.graphWidget)
        self.hbox.addLayout(self.vbox3)
        self.hbox.addLayout(self.vbox4)

        self.hbox2 = QHBoxLayout()


        self.cbuysbtn = QPushButton("Show buy trades")
        self.cbuysbtn.setMaximumWidth(150)
        self.cbuysbtn.setMinimumWidth(150)
        self.cbuysbtn.clicked.connect(self.buybtn_clicked) #function called when clicked
        self.csellsbtn = QPushButton("Show sell trades")
        self.csellsbtn.setMaximumWidth(150)
        self.csellsbtn.setMinimumWidth(150)
        self.csellsbtn.clicked.connect(self.sellbtn_clicked)

        self.hbox2.addWidget(self.cbuysbtn)
        self.hbox2.addWidget(self.csellsbtn)



        #for bottom main live data
        self.formLayout = QFormLayout()
        self.groupBox = QGroupBox("Incoming Data Stream")
        self.formLayout.addRow(QLabel("awaiting data..."))
        #self.formLayout.addRow(QLabel(str(len(data))))

        #move this to above
        self.dataList = []

        #self.vbox2.addWidget(self.formLayout)
        self.groupBox.setLayout(self.formLayout)
        self.groupBox2.setLayout(self.formLayout2)

        #scroll box main bottom with live data
        self.scrollBox = QScrollArea()
        self.scrollBox.setWidget(self.groupBox)
        self.scrollBox.setWidgetResizable(True)
        self.scrollBox.setFixedHeight(120)
        #self.scrollBox.setFixedWidth(350)




        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.vbox2)
        self.vbox.addWidget(self.scrollBox)
        self.setLayout(self.vbox)
        self.vbox.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        #the magic
        self._update_timer = QtCore.QTimer()
        self._update_timer.timeout.connect(self.updateLabel)
        self._update_timer.start(10) #100

        self.update()



        #TESTING
    def initUI(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.do_work)
        #self.formLayout.addRow(QLabel("noob"))
        self.thread.finished.connect(self.thread.deleteLater)


        self.thread.start()


    def updateLabel(self):
        try:
            for item in newData:
                pyObject = json.loads(item)

                if item not in self.dataList and pyObject['type'] != "ping":
                    self.currentPrice = float(self.getPrice(item))
                    if len(self.buyList) > 0 and len(self.buyList) != len(self.sellList):
                        if self.checkStopLoss(self.currentPrice) == True:
                            #sell
                            self.sellList.append(self.currentPrice)
                            self.returnLabel.setText("Sell Trades: " + str(len(self.sellList)))
                            self.length = len(self.buyList)
                            self.change = self.change + self.buyList[self.length - 1] - self.currentPrice
                            self.nowPrice = self.nowPrice + self.change
                            self.labelH2.setText("$" + str(self.nowPrice))  # change main wallet label


                            self.sqlSellInsert = "INSERT INTO `sell_trades` (`price`,`quantity`,`time`) VALUES (%s, %s, %s)"
                            self.confirmDB(self.sqlSellInsert, self.getPrice(item), self.getQuantity(item),self.getTime(item))


                    #print("currr: ", self.currentPrice)
                    #print(type(self.currentPrice))
                    if self.currentPrice > self.high:
                        print("new high")
                        self.high = self.currentPrice
                        self.highPriceLabel.setText("High: " + str(self.currentPrice))
                    if self.currentPrice < self.low:
                        print("new low")
                        self.low = self.currentPrice
                        self.lowPriceLabel.setText("Low: " + str(self.currentPrice))
                    if self.currentPrice < self.tempLow:
                        self.tempLow = self.currentPrice
                        self.xLow.append(self.currentPrice)
                        self.yLow.append(len(self.x)+1)# is plus 1 correct?
                    if self.currentPrice > self.tempHigh:
                        self.tempHigh = self.currentPrice
                        self.xHigh.append(self.tempHigh)
                        #self.yHigh.append(len(self.yHigh)+1)
                        self.yHigh.append(len(self.x)+1) # is plus 1 correct?

                    if self.formLayout2.count() > 19:
                        self.formLayout2.removeRow(0)


                    self.dataList.append(item)
                    #self.formLayout.addRow(QLabel(item))

                    self.formLayout2.addRow(QLabel("$"+self.getPrice(item)+"  |  "+self.getQuantity(item)+"  |  "+self.getTime(item)))
                    self.counter+=1
                    if self.counter == 5 or self.counter > 5:
                        if self.tempPrice != 0 :
                            if self.tempPrice > self.currentPrice:
                                self.trendLabel.setText("Trend: Decreasing")
                                print("DESCREASING")
                                if len(self.buyList) == len(self.sellList):
                                    self.buyList.append(self.currentPrice)
                                    self.tradeCountLabel.setText("Buy Trades: " + str(len(self.buyList)))
                                    self.sqlBuyInsert = "INSERT INTO `buy_trades` (`price`,`quantity`,`time`) VALUES (%s, %s, %s)"
                                    self.confirmDB(self.sqlBuyInsert, self.getPrice(item), self.getQuantity(item),self.getTime(item))

                            elif self.tempPrice < self.currentPrice:
                                self.trendLabel.setText("Trend: Increasing")
                                print("INCREASING")
                                if len(self.buyList) != len(self.sellList):
                                    self.sellList.append(self.currentPrice)
                                    self.tradeCount+=1
                                    self.returnLabel.setText("Sell Trades: " + str(len(self.sellList)))
                                    self.length=len(self.buyList)
                                    self.change = self.change + self.buyList[self.length-1] - self.currentPrice
                                    self.nowPrice = self.nowPrice+self.change
                                    #self.labelH2.setText("$"+str(float(self.walletReturn[0]['wallet'])+self.change)) #change main wallet label
                                    self.labelH2.setText("$" + str(self.nowPrice))  # change main wallet label

                                    #insert into sell table
                                    self.sqlSellInsert = "INSERT INTO `sell_trades` (`price`,`quantity`,`time`) VALUES (%s, %s, %s)"
                                    self.confirmDB(self.sqlSellInsert, self.getPrice(item), self.getQuantity(item),self.getTime(item))

                        self.tempPrice = self.currentPrice
                        #print("tempprice:", self.tempPrice)
                        self.counter = 0
                        print("Buys:", self.buyList)
                        print("Sells:",self.sellList)

                    self.y.append(pyObject['data'][0]['p'])
                    self.x.append(len(self.y))


                    #might be out of place 1 tab in
                newData.pop(0) #delete item after iterating it

                self.priceLabel.setText("Price: " + str(self.currentPrice))
                self.graphWidget.clear()

                self.graphWidget.plot(self.x, self.y, pen=self.pen)

            #self.graphWidget.plot(self.x,)



            # reset variables afterwards to continue
            self.tempHigh = 0
            self.tempLow = 10000000

                    #print("xxxxx",self.x)
                    #print("yyyyy",self.y)

            #return self.formLayout
            #to autoscroll to most recent

            self.area = self.scrollBox2.verticalScrollBar()
            self.area.setValue(self.area.maximum())
        except Exception as e:
            print("updateLabel error:", e)
            #return "error"
    def updateBuyTrades(self):
        pass
    def getPrice(self,data):
        #print("get price called")
        pyObject = json.loads(data)
        return str(pyObject['data'][0]['p'])
    def getQuantity(self, data):
        #print("get quantity called")
        pyObject = json.loads(data)
        return str(pyObject['data'][0]['v'])
    def getTime(self,data):
        #print("get time called")
        pyObject = json.loads(data)
        timestamp = pyObject['data'][0]['t']
        #print(type(timestamp))
        return str(datetime.fromtimestamp(timestamp/1000))[11:-2] #must divide by 1000 because timestamp is of milliseconds and remove last 2 character (trailing 0's)

    def buybtn_clicked(self):
        #print("buy clicked!")
        self.deleteRows()
        self.sql = "SELECT `buy_id`,`price`,`quantity`, `time` FROM `buy_trades` WHERE `buy_id`>0"
        #testresult=self.connectDB(self.sql)
        if len(self.connectDB(self.sql)) == 0:
            print("No trades positions have been initiated yet")
            self.formLayout.addRow(QLabel("No trade positions have been initiated yet"))
        else:
            print("trades have been made")
            #print(self.result)
            #print(type(self.result))
            testresult = self.connectDB(self.sql)
            # will need a form loop here to iterate over results as trades are made
            for item in testresult:
                self.formLayout.addRow(QLabel(str(item)))

    def sellbtn_clicked(self):
        print("sell clicked!")
        self.deleteRows()
        self.sql = "SELECT `sell_id`,`price`,`quantity`, `time` FROM `sell_trades` WHERE `sell_id`>0"
        temper = self.connectDB((self.sql))
        if len(temper) == 0:
            print("No trades positions have been exited yet")
            self.formLayout.addRow(QLabel("No trades positions have been exited yet"))
        else:
            print("trades have been made")
            #print(temper)
            # will need a form loop here to iterate over results as trades are made
            for item in temper:
                self.formLayout.addRow(QLabel(str(item)))

    def deleteRows(self):
        print("delete rows called")
        count = self.formLayout.rowCount()
        #print("count of rows:", count)
        if count == 0:
            pass
        elif count == 1:
            self.formLayout.removeRow(0)
        else:

            for item in range(self.formLayout.count()):
                #print("item:", item)
                self.formLayout.removeRow(item)

        self.formLayout.update()

    def estimate_coef(self, x, y):
        # number of observations/points
        n = np.size(x)
        # mean of x and y vector
        m_x, m_y = np.mean(x), np.mean(y)
        # calculating cross-deviation and deviation about x
        SS_xy = np.sum(y * x) - n * m_y * m_x
        SS_xx = np.sum(x * x) - n * m_x * m_x
        # calculating regression coefficients
        b_1 = SS_xy / SS_xx
        b_0 = m_y - b_1 * m_x

        return (b_0, b_1)

    def shortTrend(self):
        if newData[0] < newData[len(newData)-1]:#is increasing
            return "Increasing"
        elif newData[0] > newData[len(newData)-1]:#is decreasing
            return "Decreasing"

    #return true if stop loss triggered ( more than 10 cents loss)
    def checkStopLoss(self,currentPrice):
        val = len(self.buyList) - 1
        if currentPrice - self.buyList[val] <= - 0.03:
            print("Stop Loss Triggered")
            return True
        return False
    def connectDB(self, sqlstatement):
        self.result = ""
        print("connectDB called")
        self.rootPassword = ""
        if path.exists("PyTradeBot.txt"):
            with open("PyTradeBot.txt") as o:
                self.rootPassword = o.readline()

                # establish database connection
                self.connection = pymysql.connect(host='localhost',
                                                  user='root',
                                                  password=self.rootPassword,
                                                  database='PyTradeBot',
                                                  charset='utf8mb4',
                                                  cursorclass=pymysql.cursors.DictCursor
                                                  )
                # call for apiKey
        try:
            with self.connection.cursor() as self.cursor:
                # get API KEY
                self.cursor.execute(sqlstatement)
                self.result = self.cursor.fetchall()
                print("result",self.result)
            self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            self.connection.close()
        return self.result
    def confirmDB(self, sqlstatement,arga,argb,argc):
        print("connfirmDB called")
        self.rootPassword = ""
        if path.exists("PyTradeBot.txt"):
            with open("PyTradeBot.txt") as o:
                self.rootPassword = o.readline()

                # establish database connection
                self.connection = pymysql.connect(host='localhost',
                                                  user='root',
                                                  password=self.rootPassword,
                                                  database='PyTradeBot',
                                                  charset='utf8mb4',
                                                  cursorclass=pymysql.cursors.DictCursor
                                                  )
                # call for apiKey
        try:
            with self.connection.cursor() as self.cursor:

                self.cursor.execute(sqlstatement, (arga,argb,argc))
            self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            self.connection.close()


class Worker(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)

    def on_message(ws, message):
        print(message)
        data.append(message)
        newData.append(message)
        #check if buy here?

    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("### closed ###")

    def on_open(ws):
        #ws.send('{"type":"subscribe","symbol":"AAPL"}')
        #ws.send('{"type":"subscribe","symbol":"AMZN"}')
        ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
        #ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')
    def do_work(self):

        if websocket.isEnabledForTrace():
            pass
            print("trace already enabled")
        else:
            websocket.enableTrace(True)
            ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=bp9nhovrh5rf91tippdg",
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)
            
            ws.on_open = on_open
            ws.run_forever()


if __name__ == "__main__":
    rootPassword=""
    app = QtWidgets.QApplication(sys.argv)
    #home = HomeWidget() #newest testing
    websocket.enableTrace(False) # to aid in websocket only called once
    try:
        r = open("PyTradeBot.txt", "r")
        #HomeWidget.show()
        #sys.exit(app.exec_())
    except Exception as e:
        pass
        #print(e)

    if path.exists("PyTradeBot.txt"):
        print("Welcome back")
        with open("PyTradeBot.txt") as o:
            home = HomeWidget()  # newest testing
            rootPassword = o.readline()


            timeTracker = 0
            fiveTracker = 0

            print('Started!')
            print('Requested stop!')
            print('Finished!')




        home.show()
        sys.exit(app.exec_())

    else:
        print("Welcome to PyTradeBot\n")
        rootPassword = input("Enter your MySQL root password: ")
        introWidget = IntroductionWidget(rootPassword)  # initializing class object variable
        introWidget.show()
        sys.exit(app.exec_())



