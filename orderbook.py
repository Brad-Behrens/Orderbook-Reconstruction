import websocket
import ssl
import json
import bisect

"""
Initialise ask and bid variables to reconstruct orderbook.
"""

bids = []
asks = []

class Bid:
    def __init__(self, price=None, quantity=None):
        self.price = price
        self.quantity = quantity

    def get_Bid_Price(self):
        return self.price
    
    def get_Bid_Quantity(self):
        return self.quantity

class Ask:
    def __init__(self, price=None, quantity=None):
        self.price = price
        self.quantity = quantity

    def get_Ask_Price(self):
        return self.price
    
    def get_Ask_Quantity(self):
        return self.quantity
    

def on_open(ws):
    print("Web Socket Connected...")

def on_message(ws, message):
    data = json.loads(message)
    order = data["events"]
    order_data = order[0]
    order_type = order_data['side']

    if(order_type == 'bid'):
        # Create Bid Object
        bid_price = order_data['price']
        bid_quantity = order_data['remaining']
        new_bid = Bid(bid_price, bid_quantity)

        # Append order to bid side of orderbook.
        global bids
        if len(bids) == 0:
            bids.append(new_bid)
        elif len(bids) <= 10:
            for i in range(len(bids)):
                if bids[i].get_Bid_Price() >= new_bid.get_Bid_Price():
                    del bids[-1]
                    index = i
                    break
            bids = bids[: i] + [new_bid] + bids[i :]   
    else:
        # Create Ask Object
        ask_price = order_data['price']
        ask_quantity = order_data['remaining']
        new_ask = Ask(ask_price, ask_quantity)

        # Append order to ask side of orderbook.
        global asks
        if len(asks) == 0:
            asks.append(new_ask)
        elif len(asks) <= 10:
            for i in range(len(asks)):
                if asks[i].get_Ask_Price() >= new_ask.get_Ask_Price():
                    del asks[-1]
                    index = 1
                    break
            asks = asks[: i] + [new_ask] + asks[i :]


    print(bids[0].get_Bid_Price() + ' ' + bids[0].get_Bid_Quantity() + ' - ' + asks[0].get_Ask_Price() + ' ' + asks[0].get_Ask_Quantity())

    
socket = "wss://api.gemini.com/v1/marketdata/btcusd?top_of_book=false&bids=true&offers=true"
ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
