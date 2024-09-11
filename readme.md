Open a terminal and navigate to the directory containing these files.

Build the Docker image:
`docker build -t sdxl-lightweight .`

Run the container with GPU support:
`docker run --gpus all sdxl-lightweight`