import http.server
import os
import socketserver
import threading

import requests


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":

    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 8000
    Handler = http.server.SimpleHTTPRequestHandler  # Open a HTTP server to access to the current directory

    server = ThreadedTCPServer((HOST, PORT), Handler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print(f"Server {ip}:{port} loop running in thread {server_thread.name}")

    response = requests.get("http://127.0.0.1:8000/cinema_alien_debutant.json")
    print(response)

    server.shutdown()
    server.server_close()