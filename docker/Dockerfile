FROM python:3.9.10-slim

# Prevents .pyc files from being written (they're not needed in containers).
ENV PYTHONDONTWRITEBYTECODE 1

# Ensures logs are shown in real-time in Docker (important for debugging and logging).
ENV PYTHONUNBUFFERED 1

# Install system dependencies
# RUN apt-get update && apt-get install -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./src/requirements.txt /app/src/requirements.txt
RUN pip install -r /app/src/requirements.txt

COPY ./src /app/src

COPY ./scripts /app/scripts

COPY docker/scripts/start_server.sh /app/start_server.sh
RUN chmod +x /app/start_server.sh

CMD ["/app/start_server.sh"]
