# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch with CUDA support
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118

# Install other dependencies
RUN pip install diffusers transformers accelerate

# Copy the Python script into the container
COPY inference.py .

# Set permissions
RUN chmod +x /app/inference.py

# Run the script when the container launches
CMD ["python", "/app/inference.py"]