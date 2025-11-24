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
    # Network troubleshooting and API calls
    curl \
    # Process management (ps, top commands)
    procps \
    # Better shell than default sh
    bash \
    # Network interface management (ip command)
    iproute2 \
    # Basic network utilities (ifconfig, netstat)
    net-tools \
    # List open files and ports
    lsof \
    # PostgreSQL client tools (psql, etc.)
    postgresql-client \
    # For building Python packages & psycopg2
    # C/C++ compiler and build tools
    build-essential \ 
    # Python development headers
    python3-dev \
    # PostgreSQL client library development files
    libpq-dev \
    # Library configuration tool
    pkg-config \
    # Clean up package lists to reduce image size
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Create user and set permissions (FIXED THIS PART)
RUN adduser --uid 1000 --disabled-password --gecos '' webuser && \
    mkdir -p logs && \
    chown -R webuser:webuser /app && \
    chmod -R 755 /app

USER webuser

# Expose port for Gunicorn
EXPOSE 8020