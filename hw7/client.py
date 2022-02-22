import socket


def get_message(host, port):

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((host, port))

    message = input('Type something here: ').encode('utf-8')
    client_sock.sendall(message)

    data = client_sock.recv(1024)
    print(data)
    client_sock.close()


if __name__ == '__main__':

    get_message('', 53210)
