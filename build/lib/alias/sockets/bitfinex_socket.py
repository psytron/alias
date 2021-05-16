import json

from websocket import create_connection

ws = create_connection("wss://api.bitfinex.com/ws/2")
#ws.connect("wss://api2.bitfinex.com:3000/ws")
ws.send(json.dumps({
    "event": "subscribe",
    "channel": "book",
    "symbol": "tBTCUSD",
}))


while True:
    result = ws.recv()
    result = json.loads(result)
    xxx = result
    print(xxx)
    #print(result[1])

ws.close()