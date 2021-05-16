red='#00FFFF'
yellow='#0000FF'
lightred='#F0000F'
purple='#FF00FF'
teal='#FF330F'
gray='#888888'
diff='#dcf900'
orange='#383cb5'
diff1='#0095db'
color_map = {
    ('oanda', 'XAU/USD', 'close'):yellow,
    ('binance', 'BTC/USDT', 'close'):red,
    ('gdax',    'BTC/USD',  'close'):red,
    ('kraken',  'BTC/USD',  'close'):red,
    ('bittrex', 'BTC/USD', 'close'):red,
    ('blockchaincom', 'BTC/USD', 'close'):red,
    ('blockchaincom', 'BTC/USD', 'hash_rate'):teal,
    ('blockchaincom', 'BTC/USD', 'minutes_between_blocks'):purple,
    ('blockchaincom', 'BTC/USD', 'trade_volume_btc'):teal,
    ('blockchaincom', 'BTC/USD', 'difficulty'):red,
    ('etherchainorg', 'ETH/USD', 'difficulty'):red,
    ('bittrex',       'BTC/USD', 'bid_vol'):diff,
    ('gdax',          'BTC/USD', 'bid_vol'):diff,
    ('kraken',        'BTC/USD', 'bid_vol'):diff,
    ('gdax',          'ETH/USD', 'close'):diff1,
    ('bittrex',       'ETH/USD', 'close'):diff1,
    ('kraken',        'ETH/USD', 'close'):diff1,
    'outcome':red,
    'predict':'#00FF00'
}
line_map = {
    ('blockchaincom', 'BTC/USD', 'minutes_between_blocks'):'--',
    ('blockchaincom', 'BTC/USD', 'close'):'--',
    ('gdax',    'BTC/USD',  'close'):'-',
    ('blockchaincom', 'BTC/USD', 'difficulty'):'--',
    'outcome':'--'
}