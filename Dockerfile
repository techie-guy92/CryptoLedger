# Base image
FROM python:3.12-slim

# Set maintainer
LABEL maintainer="soheil.dalirii@gmail.com"

# Set environment variables
# Prevents .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 
# Enables real-time logging  
ENV PYTHONUNBUFFERED=1          

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # For building Python packages
    build-essential \ 
    # PostgreSQL client libraries          
    libpq-dev \                 
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .
COPY .env .env  

# Collect static files
RUN python manage.py collectstatic --noinput

# Create logs directory
RUN mkdir -p logs

# Expose port for Gunicorn
EXPOSE 8020

# Start Gunicorn with fallback if DJANGO_CMD is not set
CMD ["sh", "-c", "${DJANGO_CMD:-gunicorn config.asgi:application --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8020 --log-level info --timeout 120 --access-logfile logs/access.log --error-logfile logs/error.log}"]
