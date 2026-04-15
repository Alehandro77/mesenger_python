import socket
import threading

clients = []
clients_lock = threading.Lock()

def handle_client(client_socket, client_address):

    name = client_socket.recv(1024).decode('utf-8')

    print(f'Клиент {name} подключён')

    for client in clients:
        if client == client_socket:
                continue
        client.send(f'{name} подключился'.encode('utf-8'))

    client_socket.send(f'Добро пожаловать в чат {name}!'.encode('utf-8'))

    try:
        while True:

            message = client_socket.recv(1024).decode('utf-8')

            if not message:
                break

            for client in clients:

                if client == client_socket:
                    continue

                client.send(f'{name}: {message}'.encode('utf-8'))

            print(f'От {name} пришло:', message)

    except:

        with clients_lock:
            if client_socket in clients:
                clients.remove(client_socket)

        client_socket.close()

        for client in clients:
            client.send(f'{name} отключился'.encode('utf-8'))

        print(f'Клиент {name} отключился')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', 5001))
server_socket.listen()

print('Сервер ждёт подключения клиентов')

while True:
    client_socket, client_address = server_socket.accept()

    with clients_lock:
        clients.append(client_socket)

    thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()