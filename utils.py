from datetime import datetime
from db_commands import DBWrapper
from env import DB_PATH


def add_stats(endpoint, start, end): 
    """Add stats to the DB"""
    try: 
        db = DBWrapper(DB_PATH)
        
        readable_start = datetime.fromtimestamp(start)
        readable_end = datetime.fromtimestamp(end)

        db.add_request_stat_to_table(endpoint,readable_start, readable_end, end-start)

    except: 
        print("Failed to add statistic, continue anyway")


def register_new_word(word): 
    """Registers new word in db - with it's sorted variant"""
    try: 
        db = DBWrapper(DB_PATH)
        sorted_word = "".join(sorted(list(word)))
        if not db.word_exists(word): 
            db.add_word_to_table(word, sorted_word)
        else: 
            print("Word already exists")
    except: 
        raise Exception("Failed to add new word to DB")

