FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the contents of the local working directory to the Docker image
COPY . /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libmariadb-dev-compat gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

    
# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Switch to a non-root user
USER 1000:1000

# Expose port
EXPOSE 8080

# Start the server
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
