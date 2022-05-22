FROM python:3.8-slim-buster

RUN apt-get update && \
    apt-get install -y gcc python3-dev python3-geopandas

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3"]