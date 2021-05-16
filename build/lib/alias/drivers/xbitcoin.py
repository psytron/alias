

# protocol listener

# Mempool Size
# The aggregate size of transactions waiting to be confirmed.
from datetime import datetime
import requests
from bizutil import cass


def sync():
    res = requests.get("https://api.blockchain.info/stats").json()

    series =  datetime.now().replace(second=0, microsecond=0)
    vals = {}
    vals['minutes_between_blocks'] = res['minutes_between_blocks']
    vals['difficulty']=res['difficulty']
    vals['trade_volume_btc']=res['trade_volume_btc']
    vals['hash_rate']=res['hash_rate']
    vals['close']=res['market_price_usd']
    carrier='bitcoin'
    symbol ='network'
    for x in vals:
        xclass = x
        cass.insert_entry(carrier, symbol, xclass, series, vals[x])













def stats():
    response = requests.get("https://api.blockchain.info/stats")
    return response
