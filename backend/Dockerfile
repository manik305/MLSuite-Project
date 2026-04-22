# Use official lightweight Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies (for matplotlib and others if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
# Ensure the directory structure matches the application's relative imports
COPY ML/ ./ML/
COPY backend/ ./backend/
COPY static/ ./static/
COPY uploads/ ./uploads/

# Expose the API port
EXPOSE 8000

# Create a non-root user and set permissions
RUN useradd -m mluser && \
    chown -R mluser:mluser /app
USER mluser

# Command to run the application
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
