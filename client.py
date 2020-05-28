# Better understand server script first.

import socket
import time
import sys
from select import select
from datetime import datetime

# set server's IP address (public ip) and port.
HOST = 'localhost'
PORT = 9999

# create a socket using same address family and protocol as server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:

    # connect to the server
    client_sock.connect((HOST, PORT))
    print('Connected')

    # capture standard input stream to read text entered in terminal (by you).
    std_input = sys.stdin

    # same communication logic as server.
    # See server.py for explanation
    with client_sock:
        end = False
        while not end:
            readable, writeable, others = select([std_input, client_sock], [], [])

            for sock in readable:
                if sock == client_sock:
                    message = sock.recv(1024).decode()

                    if 'END' in message:
                        end = True
                        break

                    print(message, end='')
                else:
                    text = std_input.readline()

                    if 'END' in text:
                        client_sock.send(bytes('END', 'utf-8'))
                        time.sleep(1)
                        end = True
                        break

                    print(u"\u001b[2A\u001b[k")
                    sys.stdout.write('\033[92mYou at ' + str(datetime.now()) + ':\033[0m ')
                    sys.stdout.write(text)
                    sys.stdout.flush()

                    message = '\033[93mClient at ' + str(datetime.now()) + ':\033[0m ' + text
                    client_sock.send(bytes(message, 'utf-8'))
