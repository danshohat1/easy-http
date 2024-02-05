import socket
import threading
from .models.response import Response
from typing import Tuple

IP = "0.0.0.0"

class Server:
    def __init__(self, port: int):
        self.port = port
    
    def run(self): 
        self.server_socket = self.initiate_server(self.port)
        threading.Thread(target=self.handle_clients).start()
    
    def initiate_server(self, port):
        """Create and configure the server socket."""
        # Create a socket using IPv4 and TCP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the specified IP address and port
        server_socket.bind((IP, port))
        # Set the server to listen for incoming connections with a maximum backlog of 10
        server_socket.listen(10)
        
        # Return the configured server socket
        return server_socket

    def handle_clients(self):
        """Continuously accept and handle incoming client connections."""
        while True:
            # Accept a client connection, blocking until a connection is received
            conn, addr = self.server_socket.accept()
            # Create a new thread to handle the client independently
            clnt_thread = threading.Thread(target=self.handle_single_client, args=(conn,addr))
            # Start the client-handling thread
            clnt_thread.start()

