import os, cv2
import numpy as np


ROOT_DIR = "images"

IMG_WDTH = int(100)
IMG_HGH = int(83)

def load_images():
    content_images = []
    for ci in os.listdir(f"{ROOT_DIR}/content/"):
        cimg = cv2.imread(f'{ROOT_DIR}/content/{ci}', cv2.IMREAD_COLOR)
        cimg = cv2.cvtColor(cimg, cv2.COLOR_BGR2RGB)
        cimg = cv2.resize(cimg, (IMG_WDTH * 2, IMG_HGH * 2))
        content_images.append(cimg)

    style_images = []
    for si in os.listdir(f"{ROOT_DIR}/style/"):
        simg = cv2.imread(f'{ROOT_DIR}/style/{si}', cv2.IMREAD_COLOR)
        simg = cv2.cvtColor(simg, cv2.COLOR_BGR2RGB)
        simg = cv2.resize(simg, (int(IMG_WDTH /2), int(IMG_HGH / 2)))
        style_images.append(simg)

    return content_images, style_images

def get_stylized_rgb(st_img):
    new_img = st_img[0] / (st_img[1] + 1)
    new_img = new_img.astype(np.uint8)

    return new_img