# syntax=docker/dockerfile:1
 
FROM python:3.8-slim-buster

WORKDIR /opt/ayanami_bot/
COPY . .

RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]

ENV API_KEY=$API_KEY
