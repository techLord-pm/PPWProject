#import pandas as pd
#import numpy as np
import websocket
import requests
from time import time
import asyncio
from threading import Thread

start_time = time()
max_runtime = 5
import json
#https://pypi.org/project/websocket_client/

#The trend has strength when ADX is above 25. The trend is weak or the price is trendless when ADX is below 20, according to Wilder.
#Non-trending doesn't mean the price isn't moving. It may not be, but the price could also be making a trend change or is too volatile for a clear direction to be present.

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print("eeeeeeeeeeeee")
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    #ws.send('{"type":"subscribe","symbol":"AAPL"}')
    #ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:ETHUSDT"}')
    #ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

def getLevels():
     r = requests.get('https://finnhub.io/api/v1/scan/support-resistance?symbol=BINANCE:BTCUSDT&resolution=D&token=bp9nhovrh5rf91tippdg')
     print(r.json())
     p = requests.get('https://finnhub.io/api/v1/scan/support-resistance?symbol=BINANCE:ETHUSDT&resolution=D&token=bp9nhovrh5rf91tippdg')
     print(p.json())
     s = requests.get('https://finnhub.io/api/v1/scan/support-resistance?symbol=CHK&resolution=D&token=bp9nhovrh5rf91tippdg')
     print(s.json())

def getPattern():
     t = requests.get('https://finnhub.io/api/v1/scan/pattern?symbol=BINANCE:ETHUSDT&resolution=D&token=bp9nhovrh5rf91tippdg')
     patternList = []
     i = 0
     bearCount = 0
     bullCount = 0
     if t.json() != "{}":
         print("not null")
     else:
         print("null")
     for attribute in t.json().items():
         print(attribute)
     count = len(attribute)
     print("countSize:", count)
     while i <= count:
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

def patternReadings(request):
     #list = request.json()
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
    while time() - start_time < max_runtime:
        # do some stuff
        if ws.keep_running == True:
            print("is on")
        else:
            print("isoff")
            thread = Thread(target=ws.run_forever)
            thread.start()
        print(time())
        if end_loop():
            print("end")
            break
    return ws
if __name__ == "__main__":
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
    loop=asyncio.get_event_loop().run_until_complete(timer(ws))
    loop.close()
    
    getLevels()
    getPattern()
    getAverage()

def hello():
     print ("hello world!")     

#determine price flucuations/direction of all cryptos to compare to the one.
