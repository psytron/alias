

import hashlib
from .util.format import block

from keycache import Keycache
from .drivers.drivers import Drivers
from .vehicle import Vehicle


class Alias:

    def __init__(self , *args , **kwargs ):
        print(' New Alias Update')
        print(' Incoming should be LIST of Credentials? ')
        pub = kwargs.get('pub',None)
        self.identifier = kwargs.get('identifier','default')
        self.creds = Keycache( alias=self.identifier , private_key=kwargs.get('priv','default'))
        self.drivers = Drivers( alias=self.identifier , creds=self.creds )


    def stat(self):
        print('              ')
        print('       Alias  ')
        print('         PUB: '+str( hashlib.sha256( self.identifier.encode()).hexdigest())  )
        print('        ADDR: '+str( hex(id(self))) )
        print('  Identifier: '+self.identifier+'  ')
        print('              ')
        self.scope()

    def h(self):
        print('              ')
        print(' Data Methods:    View Methods:  ')
        print(' scope()          scp() ')
        print(' balances()       bals() ')
    # HERE is it better to get Exchange with the dot syntax OR Vehicle ?
    # must be Exchange or else need 'SYMBOL' parameter...hmmm
    # here is it better to return new Exchange class instance or just base level driver class?
    def __getattr__(self, name):
        try:
            print(' attr ')
            inst = self.drivers.instance(name)
            return inst
        except Exception as e:
            print( ' cannot attr this in alias getattr',e)

    def add_cred(self, domain, blob_in ):
        self.creds.add( domain , blob_in )
    def get_cred(self, domain ):
        return self.creds.get( domain )
    def add_all(self , blob_dict ):
        self.creds.add_all( blob_dict )
    def load_config(self):
        self.creds.load_config()
    def load_blob(self):
        self.creds.load_blob()
    def save_blob(self):
        self.creds.save()
    def scope(self):
        objs = self.creds.get_all()
        for k,v in enumerate(objs):
            c = objs[v]
            print( block( k,3 ),
                   block( c.get('domain','N/A'),16),
                   block( c.get('apiKey','N/A') ),'  ',
                   block( c.get('un','N/A') ) )
        return objs

    def vehicle(self, domain, symbol):
        return Vehicle( 
            domain=domain, 
            driver=self.drivers.instance(domain) , 
            symbol=symbol , 
            alias=self.identifier )

    def nested_search(self):
        print(' searching only nodes link')
        # Need to

    def balances(self):
        # get all domains with credentials
        # get balances in all relevant vehicles
        dom_list=self.scope()
        for d in dom_list:
            if 'secret' in dom_list[d]:
                drivx = self.drivers.instance(d)
                if drivx and callable(getattr( drivx, 'fetch_balance', None)):
                    try:
                        free_balances = drivx.fetch_balance()['free']
                        print( drivx, drivx.apiKey ,free_balances )
                        #for x in free_balances:
                        #y = { x:free_balances[x] for x in free_balances if free_balances[x]>0 }
                        #print( y )
                    except Exception as e:
                        print(d,' Error on fetch Balance',e)
                # YOU ARE HERE:
                # can this be inside self.creds ?
                # is it better for drivers to be a reference inside each creds cluster?
                # or is it better for it to be separate
                d=3




    def __getattrEX__(self, name):
        e=3
        def _missing(*args, **kwargs):
            # __getattr__ override calls this method
            # returned method receives original parameters
            print( "A missing method was called." )
            print( "The object was %r, the method was %r. " % (self, name) )
            print( "It was called with %r and %r as arguments" % (args, kwargs) )
            return self.drivers.instance(name)
        return _missing


        # YOU ARE HERE:
        # Must refactor drivercache to be instantiable AND store credentials LIKE MyCreds
        # self.drivers = Drivers( identifier='same' )
        # drivers.instance( domain , self.creds.get( domain ) )