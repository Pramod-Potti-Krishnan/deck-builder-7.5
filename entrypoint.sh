#!/bin/bash
set -e

# Use PORT environment variable from Railway, or default to 8009
PORT=${PORT:-8009}

echo "Starting uvicorn on port $PORT"
exec uvicorn server:app --host 0.0.0.0 --port $PORT
