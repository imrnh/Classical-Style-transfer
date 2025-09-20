import sys
from plotting import plot_and_save
from style_transfer_para import style_transfer as style_para
from style_transfer import style_transfer as style_mono
from utils import load_images
from time import perf_counter


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py [para|mono] patch_size stride")
        sys.exit(1)

    mode = sys.argv[1]  # "para" or "mono"
    patch_size = int(sys.argv[2])
    stride = int(sys.argv[3])

    content_images, style_images = load_images()

    stylized_images = []
    for content_img, style_img in zip(content_images, style_images):
        st = perf_counter()
        
        if mode == "para":
            st_img = style_para(content_img, style_img, patch_size=patch_size, stride=stride)
        else:
            st_img = style_mono(content_img, style_img, patch_size=patch_size, stride=stride)

        ed = perf_counter()
        print(f"Time taken: {ed - st:.4f} seconds")
        stylized_images.append(st_img)

    plot_and_save(stylized_images, content_images, style_images)
