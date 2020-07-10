# CARRIERS:
exchanges = ['binance','kraken','okex','bittrex','binanceus','bitstamp','coinbasepro','bitfinex','oanda']

carriers = ['oanda','bittrex','kraken','coinbasepro','binance']
us_carriers= ['bittrex','kraken']
china_carriers = ['binance']
fusioncohort_all= ['bitmex','binance','okex','huobipro','kraken', 'deribit','bittrex', 'hitbtc',
        'binanceus', 'coinex','poloniex','bitfinex','coinbasepro','bitstamp','bitflyer']
fusioncohort= [
               'binance',
               'binanceus',
               'bittrex',
               'bitmex',
               'bitstamp',
               'bitfinex',
               'bytetrade',
               'bitflyer',
               'coinbasepro',
               'coinex',
               'deribit',
               'ftx',
               'gemini',
               'hitbtc',
               'huobipro',
               'kucoin',
               'kraken',
               'lbank',
               'liquid',
               'okex',
               'poloniex'
               ]


# b = ['interactivebrokers']
# a = ['okex','binance','bitflyer','huobi','lbank','bitfinex','bithumb','hitbtc','bitz','gdax','bittrex','kraken']






white_list_per_domain={
    'binance':['BTC/USDT'],
    'binanceus':['BTC/USD','ETH/USD','LTC/USD'],
    'bittrex':['BTC/USD','ETH/USD'],
    'oanda':['SP500/USD']
}




# ASSETS:
stocks = []
indexes = [ 'SPX500/USD','NAS100/USD','CN50/USD']
metals = ['XPT/USD','XAU/USD','XAG/USD','XCU/USD','XPD/USD']
bonds = ['USB10Y/USD','USB02Y/USD','USB05Y/USD','USB30Y/USD']
oils = [ 'BCO/USD','WTICO/USD']
commodities = ['NATGAS/USD','SUGAR/USD','CORN/USD','WHEAT/USD']
forex = [ 'EUR/USD', 'AUD/USD','USD/CNH', 'USD/SGD','USD/JPY','USD/HKD','USD/SAR','USD/CAD','NZD/USD', 'GBP/USD']
bitcoins = ['BTC/USD', 'BTC/USDT','BTC/EUR']
ethereum = ['ETH/USD', 'ETH/USDT','ETH/BTC']
alts = ['USD/USDT','USDT/USD','LTC/USD', 'LTC/USDT','NEO/USD','NEO/USDT','XMR/USD','XMR/USDT' ,'XRP/USD','XRP/USDT',
        'XLM/USD', 'EOS/USD','NEO/USD','EOS/BTC',
       'BCH/USD','BCH/USDT' , 'XLM/USDT' ,'LTC/ETH']

#'BCHSV/USDT','BCHABC/USDT','BCHSV/BTC','BCHABC/BTC','BCH/USD',

quoted_in_eth= ['LTC/ETH','BSV/ETH']
cryptos = bitcoins + alts + ethereum
classics = indexes + stocks + bonds + commodities + forex + metals + oils
all = classics + cryptos


# CLASSES
base_classes = ['close','bid_vol','ask_vol']
synthetic_classes = ['bid_vol','ask_vol']

bitcoin_network =['minutes_between_blocks',
                  'difficulty',
                  'trade_volume_btc',
                  'hash_rate','market_price_usd']

ethereum_network=['difficulty','block_time','hashrate','tps','uncle_rate']


search__map={
    'btc':'BTC/USD',
    'oil':'WTICO/USD',
    'gold':'XAU/USD'
}


