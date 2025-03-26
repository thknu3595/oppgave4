import argparse
import threading
from socket import *

def send_http_request(server_ip, server_port, file_path):
    """Sender en HTTP GET-forespørsel til serveren"""
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((server_ip, server_port))

        http_request = f"GET {file_path} HTTP/1.1\r\nHost: {server_ip}\r\nConnection: close\r\n\r\n"
        client_socket.send(http_request.encode())

        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        print(f"\n--- Response fra {server_ip}:{server_port} ---\n")
        print(response.decode(errors="ignore"))

    except Exception as e:
        print(f"Feil: {e}")

    finally:
        client_socket.close()

def start_threads(server_ip, server_port, file_path, num_threads):
    """Starter flere tråder for å sende HTTP-forespørsler samtidig"""
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=send_http_request, args=(server_ip, server_port, file_path))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multithreaded HTTP Client")
    parser.add_argument("-i", "--ip", required=True, help="Server IP address")
    parser.add_argument("-p", "--port", type=int, required=True, help="Server port")
    parser.add_argument("-f", "--file", required=True, help="Filename or path to request")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Number of threads (requests)")

    args = parser.parse_args()

    # Starter flere tråder for å sende HTTP-forespørsler parallelt
    start_threads(args.ip, args.port, args.file, args.threads)

