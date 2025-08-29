import sqlite3
import os 

class DBWrapper: 
    def __init__(self, db_path):
        self.db_path = db_path
        self.connect()
        
    def __del__(self): 
        self.disconnect()
    
    def connect(self):
        """Connect to db"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
    def disconnect(self):
        """Disconnect from db"""
        self.conn.close()

    def create_tables(self):
        """Initializes tables"""
        self.cursor.execute("CREATE TABLE word(word, sorted_word)")
        self.cursor.execute("CREATE TABLE requests_stats(endpoint, start, end, length)")


    def add_words_to_table(self, words: list): 
        """Add many words to the table, gets the words in the format of a list of tuples"""
        self.cursor.executemany("INSERT INTO word (word, sorted_word) VALUES (?, ?)", words)
        self.conn.commit()

    def add_word_to_table(self, word, sorted_word): 
        """Add single word to word table"""
        self.cursor.execute("INSERT INTO word (word, sorted_word) VALUES (?, ?)", (word, sorted_word))
        self.conn.commit()
    
    def add_request_stat_to_table(self, endpoint, start, end, length): 
        """Add single entry to stat table"""
        self.cursor.execute("INSERT INTO requests_stats (endpoint, start, end, length) VALUES (?, ?, ?, ?)", (endpoint, start, end, length))
        self.conn.commit()
        print("added stats")
        print(length)

    def word_exists(self, word): 
        self.cursor.execute(f"SELECT word FROM word WHERE word = '{word}';")
        return bool(self.cursor.fetchall())
    
    def get_matching_words(self, sorted_word): 
        self.cursor.execute(f"SELECT word FROM word WHERE sorted_word = '{sorted_word}';")
        results = self.cursor.fetchall()
        return results
    
    def get_number_of_words(self): 
        """Get number of words in DB"""
        self.cursor.execute("SELECT COUNT(*) FROM word")
        result = self.cursor.fetchone()

        return  result[0]
    
    def endpoint_request_count(self,endpoint_name): 
        """Will return how many times endpoint_name has been accessed"""
        self.cursor.execute("SELECT COUNT(*) FROM requests_stats WHERE endpoint = ?", (endpoint_name,))
    
        count_tuple = self.cursor.fetchone()
        
        return count_tuple[0]
        
    def get_average_stats(self):
        self.cursor.execute("SELECT AVG(length) FROM requests_stats")
        average_length = self.cursor.fetchone()[0]
        return average_length