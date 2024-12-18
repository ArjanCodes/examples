# Use an official Python runtime as a parent image
FROM ubuntu:20.04 AS builder-image

ARG DEBIAN_FRONTEND=noninteractive
# Prevent Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install --no-install-recommends -y python3.13 python3.13-dev python3.13-venv python3-pip python3-wheel build-essential curl ca-certificates && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh
# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-cffi \
        python3-brotli \
        libpango-1.0-0 \
        libpangoft2-1.0-0 \
        alembic \
        && rm -rf /var/lib/apt/lists/*

# Copy only the necessary files for Poetry installation
COPY pyproject.toml poetry.lock ./

# Install Poetry and project dependencies
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev \
    # Install the dotenv plugin for Poetry for loading environment variables
    && poetry self add poetry-dotenv-plugin

# Copy the rest of the application code into the container
COPY . .

# Expose the specified port for FastAPI
EXPOSE $PORT

# Start the application with Uvicorn in production mode, using environment variable references
CMD ["poetry", "run", "uvicorn", "main:app", "--log-level", "info", "--host", "0.0.0.0", "--port", "80"]
