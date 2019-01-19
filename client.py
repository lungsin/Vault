# socket_echo_client_uds.py
import socket
import sys

testfiles = ["query_one_time.json", "query_multiple_times.json"]

for testfile in testfiles:
    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = './uds_test_socket'
    print('connecting to {}'.format(server_address))
    try:
        sock.connect(server_address)
    except socket.error as msg:
        print(msg)
        sys.exit(1)




    try:
        with open(testfile, 'rb') as f:
            message = f.read()
            
        print('sending {!r}'.format(message))
        sock.sendall(message)

        command_received = 0
        command_expected = message.count(b'\n') - 1
        print(command_expected)
        while command_received < command_expected:
            data = sock.recv(256)
            command_received += 1
            print('received {!r}'.format(data))

    finally:
        print('closing socket')
        sock.close()