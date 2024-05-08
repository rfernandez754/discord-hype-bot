""" Module handles the communications with the MySQL Database. """
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
        self.execute_query(f"USE {DATABASE_NAME}")
        query = "INSERT INTO messages (author, content, sent_time) VALUES (%s, %s, %s)"
        value = (author, content, timestamp)
        self.execute_query(query, value)
        self.db.commit()

    def check_user_exists(self, user_id: str):
        """ Checks if the user exists in the database """
        self.execute_query(f"USE {DATABASE_NAME}")
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
            self.execute_query(f"USE {DATABASE_NAME}")
            query = "INSERT INTO users (user_id) VALUES (%s)"
            self.execute_query(query, (user_id,))
            logging.info("User %s added to datbase successfully.", user_id)
        else:
            logging.error("User %s already exists in the database.", user_id)

    def add_gold(self, user_id: str, amount: int):
        """ Adds to the users current balance """
        current_balance = self.get_user_balance(user_id)
        new_balance = current_balance + amount
        self.execute_query(f"USE {DATABASE_NAME}")
        query = "UPDATE users SET balance = %s WHERE user_id = %s"
        self.execute_query(query, (new_balance, user_id))
        self.db.commit()
        logging.info("Gold added successfully.")

    def subtract_gold(self, user_id: str, amount: int):
        """ Remove from the users current balance """
        current_balance = self.get_user_balance(user_id)
        new_balance = max(0, current_balance - amount)
        self.execute_query(f"USE {DATABASE_NAME}")
        query = "UPDATE users SET balance = %s WHERE user_id = %s"
        self.execute_query(query, (new_balance, user_id))
        self.db.commit()
        logging.info("Gold removed successfully.")

    def get_user_balance(self, user_id: str):
        """ Gets the users current balance. If user not in database """
        self.execute_query(f"USE {DATABASE_NAME}")
        query = "SELECT balance FROM users WHERE user_id = %s"
        result = self.execute_query(query, (user_id,), fetchone=True)
        if result:
            return result[0]
        # User not in db so lets add them and return a starting balance of 0
        self.add_user(user_id)
        return 0

    def check_if_new_biggest_fish(self, fish_species: str, fish_rarity: int, fish_size: float, user_id: str) -> bool:
        """
        Updates the fish leaderboard if the fish is a new biggest fish.

        args:
            fish_species (str): The species of the fish
            fish_rarity (int): An mapped int assigned to the given rarity
            fish_size (float): Size of the fish
            user_id (str): Discord id of the user that caught the fish

        Returns:
            bool: True if new biggest fish, else False
        """
        self.execute_query(f"USE {DATABASE_NAME}")
        query = "SELECT max_size_cm FROM biggest_fish WHERE fish_species = %s AND user_id = %s"
        result = self.execute_query(query, (fish_species, user_id), fetchone=True)
        if result and fish_size > float(result[0]):
            # Update the fish with the new biggest
            query = "UPDATE biggest_fish SET max_size_cm = %s, user_id = %s WHERE fish_species = %s"
            self.execute_query(query, (fish_size, user_id, fish_species))
            self.db.commit()
            return True
        if result:
            # Did not catch the new biggest fish
            return False
        # First person to catch the fish
        query = "INSERT INTO biggest_fish (fish_species, fish_rarity, max_size_cm, user_id) " \
                "VALUES (%s, %s, %s, %s)"
        value = (fish_species, fish_rarity, fish_size, user_id)
        self.execute_query(query, value)
        self.db.commit()
        return True

    def get_fish_leaderboard(self) -> str:
        """ Returns the result of querying the biggest_fish table in the database. """        
        self.execute_query(f"USE {DATABASE_NAME}")
        query = "SELECT fish_species, max_size_cm, user_id FROM biggest_fish ORDER BY fish_rarity"
        result = self.execute_query(query)
        return result
