# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch and other dependencies
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118 \
    && pip install diffusers transformers accelerate

# Create directories and download the SDXL-Turbo model
RUN mkdir -p /root/.cache/huggingface /outputs \
    && chmod 777 /outputs \
    && python -c "from diffusers import DiffusionPipeline; import torch; DiffusionPipeline.from_pretrained('stabilityai/sdxl-turbo', torch_dtype=torch.float16, variant='fp16', cache_dir='/root/.cache/huggingface')"

# Copy the Python script into the container
COPY run_sdxl.py /workspace/run_sdxl.py
RUN chmod +x /workspace/run_sdxl.py

# Set default environment variables
ENV DEFAULT_PROMPT="A spaceship parked on a lilypad"

# Set the entrypoint to directly run the Python script
ENTRYPOINT ["python", "/workspace/run_sdxl.py"]