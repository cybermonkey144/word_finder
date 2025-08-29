# Similar word finder 
## Basic description
The key of the method to finding similar words, is to find words which are the same when sorted
For every word we put in the DB, we add it's 'sorted' version to the DB by it's side
So, for example, when we're looking for a similar words to 'train' - we'll search the DB's 'sorted words' for 'ainrt' (which is train sorted)

Used FastAPI as the framework

## Running locally 
To run the code just run the command  `docker-compose up --build -d`
Originally built this around having a 'dev' and 'prod' environments (handled by ENV variable)
But for now it's just handled together 

There's a docker compose which uses an image built by local Dockerfile 
The docker compose runs the code and exposes the port 8002
To access the docs, just go to localhost:8002/docs