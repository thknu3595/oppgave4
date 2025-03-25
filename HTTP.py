from socket import AF_INET, socket, SOCK_STREAM
import os

def handle_request(conn_sd):
    """Behandler en HTTP-forespørsel og sender et svar tilbake."""
    # Mottar forespørselen fra klienten
    request = conn_sd.recv(1024).decode()

    if not request:
        conn_sd.close()
        return

    print("HTTP Request:\n", request)

    # Splitter HTTP-forespørselen for å finne filbanen
    request_line = request.split("\n")[0]  # Første linje: "GET /index.html HTTP/1.1"
    parts = request_line.split()

    if len(parts) < 2 or parts[0] != "GET":
        conn_sd.close()
        return

    # Henter filnavnet (fjerner første '/')
    filename = parts[1][1:]
    if filename == "":
        filename = "index.html"  # Standard fil hvis ingen spesifikk er angitt

    # Sjekker om filen finnes
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            content = file.read()

        # Konstruerer HTTP 200 OK respons
        response_headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(content)}\r\n"
            "\r\n"
        )
        conn_sd.sendall(response_headers.encode() + content)

    else:
        # Sender HTTP 404 Not Found hvis filen ikke eksisterer
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n"
            "\r\n"
            "<html><body><h1>404 Not Found</h1></body></html>"
        )
        conn_sd.sendall(response.encode())

    conn_sd.close()

def main():
    """Starter en enkel HTTP-server."""
    server_sd = socket(AF_INET, SOCK_STREAM)
    port = 8080
    server_ip = '127.0.0.1'

    # Binder socketen til IP og port
    server_sd.bind((server_ip, port))

    # Starter å lytte for innkommende forbindelser
    server_sd.listen(1)
    print(f"Server kjører på http://{server_ip}:{port}/")

    while True:
        # Godtar en ny klientforbindelse
        conn_sd, addr = server_sd.accept()
        print(f"Tilkobling fra {addr}")

        # Behandler forespørselen
        handle_request(conn_sd)

if __name__ == "__main__":
    main()