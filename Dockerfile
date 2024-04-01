# Use the official Python base image
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements.txt file first
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Specify the command to run your Python script (main.py)
CMD flask run -h 0.0.0.0 -p 5000

# Expose port 5000 for communication with the host
EXPOSE 5000