import cv2
import numpy as np

def load_images(content_image_path, style_image_path, IMG_WDTH, IMG_HGH):
    content_image = cv2.imread(content_image_path, cv2.IMREAD_COLOR)
    content_image = cv2.cvtColor(content_image, cv2.COLOR_BGR2RGB)
    content_image = cv2.resize(content_image, (IMG_WDTH, IMG_HGH))

    style_image = cv2.imread(style_image_path, cv2.IMREAD_COLOR)
    style_image = cv2.cvtColor(style_image, cv2.COLOR_BGR2RGB)
    style_image = cv2.resize(style_image, (IMG_WDTH, IMG_HGH))

    return content_image, style_image

def get_stylized_rgb(st_img):
    new_img = st_img[0] / (st_img[1] + 1)
    new_img = new_img.astype(np.uint8)

    return new_img

