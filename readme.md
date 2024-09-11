Open a terminal and navigate to the directory containing these files.

Build the Docker image:
`docker build -t sdxl-lightweight .`

Run the container with GPU support:
`docker run --gpus all sdxl-lightweight`

Run the container with a prompt:

`docker run --gpus all -v $(pwd):/app -p 4001:4001 -p 5001:5001 -p 8090:8080 sdxl-lightweight-ipfs "lilypad in an galaxy of stars"`

