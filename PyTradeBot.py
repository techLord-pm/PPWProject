import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import websocket
import requests
from time import time
from time import mktime
from datetime import datetime
import asyncio
from threading import Thread
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor

from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

import json

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGraphicsTextItem, QLabel, QTableWidget, QBoxLayout, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QFormLayout, QButtonGroup, QScrollArea, QGroupBox, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen, QIcon
import PyQt5.QtGui
from PyQt5 import QtGui, uic, QtCore
from PyQt5.QtCore import Qt
import os.path
from os import path
import random

import pymysql.cursors
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

'''


start_time = time()
max_runtime = 15  # 15 seconds,
runtime = 0  # accounts for aiding in tracking estimated time
dataStore = []

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
                # print(pyObject['data'])
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

        def derivativePlot(self, x, y, b):
            plt.scatter(x, y, color="b",
                        marker="o", s=30)
            polyModel = np.polyder(np.poly1d(np.polyfit(x, y, 3)), 1)
            polyLine = np.linspace(0, len(x), 1000)

            y_pred = b[0] + b[1] * x

            plt.plot(x, y_pred, color="b")

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
def on_message(ws, message):
    print(message)
    dataStore.append(message)
    print("message type is of:", type(message))

def on_error(ws, error):
    print(error)
def on_close(self, ws):
    print("### closed ###")
def on_open(ws):
    #ws.send('{"type":"subscribe","symbol":"AAPL"}')
    #ws.send('{"type":"subscribe","symbol":"AMZN"}')
    #ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:ETHUSDT"}') #just one crpto currency for now
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

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

if __name__ == "__main__":
    #intitialize class object
    porfolio = {}
    bot = Trade("ETH", 230)
    timeTracker = 0
    fiveTracker = 0
    t = datetime.now()
    unix_secs = mktime(t.timetuple())
    print(unix_secs)

    websocket.enableTrace(True)

    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=bp9nhovrh5rf91tippdg",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)

    ws.on_open = on_open

    print('Started!')
    #loop.call_soon_threadsafe(ws.stop)  # here
    print('Requested stop!')
    #thread.join()
    print('Finished!')

    while True:
        try:
            print(bot.fifteenLog)
            print(bot.fifteenLowLog)
            print(bot.fifteenHighLog)

            dataStore.clear()
            bot.shortLog.clear()
            bot.shortStore.clear()
            loop=asyncio.get_event_loop().run_until_complete(timer(ws))
            print(bot.calcAverage(dataStore))
            start_time = time()
            while time() - start_time < 3:
                #do some stuff
                if end_loop():
                    print("end")
                    break
            if end_loop():
                print("true")
                #loop.close()
            else:
                print("false")
                timeTracker+=1
                bot.counter+=1
                xy = np.array(bot.shortStore)
                x = np.array(bot.shortLog)
                b = bot.estimate_coef(xy, x)
                print("Estimated coefficients:\nb_0 = {}  \
                                \nb_1 = {}".format(b[0], b[1]))
                bot.trend(xy,x,b)
                bot.derivativePlot(xy,x,b)
                try:
                    if bot.trendStore[-1] == "+" and bot.trendStore[-2] == "-":
                        bot.buy.append(bot.shortLog[-1])
                except Exception as e:
                    print("error trying buy criteria: ", e)

                if len(bot.buy) != len(bot.sell): # an open trade
                    if bot.trendStore[-1] != "+":
                        bot.sell.append(bot.shortLog[-1])
                print("BUY: ", bot.buy)
                print("SELL: ", bot.sell)
                #if closed, then we know try succeeded
                loop.close()
            if timeTracker == 4:
                timeTracker = 0
                bot.minute.append(bot.calcMinute(bot.fifteenLog))
                fiveTracker+=1

                # testing
                xy = np.array(bot.store)
                x = np.array(bot.fifteenLog)

                y = np.array(bot.fifteenHighLog)
                z = np.array(bot.fifteenLowLog)

                b = bot.estimate_coef(xy, x)
                print("Estimated coefficients:\nb_0 = {}  \
                \nb_1 = {}".format(b[0], b[1]))
                c = bot.estimate_coef(xy, y)
                print("Estimated coefficients:\nc_0 = {}  \
                               \nc_1 = {}".format(c[0], c[1]))
                d = bot.estimate_coef(xy, z)
                print("Estimated coefficients:\nd_0 = {}  \
                               \nd_1 = {}".format(d[0], d[1]))

                bot.plot_regression_line(xy,x,b,y,c,z,d)

                # end testing
                print("---------------------------------------------------")
                print("Minute Average List: ", bot.minute)
                print("---------------------------------------------------")

            if fiveTracker == 5:
                fiveTracker = 0
                bot.fiveMinute.append(bot.calcFiveMinute(bot.minute))
                print("---------------------------------------------------")
                print("5 Minute Average List: ", bot.fiveMinute)
                print("---------------------------------------------------")
        except Exception as e:
            print("error occured: ", str(e))
            continue
        #loop every 15 seconds, pause, should any trades be made? if not continue

'''
#will be utilized soon
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

        self.buttonLayout = QButtonGroup()
        self.buttonLayout.addButton(self.confirmbtn)

        self.vbox.addWidget(self.confirmbtn, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(self.vbox)
        self.vbox.setAlignment(Qt.AlignTop | Qt.AlignCenter)

    def confirmbtn_clicked(self):
        print("Confirm clicked!")

        if self.emailBox.text() != "" and self.phoneBox.text() != "":

            textFile = open("PyTradeBot.txt","w+")

            #textFile.write("!")
            #textFile.write('\n')
            textFile.write(self.mysqlPassword)
            #textFile.write('\n')
            #textFile.write("CRITICAL FOR APPLICATION FUNCTION")
            #textFile.write('\n')
            #textFile.write("DO NOT REMOVE")

            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password=self.mysqlPassword,
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor
                                         )

            try:
                with connection.cursor() as cursor:
                    sql = "CREATE DATABASE PyTradeBot"
                    #sql3 = "USE PyTradeBot;"
                    #sql2 = "CREATE TABLE Account( phone VARCHAR(50) UNSIGNED AUTO_INCREMENT PRIMARY KEY," \
                           #"apiKey VARCHAR(50) NOT NULL," \
                          # "email VARCHAR(50) NOT NULL)"
                    cursor.execute(sql)
                    #cursor.execute(sql3)
                    #cursor.execute(sql2)
                connection.commit()
            except Exception as e:
                print(e)
            finally:
                connection.close()


            self.h = HomeWidget()
            self.h.show() #show new widget window
            self.hide() #hide old widget window


