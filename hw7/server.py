import socket
import sys
import time
import threading


def run_server(port=53210):
    serv_sock = create_serv_sock(port)
    client_id = 0
    while True:
        client_sock = accept_client_conn(serv_sock, client_id)
        t = threading.Thread(target=serve_client,
                             args=(client_sock, client_id))
        t.start()
        client_id += 1


def serve_client(client_sock, client_id):
    request = read_request(client_sock)
    if request is None:
        print(f'Client #{client_id} unexpectedly disconnected')
    else:
        response = handle_request(request)
        write_response(client_sock, response, client_id)


def create_serv_sock(serv_port):
    serv_sock = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM,
                              proto=0)
    serv_sock.bind(('', serv_port))
    serv_sock.listen()
    return serv_sock


def accept_client_conn(serv_sock, client_id):
    client_sock, client_addr = serv_sock.accept()
    print(f'Client #{client_id} connected '
          f'{client_addr[0]}:{client_addr[1]}')
    return client_sock


def read_request(client_sock):
    try:
        while True:
            message = client_sock.recv(1024)
            return f'OK, received your message: {message}'.encode('utf-8')

    except ConnectionResetError:
        return None


def handle_request(request):
    time.sleep(1)
    return request


def write_response(client_sock, response, client_id):
    client_sock.sendall(response)
    client_sock.close()
    print(f'Client #{client_id} has been served')


if __name__ == '__main__':
    run_server(port=53210)
