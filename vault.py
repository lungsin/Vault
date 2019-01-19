import socket
import sys
import os
import json

def main():
    # server_address = sys.argv[1]
    server_address = './uds_test_socket'

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
    
    # from_addr = command["from_address"]
    # to_addr   = command["to_address"]
    # amount    = command["amount"]
    
    # with open(f"{from_addr}") as f:
    #     private_key = f.read()
    
    return json.dumps(response).encode()

# from web3 import Web3, IPCProvider
# import sys

# path = sys.argv[1]
# print(path)
# w3 = Web3(IPCProvider(path))

main()