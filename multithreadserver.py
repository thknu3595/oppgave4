from socket import AF_INET, socket, SOCK_STREAM
import os
import threading

def handle_request(conn_sd):
    """Behandler en HTTP-forespørsel og sender et svar tilbake."""
    try:
        request = conn_sd.recv(1024).decode()
        if not request:
            conn_sd.close()
            return

        print("HTTP Request:\n", request)

        request_line = request.split("\n")[0]  # Første linje: "GET /index.html HTTP/1.1"
        parts = request_line.split()

        if len(parts) < 2 or parts[0] != "GET":
            conn_sd.close()
            return

        filename = parts[1][1:] if parts[1] != "/" else "index.html"

        if os.path.exists(filename):
            with open(filename, "rb") as file:
                content = file.read()
            response_headers = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(content)}\r\n"
                "\r\n"
            )
            conn_sd.sendall(response_headers.encode() + content)
        else:
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html\r\n"
                "\r\n"
                "<html><body><h1>404 Not Found</h1></body></html>"
            )
            conn_sd.sendall(response.encode())
    finally:
        conn_sd.close()

def main():
    """Starter en multithreaded HTTP-server."""
    server_sd = socket(AF_INET, SOCK_STREAM)
    port = 8080
    server_ip = '127.0.0.1'
    server_sd.bind((server_ip, port))
    server_sd.listen(5)  # Lytt på opptil 5 samtidige forbindelser
    print(f"Server kjører på http://{server_ip}:{port}/")

    while True:
        conn_sd, addr = server_sd.accept()
        print(f"Tilkobling fra {addr}")
        client_thread = threading.Thread(target=handle_request, args=(conn_sd,))
        client_thread.start()

if __name__ == "__main__":
    main()
