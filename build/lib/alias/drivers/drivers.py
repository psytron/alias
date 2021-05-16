

import ccxt
from .oanda import oanda
from .alpaca import alpaca


class Drivers:

    def __init__(self , *args, **kwargs):
        self.avail_creds = kwargs.get('creds')
        self.loaded_drivers = {}

    def get(self , domain_in):
        return 'almost'

    #def instance( alias='default' , domain='default'):
    def instance( self , domain_in ):
        if domain_in in self.loaded_drivers:
            return self.loaded_drivers[ domain_in ]
        else:
            initObj = {
                'domain':domain_in,
                'verbose':False,
                'enableRateLimit':True ,
                'options':{
                    'fetchMinOrderAmounts': False
                }
            }
            try:
                exch = getattr( ccxt, domain_in )
                # HERE IF CREDS DONT EXIST SHOULD RETURN BAREBONES NO PARAMS ( TEMP BELOW )
                creds = self.avail_creds.get( domain_in )

                # VPNURL IF CONFIGURED
                if creds != None and 'vpnurl' in creds:
                    initObj['proxies']={ 'tcp':creds['vpnurl'] }

                # RETURN PUBLIC EXCHANGE FOR UNCREDENTIALED DOMAINS
                if( creds == None ):
                    inst = exch( { **initObj} )
                else:
                    inst = exch( { **creds , **initObj } )

                self.loaded_drivers[ domain_in ]=inst
                return inst
            except Exception as e:
                if( domain_in == 'oanda'):
                    exch=oanda
                    creds = self.avail_creds.get( domain_in )
                    inst = exch( { **creds , **initObj } )
                    self.loaded_drivers[ domain_in ]=inst
                    return inst
                if( domain_in =='alpaca'):
                    exch=alpaca
                    creds = self.avail_creds.get( domain_in )
                    inst = exch( { **creds , **initObj } )
                    self.loaded_drivers[ domain_in ]=inst
                    return inst
