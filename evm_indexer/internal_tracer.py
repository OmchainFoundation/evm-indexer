import requests, json
from web3 import Web3

class InternalTracer:
  def __init__(self, node_endpoint):
    self.node_endpoint = node_endpoint
    
  def get_tx_receipt(self, tx_hash):
    try:
      
      if type(tx_hash) != str:
        tx_hash = Web3.to_hex(tx_hash)
     
      headers = {'Content-Type': 'application/json'}
      payload = {
          "jsonrpc": "2.0",
          "id": 1,
          "method": "eth_getTransactionReceipt",
          "params": [tx_hash]
      }

      response = requests.post(self.node_endpoint, headers=headers, data=json.dumps(payload))
      if response.status_code == 200:
          return response.json()
      else:
          return None
    except Exception as e:
      return None
    
  def get_trace(self, tx_hash):
    try:
      headers = {'Content-Type': 'application/json'}
      payload = {
          "jsonrpc": "2.0",
          "id": 1,
          "method": "debug_traceTransaction",
          "params": [
              tx_hash,
          ]
      }

      response = requests.post(self.node_endpoint, headers=headers, data=json.dumps(payload))
      if response.status_code == 200:
          return response.json()
      else:
          return None
    except Exception as e:
      return None
    
  def capture_internal_calls(self, trace_response, tx_receipt):
    captured_calls = []
    struct_logs = trace_response['result']['structLogs']

    # Initial call from EOA to the contract
    initiator_address = tx_receipt['from']
    contract_address = tx_receipt['to']  # Contract being called
    current_call = {'from': initiator_address, 'to': contract_address}

    for log in struct_logs:
        op = log['op']
        stack = log['stack']

        if op in ['CALL', 'CALLCODE', 'DELEGATECALL', 'STATICCALL']:
            if len(stack) >= 7:
                # Extract 'to' address and value from the stack
                to_address = '0x' + stack[-2][-40:]
                value = int(stack[-3], 16) if op == 'CALL' else 0  # Value is relevant only for CALL

                captured_call = {'op': op, 'from': current_call['to'], 'to': to_address, 'value': value}
                captured_calls.append(captured_call)

                # Update the current call context
                current_call['from'] = current_call['to']
                current_call['to'] = to_address

    return captured_calls
  
  def calculate_net_changes(captured_calls):
    net_changes = {}
    for call in captured_calls:
        if call['from'] not in net_changes:
            net_changes[call['from']] = 0
        if call['to'] not in net_changes:
            net_changes[call['to']] = 0

        net_changes[call['from']] -= call['value']
        net_changes[call['to']] += call['value']

    return net_changes