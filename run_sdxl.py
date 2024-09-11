import torch
from diffusers import DiffusionPipeline
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        logging.info("Starting SDXL lightweight script")
        
        # Check CUDA availability
        logging.info(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            logging.info(f"CUDA device: {torch.cuda.get_device_name(0)}")

        # Load the SDXL-Turbo pipeline
        model_id = "stabilityai/sdxl-turbo"
        cache_dir = "/root/.cache/huggingface"
        
        logging.info(f"Checking for cached model in {cache_dir}")
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
        prompt = "A beautiful landscape with mountains and a lake"
        logging.info(f"Generating image with prompt: {prompt}")
        image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0).images[0]

        # Save the image in the current working directory
        output_path = os.path.join(os.getcwd(), "output.png")
        image.save(output_path)
        logging.info(f"Image generated and saved as {output_path}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
