# Use official Playwright Python base image (includes framework, browsers installed separately)
FROM mcr.microsoft.com/playwright/python:v1.48.0-noble

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (CRITICAL: Required for PDF/PPTX generation)
RUN playwright install --with-deps chromium

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8009

# Expose port (Railway will override with $PORT)
EXPOSE 8009

# Start command - Use $PORT which Railway sets, or defaults to 8009 from ENV above
CMD sh -c "uvicorn server:app --host 0.0.0.0 --port $PORT"
