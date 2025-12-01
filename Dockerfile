FROM python:3.11-slim

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y build-essential gcc && rm -rf /var/lib/apt/lists/*

# copy and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app code
COPY . .

# copy entrypoint and make it executable (done as root)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Note: For simplicity on Windows mounts we run as root in the container.
# In production you should switch to a non-root user and set appropriate permissions.
EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
