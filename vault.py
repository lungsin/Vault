#!./venv/bin/python

import socket
import sys
import os
import json

def main():
    server_address = sys.argv[1]
    # server_address = './uds_test_socket'

    # Make sure the socket does not already exist
    try:
        os.unlink(server_address)
    except OSError:
        if os.path.exists(server_address):
            raise
            
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Bind the socket to the address
    print(f'starting up on {server_address}')
    sock.bind(server_address)

    sock.listen(1)

    while True:
        print('waiting for a connection')
        connection, client_address = sock.accept()
        
        handle(connection, client_address)
        
        
        
def handle(connection, client_address):
    print('connection from', client_address)
    
    conn_file = connection.makefile()
    while True:
        command = read_command(conn_file)
        if (command is None): break
        response = process_command(command)
        print(f"response : {response}")
        connection.sendall(response)
    
    print('done')
    connection.close()
    
def read_command(conn_file):
    print('waiting for command')
    line = conn_file.readline()
    print(f"here is : {line}")
    if (line == '\n'): return None
    return json.loads(line)
    
def process_command(command):
    response = {}
    response["id"] = command["id"]
    
    from_addr = command["from_address"]
    to_addr   = command["to_address"]
    amount    = int(command["amount"])
    
    with open(f"{from_addr}", 'r') as f:
        private_key = f.read()
    
    tx = generateTx(from_addr, to_addr, amount, private_key)
    response["tx"] = tx
    return json.dumps(response).encode()

def generateTx(from_addr, to_addr, amount, private_key):
    from web3 import Web3, HTTPProvider
    
    endpoint = "https://ropsten.infura.io/v3/dbb2e3c355894aec995396e31bce9ba9"
    w3 = Web3(HTTPProvider(endpoint))
    
    transaction = {
        'from': from_addr,
        'to': to_addr,
        'value': amount,
        'gasPrice': w3.eth.gasPrice,
        'nonce': w3.eth.getTransactionCount(from_addr)
    }
    transaction['gas'] = w3.eth.estimateGas(transaction)
    print(f"estimate cost = {transaction['gas'] * transaction['gasPrice']}")
    transaction['value'] -= transaction['gas'] * transaction['gasPrice']
    signed = w3.eth.account.signTransaction(transaction, private_key)
    
    # print(w3.eth.sendRawTransaction(signed.rawTransaction))
    return w3.toHex(signed.rawTransaction)



def testing():
    addr1 = "0x1348E7E2b73993bEE501aa4413C193d3722f2b60"
    addr2 = "0xdD8dA64825a55b3339fccEEE4c0443174517A666"
    
    with open(addr1, 'r') as f:
        key1 = f.read()
        
    with open(addr2, 'r') as f:
        key2 = f.read()
    
    print("key1 : " + key1)
    print("key2 : " + key2)
    amount = 30000000000000
    print(generateTx(addr1, addr2, amount, key1))
 
main()   
# testing()