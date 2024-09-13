# SDXL Turbo Pipeline: a lightweight model to 

Open a terminal and navigate to the directory containing these files.

Build the Docker image:
`docker build -t sdxl-lightweight .`

Run the container with GPU support:
`docker run --gpus all sdxl-lightweight`

Run the container with a prompt:

`docker run --gpus all -v $(pwd):/app -p 4001:4001 -p 5001:5001 -p 8090:8080 sdxl-lightweight-ipfs "lilypad in an galaxy of stars"`

`docker run --gpus all \
  -v $(pwd):/app \
  -v $(pwd)/outputs:/outputs \
  -p 4001:4001 -p 5001:5001 -p 8090:8080 \
  sdxl-lightweight-ipfs "a lake house with snow"`

## Run using Lilypad localNet
`go run . run --network dev github.com/noryev/module-sdxl-ipfs:ae17e969cadab1c53d7cabab1927bb403f02fd2a --web3-private-key < admin key found within hardhat/utils/accounts.ts > -i prompt="a spaceship parked on mountain"`
