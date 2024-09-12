import torch
from diffusers import DiffusionPipeline
import logging
import os
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        logging.info("Starting SDXL lightweight script")

        # Determine the prompt
        if 'LILYPAD_INPUT_FILE' in os.environ:
            # We're running in Lilypad
            with open(os.environ['LILYPAD_INPUT_FILE'], 'r') as f:
                input_data = json.load(f)
            prompt = input_data.get('PROMPT', os.environ.get('DEFAULT_PROMPT', "A beautiful landscape with mountains and a lake"))
        else:
            # We're running directly in Docker
            prompt = os.environ.get('PROMPT', os.environ.get('DEFAULT_PROMPT', "A beautiful landscape with mountains and a lake"))

        logging.info(f"Using prompt: {prompt}")

        # Load the SDXL-Turbo pipeline
        logging.info("Loading SDXL-Turbo pipeline")
        model_id = "stabilityai/sdxl-turbo"
        cache_dir = "/root/.cache/huggingface"
        
        logging.info("Using pre-downloaded model")
        pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, variant="fp16", cache_dir=cache_dir)
        
        # Move the pipeline to GPU if available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logging.info(f"Using device: {device}")
        pipe = pipe.to(device)

        # Generate an image
        logging.info(f"Generating image with prompt: {prompt}")
        image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0).images[0]

        # Save the image in the outputs directory
        output_dir = "/outputs"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "output.png")
        image.save(output_path)
        logging.info(f"Image generated and saved as {output_path}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()