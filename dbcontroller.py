import os
import mysql.connector
from dotenv import load_dotenv

DATABASE_NAME = "DiscordBotDB"

class DBController:
    """ Controls the python connection the MySQL database """

    db = None

    def __init__(self):
        load_dotenv()
        self.db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv('DB_PASSWORD')
        )
        print(f"Initiated connection to databse: {self.db}")

    def add_message_info(self, author, content, timestamp):
        """ Adds a users message info to the db """
        mycursor = self.db.cursor()
        mycursor.execute(f"USE {DATABASE_NAME}")
        query = "INSERT INTO messages (author, content, sent_time) VALUES (%s, %s, %s)"
        value = (author, content, timestamp)
        mycursor.execute(query, value)

        self.db.commit()

        print(mycursor.rowcount, "record inserted.")

