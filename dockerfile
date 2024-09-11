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

# Create a directory for the model cache
RUN mkdir -p /root/.cache/huggingface

# Copy the Python script into the container
COPY run_sdxl.py .

# Set permissions
RUN chmod +x /app/run_sdxl.py

# Run the script when the container launches
CMD ["python", "/app/run_sdxl.py"]