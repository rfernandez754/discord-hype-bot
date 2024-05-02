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
