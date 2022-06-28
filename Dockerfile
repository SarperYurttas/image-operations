FROM python:3.9-slim


RUN apt-get update && \
    apt-get install -y build-essential  && \
    apt-get install -y wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app


ENTRYPOINT gunicorn -w 4 --bind 0.0.0.0:8080 run:app