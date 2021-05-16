
import base64
from ..util import symbols

# endpoint: https://paper-api.alpaca.markets

import alpaca_trade_api as tradeapi

#  https://paper-api.alpaca.markets

key_map = {
    'EUR/USD':'EUR_USD',
    'GBP/USD':'GBP_USD'
}





class alpaca():

    def __init__(self , *args, **kwargs):
        
        self.key = kwargs['apiKey']
        self.secret = kwargs['secret']
        # self.client = # meshcache()
        self.client = tradeapi.REST(kwargs['apiKey'], kwargs['secret'], base_url='https://paper-api.alpaca.markets', api_version='v2')
        self.instruments = self.fetchMarkets()


    def fetchTicker(self , *args , **kwargs ):
        #symbol = key_map[ args[0] ]
        print( ' fetchTicker not implemented yet for Alpaca ')
        return {'close':23 , 'open':23 , 'bid':234,'ask':20393 , 'vol':2343}


    def fetchTickers(self , *args , **kwargs):
        try:
            response = self.client.get_barset( ['GOOG','AAPL','TSLA','SBUX','NVDA','JPM','MSFT','PG'] ,'minute' , limit='1' )
            outhash ={}
            for sym in response:
                obj = response[sym]
                dom = self.instruments.loc[ self.instruments['symbol'] == sym ].get('exchange').iloc[0]
                outhash[ sym+'/USD']={ 'domain':dom.lower(), 'symbol':sym+'/USD' ,  'vals':{ 'close':obj[0].c , 'vol':obj[0].v } }
        except Exception as e:
            print( e )
            print(' ')
        return outhash

        #{ x.instrument:{ 'ask':x.closeoutAsk , 'bid':x.closeoutBid , 'close':x.closeoutAsk } for x in prices }
        #return val_obj


    def describe(self):
        return {'alpaca':'base'}


    def load_markets(self):
        pass
        #print(' load markets in oanda')


    def fetchMarkets(self):
        import pandas as pd
        response = self.client.list_assets()
        df = pd.DataFrame( [ x._raw for x in response ] )
        return df

    def fetch_balance(self, params={}):
        return True
    def fetchBalance(self, params={}):
        return {}

    def parse_trade(self, trade, market=None):
        return True

    def fetch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        return True
    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        return True

    def parse_order(self, order, market=None):
        return True

    def fetch_order(self, id, symbol=None, params={}):
        return True

    def fetch_orders(self, symbol=None, since=None, limit=None, params={}):
        return True

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        return True

    def fetch_closed_orders(self, symbol=None, since=None, limit=None, params={}):
        return True

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        return True

    def cancel_order(self, id, symbol=None, params={}):
        return True
    def fee_to_precision(self, currency, fee):
        return True
    def calculate_fee(self, symbol, type, side, amount, price, takerOrMaker='taker', params={}):
        return True
    def get_payment_methods(self):
        return True
    def deposit(self, currency, amount, address, params={}):
        return True
    def withdraw(self, currency, amount, address, tag=None, params={}):
        return True

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        return True

    def handle_errors(self, code, reason, url, method, headers, body):
        return True

    def request(self, path, api='public', method='GET', params={}, headers=None, body=None):
        return True