import sqlite3
import os 



class DBWrapper: 
    def __init__(self, db_path):
        self.db_path = db_path
        self.connect()
        
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        # The cursor object is used to execute SQL queries.

    def create_word_table(self):
        # Creates 
        self.cursor.execute("CREATE TABLE word(word)")
            # id TEXT

    def add_words_to_table(self, words): 
        if len(words) < 1: 
            return False
        
        sql_command = f"""INSERT INTO word VALUES
        ('{words[0]}')"""

        for word in words[1:]: 
            sql_command += f",\n('{word}')"

        # TODO remove this 
        print("The sql command")
        print(sql_command)
        self.cursor.execute(sql_command)
        
    # def create_db()

# Connect to a database file. If it doesn't exist, it will be created.
# You can also use ":memory:" to create a database in RAM for temporary use.
