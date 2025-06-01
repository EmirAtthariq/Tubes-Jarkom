import socket
import threading
import os

def handle_client(connection_socket, client_address):
    try:
        request = connection_socket.recv(1024).decode()
        print(f"[REQUEST from {client_address}]:\n{request}")
        
        # Menghapus "/" dari nama file
        filename = request.split()[1][1:] 

        #kirim response
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                content = f.read()
            header = "HTTP/1.1 200 OK\r\n"
            header += f"Content-Length: {len(content)}\r\n"
            header += "Content-Type: text/html\r\n\r\n"
            response = header.encode() + content
        else:
            response = b"HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>"

        connection_socket.sendall(response)
    except Exception as e:
        print(f"[ERROR]: {e}")
    finally:
        connection_socket.close()

def start_server(server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(5)
    print(f"[SERVER RUNNING] Listening on port {server_port}...")

    # Membuat thread baru ketika client connect ke server
    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()
        print(f"[NEW CONNECTION] {addr} connected.")

if __name__ == "__main__":
    PORT = 6789  # Port yang berjalan pada server
    start_server(PORT)
