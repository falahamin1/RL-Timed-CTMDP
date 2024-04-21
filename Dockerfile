# Use an official Python runtime as a parent image, with a version compatible with TensorFlow
FROM python:3.8

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies for h5py and TensorFlow
RUN apt-get update && apt-get install -y \
    libhdf5-dev \
    libc-ares-dev \
    libeigen3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    numpy \
    h5py \
    tensorflow



# Command to run the script, adjust with actual parameters needed for your application
CMD ["python", "RL-algorithm.py", "-s", "Specification1.py", "-m", "single", "--model", "path/to/model.prism", "-p", "0.05", "-f", "results.txt"]

