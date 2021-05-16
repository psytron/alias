





from datetime import datetime
import requests
from bizutil import xtime, cass

blackout_period = 30
lightson_period = 30
step=0

def sync():
    if datetime.now().second > 30:
        res = requests.get("https://www.etherchain.org/api/basic_stats").json()
        #series =  datetime.now().replace(second=0, microsecond=0)
        series =  xtime.series_now()
        carrier = 'etherchainorg'
        symbol = 'ETH/USD'
        obj=res['currentStats']
        whitelist = {}
        whitelist['close']=obj['price_usd']
        whitelist['difficulty']=obj['difficulty']
        whitelist['block_time']=obj['block_time']
        whitelist['hashrate']=obj['hashrate']
        whitelist['tps']=obj['tps']
        whitelist['uncle_rate']=obj['uncle_rate']

        #for xclass in whitelist:
        #    cass.insert_entry(carrier, symbol, xclass, series, whitelist[xclass])

        cass.insert_collection( carrier , symbol , xtime.series_now() , whitelist )










def stats():
    response = requests.get("https://api.blockchain.info/stats")
    return response
