import socket
import threading
import os
import sys

def recovery_message(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(data.decode('utf-8'))
        except:
            break

def send_message(client_socket):

    while True:
        message = input()
        sys.stdout.write('\033[F\033[K')
        print(f'Вы: {message}')

        if message == "exit":
            client_socket.close()
            return
        client_socket.send(message.encode('utf-8'))

os.system('cls')
name = input('Введите имя: ')
os.system('cls')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 5001))

client_socket.send(name.encode('utf-8'))

receive_thread = threading.Thread(target=recovery_message, args=(client_socket,))
receive_thread.start()

send_message(client_socket)