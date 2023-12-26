import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from evm_indexer.fetcher import Fetcher
from evm_indexer.decoder import Decoder
from evm_indexer.internal_tracer import InternalTracer
from web3 import Web3

NODE_URL = 'https://seed.omchain.io'

fetcher = Fetcher(NODE_URL, is_poa=True)
decoder = Decoder(fetcher=fetcher)
internal_tracer = InternalTracer(NODE_URL)

fetched_transactions = fetcher.fetch_transactions_in_block(32582884)

tx_receipts = []
for transaction in fetched_transactions:
    tx_receipts.append(internal_tracer.get_tx_receipt(transaction['hash'])['result'])


tx_data = {}
for tx_receipt in tx_receipts:
    if tx_receipt['status'] == '0x1':
      tx_data[tx_receipt['transactionHash']] = [internal_tracer.get_trace(tx_receipt['transactionHash']), tx_receipt]

erc20_transactions = []
native_transactions = []
internal_transactions = []


for tx in tx_data:
    erc20_transactions.extend(decoder.get_erc20_transfers_from_tx(tx_data[tx][1]))
    native_transactions.extend(decoder.get_native_transfers_from_tx(tx_data[tx][1]['transactionHash']))
    internal_transactions.extend(internal_tracer.capture_internal_calls(tx_data[tx][0], tx_data[tx][1]))
    
print('ERC20 Transactions:')
for tx in erc20_transactions:
    print(tx)
    
print('Native Transactions:')
for tx in native_transactions:
    print(tx)
    
print('Internal Transactions:')
for tx in internal_transactions:
    print(tx)
    
    