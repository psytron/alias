

# protocol listener

# Mempool Size
# The aggregate size of transactions waiting to be confirmed.
from datetime import datetime
import requests
from bizutil import xtime, cass

blackout_period = 30
lightson_period = 30
step=0

def sync():
    if datetime.now().second > 30:
        res = requests.get("https://api.blockchain.info/ticker").json()
        series =  xtime.series_now()
        carrier = 'blockchaincom'
        for y in res:
            node = res[y]
            symbol = 'BTC/'+y
            cass.insert_entry(carrier, symbol, 'close', series, node['last'])
            #print( carrier,  symbol , 'close', series , node['last'] )
            #print( carrier,  symbol , 'bid' , series  , node['buy'] )
            #print( carrier,  symbol , 'ask' , series  , node['sell'] )
        symbol ='BTC/USD'
        res = requests.get("https://api.blockchain.info/stats").json()
        series =  datetime.now().replace(second=0, microsecond=0)
        vals = {}
        vals['minutes_between_blocks'] = res['minutes_between_blocks']
        vals['difficulty']=res['difficulty']
        vals['trade_volume_btc']=res['trade_volume_btc']
        vals['hash_rate']=res['hash_rate']

        #vals['close']=res['market_price_usd']
        #for x in vals:
        #    xclass = x
        #    cass.insert_entry(carrier, symbol, xclass, series, vals[x])
        cass.insert_collection( carrier , symbol , xtime.series_now(), vals )



def trans_status():

    tx = 'fe76fd52f1edeb711491fd21cabca68fdb1c72f97e7e00cefc765252e11aa224'
    #res = requests.get("https://blockchain.info/rawtx/$tx_hash")
    res = requests.get("https://blockchain.info/rawtx/"+tx).json()
    for x in res:
        print( x , res[x] )
    return res








def stats():
    response = requests.get("https://api.blockchain.info/stats")
    return response
