# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory to the working directory in the container
COPY . /app

# Install required dependencies
RUN pip3 install -r requirements.txt

# Expose port 8080 to the outside world
EXPOSE 8080

# Command to run Streamlit
CMD ["streamlit", "run", "Main.py", "--server.port=8080", "--server.address=0.0.0.0"]