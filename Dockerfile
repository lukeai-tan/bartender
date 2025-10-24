# Use the official Python image for 3.13.7
FROM python:3.13.9-slim-trixie

# Set working directory inside the container
WORKDIR /app

# Copy only dependency files first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Run your main script
CMD ["python", "main.py"]
