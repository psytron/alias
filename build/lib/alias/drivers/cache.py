



import ccxt
from .oanda import oanda
import keycache

def instance( alias='default' , domain='default'):
    initObj = {
        'domain':domain,
        'verbose':False,
        'enableRateLimit':True }
    try:
        exch = getattr( ccxt, domain )
        creds = keycache.get(domain)
        # creds = credstore.get( alias=alias_in , domain=domain )
        inst = exch( { **creds , **initObj } )
        return inst
    except Exception as e:
        if( domain == 'oanda'):
            exch=oanda
            creds = keycache.get(domain)
            inst = exch( { **creds , **initObj } )
            return inst




def getooo( domain='default' , alias='default' ):
    global cached_exchanges
    initObj = {
        'domain':domain,
        'verbose':False,
        'enableRateLimit':True }
    try:
        exch = getattr( ccxt, domain )
        #creds = megablobstore.get( operator=operator, domain=domain )
        creds = keycache.get( domain )
        inst = exch( { **creds , **initObj } )
        return inst
    except Exception as e:
        if( domain == 'oanda'):
            exch=oanda
            creds = keycache.get( domain)
            inst = exch( { **creds , **initObj } )
            return inst








#from tradespace import megablobstore

cached_exchanges = {}


def getDriver( domain_in ):
    # import ib_gateway
    try:
        exch = getattr( ccxt, domain_in )
    except Exception as exc:
        try:
            exch = oanda
        except Exception as exc:
            print('total-fail' , exc)
    return exch






'''
def get_driver_class( domain_in ):
    try:
        exch = getattr( ccxt, domain_in )
    except Exception as exc:
        try:
            exch = oanda
        except Exception as exc:
            print('total fail to getDriver()')
    return exch


def get_driver_instance_by_domain_and_symbol( domain_in , symbol_in ):
    print(' wow ')


def get_driver_instance_by_domain( domain_in ):

    try:
        cred = megablobstore.credential(domain_in)
        exch_class = getattr( ccxt, domain_in )
        exch_inst = exch_class( { **cred , 'domain':domain_in } )
    except Exception as exc:

        try:
            exch_class = oanda
            exch_inst = oanda()
        except Exception as exc:
            print('total fail to getDriver()')

    return exch_inst
    '''