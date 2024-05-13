import socket
import threading

class ChatServer:
    def __init__(self):
        self.host = 'localhost'
        self.port = 12345
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Servidor escuchando en", self.host, ":", self.port)

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Nueva conexión establecida desde {client_address}")
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print("Mensaje recibido:", message)
                self.broadcast(message, client_socket)
            except Exception as e:
                print("Error:", e)
                client_socket.close()
                self.clients.remove(client_socket)
                break

    def broadcast(self, message, sender_socket):
        for client_socket in self.clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except Exception as e:
                    print("Error al enviar mensaje:", e)
                    client_socket.close()
                    self.clients.remove(client_socket)

if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start()
