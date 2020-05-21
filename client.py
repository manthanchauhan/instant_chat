import socket
import sys
from select import select
from datetime import datetime

HOST = '100.82.176.46'
POST = 1029

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
    client_sock.connect((HOST, POST))
    print('Connected')

    std_input = sys.stdin

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
                        end = True
                        break

                    print(u"\u001b[2A\u001b[k")
                    sys.stdout.write('\033[92mYou at ' + str(datetime.now()) + ':\033[0m ')
                    sys.stdout.write(text)
                    sys.stdout.flush()

                    message = '\033[93mClient at ' + str(datetime.now()) + ':\033[0m ' + text
                    client_sock.send(bytes(message, 'utf-8'))
