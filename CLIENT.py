import argparse
from socket import *

def send_http_request(server_ip, server_port, file_path):
    """Metode som sender request """
    # Opprett en TCP-klient
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # Bygger HTTP GET-forespørselen
    http_request = f"GET {file_path} HTTP/1.1\r\nHost: {server_ip}\r\nConnection: close\r\n\r\n"
    client_socket.send(http_request.encode())

    # Mottar og skriver ut responsen
    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data

    print(response.decode())

    client_socket.close()

if __name__ == "__main__":
    # Definer kommandolinjeargumenter
    parser = argparse.ArgumentParser(description="Simple HTTP Client")
    parser.add_argument("-i", "--ip", required=True, help="Server IP address")
    parser.add_argument("-p", "--port", type=int, required=True, help="Server port")
    parser.add_argument("-f", "--file", required=True, help="Filename or path to request")

    # Parse argumentene
    args = parser.parse_args()

    # Kjør HTTP-forespørselen
    send_http_request(args.ip, args.port, args.file)










