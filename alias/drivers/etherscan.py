
print('running ')
# TESTS OF ETHERSCAN RESULTS:
print(' passing ')
f=4



from pyetherscan import Client
client = Client()
address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'
address_balance = client.get_single_balance(address)
address_balance.response_status_code
address_balance.message
address_balance.balance


#nd is to use ``pyetherscan`` objects which fully abstract the API. These
#can be found in the ``pyetherscan.ethereum`` module and include:


from pyetherscan import Address
address = '0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae'
ethereum_address = Address(address)
ethereum_address.balance
for txn in ethereum_address.transactions:
    print( txn.value)
