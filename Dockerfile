FROM python:3.9-slim

WORKDIR /src/scraper

RUN apt-get update && apt-get install -y \
    ca-certificates \
    && update-ca-certificates

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python scraper.py
