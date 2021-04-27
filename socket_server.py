from multiprocessing import Process, Lock, Manager
import protocol
import socket

def server_start():
    server_socket = socket.socket()
    host = '127.0.0.1'
    port = 5001

    dataset=[]
    try:
        server_socket.bind((host, port))
    except socket.error as e:
        server_socket.close()
        return

    while True:
        try:
            client, address = server_socket.accept()
            print('Connected to: {}:{}'.format(address[0], address[1]))

            # SYNC START
            # receive request

            request_data = protocol.receive_data(client)
            dataset += [request_data]

            client.close()

        except Exception as e:
            print('Server Exception: {}'.format(e))
            break
    server_socket.close()

if __name__=='__main__':
    server_start()