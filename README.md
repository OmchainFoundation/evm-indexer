# EVM Indexer
EVM Indexer is a Python package designed to interact with the Ethereum Virtual Machine (EVM). It facilitates the fetching, decoding, and tracing of transactions on the Ethereum blockchain. This package is particularly useful for analyzing transaction data, including ERC20 token transfers, native Ethereum transactions, and internal contract calls with value.

## Features
* Fetching Transactions: Retrieve transactions from a specific block on the Ethereum blockchain.
* Decoding ERC20 Transfers: Extract and decode ERC20 token transfer events from transaction receipts.
* Tracing Internal Transactions: Trace internal Ethereum contract calls and operations.
* Handling Native Ethereum Transfers: Identify and process native Ethereum (ETH) transfers.

## Installation
To install the EVM Indexer package, use pip:

```bash
pip install evm_indexer
```

## Usage
Here's a quick example to demonstrate the basic functionality of the EVM Indexer package:

```python
from evm_indexer.fetcher import Fetcher
from evm_indexer.decoder import Decoder
from evm_indexer.internal_tracer import InternalTracer
from web3 import Web3

# Set the node URL
NODE_URL = 'https://seed.omchain.io'

# Initialize fetcher, decoder, and internal tracer
fetcher = Fetcher(NODE_URL, is_poa=True)
decoder = Decoder(fetcher=fetcher)
internal_tracer = InternalTracer(NODE_URL)

# Fetch transactions from a specific block
fetched_transactions = fetcher.fetch_transactions_in_block(32582884)

# Process each transaction
tx_receipts = [internal_tracer.get_tx_receipt(tx['hash'])['result'] for tx in fetched_transactions]
tx_data = {tx_receipt['transactionHash']: [internal_tracer.get_trace(tx_receipt['transactionHash']), tx_receipt] for tx_receipt in tx_receipts if tx_receipt['status'] == '0x1'}

# Extract different types of transactions
erc20_transactions = [decoder.get_erc20_transfers_from_tx(tx_data[tx][1]) for tx in tx_data]
native_transactions = [decoder.get_native_transfers_from_tx(tx_data[tx][1]['transactionHash']) for tx in tx_data]
internal_transactions = [internal_tracer.capture_internal_calls(tx_data[tx][0], tx_data[tx][1]) for tx in tx_data]

# Print the transactions
print('ERC20 Transactions:', erc20_transactions)
print('Native Transactions:', native_transactions)
print('Internal Transactions:', internal_transactions)
```

And the example output;

```bash
ERC20 Transactions:
{'from': '0xe6F4967DD4F6dC31DE2c5C047cE931f74d92ba8C', 'to': '0x7c6ed537aa6348aF18AbCdf3Cf417882c95060de', 'amount': 148062317306291907612, 'token_address': '0x779da1b95e81de928fbe9f293629a346f88e86f7'}
Native Transactions:
{'from': '0xe210a02ED752624d70c325688c9fdC1ccC97d81F', 'to': '0xcDa8C9991f725fF4fa6369FBC0A4F1Ab51Eae354', 'amount': 20000000000000000000000, 'token_address': None}
Internal Transactions:
{'op': 'CALL', 'from': '0xe6f4967dd4f6dc31de2c5c047ce931f74d92ba8c', 'to': '0x779da1b95e81de928fbe9f293629a346f88e86f7', 'value': 0}
```

## Modules and Methods

### Fetcher (`fetcher.py`)

**Class Description:**  
Handles the retrieval of blockchain data from an Ethereum node.

- **`__init__(self, node_endpoint, is_poa=True)`**  
  Constructor for the Fetcher class.  
  **Parameters:**
  - `node_endpoint` (str): The URL of the Ethereum node.
  - `is_poa` (bool, optional): Indicates if the node is part of a Proof of Authority network. Default is `True`.

- **`fetch_block(self, block_number)`**  
  Fetches a complete block using its number.  
  **Parameters:**
  - `block_number` (int): The number of the block to fetch.  
  **Returns:**  
  - `dict`: The block data, or `None` if fetching fails.

- **`fetch_latest_block_number(self)`**  
  Retrieves the number of the most recent block on the blockchain.  
  **Returns:**  
  - `int`: The latest block number.

- **`fetch_blocks_in_range(self, start_block, end_block)`**  
  Fetches all blocks within a specified range.  
  **Parameters:**
  - `start_block` (int): The starting block number.
  - `end_block` (int): The ending block number.  
  **Returns:**  
  - `list`: A list of block data within the specified range.

- **`fetch_transactions_in_block(self, block_number)`**  
  Retrieves all transactions from a specific block.  
  **Parameters:**
  - `block_number` (int): The block number to fetch transactions from.  
  **Returns:**  
  - `list`: A list of transactions in the specified block.

- **`fetch_transactions_in_range(self, start_block, end_block)`**  
  Fetches transactions within a specified block range.  
  **Parameters:**
  - `start_block` (int): The starting block number.
  - `end_block` (int): The ending block number.  
  **Returns:**  
  - `list`: A list of transactions across the specified range of blocks.

### Decoder (`decoder.py`)

**Class Description:**  
Decodes transaction data to extract specific information, such as ERC20 token transfers and native Ethereum transfers.

- **`__init__(self, fetcher)`**  
  Constructor for the Decoder class.  
  **Parameters:**
  - `fetcher` (Fetcher): An instance of the Fetcher class used to fetch blockchain data.

- **`get_erc20_transfers_from_tx(self, tx_receipt)`**  
  Extracts ERC20 token transfers from a transaction receipt.  
  **Parameters:**
  - `tx_receipt` (dict): The transaction receipt containing logs.  
  **Returns:**  
  - `list`: A list of decoded ERC20 transfer events.

- **`get_native_transfers_from_tx(self, tx_hash)`**  
  Retrieves and decodes native Ethereum (ETH) transfers from a transaction.  
  **Parameters:**
  - `tx_hash` (str): The hash of the transaction.  
  **Returns:**  
  - `list`: A list containing the details of native ETH transfers, if any.

### InternalTracer (`internal_tracer.py`)

**Class Description:**  
Traces internal Ethereum transactions and contract calls for detailed analysis.

- **`__init__(self, node_endpoint)`**  
  Constructor for the InternalTracer class.  
  **Parameters:**
  - `node_endpoint` (str): The URL of the Ethereum node.

- **`get_tx_receipt(self, tx_hash)`**  
  Fetches the receipt of a given transaction.  
  **Parameters:**
  - `tx_hash` (str): The hash of the transaction.  
  **Returns:**  
  - `dict`: The transaction receipt, or `None` if fetching fails.

- **`get_trace(self, tx_hash)`**  
  Retrieves the trace of a given transaction.  
  **Parameters:**
  - `tx_hash` (str): The hash of the transaction.  
  **Returns:**  
  - `dict`: The transaction trace data, or `None` if fetching fails.

- **`capture_internal_calls(self, trace_response, tx_receipt)`**  
  Captures and processes internal contract calls and operations from a transaction trace.  
  **Parameters:**
  - `trace_response` (dict): The response object from `get_trace`.
  - `tx_receipt` (dict): The transaction receipt object.  
  **Returns:**  
  - `list`: A list of captured internal calls with their details.



## Contributing
Contributions to the EVM Indexer package are welcome. Please feel free to fork the repository, make changes, and submit pull requests.

## License
This project is licensed under the MIT License.