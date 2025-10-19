import os, cv2
import numpy as np
from config import generation_config

def load_images():
    content_images = []
    for ci in os.listdir(f"{generation_config.root_directory}/content/"):
        cimg = cv2.imread(f'{generation_config.root_directory}/content/{ci}', cv2.IMREAD_COLOR)
        cimg = cv2.cvtColor(cimg, cv2.COLOR_BGR2RGB)
        cimg = cv2.resize(cimg, (generation_config.content_image_width, generation_config.content_image_height))
        content_images.append(cimg)

    style_images = []
    for si in os.listdir(f"{generation_config.root_directory}/style/"):
        simg = cv2.imread(f'{generation_config.root_directory}/style/{si}', cv2.IMREAD_COLOR)
        simg = cv2.cvtColor(simg, cv2.COLOR_BGR2RGB)
        simg = cv2.resize(simg, (int(generation_config.style_image_width), int(generation_config.style_image_height)))
        style_images.append(simg)

    return content_images, style_images

def get_stylized_rgb(st_img):
    new_img = st_img[0] / (st_img[1] + 1)
    new_img = new_img.astype(np.uint8)

    return new_img