# Use an official Python runtime as a base image
FROM python:3.8-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Install git
RUN apt-get -y update
RUN apt-get -y install git

# Copy the current directory contents into the container at /app
COPY . /app


# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run your Streamlit app
CMD ["streamlit", "run", "app.py"]
