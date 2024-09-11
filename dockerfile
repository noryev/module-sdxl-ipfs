# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install IPFS
RUN wget https://dist.ipfs.tech/kubo/v0.18.1/kubo_v0.18.1_linux-amd64.tar.gz && \
    tar -xvzf kubo_v0.18.1_linux-amd64.tar.gz && \
    cd kubo && \
    ./install.sh && \
    cd .. && \
    rm -rf kubo kubo_v0.18.1_linux-amd64.tar.gz

# Install PyTorch with CUDA support
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118

# Install other dependencies
RUN pip install diffusers transformers accelerate requests


# Create a directory for the model cache
RUN mkdir -p /root/.cache/huggingface

# Copy the Python script into the container
COPY run_sdxl.py .

# Set permissions
RUN chmod +x /app/run_sdxl.py

# Expose IPFS ports
EXPOSE 4001 5001 8080

# Create a startup script
# Create a startup script in /usr/local/bin instead of /app
RUN echo '#!/bin/bash\nipfs init\nipfs daemon --writable &\npython /app/run_sdxl.py "$@"' > /usr/local/bin/start.sh && \
    chmod +x /usr/local/bin/start.sh

# Set the entrypoint to the startup script
ENTRYPOINT ["/usr/local/bin/start.sh"]

# Default command (can be overridden)
CMD ["A beautiful landscape with mountains and a lake"]