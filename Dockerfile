# Use the official Python image from the Docker Hub
FROM python:3.10-slim


# Copy the current directory contents 
COPY . .

# Install any needed packages specified in requirements.txt
RUN apt update
RUN apt install -y curl
RUN apt install -y net-tools 
RUN apt install -y iputils-ping
RUN apt install -y traceroute
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80
EXPOSE 5000
EXPOSE 5001
EXPOSE 5002

# Run the application
CMD ["python", "main_server/app.py"]