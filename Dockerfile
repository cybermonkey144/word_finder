FROM python:3.12

COPY requirements.txt requirements.txt 

EXPOSE 8000
RUN python3 -m pip install -r requirements.txt 