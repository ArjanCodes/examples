#!/bin/sh
# ------------------------------------------------------------------------------
# Docker Entrypoint for the FastAPI + Uvicorn app
# ------------------------------------------------------------------------------
# This script:
#   - Reads runtime configuration from environment variables
#   - Defaults to safe production values
#   - Executes Uvicorn as PID 1 child (so Tini can manage signals cleanly)
# ------------------------------------------------------------------------------

set -e  # Exit on any error
set -u  # Treat unset variables as errors

# ----------------------------- Runtime Config ----------------------------- #
# Host, Port, and Worker Count can be overridden at runtime:
UVICORN_HOST="${UVICORN_HOST:-0.0.0.0}"
UVICORN_PORT="${APP_PORT:-8080}"
UVICORN_WORKERS="${UVICORN_WORKERS:-2}"
UVICORN_LOG_LEVEL="${UVICORN_LOG_LEVEL:-info}"

# Application entrypoint (FastAPI app path)
APP_IMPORT_PATH="${UVICORN_APP_IMPORT_PATH:-src.main:app}"

# ----------------------------- Logging Startup ---------------------------- #
echo "[Entrypoint] Starting FastAPI app via Uvicorn"
echo "[Entrypoint] Host: ${UVICORN_HOST}"
echo "[Entrypoint] Port: ${UVICORN_PORT}"
echo "[Entrypoint] Workers: ${UVICORN_WORKERS}"
echo "[Entrypoint] Log Level: ${UVICORN_LOG_LEVEL}"
echo "[Entrypoint] App Import Path: ${APP_IMPORT_PATH}"

# ----------------------------- Run Uvicorn ------------------------------- #
# exec replaces the shell with uvicorn so it receives signals directly.
exec uvicorn "${APP_IMPORT_PATH}" \
    --host "${UVICORN_HOST}" \
    --port "${UVICORN_PORT}" \
    --workers "${UVICORN_WORKERS}" \
    --log-level "${UVICORN_LOG_LEVEL}"