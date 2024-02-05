import socket
import threading
from server_data import *
from http_handler import Http_Handler


def main():
    """Main function to start the server."""
    Server()


class Server:
    def __init__(self):
        """Initialize the server by creating and configuring the server
        socket, then start handling clients."""
        self.server_socket = self.initiate_server()
        self.handle_clients()

    def initiate_server(self):
        """Create and configure the server socket."""
        # Create a socket using IPv4 and TCP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the specified IP address and port
        server_socket.bind((IP, PORT))
        # Set the server to listen for incoming connections with a maximum backlog of 10
        server_socket.listen(10)
        # Print a message indicating that the server is running
        print(f"The server is running at port: {PORT}")
        # Return the configured server socket
        return server_socket

    def handle_clients(self):
        """Continuously accept and handle incoming client connections."""
        while True:
            # Accept a client connection, blocking until a connection is received
            conn, addr = self.server_socket.accept()
            # Create a new thread to handle the client independently
            clnt_thread = threading.Thread(target=self.handle_single_client, args=(conn,))
            # Start the client-handling thread
            clnt_thread.start()

    def handle_single_client(self, client):
        """Handle a single client connection by creating an instance of the
        Http_Handler class."""
        # Create an instance of the Http_Handler class to handle HTTP requests
        # from the client
        client_http = Http_Handler(client)


if __name__ == "__main__":
    """Entry point of the script, calling the main function."""
    main()
