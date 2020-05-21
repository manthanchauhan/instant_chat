import socket
import sys
import time
from select import select
from datetime import datetime

HOST = 'localhost'
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
    server_sock.bind((HOST, PORT))

    server_sock.listen(1)
    print('Listening ...')

    client_sock, client_ip = server_sock.accept()
    std_input = sys.stdin

    with client_sock:
        end = False

        while not end:
            readable, writeable, others = select([std_input, client_sock], [], [])

            for sock in readable:
                if sock == client_sock:
                    message = sock.recv(1024).decode()

                    if 'END' in message:
                        client_sock.send(bytes('END', 'utf-8'))
                        time.sleep(1)
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

                    message = '\033[93mServer at ' + str(datetime.now()) + ':\033[0m ' + text
                    client_sock.send(bytes(message, 'utf-8'))
