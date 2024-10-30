from PIL import Image as PILImage
import os

PROCESSED_IMAGES_PATH = "processed_images"
os.makedirs(PROCESSED_IMAGES_PATH, exist_ok=True)

def process_image(file_path: str, sizes=[100, 500]):
    pil_image = PILImage.open(file_path)
    width, height = pil_image.size
    original_size = os.path.getsize(file_path)
    image_format = pil_image.format or "unknown"
    
    processed_files = []
    for size in sizes:
        resized_image = pil_image.resize((size, size)).convert("L")
        processed_file_path = f"{PROCESSED_IMAGES_PATH}/{size}x{size}_{os.path.basename(file_path)}"
        resized_image.save(processed_file_path)
        processed_files.append({"size": f"{size}x{size}", "file_path": processed_file_path})
    
    return {
        "resolution": f"{width}x{height}",
        "size": original_size,
        "format": image_format,
        "processed_files": processed_files
    }
