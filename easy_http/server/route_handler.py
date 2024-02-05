from database import Database
from chat_handler import *
route_map = {}
OK = "200 OK"
UNAUTHORIZED = "401 Unauthorized"

class Route_handler:
    @staticmethod
    def route(path):
        """Decorator to register a function as a route handler for a specific path."""
        def _route(f):
            route_map[path] = f
            return

        return _route

    @staticmethod
    @route("/signup_post")
    def signup_post(*args):
        """Handle the signup POST request to create a new user."""
        update_users = Datbase()

        # Check if the username already exists
        check = any(args[0] == username[0] for username in update_users.get_all_usernames())

        if check:
            return "User already exists", OK

        # Create a new user
        update_users.create_user(args[0], args[1])
        update_users.close()
        return "User created successfully", OK

    @staticmethod
    @route("/update_user_put")
    def update_user_put(*args):
        """Handle the update user PUT request to modify user information."""
        print("in update")
        update_users = Datbase()
        update_users.update_user(args[0], args[1], args[2])
        update_users.close()
        print(args)
        print("here")
        return "User updated successfully", OK

    @staticmethod
    @route("/password_get")
    def password_get(*args):
        """Handle the password GET request to retrieve a user's password."""
        password_db = Datbase()
        password = password_db.get_password_by_username(args[0])
        password_db.close()

        return password, OK

    @staticmethod
    @route("/update_user_delete")
    def update_user_delete(*args):
        """Handle the update user DELETE request to delete a user."""
        update_users = Datbase()
        update_users.delete_user_by_username(args[0])
        update_users.close()

        return "User deleted successfully", OK

    @staticmethod
    @route("/login_post")
    def login_post(*args):
        """Handle the login POST request to authenticate a user."""
        database = Datbase()

        # Check if the username exists
        check = any(args[0] == username[0] for username in database.get_all_usernames())

        if not check:
            return f"Username '{args[0]}' is not recognized in the system.", OK

        # Check if the provided password is valid
        if args[1] == database.get_password_by_username(args[0])[0]:
            return "Logged in successfully", OK

        return "Your password is invalid. Please try again.", OK

    @staticmethod
    @route(f"/home_screen_get")
    def home_screen_get(*args):
        """Handle the home screen GET request to retrieve user language progress."""
        database = Datbase()

        # Retrieve and return language progress information for the user
        home = database.handle_home_screen(args[0])

        database.close()
        return home, OK

    @staticmethod
    @route(f"/all_stages_by_language_get")
    def all_stages_by_language_get(*args):
        """Handle the all stages by language GET request to retrieve all stages for a user in a specific language."""
        database = Datbase()

        # Retrieve and return all stages for the user in the specified language
        stages = database.get_all_stages(args[0], args[1])

        database.close()

        return stages, OK

    @staticmethod
    @route(f"/join_chat_get")
    def join_chat_get(*args):
        """Handle the join chat GET request to create or join a chat session."""
        # Index 0 is the chat language
        c = Chat_Handler()

        if c.get_chat_server_running():
            return {"io_port": c.get_chat_server_port(), "peer_port": c.get_peerjs_port()}, OK

        # Create a new chat session
        c.create_chat(args[0])
        return {"io_port": c.get_chat_server_port(), "peer_port": c.get_peerjs_port()}, OK
