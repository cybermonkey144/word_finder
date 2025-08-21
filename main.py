from fastapi import FastAPI
import time 
import datetime
from db_commands import DBWrapper
from contextlib import asynccontextmanager
import os 


# TODO check what this page is really supposed to look like 

APP_STATE = os.environ.get('APP_STATE')
PROD = APP_STATE == 'PROD'
app = FastAPI()

@app.get("/")
async def root(): 
    print("starting")
    time.sleep(8)
    print("finishing")
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"message": f"Hello World {t}"}

@app.get("/api/v1/similar")
async def get_similar_word(word=None):
    return {"was": f"the word is {word}"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events for the application.
    """
    print("Application starting up...")
    db_path = f'db_file_{APP_STATE}.db'
    new_db = os.path.exists(db_path)
    db = DBWrapper(db_path)
    if new_db: 
        print("Creating db")
        db.create_word_table()
    yield  # The application will run after this line
    # TODO shutdown db
    print("Application shutting down...")


    


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
