import websocket
import json
import time
from datetime import datetime

total_price = 0
total_volume = 0


def sort_message(message):
    for data in json.loads(message)['data']:
        # running vwap in background
        p = data['p']
        v = data['v']
        vwap(p, v)

        # printing the trades
        print(datetime.utcfromtimestamp(data['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
              "price:", data['p'],
              "volume:", data['v'])


def on_message(ws, message):
    # option to print all relevant trades
    sort_message(message)

    # option for VWAP
    for data in json.loads(message)['data']:
        # getting the last two characters of current time
        checker = datetime.utcfromtimestamp(data['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        checker1 = str(checker[-2:])

        # if the last two characters are 00 it means a minute has passed, so we run vwap_final()
        if int(checker1) == 00:
            vwap_final()


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')


def vwap(p, v):
    global total_price
    global total_volume

    total_price += p
    total_volume += v


def vwap_final():
    global total_price
    global total_volume

    print("VWAP is ", (total_price * total_volume) / total_volume)
    total_price = 0
    total_volume = 0


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c7skc72ad3i9jn7rfj1g",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.on_open = on_open
    ws.run_forever()






