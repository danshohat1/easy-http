import subprocess
from chat_server import Chat_Server
import threading
import socket

chat_server_port = None
chat_server_running = False
peerjs_port = None

class Chat_Handler:
    @staticmethod
    def find_available_port(start_port, max_attempts=10):
        """Find an available port in the specified range."""
        for _ in range(max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(5)
                    sock.connect(("127.0.0.1", start_port))
            except:
                return start_port
            start_port += 1
        return None

    def create_chat(self, lang, start_port=5000):
        """Create a new chat with the specified language"""
        global chat_server_running
        global peerjs_port
        global chat_server_port

        # Find an available port for PeerJS server
        available_port = self.find_available_port(start_port)
        peerjs_port = available_port

        # Start the PeerJS server in a separate thread
        command = f"peerjs --port {peerjs_port}"
        func = lambda: subprocess.run(command, shell=True)
        t1 = threading.Thread(target=func)
        t1.start()

        # Create and start the Chat Server
        chat_server = Chat_Server(lang)
        chat_server_port = chat_server.port

        # Set the flag indicating that the chat server is running
        chat_server_running = True

    @staticmethod
    def get_peerjs_port():
        """Get the port on which the PeerJS server is running."""
        global peerjs_port
        return peerjs_port

    @staticmethod
    def get_chat_server_port():
        """Get the port on which the Chat Server is running."""
        global chat_server_port
        return chat_server_port

    @staticmethod
    def get_chat_server_running():
        """Check if the Chat Server is running."""
        global chat_server_running
        return chat_server_running
