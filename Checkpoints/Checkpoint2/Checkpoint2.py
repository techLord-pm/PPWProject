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
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

# just for practice/fun
buy = []
sell = []

start_time = time()
max_runtime = 15 #15 seconds,
runtime = 0 #accounts for aiding in tracking estimated time
#intitialize lists
counter = 0
#dictionary to store all these as key value pairs?
fifteenLowLog = []
fifteenHighLog = []

#will be updated
shortLog = [] # to hold all values from 15 second data pull
shortStore = [] #counter to match plot shortLog
trendStore = []
store = []
dataStore = []
fifteenLog = []
minute = []
fiveMinute = []
fifteenMinute = []
thirtyMinute = []
hour = [] #by 15 second intervals
day = [] #by 5 min intervals

wallet = 200


import json
#https://pypi.org/project/websocket_client/

#info from finnhubb.io
#The trend has strength when ADX is above 25. The trend is weak or the price is trendless when ADX is below 20, according to Wilder.
#Non-trending doesn't mean the price isn't moving. It may not be, but the price could also be making a trend change or is too volatile for a clear direction to be present.

#Factory class design
class Trade:
        #below does nothing as of yet
        '''
        def __init__(self,clayburn,wrecktify,immortal):
            self.clayburn = clayburn #ticker
            self.wrecktify = wrecktify
            self.immortal - immortal
            return 1
        '''

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
def on_error(ws, error):
    print(error)
def on_close(self, ws):
    print("### closed ###")
def on_open(ws):
    #ws.send('{"type":"subscribe","symbol":"AAPL"}')
    #ws.send('{"type":"subscribe","symbol":"AMZN"}')
    #ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:ETHUSDT"}') #just one crpto currency for now
    #ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')
def getLevels():
    p = requests.get('https://finnhub.io/api/v1/scan/support-resistance?symbol=BINANCE:ETHUSDT&resolution=D&token=bp9nhovrh5rf91tippdg')
    print(p.json())
def getPattern():
    t = requests.get('https://finnhub.io/api/v1/scan/pattern?symbol=BINANCE:ETHUSDT&resolution=D&token=bp9nhovrh5rf91tippdg')
    patternList = []
    i = 0
    bearCount = 0
    bullCount = 0
    print(t.json())
    if t.json() != "{}":
        print("not null")
    else:
        print("null")
    for attribute in t.json().items():
        print(attribute)
    count = len(attribute)
    print("countSize:", count)
    while i < count:
        print(attribute[1][i]) #each object in json
        patternList.append(attribute[1][i]["patterntype"])
        i += 1
    print(patternList)
    for item in patternList:
        if item == "bearish":
            bearCount+=1
        else:
            bullCount+=1
    if bullCount+bearCount == 0:
        print("No data")
    elif (bullCount / (bearCount + bullCount)) > 0.5:
        print("Bullish")
    else:
        print("Bearish")
def calcAverage(list):
    totalSum=0
    count=0
    min = 1000000
    max = 0
    for item in list:
        pyObject = json.loads(item)
        if pyObject['type'] == "ping":
            print("ping!")
            continue
        #print(pyObject['data'])
        print(pyObject['data'][0]['p'])
        if pyObject['data'][0]['p'] < min:
            min = pyObject['data'][0]['p']
        if pyObject['data'][0]['p'] > max:
            max = pyObject['data'][0]['p']
        #print(item[1]['p']) #enumerated number
        #print(item[1]) #data set in json form
        totalSum=totalSum+pyObject['data'][0]['p']
        shortLog.append(pyObject['data'][0]['p'])
        count+=1
        shortStore.append(count)
    fifteenLog.append((totalSum/count))
    fifteenLowLog.append(min)
    fifteenHighLog.append(max)
    store.append(counter)

    return (totalSum/count)
def isNear(price, price2):
    return (abs(price-price2) <= 0.15)
def patternReadings(request):
    return(request)
def end_loop():
    if time()-start_time > max_runtime:
        return True
    else:
        return False
def getAverage():
    eth = requests.get('https://finnhub.io/api/v1/scan/technical-indicator?symbol=BINANCE:ETHUSDT&resolution=D&token=bp9nhovrh5rf91tippdg')
    btc = requests.get('https://finnhub.io/api/v1/scan/technical-indicator?symbol=BINANCE:BTCUSDT&resolution=D&token=bp9nhovrh5rf91tippdg')
    n = requests.get(
        'https://finnhub.io/api/v1/scan/technical-indicator?symbol=BINANCE:ETHUSDT&resolution=D&token=bp9nhovrh5rf91tippdg')
    print(n.json())

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

def calcMinute(list):
    try:
        i=0
        size = len(list)
        total = 0
        while i < 4:
            total+=list[size-1-i]
            i+=1
    except Exception as e:
        print("error in calcMinute...", e)
    return (total/4)

