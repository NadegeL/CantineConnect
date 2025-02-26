FROM python:3.12

WORKDIR /app

# Update packages and install necessary system dependencies
RUN apt update && apt install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies file first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files after installing dependencies
COPY . .

# Make the wait-for-it.sh script executable
RUN chmod +x /app/wait-for-it.sh /app/start.sh

# Expose the port on which the application will run
EXPOSE 8000

# Define entry point
ENTRYPOINT ["/app/start.sh"]
