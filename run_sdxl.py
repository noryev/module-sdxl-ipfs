import torch
from diffusers import DiffusionPipeline
import logging
import os
import sys
import requests
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def wait_for_ipfs():
    max_retries = 30
    for _ in range(max_retries):
        try:
            response = requests.post('http://127.0.0.1:5001/api/v0/id')
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            time.sleep(1)
    return False

def main():
    try:
        logging.info("Starting SDXL lightweight script")

        # Wait for IPFS to start
        if not wait_for_ipfs():
            logging.error("IPFS failed to start")
            sys.exit(1)

        # Get the prompt from command line argument or use a default
        prompt = sys.argv[1] if len(sys.argv) > 1 else "A beautiful landscape with mountains and a lake"

        # Add the prompt to IPFS
        files = {'file': prompt}
        response = requests.post('http://127.0.0.1:5001/api/v0/add', files=files)
        if response.status_code == 200:
            prompt_hash = response.json()['Hash']
            logging.info(f"Prompt added to IPFS with hash: {prompt_hash}")
        else:
            logging.error(f"Failed to add prompt to IPFS: {response.text}")
            sys.exit(1)

        # Retrieve the prompt from IPFS
        response = requests.post(f'http://127.0.0.1:5001/api/v0/cat?arg={prompt_hash}')
        if response.status_code == 200:
            retrieved_prompt = response.text
            logging.info(f"Retrieved prompt from IPFS: {retrieved_prompt}")
        else:
            logging.error(f"Failed to retrieve prompt from IPFS: {response.text}")
            sys.exit(1)

        # Load the SDXL-Turbo pipeline
        logging.info("Loading SDXL-Turbo pipeline")
        model_id = "stabilityai/sdxl-turbo"
        cache_dir = "/root/.cache/huggingface"
        
        if os.path.exists(os.path.join(cache_dir, "diffusers", model_id)):
            logging.info("Using cached model")
        else:
            logging.info("Downloading model (this may take a while)")
        
        pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, variant="fp16", cache_dir=cache_dir)
        
        # Move the pipeline to GPU if available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logging.info(f"Using device: {device}")
        pipe = pipe.to(device)

        # Generate an image
        logging.info(f"Generating image with prompt: {retrieved_prompt}")
        image = pipe(prompt=retrieved_prompt, num_inference_steps=1, guidance_scale=0.0).images[0]

        # Save the image in the current working directory
        output_path = os.path.join(os.getcwd(), "output.png")
        image.save(output_path)
        logging.info(f"Image generated and saved as {output_path}")

        # Add the generated image to IPFS
        with open(output_path, "rb") as image_file:
            files = {'file': image_file}
            response = requests.post('http://127.0.0.1:5001/api/v0/add', files=files)
            if response.status_code == 200:
                image_hash = response.json()['Hash']
                logging.info(f"Image added to IPFS with hash: {image_hash}")
            else:
                logging.error(f"Failed to add image to IPFS: {response.text}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()