def calcFiveMinute(list):
    try:
        i = 0
        size = len(list)
        total = 0
        while i < 5:
            total+=list[size-1-i]
            i+=1
    except Exception as e:
        print("error in calcFiveMinute...", e)
    return (total/5)


def estimate_coef(x, y):
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

#plots every average 15 second log low, average, and high price over time. Includes linear and polynomial regression
def plot_regression_line(x, y, b, a, c, d, k):
    # plotting the actual points as scatter plot
    plt.scatter(x, y, color="b",
                marker="o", s=30)
    plt.scatter(x, a, color="g", marker="o", s=30)
    plt.scatter(x, d, color="r", marker="o", s=30)

    polyModel = np.poly1d(np.polyfit(x, y, 3))
    polyLine = np.linspace(0,len(x), 1000)

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
def trend(x, y, b):
    plt.scatter(x, y, color="b",
                marker="o", s=30)
    polyModel = np.poly1d(np.polyfit(x, y, 3))
    polyLine = np.linspace(0, len(x), 1000)

    y_pred = b[0] + b[1] * x

    plt.plot(x, y_pred, color="b")
    if b[1] > 0: #positive trend
        trendStore.append("+")
    else:
        trendStore.append("-")
    plt.plot(polyLine, polyModel(polyLine))
    plt.show()

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
    #ws.run_forever()
    #ws.keep_running = False
    #loop = asyncio.get_event_loop()
    #thread = Thread(target=ws.run_forever)
    #thread.start()
    print('Started!')
    #loop.call_soon_threadsafe(ws.stop)  # here
    print('Requested stop!')
    #thread.join()
    print('Finished!')

    while True:
        try:
            print(fifteenLog)
            print(fifteenLowLog)
            print(fifteenHighLog)

            dataStore.clear()
            shortLog.clear()
            shortStore.clear()
            loop=asyncio.get_event_loop().run_until_complete(timer(ws))
            print(calcAverage(dataStore))
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
                counter+=1
                xy = np.array(shortStore)
                x = np.array(shortLog)
                b = estimate_coef(xy, x)
                print("Estimated coefficients:\nb_0 = {}  \
                                \nb_1 = {}".format(b[0], b[1]))
                trend(xy,x,b)
                try:
                    if trendStore[-1] == "+" and trendStore[-2] == "-":
                        buy.append(shortLog[-1])
                except Exception as e:
                    print("error trying buy criteria: ", e)

                if len(buy) != len(sell): # an open trade
                    if trendStore[-1] != "+":
                        sell.append(shortLog[-1])
                print("BUY: ", buy)
                print("SELL: ", sell)
                #if closed, then we know try succeeded
                loop.close()
            if timeTracker == 4:
                timeTracker = 0
                minute.append(calcMinute(fifteenLog))
                fiveTracker+=1

                # testing
                xy = np.array(store)
                x = np.array(fifteenLog)

                y = np.array(fifteenHighLog)
                z = np.array(fifteenLowLog)

                b = estimate_coef(xy, x)
                print("Estimated coefficients:\nb_0 = {}  \
                \nb_1 = {}".format(b[0], b[1]))
                c = estimate_coef(xy, y)
                print("Estimated coefficients:\nc_0 = {}  \
                               \nc_1 = {}".format(c[0], c[1]))
                d = estimate_coef(xy, z)
                print("Estimated coefficients:\nd_0 = {}  \
                               \nd_1 = {}".format(d[0], d[1]))

                '''
                plot_regression_line((xy, x, b))
                plot_regression_line(xy, y, c)
                plot_regression_line(xy, z, d)
                '''
                plot_regression_line(xy,x,b,y,c,z,d)



                # end testing
                print("---------------------------------------------------")
                print("Minute Average List: ", minute)
                print("---------------------------------------------------")

            if fiveTracker == 5:
                fiveTracker = 0
                fiveMinute.append(calcFiveMinute(minute))
                print("---------------------------------------------------")
                print("5 Minute Average List: ", fiveMinute)
                print("---------------------------------------------------")

        except Exception as e:
            print("error occured: ", str(e))
            continue
        #getLevels()
        #getPattern()
        #getAverage()
        #loop every 15 seconds, pause, should any trades be made? if not continue
        '''
        print(dataStore) # holds all data entered in a different thread
        print(calcAverage(dataStore)) #prints average
        print(max(dataStore))
        print(min(dataStore))
        #if last value is greater than average -> trending up?
        #if last value is less than average -> trending down?
        if isNear(1,1.02) == True:
            print("asdfasdf")
        '''

#determine price fluctuations/direction of all cryptos to compare to the one.