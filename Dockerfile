# Base
FROM python:3.11-slim

# Env
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CRYPTOGRAPHY_DONT_BUILD_RUST=1

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Python deps (cache friendly)
COPY requirements/ ./requirements/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements/production.txt

# Copy project
COPY . /app/

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
