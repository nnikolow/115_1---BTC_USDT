import websocket
import json
from datetime import datetime


def sort_message(message):
    for data in json.loads(message)['data']:
        print(datetime.utcfromtimestamp(data['t'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
              "price:", data['p'],
              "volume:", data['v'])


def on_message(ws, message):
    # option to print all relevant trades
    # sort_message(message)

    # option for VWAP
    for data in json.loads(message)['data']:
        p = data['p']
        v = data['v']
        vwap(p, v)


total_price = 0
total_volume = 0
message_counter = 0


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')


def vwap(p, v):
    global total_price
    global total_volume
    global message_counter

    total_price += p
    total_volume += v
    message_counter += 1

    if message_counter == 10:
        vwap_final()
        total_price = 0
        total_volume = 0
        message_counter = 0


def vwap_final():
    global total_price
    global total_volume

    print("VWAP is ", (total_price * total_volume) / total_volume)


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=c7skc72ad3i9jn7rfj1g",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.on_open = on_open
    ws.run_forever()






