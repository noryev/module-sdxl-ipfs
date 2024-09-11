import torch
from diffusers import DiffusionPipeline
import logging

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
        logging.info("Loading SDXL-Turbo pipeline")
        pipe = DiffusionPipeline.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")
        
        # Move the pipeline to GPU if available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logging.info(f"Using device: {device}")
        pipe = pipe.to(device)

        # Generate an image
        prompt = "A beautiful landscape with mountains and a lake"
        logging.info(f"Generating image with prompt: {prompt}")
        image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0).images[0]

        # Save the image
        output_path = "/app/output.png"
        image.save(output_path)
        logging.info(f"Image generated and saved as {output_path}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()