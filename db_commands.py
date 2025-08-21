import sqlite3
import os 

class DBWrapper: 
    def __init__(self, db_path):
        self.db_path = db_path
        self.connect()
        
    def __del__(self): 
        print("deleting")
        self.disconnect()
    
    def connect(self):
        """Connect to db"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
    def disconnect(self):
        """Disconnect from db"""
        self.conn.close()

    def create_word_table(self):
        """Initializes tables"""
        self.cursor.execute("CREATE TABLE word(word, sorted_word)")

    def add_words_to_table(self, words: list): 
        self.cursor.executemany("INSERT INTO word (word, sorted_word) VALUES (?, ?)", words)
        self.conn.commit()
    
    def get_matching_words(self, sorted_word): 
        self.cursor.execute(f"SELECT word FROM word WHERE sorted_word = '{sorted_word}';")
        results = self.cursor.fetchall()
        return results
