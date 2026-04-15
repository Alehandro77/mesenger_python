import socket
import threading

clients = []
clients_lock = threading.Lock()

def broadcast(message, send_socket=None):
    with clients_lock:
        copy_clients = clients.copy()

    for client in copy_clients:
        if client == send_socket:
            continue
        try:
            client.send(message.encode('utf-8'))
        except:
            pass

def handle_client(client_socket, client_address):

    name = client_socket.recv(1024).decode('utf-8')

    print(f'Клиент {name} подключён')
    broadcast(f'{name} подключился', client_socket)

    client_socket.send(f'Добро пожаловать в чат {name}!'.encode('utf-8'))

    try:
        while True:

            message = client_socket.recv(1024).decode('utf-8')

            if not message:
                break

            broadcast(f'{name}: {message}', client_socket)
            print(f'От {name} пришло:', message)

    except:
        pass

    finally:
        with clients_lock:
            if client_socket in clients:
                clients.remove(client_socket)

        broadcast(f'{name} отключился')
        client_socket.close()
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
