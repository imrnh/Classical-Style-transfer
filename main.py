import sys
from plotting import save_stylized_outputs
from style_transfer_parallel import style_transfer as style_parallel
from style_transfer import style_transfer as style_mono
from utils import load_images
from time import perf_counter
from config import generation_config


if len(sys.argv) < 4:
    print("Usage: python main.py [p|m] patch_size stride")
    sys.exit(1)

mode = sys.argv[1]  # "p" or "m" | Indicates if we want to run the style transfer parallely on all the CPU cores available or 1 single CPU core
patch_size = int(sys.argv[2])
stride = int(sys.argv[3])


# Load Images
content_images, style_images = load_images()

output_images = []
for content_img, style_img in zip(content_images, style_images):
    st = perf_counter()
    
    if mode == "p":
        st_img = style_parallel(content_img, style_img, patch_size=patch_size, stride=stride)
    else:
        st_img = style_mono(content_img, style_img, patch_size=patch_size, stride=stride)

    ed = perf_counter()
    print(f"Time taken: {ed - st:.4f} seconds")
    output_images.append(st_img)

# Save images
save_stylized_outputs(output_images, content_images, style_images, output_dir=generation_config.output_directory)
