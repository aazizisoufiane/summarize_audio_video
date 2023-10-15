# Use an official Python runtime as a base image
# Use Ubuntu as the base image
FROM ubuntu:latest

# Set environment variables to non-interactive (this prevents some prompts)
ENV DEBIAN_FRONTEND=non-interactive

# Update and install system dependencies and Python
RUN apt-get update && \
    apt-get install -y g++ gdb make ninja-build rsync zip python3 python3-pip

# Upgrade pip and install Python packages
RUN pip3 install --upgrade pip setuptools wheel

# Set the working directory inside the container
WORKDIR /app

# Install git
RUN apt-get -y update
RUN apt-get -y install git

# Add C++ compiler and other build essentials for packages requiring compilation
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       gcc \
       g++ \
       cmake \
    && rm -rf /var/lib/apt/lists/*


# Copy the current directory contents into the container at /app
COPY . /app


# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run your Streamlit app
CMD ["streamlit", "run", "app.py"]
