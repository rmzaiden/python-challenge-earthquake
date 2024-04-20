FROM python:alpine3.19

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY logging.conf /app/logging.conf
COPY src/ ./
RUN chmod +x /app/main.py

USER appuser

ENTRYPOINT [ "python", "/app/main.py" ]