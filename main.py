import websocket
import json
from datetime import datetime
import time
import threading


def sort_message(message):
    for data in json.loads(message)['data']:
        print(datetime.utcfromtimestamp(data['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
              "price:", data['p'],
              "volume:", data['v'])


def on_message(ws, message):
    sort_message(message)

    # if we want to see the VWAP price:
    vwap(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')


def vwap(message):
    for data in json.loads(message)['data']:
        p = data['p']
        v = data['v']
        print("VWAP is: " + str((p * v) / v))


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c7skc72ad3i9jn7rfj1g",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


