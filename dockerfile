# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /sdxl

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

# Create directories for the model cache and output
RUN mkdir -p /root/.cache/huggingface /app

# Download the SDXL-Turbo model
RUN python -c "from diffusers import DiffusionPipeline; import torch; DiffusionPipeline.from_pretrained('stabilityai/sdxl-turbo', torch_dtype=torch.float16, variant='fp16', cache_dir='/root/.cache/huggingface')"

# Copy the Python script into multiple locations in the container
COPY run_sdxl.py /sdxl/run_sdxl.py
COPY run_sdxl.py /app/run_sdxl.py
COPY run_sdxl.py /root/run_sdxl.py

# Set permissions
RUN chmod +x /sdxl/run_sdxl.py /app/run_sdxl.py /root/run_sdxl.py

# Expose IPFS ports
EXPOSE 4001 5001 8080

# Create a startup script
RUN echo '#!/bin/bash\n\
    ipfs init\n\
    ipfs daemon --writable &\n\
    if [ -f /sdxl/run_sdxl.py ]; then\n\
    python /sdxl/run_sdxl.py "$@"\n\
    elif [ -f /app/run_sdxl.py ]; then\n\
    python /app/run_sdxl.py "$@"\n\
    else\n\
    python /root/run_sdxl.py "$@"\n\
    fi\n\
    if [ -f /sdxl/output.png ]; then\n\
    cp /sdxl/output.png /app/output.png\n\
    fi' > /usr/local/bin/start.sh && \
    chmod +x /usr/local/bin/start.sh

# Set the entrypoint to the startup script
ENTRYPOINT ["/usr/local/bin/start.sh"]

# Default command (can be overridden)
CMD ["A beautiful landscape with mountains and a lake"]