from fastapi import FastAPI
import time 
import datetime
from db_commands import DBWrapper
from contextlib import asynccontextmanager
import time 
import os 


# TODO check what this page is really supposed to look like 

APP_STATE = os.environ.get('APP_STATE')
PROD = APP_STATE == 'PROD'
DB_PATH = f'db_file_{APP_STATE}.db'

def timer(func):
    def wrapper(*args, **kwargs):
        print('starting')
        print('*'*88)
        start = time.time()
        func(*args, **kwargs)
        length = time.time() - start
        print(f"Took {length} time")
    return wrapper

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initializes DB
    """
    print("Application starting up...")

    
    new_db = not os.path.exists(DB_PATH)

    db = DBWrapper(DB_PATH)
    if new_db: 
        print("current dir")
        print(os.listdir('Badatz-task'))
        print("Creating db")
        db.create_word_table()
        
        with open("Badatz-task/words_dataset.txt",'r') as f: 
            word_list = [word.strip() for word in f.readlines()]
        
        items_list = []
        for word in word_list: 
            sorted_word = "".join(sorted(list(word)))
            # letters = list(word)
            # letters.sort()
            # sorted_word = "".join(letters)

            items_list.append((word, sorted_word))
        db.add_words_to_table(items_list)
    db.disconnect()
    yield  # The application will run after this line
    # TODO shutdown db
    print("Application shutting down...")


app = FastAPI(lifespan=lifespan)


@timer
@app.get("/")
async def root(): 
    print("starting")
    time.sleep(8)
    print("finishing")
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"message": f"Hello World {t}"}

# TODO: create timer 
@app.get("/api/v1/similar")
async def get_similar_word(word=None):
    sorted_word = "".join(sorted(list(word)))
    db = DBWrapper(DB_PATH)
    return db.get_matching_words(sorted_word)




    


# GET   /api/v1/similar?word=stressed
# .lower() the word - turn into lowercase 
# Get the 'id' of our word - which is our word after it's sorted 
# Get the entry from the db of that id - if exists

# Post  /api/v1/add-word
# Get the 'id' of our word - use the function from GET 
# Create an entry in the db of the id with the word, if it exists add it to the list - otherwise create the entry 

# For the above functions get stats of how long each run took - maybe create decorator for this 

# GET /api/v1/stats
# TODO
