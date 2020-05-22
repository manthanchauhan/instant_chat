import socket
import time
import sys
from select import select
from datetime import datetime

# specifying server's ip address and port number to listen to.
# use private ip address
HOST = 'localhost'
PORT = 9999

# create a socket specifying address family as IPv4 (AF_INET) and protocol as TCP(SOCK_STREAM).
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:

    # bind the socket to the above specified ip address and port.
    server_sock.bind((HOST, PORT))

    # start listening to client connections, at max 1 client at a time.
    server_sock.listen(1)
    print('Listening ...')

    # accept any incoming client connections
    client_sock, client_ip = server_sock.accept()
    print('Connected')

    # capturing input stream to capture messages typed in terminal (to be sent to client).
    std_input = sys.stdin

    with client_sock:
        end = False

        # while none of the client & server generates 'END' request,
        # keep the communication going.
        while not end:

            # detect which of the `std_input` or `client_sock` are ready to read.
            readable, writeable, others = select([std_input, client_sock], [], [])

            # when client sends a message, `client_sock` will become readable
            # when you send some message, `std_input` will become readable

            # read every readable stream and show output on terminal
            for sock in readable:

                if sock == client_sock:
                    # read message sent by client
                    message = sock.recv(1024).decode()

                    # if client sends 'END', break the communication
                    if 'END' in message:
                        end = True
                        break

                    # else print client message on terminal
                    print(message, end='')
                else:
                    # read text entered at terminal (by you)
                    text = std_input.readline()

                    # if your request to END the communication
                    if 'END' in text:

                        # inform client to END his connection
                        client_sock.send(bytes('END', 'utf-8'))

                        # wait while message is being sent, before closing the connection
                        time.sleep(1)
                        end = True
                        break

                    # else print your message with proper formatting and colors.
                    print(u"\u001b[2A\u001b[k")
                    sys.stdout.write('\033[92mYou at ' + str(datetime.now()) + ':\033[0m ')
                    sys.stdout.write(text)
                    sys.stdout.flush()

                    # send the message to client
                    message = '\033[93mServer at ' + str(datetime.now()) + ':\033[0m ' + text
                    client_sock.send(bytes(message, 'utf-8'))
