# Use an official Python runtime as a parent image, with a version compatible with TensorFlow
FROM python:3.8

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install TensorFlow and NumPy
# Note: The version of TensorFlow should be compatible with the version of Python used.
# Replace 'tensorflow' with 'tensorflow-gpu' if GPU support is needed and available.
RUN pip install --no-cache-dir tensorflow numpy

# Install any other dependencies as required
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Command to run the script, adjust with actual parameters needed for your application
CMD ["python", "RL-algorithm.py", "-s", "Specification1.py", "-m", "single", "--model", "path/to/model.prism", "-p", "0.05", "-f", "results.txt"]

