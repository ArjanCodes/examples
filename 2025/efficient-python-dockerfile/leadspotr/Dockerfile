# Use an official Python runtime as a parent image
FROM python:3.13-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential \
        alembic && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download the latest installer, install it and then remove it
ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh

COPY ./pyproject.toml . 

RUN /root/.local/bin/uv sync

FROM python:3.13-slim-bookworm AS production
# COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /.venv /.venv
ENV PATH="/.venv/bin:{$PATH}"
# To not store everything in the root directory
WORKDIR /leadspotr

# The COPY target location is NOT relative to the WORKDIR, if you are using the full path
COPY /app /leadspotr/app

# This is relative to the WORKDIR
COPY main.py main.py

# Expose the specified port for FastAPI
EXPOSE $PORT

RUN ls -la

# Start the application with Uvicorn in production mode, using environment variable references
CMD ["uvicorn", "main:app", "--log-level", "info", "--host", "0.0.0.0" , "--port", "80"]

FROM python:3.13-bookworm AS development

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]



