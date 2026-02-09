FROM python:3.11-slim

RUN apt-get update && apt-get install -y python3 python3-pip\
    gcc \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=False
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /app

COPY . .

RUN poetry install --no-interaction --no-ansi
