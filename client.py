import socket
import sys

def main():
    if len(sys.argv) != 4:
        print("Penggunaan: python client.py server_host server_port filename")
        sys.exit(1)
    
    # Mengambil argumen dari command line
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]
    
    try:
        # Buat socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set timeout
        client_socket.settimeout(5)
        
        # Connect ke server
        print(f"Menghubungkan ke {server_host}:{server_port}")
        client_socket.connect((server_host, server_port))
        
        # Buat HTTP GET request
        request = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"
        
        # Kirim request
        print(f"Mengirim request untuk: /{filename}")
        client_socket.send(request.encode())
        
        # Terima response
        response = b""
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            response += data
        
        # Tampilkan response
        if response:
            print("Ditemukan:" if b"200 OK" in response else "Tidak ditemukan:")
            print(response.decode(errors='replace'))
        else:
            print("Respons kosong dari server.")
        
        client_socket.close()
        
    except socket.timeout:
        print(f"Error: Timeout ketika terhubung ke server di {server_host}:{server_port}.")
        print("Server mungkin terlalu lambat merespons atau tidak merespons.")
    except ConnectionRefusedError:
        print(f"Error: Tidak dapat terhubung ke server di {server_host}:{server_port}.")
        print("Pastikan server sedang berjalan dan port sudah benar.")
    except socket.gaierror:
        print(f"Error: Tidak dapat menemukan host '{server_host}'.")
        print("Periksa apakah nama host benar.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()