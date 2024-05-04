import os
import logging
import mysql.connector
from dotenv import load_dotenv

DATABASE_NAME = "DiscordBotDB"
logging.basicConfig(level=logging.INFO)

class DBController:
    """ Controls the python connection the MySQL database """

    def __init__(self):
        load_dotenv()
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password=os.getenv('DB_PASSWORD')
            )
            logging.info("Initialized connection to database.")
        except mysql.connector.Error as err:
            logging.error("Error connecting to database: %s", err)

    def __del__(self):
        """ Destructor to ensure database connection is closed when object is destroyed """
        if hasattr(self, 'db') and self.db.is_connected():
            self.db.close()
            logging.info("Closed database connection.")

    def execute_query(self, query, params=None, fetchone=False):
        """ Context manager for executing a query """
        try:
            with self.db.cursor() as cursor:
                cursor.execute(query, params)
                if fetchone:
                    return cursor.fetchone()
                return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            return None

    def store_message_info(self, author, content, timestamp):
        """ Adds a users message info to the db """
        try:
            with self.db.cursor() as cursor:
                cursor.execute(f"USE {DATABASE_NAME}")
                query = "INSERT INTO messages (author, content, sent_time) VALUES (%s, %s, %s)"
                value = (author, content, timestamp)
                cursor.execute(query, value)
                self.db.commit()
                logging.info("%s record(s) inserted.", cursor.rowcount)
        except mysql.connector.Error as err:
            logging.error("Error adding message info to database: %s", err)

    def check_user_exists(self, user_id: str):
        """ Checks if the user exists in the database """
        query = "SELECT user_id FROM users WHERE user_id = %s"
        result = self.execute_query(query, (user_id,), fetchone=True)
        if result:
            logging.info("Successfully found user %s in database.", user_id)
            return True
        logging.info("Could not find user %s in database.", user_id)
        return False

    def add_user(self, user_id: str):
        """ Adds to the users current balance """
        if not self.check_user_exists(user_id):
            query = "INSERT INTO (users) VALUES (%s)"
            self.execute_query(query, (user_id,))
            logging.info("User %s added to datbase successfully.", user_id)
        else:
            logging.error("User %s already exists in the database.", user_id)

    def add_gold(self, user_id: str, amount: int):
        """ Adds to the users current balance """
        current_balance = self.get_user_balance(user_id)
        if current_balance:
            new_balance = new_balance + amount
            query = "UPDATE users SET balance = %s WHERE user_id = %s"
            self.execute_query(query, (new_balance, user_id))
            logging.info("Gold added successfully.")
        else:
            logging.error("Could not get current balance.")

    def get_user_balance(self, user_id: str):
        """ Gets the users current balance """
        query = "SELECT balance FROM users WHERE user_id = %s"
        result = self.execute_query(query, (user_id,), fetchone=True)
        if result:
            return result[0]
        return None
