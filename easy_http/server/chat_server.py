import eventlet
import socketio
import socket

from server_data import PORT, IP
import threading

LOCALHOST = "127.0.0.1"
START_PORT = 3000

groups = {

}


class Chat_Server:

    # Initialize the socket.io server and application
    global sio, app
    sio = socketio.Server(cors_allowed_origins="*")
    app = socketio.WSGIApp(sio)

    def __init__(self, chat_lang):
        """Initialize the Chat_Server"""
        self.lang = chat_lang

        # Find an open port and start the server on that port
        self.port = self.check_open_port(START_PORT)
        print("in server")
        print(f"Chat server is running at port {self.port}, updating chats")

        # Create a thread to run the socket.io server
        func = lambda: eventlet.wsgi.server(eventlet.listen((IP, self.port)), app)
        run = threading.Thread(target= func)
        run.start()

        # Check for new connections
        self.check()

    @staticmethod
    def is_port_open(port):
        """Check if a given port is open."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.bind(("0.0.0.0", port))
            sock.close()
            return True
        except:
            return False

    def check_open_port(self, start_port):
        """Find the first open port starting from a specified port."""
        while not self.is_port_open(start_port):
            start_port += 1
        return start_port

    def check(self):
        """Define and handle socket.io events for new connections"""

        @sio.event()
        def new_connection(sid, lang):
            """Handle a new connection event."""
            if lang in groups.keys():
                # Inform existing users in the group about the new user
                for user_sid in groups[lang]:
                    sio.emit("user_connected", sid, room=user_sid)

                groups[lang].append(sid)
            else:
                groups[lang] = [sid]

        @sio.event
        def disconnect(sid):
            """Handle a disconnection event."""
            print(f"User disconnected: {sid}")

            # Find the language associated with the disconnected user
            user_lang = [lang for lang, sids in groups.items() for user_sid in sids if user_sid == sid][0]

            # Inform remaining users in the group
            for user_sid in groups[user_lang]:
                if user_sid != sid:
                    sio.emit("user_disconnected", sid, room=user_sid)

            # Remove the disconnected user from the group
            groups[user_lang].remove(sid)

        @sio.event
        def peer(sid, target_sid, id, username):
            """Handle a peer communication event."""
            # Emit a 'peer' event to the target user with relevant details
            sio.emit("peer", {"user_id": id, "sender_sid": sid, "username": username}, room=target_sid)
            print("Peer sent to " + target_sid)

        @sio.event
        def get_peer_id(sid, target_sid, id, username):
            """Handle a get peer ID event."""
            print(id)
            # Emit a 'get_peer_id' event to the target user with relevant details
            sio.emit("get_peer_id", {"peer_id": id, "sender_sid": sid, "username": username}, room=target_sid)
            print("Peer sent to " + target_sid)
