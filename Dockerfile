# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for reportlab & PIL
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libjpeg62-turbo-dev \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (to make docker cache more efficient)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy complete project into container
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Default command for Docker Compose (Streamlit frontend)
CMD ["streamlit", "run", "streamlit_app.py", \
     "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false"]
