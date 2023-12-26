from web3 import Web3
from web3.middleware import geth_poa_middleware

class Fetcher:
  def __init__(self, node_endpoint, is_poa=True):
    self.web3 = Web3(Web3.HTTPProvider(node_endpoint))
    if is_poa:
      self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
      
    if not self.web3.is_connected():
      raise ConnectionError('Could not connect to node at {}'.format(node_endpoint))
    
  def fetch_block(self, block_number):
    try:
      return self.web3.eth.get_block(block_number, full_transactions=True)
    except Exception as e:
      return None
    
  def fetch_latest_block_number(self):
    return self.web3.eth.block_number
  
  def fetch_blocks_in_range(self, start_block, end_block):
    blocks = []
    for block_number in range(start_block, end_block + 1):
      block = self.fetch_block(block_number)
      if block:
        blocks.append(block)
    return blocks
  
  def fetch_transactions_in_block(self, block_number):
    block = self.fetch_block(block_number)
    if block:
      return block['transactions']
    else:
      return None
    
  def fetch_transactions_in_range(self, start_block, end_block):
    transactions = []
    for block_number in range(start_block, end_block + 1):
      print('Fetching block {}'.format(block_number))
      block_transactions = self.fetch_transactions_in_block(block_number)
      if block_transactions:
        transactions.extend(block_transactions)
    return transactions