#home widget for home view
class HomeWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyTradeBot")
        self.setGeometry(0, 0, 800, 650)
        screen_center = lambda \
                widget: app.desktop().screen().rect().center() - widget.rect().center()  # determines center of view
        self.move(screen_center(self))  # move to center

        # sets background color
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)  # set background color of widget to green
        self.setPalette(p)

        self.label1 = QLabel("PyTradeBot")
        self.label1.setFont(QtGui.QFont("Courier", 72, QtGui.QFont.Bold))
        self.label1.setAlignment(QtCore.Qt.AlignCenter)

        self.emptyLabel = QLabel(" ")  # to add an empty line

        #linear graphical model of overall account representation

        self.graphWidget = pg.PlotWidget()
        '''
        #self.setCentralWidget(self.graphWidget)
        self.hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.temperature = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.graphWidget.setBackground('w')
        self.pen = pg.mkPen(color=(100, 100, 0))
        self.graphWidget.plot(self.hour, self.temperature, pen=self.pen)
        '''

        #pie graph model of investment diversity
        '''
        self.df = pd.DataFrame({'Empty':[100]}, index = ['Empty'])
        self.df.plot.pie(y='Empty', figsize=(10,100))
        '''


        #self.scrollArea = QScrollArea()
        #self.scrollArea.setBackgroundRole(Qt.darkGray)

        #self.scrollArea.setWidget()


        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.label1)
        self.vbox.addWidget(self.emptyLabel)
        self.vbox.addWidget(self.graphWidget)
        self.setLayout(self.vbox)
        self.vbox.setAlignment(Qt.AlignTop | Qt.AlignCenter)


if __name__ == "__main__":
    rootPassword=""
    app = QtWidgets.QApplication(sys.argv)
    home = HomeWidget()

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
            rootPassword = o.readline()

        home.show()
        sys.exit(app.exec_())

    else:
        #print("Welcome to PyTradeBot")
        rootPassword = input("Enter your MySQL root password: ")
        introWidget = IntroductionWidget(rootPassword)  # initialzing class object variable
        introWidget.show()
        sys.exit(app.exec_())


    #establish database connection
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 #password='Peter44',
                                 password=rootPassword,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor
                                 )

    try:
        with connection.cursor() as cursor:
            sql = "CREATE DATABASE PyTradeBot2"
            cursor.execute(sql)
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        connection.close()

    print("Application Launching...")

    #introWidget = IntroductionWidget(rootPassword) #initialzing class object variable
    #introWidget.show()


    #sys.exit(app.exec_())
