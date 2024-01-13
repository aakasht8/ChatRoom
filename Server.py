import threading
import socket

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


# Receive the message
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            print('Exception Occurred!!')
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat room!!'.encode('ascii'))
            nicknames.remove(nickname)
            break


# The main function to create a thread for the client
def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of connected client is: {nickname}')
        broadcast(f'{nickname} joined the chat \n'.encode('ascii'))
        client.send('Connected to the server'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print('Server is listening....')
receive()




