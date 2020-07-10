import alpaca_trade_api as tradeapi
import pandas as pd

api = tradeapi.REST('PK5CXXXXX2JALX', 'irVkPYXXXXXXXXXXRxoT', base_url='https://paper-api.alpaca.markets', api_version='v2') # or use ENV Vars shown below
account = api.get_account()
print( account.status )

all_assets = api.list_assets()
df = pd.DataFrame( [ x._raw for x in all_assets ] )
print( df.tail() )

ticker = 'GOOG'
res = api.alpha_vantage.intraday_quotes(  symbol='GOOG' , interval='1min' , outputsize='full' , output_format='pandas' )
print( res )
print( 'wo' )
l=api.alpha_vantage.last_quote(  symbol='GOOG' , output_format='pandas' )

# GET MULTIPLE LOOKS LIKE
z=api.get_barset( ['GOOG','AAPL','SPX'] ,'minute' , limit='1' )

l=9
