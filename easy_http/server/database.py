import sqlite3

def main():
    # Create a Database instance and demonstrate the usage of one of its functions
    data = Database()
    print(data.get_user_id_by_username("user 1"))


class Database:
    def __init__(self):
        """Initialize the Database instance """
        self.con = sqlite3.connect("users.sql")
        self.cur = self.con.cursor()

    def handle_home_screen(self, username):
        """Retrieve language progress information for a user"""
        user_id = self.get_user_id_by_username(username)

        # Fetch distinct language codes associated with the user
        self.cur.execute(f"SELECT DISTINCT language_code FROM LanguageProgress WHERE user_id = {user_id};")
        languages = self.cur.fetchall()

        language_and_stage = {}

        for language_tuple in languages:
            language = language_tuple[0]  # Extract the language from the tuple
            # Fetch the last stage and stage points for each language
            last_stage = self.cur.execute(
                f"SELECT stage, stage_points FROM LanguageProgress WHERE user_id = {user_id} AND language_code = '{language}' ORDER BY stage DESC LIMIT 1;").fetchone()
            language_and_stage[language] = last_stage

        return language_and_stage

    def get_all_usernames(self):
        """Get a list of all usernames from the 'users' table."""
        return self.cur.execute("SELECT username FROM users").fetchall()

    def get_password_by_username(self, username):
        """Get the password associated with a given username."""
        return self.cur.execute(f"SELECT password FROM users WHERE username = '{username}';").fetchone()

    def create_user(self, username, password):
        """Create a new user in the 'users' table."""
        self.cur.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}');")
        self.con.commit()

    def delete_user_by_username(self, username):
        """Delete a user from the 'users' table based on the username."""
        self.cur.execute(f"DELETE FROM users WHERE username = '{username}';")
        self.con.commit()

    def update_user(self, old_username, new_username, new_password):
        """Update the username and password of a user in the 'users' table."""
        id = self.cur.execute(f"SELECT id FROM users WHERE username = '{old_username}';").fetchone()[0]
        self.cur.execute(f"UPDATE users SET username = '{new_username}', password = '{new_password}' WHERE id = {id};")
        self.con.commit()

    def get_user_id_by_username(self, username):
        """Get the user ID associated with a given username."""
        return self.cur.execute(f"SELECT id FROM users WHERE username = '{username}'").fetchone()[0]

    def get_user_by_id(self, id):
        """Get the username and password associated with a given user ID."""
        return self.cur.execute(f"SELECT username, password FROM users WHERE id = {id}")

    def get_all_stages(self, username, language_code):
        """Get all stages and stage points for a user in a specific language."""
        user_id = self.get_user_id_by_username(username)

        # Fetch all stages and stage points for the user ID and language code
        stages = self.cur.execute(
            f"SELECT stage, stage_points FROM LanguageProgress WHERE user_id = {user_id} AND language_code = '{language_code}';").fetchall()

        stages_dic = {}

        for stage in stages:
            stages_dic[stage[0]] = stage[1]

        return stages_dic

    def get_all_languages(self, id):
        """Get all distinct languages that a user is learning."""
        return self.cur.execute(f"SELECT DISTINCT language_code FROM LanguageProgress WHERE user_id = {id};")

    def close(self):
        """Close the database connection."""
        self.con.close()


if __name__ == "__main__":
    main()
