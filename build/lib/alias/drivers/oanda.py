# -*- coding: utf-8 -*-




import base64
import hashlib
import json
import v20
from ..util import symbols


# Emdaxgmx:


key_map = {
    'EUR/USD':'EUR_USD',
    'GBP/USD':'GBP_USD'
}

# NEW
OANDA_URL = 'api-fxpractice.oanda.com'



# test debug ::
# v20.Context('api-fxpractice.oanda.com',443,True,token='8f416612e530a12d0d6257cf97519622-75d4727e0b4c985bf23ad57b4a087710').pricing.get('101-004-8599845-001',instruments= 'XAU/USD' ,includeUnitsAvailable=False)


# response = v20.Context('api-fxpractice.oanda.com',443,True,token='8f416612e530a12d0d6257cf97519622-75d4727e0b4c985bf23ad57b4a087710').pricing.get( '101-004-8599845-001' ,instruments=",".join(['XAU/USD','XAG/USD']),includeUnitsAvailable=False)


import requests
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    print(' Attribute Error in OANDA Driver, OpenSSL URLLIb3')
    pass


# WORKS WORKS WORKS ON SERVER WITH ABOVE:
# api = v20.Context('api-fxpractice.oanda.com', token=OANDA_NEW_TOKEN )
# res = api.pricing.get( '101-001-6394817-001', instruments=",".join( ['XAU/USD','XAG/USD'] ),includeUnitsAvailable=False )


#print( 'big res: ')
#print( res )
#print( res.raw_body )
#v20.Context('api-fxpractice.oanda.com', token='9a5b803cfc0612a8b5f01015b1316e14-b098c4c29510c5abe14dd8d380321735' ).pricing.get( '101-001-6394817-001', instruments=",".join( ['XAU/USD','XAG/USD'] ),includeUnitsAvailable=False )
#res = api.pricing.get( '101-001-6394817-001', instruments=",".join( ['XAU/USD','XAG/USD'] ),includeUnitsAvailable=False )
#print( res.body_raw )
#response = v20.Context('api-fxpractice.oanda.com',443,True,token='9a5b803cfc0612a8b5f01015b1316e14-b098c4c29510c5abe14dd8d380321735').pricing.get( '101-004-8599845-001' ,instruments=",".join(['XAU/USD','XAG/USD']),includeUnitsAvailable=False)

has = {'somemethod':True }

class oanda():


    def __init__(self , *args, **kwargs):
        # self.client = # meshcache()
        self.key = kwargs['OANDA_TOKEN']
        self.account_id = kwargs['OANDA_ACCOUNTID']
        self.client = v20.Context(
            OANDA_URL,
            '443',
            token= self.key )
        #self.markets = self.loadMarkets()



    def fetchMarkets(self , *args , **kwargs ):
        s = 0
        syms = json.loads( self.client.account.instruments( self.account_id ).raw_body )['instruments']
        market_list = {
            x['displayName']:{
                'symbol':x['displayName'],
                'type':x['type'],
                'base':  x['displayName'].split('/', 1)[0],
                'quote': x['displayName'].split('/', 1)[1],
                'raw':x }
            for x in syms }
        return market_list



    def fetchTickers(self , *args , **kwargs):
        syms_list = symbols.oils + symbols.bonds + symbols.metals + symbols.commodities + symbols.indexes + symbols.forex
        syms = ','.join( syms_list )
        try:
            response = self.client.pricing.get(
                self.account_id,
                instruments= syms ,
                includeUnitsAvailable=False)
            #print( response )
        except Exception as e:
            print( e )
            print(' ')
        prices = response.body['prices']
        val_obj = { x.instrument:{ 'ask':x.closeoutAsk , 'bid':x.closeoutBid , 'close':x.closeoutAsk } for x in prices }
        return val_obj


    def fetchTicker(self , *args , **kwargs ):
        #symbol = key_map[ args[0] ]
        symbol = args[0]
        print(' Getting : ', self.account_id,' : ', symbol)
        try:
            print( 'Actual Response: ')
            response = self.client.pricing.get(
                self.account_id,
                instruments= symbol ,
                includeUnitsAvailable=False)
            print( 'Actual Response: ')
            print( response )
        except Exception as e:
            print( e )
            print(' ')
        #print( 'Post Actual Response: ')

        #res_json = json.loads(response.raw_body)
        #res = float(res_json['prices'][0]['closeoutBid'])
        #return res
        res_json = json.loads(response.raw_body)
        print(' Parsed Response: ')
        print( res_json )
        res = {}
        #res['bid'] = float(res_json['prices'][0]['bids'][0]['price'])
        #res['ask'] = float(res_json['prices'][0]['asks'][0]['price'])
        #res['vol'] = 0.0
        #res['baseVolume'] = 0.0
        #res['askVolume'] = 0.0

        res['bid'] = response.body['prices'][0].closeoutBid
        res['ask'] = response.body['prices'][0].closeoutAsk
        res['open'] = response.body['prices'][0].closeoutBid
        res['close'] = response.body['prices'][0].closeoutBid
        res['high'] = response.body['prices'][0].closeoutAsk
        res['low'] = response.body['prices'][0].closeoutBid
        res['symbol'] = symbol
        res['domain']='oanda'
        return res




    def describe(self):
        return {'oanda':'base'}


    def load_markets(self):
        pass
        #print(' load markets in oanda')


    def loadMarkets(self):
        #active_symbols = symbols.forex + symbols.commodities + symbols.bonds + symbols.stocks
        response = self.client.account.instruments(self.account_id)
        syms = symbols.commodities + symbols.bonds + symbols.forex + symbols.indexes + symbols.stocks + symbols.metals + symbols.oils
        market_list = { x:{'symbol':x,'base':  x.split('/', 1)[0],'quote': x.split('/', 1)[1] } for x in syms }
        return market_list

    def fetchMarkets(self):
        #active_symbols = symbols.forex + symbols.commodities + symbols.bonds + symbols.stocks

        response = self.client.account.instruments(self.account_id)
        p = 3
        syms = symbols.commodities + symbols.bonds + symbols.forex + symbols.indexes + symbols.stocks + symbols.metals + symbols.oils
        market_list = [ {'symbol':x,
                         'base':  x.split('/', 1)[0] ,
                         'quote': x.split('/', 1)[1] } for x in syms ]
        return market_list

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