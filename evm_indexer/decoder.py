from web3 import Web3
from web3.exceptions import BadFunctionCallOutput

ERC20_TRANSFER_EVENT_SIGNATURE_HASH = Web3.keccak(text="Transfer(address,address,uint256)").hex()

class Decoder:
    def __init__(self, fetcher):
        self.fetcher = fetcher
        self.web3 = fetcher.web3
    
    def get_erc20_transfers_from_tx(self, tx_receipt):
        # Filter the logs for ERC20 Transfer events
        transfer_events = []
        for log in tx_receipt['logs']:
            if log['topics'][0] == ERC20_TRANSFER_EVENT_SIGNATURE_HASH and len(log['topics']) == 3:
                try:
                    from_address = self.web3.to_checksum_address('0x' + log['topics'][1][-40:])
                    to_address = self.web3.to_checksum_address('0x' + log['topics'][2][-40:])
                    token_address = log['address']
                    amount = Web3.to_int(hexstr=log['data'])

                    transfer_events.append({
                        'from': from_address,
                        'to': to_address,
                        'amount': amount,
                        'token_address': token_address
                    })
                except BadFunctionCallOutput:
                    # Handle error if the log decoding fails
                    continue
        return transfer_events
    
    def get_native_transfers_from_tx(self, tx_hash):
        tx = self.web3.eth.get_transaction(tx_hash)
        value = tx['value']
        if value == 0:
            return []
        
        from_address = self.web3.to_checksum_address(tx['from'])
        to_address = self.web3.to_checksum_address(tx['to'])
        return [{
            'from': from_address,
            'to': to_address,
            'amount': value,
            'token_address': None
        }]
        