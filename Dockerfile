# Use official Playwright Python base image (includes all dependencies and browsers)
FROM mcr.microsoft.com/playwright/python:v1.48.0-noble

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8009

# Expose port (Railway will override with $PORT)
EXPOSE 8009

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8009/', timeout=5)" || exit 1

# Start command - Railway will set $PORT automatically
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port ${PORT:-8009}"]
