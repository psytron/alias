# Alias
Identity and asset containers for portfolio mass-management. Alias enables simplified private key management and operational concurrency of exchanges, wallets, APIs and shell protocols by using uniform containers. All orderbooks, trade data, time series and calculations are returned as composable Numpy / Dataframes and can be chained, stacked and grouped into aggregate DataFrames compatible with your favorite data science tools and machine learning libraries. 

Install
    
    pip install alias

Usage

```python
from alias import Alias

a1 = Alias(                                # Assumes someID already has added keys
    identifier='BigHodler' ,               # Any name or identifier to access your vault
    private_key=channel.get('default') )   # Private key from message bus

a1.stat()                                  # shows overview of current container state
a1.scope()                                 # returns all capabilities within scope of container
a1.vehicle('coinbase', 'BTC/USD')          # returns Vehicle() initialized with available credentials
a1.all('BTC/USD')                          # returns all in-scope vehicles with BTC/USD capability
```

Create From Local Config File
```python
a1 = Alias( 
    identifier='BigHodler' ,
    private_key=channel.get('default') ,
    config_file='tmp/privatekeys.yml',
    blob_dir='./blobs ')                  # Default name is hash of identifier
a1.save()                                 # Writes AES encrypted Blob to Disk
```

Create In Python 
```python
a1 = Alias( identifier='BigHolder', private_key=channel.get('default')  )
a1.add( 'bittrex', { 'key':'a1b2c3d4e5d4', 'secret':'e8d9e9d9a9d9' } )
a1.add( 'coinbase', { 'key':'b1b2c3d4e5e1', 'secret':'e8d9e9d9a9d9' } )  
a1.add( 'local_btc', { 'key':'e5d4c54e53b5', 'secret':'e8d9e9d9a9d9', 'type':'corebtc' } )      
a1.add( 'local_eth', { 'key':'c1e0c54e53a5', 'secret':'e8d9e9d9a9d9', 'type':'geth' } )          
a1.add( 'signalmesh' { 'key':'xxxxxxxxxxxx', 'secret':'yyyyyyyyyyyy', 'type':'signalmesh' } )
a1.save() # writes encrypted blob 
```
    
    
### Vehicle
A Vehicle is a TAC (Transactable Asset Container) for any kind of transactable asset. It abstracts the differences between exchanges, wallets, APIs, or shell protocols. Vehicles expose a broad range of functionality while hiding the inner workings and eliminating the differences between underlying assets. Vehicles can be used to store, access, move, and analyze all of your holdings simultanously. 

Usage
                                              
    x1 = a1.vehicle( ‘bittrex’ , ‘BTC/USD’ )   # Create a few random vehicle containers
    x2 = a1.vehicle( ‘coinbase’, ‘BTC/USD’ ) 
    x3 = a1.vehicle( ‘kraken’ , ‘ETH/USD’ )  
    
    x1.route( x3 )                             # finds cheapest route and moves all value to x3
    x1.collect( [ x2 , x3 , x4 ] )             # collect all value into x1
    x1.disperse( [ x2 , x4 ] )                 # disperse vall value accross x2, x4
    x1.transfer( x2 , 0.1 )                    # transfers 0.1 of base value to x2
    
    

Analytics Usage

    x1.mineTradebook()                          # Numpy / DataFrame with formatted tradebook + metadata
    x2.mineOrderbook()                          # Numpy / DataFrame with formatted orderbook + metadata
    x3.mineMetadata()                           # Extended metadata for vehicles asset


### Group
Provides a [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) multiprocessing wrapper to enable fast and parallel execution of concurrent operations on all Vehicles and Aliases. Vehicle and Alias return matrices which are composable into aggregates using vectorized operations and available for asset and portfolio wide operations.

Usage
    from alias import Group

    g1 = Group( [x1,x2,x3] )
    g1.mineTradebook()                          # Concurrently Mine all Tradebooks 
    g1.mineOrderbook()                          # Concurrently Mine all Orderbooks
    

[ ] Add docs about group usage
