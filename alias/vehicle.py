#from mesh.models.sample import Sample
#from bizutil import neo #, dbutil
import pandas as pd
import time
#from tradespace import rdd
from .drivers import cache as drivercache
#from bizutil import hashtricks as ht
from .util import xtime
from .util.format import block
from .util.format import block_right
from datetime import datetime



class Vehicle:
    def __init__(self , *args , **kwargs ):
        self.alias = kwargs.get('alias', 'default')
        self.domain = kwargs['domain']
        self.carrier = kwargs['domain']
        self.symbol = kwargs['symbol']
        self.logic = kwargs.get('driver')
        if '/' in kwargs['symbol']:
            self.base = kwargs['base'] if 'base' in kwargs else kwargs['symbol'].split('/')[0]
            self.quote = kwargs['quote'] if 'quote' in kwargs else kwargs['symbol'].split('/')[1]
        self.deposit_info = None
        self.prev_asks = False
        self.prev_bids = False
        self.storage = kwargs.get('storage',False)

        #self.last_vol = { 'timestamp':datetime.utcnow() , 'val':0 }
    def stat(self):
        print('                        ')
        print('           Vehicle      ')
        print('    Alias: '+self.alias  )
        print('   Domain: '+self.domain )
        print('   SYMBOL: '+self.symbol )
        print('                        ')

    def dbref(self , *args , **kwargs):
        #inst = neo.power_merge( "Vehicle" , {'domain':self.domain , 'base':self.base , 'quote':self.quote  } )
        #return inst
        print(' temp deactivated ')

    def market(self):
        try:
            return self.logic.market( self.symbol )
        except Exception as e:
            print( e )
            self.logic.load_markets()
            return self.logic.market( self.symbol )

    def insert_entry(self , *args , **kwargs):
        #.insert_entry( vals['domain'], vals['symbol'], 'close', series, vals['close'])
        #insert_dom_sub_cla_val( 'binanc_rmgold' , 'BTC/USD' , 'close' , 7321 )
        #insert( dom, sub, xcl, val )   # last arg is always value
        #insert( dom , val ) # defaults all other subnamspaces
        # read( ['dom'] ,['sub'], ['xclass'] )   # This will also Defer background process to WRITE Nodes to graph if they don't exist 1
        # write( dom, sub, xcl, val ) # series internal stamp
        # cas.write( x , y , z , val )
        # IF STORAGE IS ASSIGNED ELSE JUST PRINT 
        if self.storage: 
            self.storage.insert_entry( *args )
        else:
            print( *args )

    def sync( self ,*args , **kwargs):
        try:
            vals = self.logic.fetchTicker( self.symbol )
            vals['series']= xtime.series_now()
            vals['domain']=self.domain
            series = xtime.series_now()              #samp = Sample( **vals) #samp.sync() # Struct for Cython

            self.insert_entry( vals['domain'], vals['symbol'], 'close', series, vals['close'])
            self.insert_entry( vals['domain'], vals['symbol'], 'high', series, vals['high'])
            self.insert_entry( vals['domain'], vals['symbol'], 'low', series, vals['low'])
            self.insert_entry( vals['domain'], vals['symbol'], 'bid', series, vals['bid'])
            self.insert_entry( vals['domain'], vals['symbol'], 'ask', series, vals['ask'])

            if vals.get('baseVolume') or False :
                self.insert_entry( vals['domain'], vals['symbol'], 'bvol', series, vals['baseVolume'])
            if vals.get('quoteVolume') or False :
                self.insert_entry( vals['domain'], vals['symbol'], 'qvol', series, vals['quoteVolume'])
            if vals.get('open') or False :
                self.insert_entry( vals['domain'], vals['symbol'], 'open', series, vals['open'])
            return vals
        
        except Exception as e:
            print( "Vehicle Sync Exception: ",self.domain,' ',self.symbol,' \n Error:', e )
            try:
                print(vals)
            except Exception as e2:
                print('Exception printing vals ',e2)

    def patch( self , *args ,**kwargs ):
        h_sym = self.symbol
        h_dom = self.domain
        cur_date = datetime.utcnow()
        cur_timestamp = datetime.utcnow().timestamp()
        cur_date_from_ts = datetime.fromtimestamp( cur_timestamp )
        df = rdd.segment( [self.domain],[self.symbol],['vol'],16480,16482)
        df = df.resample('1Min').last()
        df.index.rename('timecoord', inplace=True)

        resx  = self.logic.fetch_ohlcv(self.symbol, '1m')
        resx_by_time = { str( datetime.utcfromtimestamp(x[0]/1000)):x for x in resx }
        df_nans = df[df.isna().any(axis=1)]

        for index, row in df_nans.iterrows():
            if str( index ) in resx_by_time:
                x1obj = resx_by_time[ str(index) ]
                h_date = index.to_datetime64()
                self.insert_entry( h_dom , h_sym , 'open_h' , h_date , x1obj[1]  )
                self.insert_entry( h_dom , h_sym , 'high_h' , h_date , x1obj[2]  )
                self.insert_entry( h_dom , h_sym , 'low_h' ,  h_date , x1obj[3]  )
                self.insert_entry( h_dom , h_sym , 'close_h', h_date , x1obj[4]  )
                self.insert_entry( h_dom , h_sym , 'vol' ,  h_date , x1obj[5]  )

    def synco( self , *args ,**kwargs ):
        h_sym = self.symbol
        h_dom = self.domain

        try:
            if( self.logic.has['fetchOHLCV'] ):
                resx  = self.logic.fetch_ohlcv(self.symbol, '1m')
        except Exception as e:
            return False

        insert_count=0
        for rec in reversed(resx):
            h_date=datetime.fromtimestamp( rec[0]/1000 )
            self.insert_entry( h_dom , h_sym , 'open_h' , h_date , rec[1]  )
            self.insert_entry( h_dom , h_sym , 'high_h' , h_date , rec[2]  )
            self.insert_entry( h_dom , h_sym , 'low_h' ,  h_date , rec[3]  )
            self.insert_entry( h_dom , h_sym , 'close_h', h_date , rec[4]  )
            self.insert_entry( h_dom , h_sym , 'vol' ,  h_date , rec[5]  )
            insert_count+=1
            if insert_count > 3:
                break
        return resx

    def impute_derivatives(self , *args, **kwargs ):
        #if('close' in args[0] ):
        #    vals = args[0]
        #    neo.power_upsert('Vehicle', {'domain':self.domain,'symbol':self.symbol} , {'close':vals['close'] })
        pass

    def samplesx(self,*args, **kwargs):
        #from models import Sample
        #session = dbutil.get_store()
        #rows = session.execute("""SELECT * FROM sample WHERE domain=%s AND symbol=%s""" , ( self.domain , self.symbol ) )
        #return rows
        print(' no longer implemented ')

    def ops(self):
        # CONVERSIONS
        # read fees if have private API
        if self.logic.has['privateAPI']:
            fees = self.logic.fees
            #print( fees )
        convertibles = [x['quote'] for x in self.logic.fetchMarkets() if x['base'] == 'LTC' ]
        return convertibles
        # TRANSFERS


    ##################### TRANSFER OPTIONS 
    def trades(self):
        trades_arr = self.logic.fetchMyTrades( self.symbol )
        #for t in trades_arr:
        #    print( block(t['datetime'],19) ,block(t['symbol'],8), block(t['price'],14) ,  block_right(t['side'],4),block(t['amount'],9),block(t['cost'],9) )
        return trades_arr
    
    def lt(self):
        trades_arr = self.trades()
        trades_arr = trades_arr[-9:]
        for t in trades_arr:
            print( block(t['datetime'],19) ,block(t['symbol'],8), block(t['price'],14) ,  block_right(t['side'],4),block(t['amount'],9),block(t['cost'],9) )
    
    def tradebook(self):
        dom = self.domain
        mtrades = self.logic.fetchTrades( self.symbol ,since=self.logic.milliseconds()-120000 )
        #lastfew = mtrades[-50:]
        if self.domain == 'bitmex' and self.symbol=='BTC/USD':
            l=3
        if self.domain == 'bittrex' and self.symbol=='BTC/USD':
            l=3
        #for t in lastfew:
        #    print( block( t['datetime'])+' '+ block(t['side'],4) +'  '+block( str( t['amount'] ),8)+' @ '+block( ' $'+str( t['price'] ))  )
        return mtrades

    def roi(self):
        print(' ROI')
        #cached_tradebook =
        #cached_orderbook =
        trades_arr = self.trades()  # this should cache in DB later , ObVec should be TIGHT!
        df = pd.DataFrame( trades_arr )

        df_simp = df.drop(['timestamp','info','fee'],axis=1).tail(10)

        last_trade = trades_arr[-1]
        ob_meta = self.mineOrderbook()
        obj_out={}
        obj_out['domain']=self.domain
        obj_out['symbol']=self.symbol
        obj_out['roi'] =  ob_meta['vals']['bid'] - last_trade['price']
        obj_out['last_date']=last_trade['datetime']
        obj_out['curr_date']=str( datetime.now() )
        obj_out['last_price']=last_trade['price']
        obj_out['last_action']=last_trade['side']
        obj_out['curr_price']=ob_meta['vals']['bid']
        return obj_out
        # Method checks last transaction, current price on exchange
        # subtracts it and subtracts its own fee.
        # SHOWS  ENTRY PRICE / DATE
        # change since entry
        # current ROI  /  lyft

    ##################################### MINING AGGREGATES 
    def mineTradebook(self):
        try:
            mtrades = self.logic.fetchTrades( self.symbol ,since=self.logic.milliseconds()-60000 )
        except Exception as e:
            print('Exception in Vehicle ',self.domain, self.symbol)
            print( e )
            return False

        if self.domain == 'bitmex':
            for t in mtrades:
                tcos = t['amount']
                tvol = t['amount'] / t['price']
                t['amount']=tvol
                t['cost']=tcos

        if self.domain == 'deribit':
            for t in mtrades:
                tcos = t['amount']
                tvol = t['amount'] / t['price']
                t['amount']=tvol
                t['cost']=tcos

        vals = {}
        base_frame = pd.DataFrame(
            {"datetime": ['2020','2020'],
             "type": ['market','limit']  ,
             'side':['buy','sell'] ,
             'amount':[0.0,0.0] ,
             'price':[0.0,0.0]})

        df = pd.DataFrame( mtrades )
        #tf = trade_frame
        #df = pd.merge(base_frame, trade_frame , on = ['datetime','type','side','amount','price'], how = 'inner')

        if df.shape[0] == 0:
            vals['buy_vol']=0
            vals['sell_vol']=0
            vals['total_vol']=0
            vals['buy_count']=0
            vals['sell_count']=0
            vals['order_slope']=0
        else:
            g = df.groupby('side')
            g_sum=g['amount'].sum()
            vals['buy_vol']=g_sum['buy'] if 'buy' in g_sum else 0
            vals['sell_vol']=g_sum['sell'] if 'sell' in g_sum else 0
            vals['total_vol']=df['amount'].sum()
            g_count = g['datetime'].count()
            vals['buy_count']=g_count['buy'] if 'buy' in g_count else 0
            vals['sell_count']=g_count['sell'] if 'sell' in g_count else 0
            vals['order_slope']=0 if df.shape[0] < 2 else df['price'].iloc[-1] - df['price'].iloc[0]
            if df.shape[0]>0: # ONLY ADD CLOSE PRICE IF AVAILABLE otherwise system will ffill()
                vals['close_price']=df['price'].iloc[0]

        obj_out={}
        obj_out['df']=df
        obj_out['vals']=vals
        obj_out['raw']=mtrades
        obj_out['domain']=self.domain
        obj_out['symbol']=self.symbol
        return obj_out

    def mineOrderbook(self):
        start_time = time.time()
        try:
            obj= self.logic.fetchOrderBook( self.symbol )
            if( type(obj ) == str ):
                print( ' Type returned seems like error: ',obj , '  domain: ',self.domain )
        except Exception as e:
            print('Exception in Vehicle ')
            print( e )
            return False

        if( self.domain == "kraken"):
            obj['asks'] = [ x[0:2] for x in obj['asks'] ]
            obj['bids'] = [ x[0:2] for x in obj['bids'] ]


        df_asks = pd.DataFrame( obj['asks'][:20], columns=['price','quant'] )
        df_bids = pd.DataFrame( obj['bids'][:20], columns=['price','quant'] )
        top_bids = df_bids.head( 15 )
        top_asks = df_asks.head( 15 )

        if self.domain =='bitmex':
            df_asks['quant']=(df_asks['quant']/df_asks['price'])/20
            df_bids['quant']=(df_bids['quant']/df_bids['price'])/20

        if self.domain=='deribit':
            df_asks['quant']=(df_asks['quant']/df_asks['price'])
            df_bids['quant']=(df_bids['quant']/df_bids['price'])

        if self.domain=='ftx':
            df_asks['quant']=df_asks['quant']/10
            df_bids['quant']=df_bids['quant']/10


        df_bids['pdiff']=df_bids['price'].diff(1).shift(-1)
        df_asks['pdiff']=df_asks['price'].diff(1).shift(-1)

        df_bids['stx']=df_bids['pdiff'].expanding().std()
        df_asks['stx']=df_asks['pdiff'].expanding().std()

        df_bids['price_range']=df_bids['pdiff'].expanding().sum()
        df_asks['price_range']=df_asks['pdiff'].expanding().sum()
        df_bids['quant_range']=df_bids['quant'].expanding().sum()
        df_asks['quant_range']=df_asks['quant'].expanding().sum()


        #print( self.domain )
        #print( df_asks.head(10) )
        #print( df_bids.head(10) )
        #print('\n\n\n')

        meta_obj = {}
        #meta_obj['domain']=self.domain
        #meta_obj['symbol']=self.symbol

        meta_obj['ask_stx10']=df_asks['stx'][9]
        meta_obj['bid_stx10']=df_bids['stx'][9]

        meta_obj['bid_price_range10']=df_bids['price_range'][10]*-1
        meta_obj['ask_price_range10']=df_asks['price_range'][10]
        meta_obj['bid_price_range20']=df_bids['price_range'][19]*-1
        meta_obj['ask_price_range20']=df_asks['price_range'][19]

        meta_obj['bid_quant_range10']=df_bids['quant_range'][10]
        meta_obj['ask_quant_range10']=df_asks['quant_range'][10]
        meta_obj['bid_quant_range20']=df_bids['quant_range'][19]
        meta_obj['ask_quant_range20']=df_asks['quant_range'][19]
        #meta_obj['asks_stx24']=df_asks['stx'][19]


        meta_obj['ob_pingtime']=time.time()-start_time
        meta_obj['spread']=df_asks['price'].min()-df_bids['price'].max()

        meta_obj['ask']=df_asks.iloc[0,0]
        meta_obj['bid']=df_bids.iloc[0,0]
        meta_obj['close']=meta_obj['bid']+( (meta_obj['ask']-meta_obj['bid'])/2 )
        meta_obj['bid_vol']=df_bids['quant'].sum()
        meta_obj['ask_vol']=df_asks['quant'].sum()
        meta_obj['bid_depth']=df_bids['price'].max() - df_bids['price'].min()
        meta_obj['ask_depth']=df_asks['price'].max() - df_asks['price'].min()
        #meta_obj['ob_bid_price_deviation']=df_bids.iloc[:,0].std()
        #meta_obj['ob_bid_quant_deviation']=df_bids.iloc[:,1].std()
        #meta_obj['ob_ask_price_deviation']=df_asks.iloc[:,0].std()
        #meta_obj['ob_ask_quant_deviation']=df_asks.iloc[:,1].std()

        #meta_obj['ob_t15_bid_vol']=top_bids[1].sum()
        ##meta_obj['ob_t15_ask_vol']=top_asks[1].sum()
        #meta_obj['ob_t15_bid_range']=top_bids[0].max() - top_bids[0].min()
        #meta_obj['ob_t15_ask_range']=top_asks[0].max() - top_asks[0].min()

        # GET  standard deviation or VOlatility for last minute
        # GET volatility last 10 minutes
        # GET  dispersion per all subs , fusion
        # GET Volatility Per this Vehicle and get NET dispersion / Volatility
        # GET liquidity_depth
        # GET mid-point of spread to replace close -->  ob_top((ob_top -ob_bottom)/2)
        # 'ob_new_ basically , graph if ob is leaning towards buyers or sellers market
        # 'ob_topvol_fresh_bids'
        # 'ob_topvol_fresh_asks'
        # 'ob_big_vol_10_fresh_asks'
        # TO JSON IN  # doesn't work cause andra type field
        #meta_obj['ob_bids_json']=df_bids.to_json(orient='records')
        #meta_obj['ob_asks_json']=df_asks.to_json(orient='records')
        #df =  self.p
        # df.append(  orderbook_raw )

        # fresh_ask_vol

        # fresh_bid_vol
        # ( get volume of only the fresh bids and asks :)


        if( self.prev_bids is not False ):
            set_diff_df = pd.concat([df_bids[['price','quant']], self.prev_bids]).drop_duplicates(keep=False)
            meta_obj['fresh_bids']= set_diff_df.shape[0]
        else:
            meta_obj['fresh_bids']=0
        self.prev_bids = df_bids[['price','quant']]

        if( self.prev_asks is not False ):
            set_diff_df = pd.concat([df_asks[['price','quant']], self.prev_asks]).drop_duplicates(keep=False)
            meta_obj['fresh_asks']= set_diff_df.shape[0]
        else:
            meta_obj['fresh_asks']=0
        self.prev_asks = df_asks[['price','quant']]

        obj['domain']=self.domain
        obj['symbol']=self.symbol
        obj['meta']=meta_obj
        obj['vals']=meta_obj
        return obj

    
    ##################################### COMMAND SHORTCUTS 
    def mt(self):
        atrades = self.logic.fetchTrades( self.symbol )
        for t in atrades:
            print( block(t['datetime'],19) ,block(t['side'],8), block(t['price'],14) ,  block_right(t['amount'],4) )
    def orders(self):
        return self.logic.fetch_open_orders( self.symbol )
    def cancel_order(self , id_in ):
        res = self.logic.cancelOrder( id_in , self.symbol )
        print( res )
        return res
    def cancel_orders(self):
        # finds and cancels all on vehicle
        for o in self.orders():
            self.cancel_order( o['id'] )

    def concentrate(self):
        # This aggregates all balances from other coins onto this
        print('concentrate')

    def balances(self):
        all_balances = self.logic.fetchBalance()
        free = all_balances['free']
        for b in free:
            if free[b]>0:
                print( block( b ,4 ) , block( free[b] ,10 )  )
        f = { x:free[x] for x in free if free[x]>0 }
        return f
    def base_balance(self):
        all_balances = self.logic.fetchBalance()
        currency_obj = all_balances[ self.base ] if self.base in all_balances else {}
        balance = currency_obj['total'] if 'total' in currency_obj else 0.0
        return balance
    def quote_balance(self):
        all_balances = self.logic.fetchBalance()
        currency_obj = all_balances[ self.quote ] if self.quote in all_balances else {}
        balance = currency_obj['total'] if 'total' in currency_obj else 0.0
        return balance
    def max_entry(self):
        fee_percent = self.market()['maker']
        avail_bal = self.qbal()
        price = self.fastBuyPricePerAvailQuote( avail_bal )
        target_amount_pre_fees = avail_bal / price # Calc avail purch power
        target_amount = target_amount_pre_fees - ( target_amount_pre_fees * fee_percent )
        obj={ 'amount':round(target_amount,8),
              'price':price,
              'qbal':avail_bal}
        return obj
        #market_values = self.market()
        #prec_amount = market_values['precision']['amount']
        #prec_price = market_values['precision']['price']
        #min_trans = market_values['limits']['amount']['min']
    def usd_val(self):
        return self.max_entry()['price']* self.balance()    
    
    # aliases
    bal = base_balance
    bbal = base_balance
    qbal = quote_balance
    balance = base_balance
    usdval=usd_val

    def fastBuyPricePerAvailQuote(self,bal_in):
        ob = self.orderbook()
        asks = ob['asks']
        q_avail=bal_in
        price=0
        for nx, a in asks.iterrows():
            ask_price=a[0]
            ask_avail=a[1]
            cost_to_fill_segment = ask_avail * ask_price
            q_avail -= cost_to_fill_segment
            if q_avail <= 0:
                price=ask_price
                break;
            else:
                continue
        return price
    def allocation_status(self):
        # return status of allocation
        # allocation status
        # if  balance is available
        # if  orders are pending , if price of  order is still matched to desirable / target
        print(' order status')

    ##################################### ENTER / EXIT 
    def enter( self , amount=False ):
        self.lo()
        domain_alias = self.domain+'_'+self.alias
        # PREPARE
        # DURING THE ORDER it SHOULD STAMP SAVE TO DB all the Parameters being used to calculate the deal
        # SAVE / SYNC orderbook + Tradebook AND
        buy_obj = self.max_entry()
        qbal = buy_obj['qbal']
        if amount:
            target_amount= amount
            target_price = self.fastBuyPrice( target_amount )
        else:
            target_price  = buy_obj['price']
            target_amount = buy_obj['amount']  # Fees included ( rounded )

        if float( qbal ) <= 0.5:
            print('Already Entered:  ',self.domain, self.symbol)
            return False
        fee_percent = self.market()['maker']
        amount_cost = target_amount * target_price
        fee_cost = amount_cost * fee_percent
        expected_cost = amount_cost + fee_cost

        amount_minus_fee = target_amount - ( target_amount * fee_percent )
        print('      Buy Order: ', self.symbol   ,'\n'
              '  Target Amount: ', target_amount ,'\n'
              '   Target Price: ', target_price  ,'\n'
              '          Fee %: ', fee_percent   ,'%\n'
              '       Fee Cost: ', fee_cost      ,'\n'
              '    Amount Cost: ', amount_cost   ,'\n'
              '     Amount-Fee: ', amount_minus_fee,'\n'
              'Expected T Cost: ', expected_cost ,'\n')

        #  createMarketBuyOrderRequiresPrice  for exchanges that need to create buy order based on quote currency
        # 'GTC' = Good To Cancel(default),
        # 'IOC' = Immediate Or Cancel

        # PLACE ORDER
        self.logic.verbose=True
        series = xtime.series_now()
        self.insert_entry( domain_alias , self.symbol , 'order_attempt',   series, 1 )
        res = self.logic.create_order( self.symbol , 'limit' , 'buy' , amount_minus_fee , target_price , {'timeInForce':'IOC'} )

        #if self.logic.has['createMarketOrder']:
        #    pass
            # market
            #res = self.logic.create_order( self.symbol , 'market' , 'buy' , target_amount  , {'trading_agreement':'agree' } )
        #else:
        #    res = self.logic.create_order( self.symbol , 'limit' , 'buy' , target_amount , target_price , {'trading_agreement':'agree'} )
        #tele.send(' ETR'+str(target_amount)+"@"+str(target_price) )
        self.logic.verbose=False

        # RECORD ORDER
        if res['status']=='closed':
            self.insert_entry( domain_alias , self.symbol , 'order_side',   series, 1 )
            self.insert_entry( domain_alias , self.symbol , 'order_target', series, target_price )
            self.insert_entry( domain_alias , self.symbol , 'order_price',  series, res['price'] )
            self.insert_entry( domain_alias , self.symbol , 'order_quant',  series, res['amount'] )
        else:
            self.insert_entry( domain_alias , self.symbol , 'order_side', series, 1 )
            self.insert_entry( domain_alias , self.symbol , 'order_target', series, target_price )
        return res
    def exit(self , amount=False ):
        domain_alias = self.domain+'_'+self.alias
        # PREPARE
        base_bal=self.base_balance()
        if amount:
            target_amount = amount
        else:
            target_amount = base_bal
        if( float(target_amount) <= 0.0001):
            print('Already exited:  ',self.domain,':',self.symbol)
            #raise Exception('Zero Ammount Cannot Load')
            return False
        price = self.fastSellPrice( base_bal )
        target_price = price
        fee = self.market()['maker']
        expected_fee = ( target_amount * fee )
        expected_p = ( target_amount * price )
        print('     Sell Order: ', self.symbol   ,'\n'
              '         Amount: ', target_amount ,'\n'
              '   Target Price: ', target_price  ,'\n'
              '            Fee: ', fee           ,'% \n'
              '   Expected_fee: ', expected_fee  ,'\n'
              ' Expect_proceed: ', expected_p    ,'\n'
              '       Base Bal: ', base_bal,'',self.quote )

        # PLACE ORDER
        self.logic.verbose=True
        series = xtime.series_now()
        self.insert_entry( domain_alias , self.symbol , 'order_attempt',   series, -1 )
        res = self.logic.create_order( self.symbol , 'limit' , 'sell' , target_amount , target_price , {'timeInForce':'IOC'} )
        #res = self.logic.create_order( self.symbol , 'limit' , 'buy' , target_amount , target_price , {'timeInForce':'IOC'} )
        #if self.logic.has['createMarketOrder']:
        #    res = self.logic.createOrder( self.symbol , 'market' , 'sell' , target_amount , {'trading_agreement':'agree'} )
        #else:
        #    res = self.logic.create_order( self.symbol , 'limit' , 'sell' , target_amount , target_price , {'trading_agreement':'agree'} )
        #tele.send(' EXT'+str(target_amount)+"@"+str(target_price) )
        self.logic.verbose=False

        # RECORD ORDER
        if res['status']=='closed':
            self.insert_entry( domain_alias , self.symbol , 'order_side', series, -1 )
            self.insert_entry( domain_alias , self.symbol , 'order_target', series, target_price )
            self.insert_entry( domain_alias , self.symbol , 'order_price',  series, res['price'] )
            self.insert_entry( domain_alias , self.symbol , 'order_quant',  series, res['amount'] )
        else:
            self.insert_entry( domain_alias , self.symbol , 'order_side', series, -1 )
            self.insert_entry( domain_alias , self.symbol , 'order_target', series, target_price )
        return res

        # Gotta Save some record of the Transaction intent # Ideal=
        # t = Transaction( domain=self.domain , target_amount=target_amount , target_price=target_price )
        # REAL TRANSACTION:
        # res = self.logic.create_limit_sell_order( self.symbol , target_amount , target_price , {'trading_agreement':'agree'} )
        # def create_order(self, symbol, type, side, amount, price=None, params={}):
        # res = self.logic.create_limit_sell_order( self.symbol , target_amount , target_price , {'trading_agreement':'agree'} )
        # res = self.logic.create_limit_sell_order( self.symbol , target_amount , target_price , {'trading_agreement':'agree'} )
        # res = self.logic.create_limit_sell_order( self.symbol , target_amount , target_price , {'trading_agreement':'agree'} )
        # res = self.logic.create_limit_sell_order( self.symbol , target_amount , target_price , {'trading_agreement':'agree'} )
        # print( res )
    def grab( self , amount=False ):

        domain_alias = self.domain+'_'+self.alias
        # PREPARE
        # DURING THE ORDER it SHOULD STAMP SAVE TO DB all the Parameters being used to calculate the deal
        # SAVE / SYNC orderbook + Tradebook AND


        buy_obj = self.max_entry()
        qbal = buy_obj['qbal']

        if amount:
            target_amount= amount
            target_price = self.fastBuyPrice( target_amount )
        else:
            target_price  = buy_obj['price']
            target_amount = buy_obj['amount']  # Fees included ( rounded )

        if float( qbal ) <= 0.5:
            print('Already Entered:  ',self.domain, self.symbol)
            return False
        fee_percent = self.market()['taker']
        amount_cost = target_amount * target_price
        fee_cost = amount_cost * fee_percent
        expected_cost = amount_cost + fee_cost

        amount_minus_fee = target_amount - ( target_amount * fee_percent )
        print('      Buy Order: ', self.symbol   ,'\n'
              '  Target Amount: ', target_amount ,'\n'
              '   Target Price: ', target_price  ,'\n'
              '          Fee %: ', fee_percent   ,'%\n'
              '       Fee Cost: ', fee_cost      ,'\n'
              '    Amount Cost: ', amount_cost   ,'\n'
              '     Amount-Fee: ', amount_minus_fee,'\n'
              'Expected T Cost: ', expected_cost ,'\n')

        #  createMarketBuyOrderRequiresPrice  for exchanges that need to create buy order based on quote currency
        # 'GTC' = Good To Cancel(default),
        # 'IOC' = Immediate Or Cancel

        # PLACE ORDER
        self.logic.verbose=True
        series = xtime.series_now()
        #self.insert_entry( domain_alias , self.symbol , 'order_attempt',   series, 1 )
        #res = self.logic.create_order( self.symbol , 'limit' , 'buy' , amount_minus_fee , target_price , {'timeInForce':'IOC'} )

        if self.logic.has['createMarketOrder']:
            res = self.logic.create_order( self.symbol , 'market' , 'buy' , target_amount  , {'trading_agreement':'agree' } )
        else:
            res = self.logic.create_order( self.symbol , 'limit' , 'buy' , target_amount , target_price , {'trading_agreement':'agree'} )
        #tele.send(' ETR'+str(target_amount)+"@"+str(target_price) )
        self.logic.verbose=False

        # RECORD ORDER
        if res['status']=='closed':
            self.insert_entry( domain_alias , self.symbol , 'order_side',   series, 1 )
            self.insert_entry( domain_alias , self.symbol , 'order_target', series, target_price )
            self.insert_entry( domain_alias , self.symbol , 'order_price',  series, res['price'] )
            self.insert_entry( domain_alias , self.symbol , 'order_quant',  series, res['amount'] )
        else:
            self.insert_entry( domain_alias , self.symbol , 'order_side', series, 1 )
            self.insert_entry( domain_alias , self.symbol , 'order_target', series, target_price )
        return res
    def dump( self , amount=False ):
        domain_alias = self.domain+'_'+self.alias
        base_bal=self.base_balance()
        target_amount = amount if amount is not False else base_bal
        if( float(target_amount) <= 0.0001):
            print('Already exited:  ',self.domain,':',self.symbol)
            return False

        price = self.fastSellPrice( base_bal )
        target_price = price
        fee = self.market()['maker']
        expected_fee = ( target_amount * fee )
        expected_p = ( target_amount * price )
        print('     Sell Order: ', self.symbol   ,'  \n'
              '         Amount: ', target_amount ,'  \n'
              '   Target Price: ', target_price  ,'  \n'
              '            Fee: ', fee           ,'% \n'
              '   Expected_fee: ', expected_fee  ,'  \n'
              ' Expect_proceed: ', expected_p    ,'  \n'
              '       Base Bal: ', base_bal,'',self.quote )

        # PLACE ORDER
        self.logic.verbose=True
        series = xtime.series_now()
        self.insert_entry( domain_alias , self.symbol , 'order_attempt',   series, -1 )
        #res = self.logic.create_order( self.symbol , 'limit' , 'sell' , target_amount , target_price , {'timeInForce':'IOC'} )
        #res = self.logic.create_order( self.symbol , 'limit' , 'buy' , target_amount , target_price , {'timeInForce':'IOC'} )
        if self.logic.has['createMarketOrder']:
            res = self.logic.createOrder( self.symbol , 'market' , 'sell' , target_amount , {'trading_agreement':'agree'} )
        else:
            res = self.logic.create_order( self.symbol , 'limit' , 'sell' , target_amount , target_price , {'trading_agreement':'agree'} )
        #tele.send(' EXT'+str(target_amount)+"@"+str(target_price) )
        self.logic.verbose=False

        # if status closed:
        #self.record_transaction_result()
        # RECORD ORDER
        if res['status']=='closed':
            self.insert_entry( domain_alias , self.symbol , 'order_side', series, -1 )
            self.insert_entry( domain_alias , self.symbol , 'order_target', series, target_price )
            self.insert_entry( domain_alias , self.symbol , 'order_price',  series, res['price'] )
            self.insert_entry( domain_alias , self.symbol , 'order_quant',  series, res['amount'] )
        else:
            self.insert_entry( domain_alias , self.symbol , 'order_side', series, -1 )
            self.insert_entry( domain_alias , self.symbol , 'order_target', series, target_price )
        return res

    def convert_maximum_to(self , target_base_in):
        # find_or_get_param_of_price
        amount = self.balance()
        if( amount == 0):
            return ' 0 balance cannot convert '
        price = self.getReasonablePrice()
        #target_base_in
        target_amount = amount
        target_price = price
        self.logic.verbose=True
        print(' Sell Order in progress:: ', target_amount , target_price )
        res = self.logic.create_limit_sell_order( self.symbol , target_amount , target_price , {'trading_agreement':'agree'} )
        print( res )
        self.logic.verbose=False
        return res


    def retrieve_deposit_info(self):
        cluster = False
        attempts = 0
        while not cluster and attempts < 4:
            try:
                cluster = self.logic.fetchDepositAddress( self.base )
            except Exception as e1:
                try:
                    cluster = self.logic.createDepositAddress( self.base )
                except Exception as e2:
                    attempts= attempts +1
                    print( 'wow create failed too: ',self.domain, self.symbol,' : ',e2)
        return cluster
    def memo(self):
        out_memo=False
        if self.deposit_info == None:
            self.deposit_info = self.retrieve_deposit_info()
        if( 'tag' in self.deposit_info and self.deposit_info['tag'] != None ):
            out_memo = self.deposit_info['tag']
        else:
            if( 'destination_tag' in self.deposit_info['info'] ):
                out_memo = self.deposit_info['info']['destination_tag']
            else:
                out_memo = False
        return out_memo
    def address(self):
        if self.deposit_info == None:
            self.deposit_info = self.retrieve_deposit_info()
        return self.deposit_info['address']
    def withdraw(self , target_address, target_amount ,memo=None):
        # prepare requirements:
        target_address = target_address
        target_memo = memo
        print(' Ok Flight check : ' , target_address , target_memo  )
        self.logic.verbose = True
        self.logic.withdraw( self.base , target_amount , target_address , tag=target_memo )
        self.logic.verbose = False
        # Turn on Verbose for XFERS Cause yeah
    def withdrawls(self):
        return self.logic.fetchWithdrawals()
    def list_withdrawls(self):
        for w in self.logic.fetchWithdrawals():
            print( w )
    def deposit_address(self):
        addy = False
        # a = self.logic.has['fetchDepositAddress']
        # b = self.logic.has['createDepositAddress']
        #self.logic.fetchDepositAddresses (codes = undefined, params = {})
        #self.logic.fetchDepositAddresses (codes = ['BTC','ETH'], params = {})
        attempts = 0
        while not addy and attempts < 4:
            try:
                cluster = self.logic.fetchDepositAddress( self.base )
                addy = cluster['address']
            except Exception as e1:
                try:
                    cluster = self.logic.createDepositAddress( self.base )
                    addy = cluster['address']
                    print( ' address not generated?: ', e1)
                    print(' tried create: ', addy )
                except Exception as e2:
                    attempts= attempts +1
                    print( 'wow create failed too: ',self.domain, self.symbol,' : ',e2)
        return addy
        # Some exchanges will also allow the user to create new addresses for deposits.
        # Some of exchanges require a new deposit address to be created for each new deposit.
        # The address for depositing can be either an already existing address that was created previously
        # or it can be created upon request. In order to see which of the two methods are supported,
        # check the exchange.has['fetchDepositAddress'] and exchange.has['createDepositAddress'] properties.
        # check SELF in DB For deposit address list
        # check exchange address balances if both don't exist issue new deposit address

    ################################# INFORMATIONAL #####################################
    def orderbook(self):
        ordr = self.mineOrderbook()
        books = { 'asks':pd.DataFrame(ordr['asks']) , 'bids':pd.DataFrame(ordr['bids']) }
        return books

    def lo(self):
        books = self.orderbook()
        merged_table = pd.concat([books['asks'],books['bids']], axis=1, sort=False)
        merged_table.columns=['ask_p','ask_q','bid_p','bid_q']
        print( merged_table.head(15) )

    def getReasonablePrice(self):
        book = self.orderbook()
        lowest = book['bids'][0][0]
        highest = book['asks'][1][0]
        return lowest

    def fastSellPrice(self , quant):
        book = self.orderbook()
        bids = book['bids']
        bids['qsum']=bids[1].cumsum()
        price = bids[bids.qsum>=quant][0].iloc[0]
        return price

    def fastBuyPrice(self, quant):
        book = self.orderbook()
        asks = book['asks']
        asks['qsum']=asks[1].cumsum()
        price = asks[asks.qsum>=quant][0].iloc[0] # GET PRICE BY ROW WHERE QSUM > quant
        return price

    def fetchMarkets(self):
        self.logic.fetchMarkets()
        return self.logic.markets




    ########################## GRAPH BUILDERS 
    @classmethod
    def merge( self,   *args , **kwargs ):
        #instance = Vehicle( *args , **kwargs )
        #node_data = ht.erase_keys( kwargs , ['apiKey','key','secret','password','passphrase'] )
        #n = neo.hash_merge( "Vehicle" , {'domain':kwargs['domain'] , 'symbol':kwargs['symbol'] } , node_data )
        #instance.node = n
        return instance

    def caps(self , allowed_list ):
        allowed_markets = {e:False for e in allowed_list}
        all_markets = self.logic.loadMarkets()
        markets = self.logic.markets
        vehicles = rdd.vehicles()
        white_listed = {  x:markets.get(x) for x in allowed_markets if x in markets }
        #what_can_i_buy_with_this_base  = [ white_listed[x] for x in white_listed if white_listed[x]['quote']==self.base or white_listed[x]['base']==self.base ]
        where_can_i_move_this_base = [ x for x in vehicles if x.base==self.base and x.domain!=self.domain ]
        what_can_i_buy_with_this_base = [ x for x in vehicles if x.domain==self.domain and ( self.base == x.base or self.base == x.quote ) ]

        node_1 = self.dbref()
        outbound_conversions = []
        for b in what_can_i_buy_with_this_base :
            node_2 = b.dbref()
            if( node_1 != node_2):
                outbound_conversions.append( { 'type':'CONVERTS',  'source':node_1 , 'destination':node_2 ,'domain':self.domain , 'carrier':self.carrier })

        outbound_transfers = []
        for b in where_can_i_move_this_base :
            node_2 = b.dbref()
            outbound_transfers.append( { 'type':'TRANSFERS', 'source':node_1 , 'destination':node_2  , 'base':b.base })

        return {
            'transfers':outbound_transfers,
            'conversions':outbound_conversions  }

    def caps_ext(self , allowed_list ):
        all_markets = self.logic.loadMarkets()
        allowed_markets = {e:False for e in allowed_list}
        markets = self.logic.markets
        vehicles = rdd.vehicles()
        #white_listed = {  x:markets.get(x) for x in allowed_markets if x in markets }
        white_listed = all_markets
        #what_can_i_buy_with_this_base  = [ white_listed[x] for x in white_listed if white_listed[x]['quote']==self.base or white_listed[x]['base']==self.base ]
        where_can_i_move_this_base = [ x for x in vehicles if x.base==self.base and x.domain!=self.domain ]
        what_can_i_buy_with_this_base = [ x for x in vehicles if x.domain==self.domain and ( self.base == x.base or self.base == x.quote ) ]
        node_1 = self.dbref()
        outbound_conversions = []
        for b in what_can_i_buy_with_this_base :
            node_2 = b.dbref()
            if( node_1 != node_2):
                outbound_conversions.append( { 'type':'CONVERTS',  'source':node_1 , 'destination':node_2 ,'domain':self.domain , 'carrier':self.carrier })

        outbound_transfers = []
        for b in where_can_i_move_this_base :
            node_2 = b.dbref()
            outbound_transfers.append( { 'type':'TRANSFERS', 'source':node_1 , 'destination':node_2  , 'base':b.base })

        return {
            'transfers':outbound_transfers,
            'conversions':outbound_conversions  }
