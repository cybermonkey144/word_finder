import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import JSONResponse, Response
import os 
import time 
from typing import Annotated

from db_commands import DBWrapper
from env import APP_STATE, DB_PATH
from utils import add_stats, register_new_word


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initializes DB if required 
    """
    print("Application starting up...")
    
    # Check whether we need to initialize a new DB
    new_db = not os.path.exists(DB_PATH)

    if new_db: 
        db = DBWrapper(DB_PATH)
        # Creating db 
        db.create_tables()
        
        # Migrate .txt conent to DB
        with open("Badatz-task/words_dataset.txt",'r') as f: 
            word_list = [word.strip() for word in f.readlines()]
        
        # Each word has a 'sorted' version which will be a more efficient way to find 'similar' words 
        items_list = []
        
        for word in word_list: 
            sorted_word = "".join(sorted(list(word)))
            items_list.append((word, sorted_word))
        
        db.add_words_to_table(items_list)
        db.disconnect()

    else: 
        pass
        # Consider adding DB healthcheck
    yield 


app = FastAPI(lifespan=lifespan)


@app.get("/api/v1/similar")
async def get_similar_word(word=None):
    """Will find words with same letters"""
    try: 
        start = time.time()
        
        db = DBWrapper(DB_PATH)

        sorted_word = "".join(sorted(list(word)))
        similar_words = db.get_matching_words(sorted_word)
        add_stats('/api/v1/similar', start, time.time())
        
        return JSONResponse(content=similar_words, status_code=200)
    except: 
        raise HTTPException(status_code=400)


@app.post("/api/v1/add-word")
def add_word(word: Annotated[str, Body(embed=True)]
):
    """Adds new word to DB"""
    try: 
        start = time.time()
        register_new_word(word)
        add_stats('/api/v1/add-word', start, time.time())
        print("84")
        return Response(status_code=200)
    except: 
        raise HTTPException(status_code=400)


@app.get("/api/v1/stats")
async def get_statistics():
    """Gets server statistics"""
    db = DBWrapper(DB_PATH)
    number_of_words = db.get_number_of_words()
    stats_similar_endpoint = db.endpoint_request_count("/api/v1/similar")
    average_processing_time = db.get_average_stats()

    content = {
        "avgProcessingTimeMs": average_processing_time,
        "totalWords": number_of_words, 
        "totalRequests": stats_similar_endpoint
    }
    return JSONResponse(content = content, status_code=200)

