import cv2
import numpy as np
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

def extract_patches(image, patch_size=5, stride=1):
    height, width = image.shape[:2]
    patches = []
    for y in range(0, height - patch_size + 1, stride):
        for x in range(0, width - patch_size + 1, stride):
            patch = image[y:y + patch_size, x:x + patch_size]
            patches.append(patch)
    return np.array(patches)

def calculate_features(patch):
    gray_patch = cv2.cvtColor(patch, cv2.COLOR_RGB2GRAY)
    mean_color = np.mean(gray_patch)
    std_dev = np.std(gray_patch)
    return mean_color, std_dev

def style_transfer(content_img, style_img, patch_size=5, stride=1):
    content_patches = extract_patches(content_img, patch_size, stride)
    style_patches = extract_patches(style_img, patch_size, stride)

    result_img = np.zeros_like(content_img)
    height, width = content_img.shape[:2]
    patch_h, patch_w = patch_size, patch_size

    print(f"Patch count\t content: {len(content_patches)} style: {len(style_patches)}")

    with ProcessPoolExecutor() as executor:
        futures = []
        for i, content_patch in enumerate(content_patches):
            futures.append(executor.submit(process_content_patch, content_patch, style_patches, i, width, stride,content_img, patch_h, patch_w))

        for future in as_completed(futures):
            y, x, h, w, best_match_idx = future.result()
            result_img[y:y + h, x:x + w] = style_patches[best_match_idx][:h, :w]

    overlap_counts = np.zeros_like(result_img)
    for patch in extract_patches(result_img, patch_size, stride=1):
        y = (i // (width // stride)) * stride
        x = (i % (width // stride)) * stride
        overlap_counts[y:y + patch_h, x:x + patch_w] += 1

    return result_img.astype(np.uint8), overlap_counts

def process_content_patch(content_patch, style_patches, i, width, stride, content_img, patch_h, patch_w):
    content_mean, content_std = calculate_features(content_patch)
    best_match_idx = np.argmin([np.sum((content_mean - style_mean)**2 + (content_std - style_std)**2)
                               for style_mean, style_std in map(calculate_features, style_patches)])

    y = (i // (width // stride)) * stride
    x = (i % (width // stride)) * stride
    h = min(patch_h, content_img.shape[0] - y)
    w = min(patch_w, content_img.shape[1] - x)
    return y, x, h, w, best_match_idx