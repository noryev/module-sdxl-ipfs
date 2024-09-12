import sys
import torch
from diffusers import DiffusionPipeline
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_prompt():
    # Use sys.argv[1] if available, otherwise fall back to environment variable or default
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])  # Join all arguments to allow for prompts with spaces
    else:
        prompt = os.environ.get('PROMPT', os.environ.get('DEFAULT_PROMPT', "A spaceship parked on a lilypad"))
    logging.info(f"Using prompt: {prompt}")
    return prompt

def main():
    try:
        logging.info("Starting SDXL lightweight script")
        
        # Get the prompt
        prompt = get_prompt()
        
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