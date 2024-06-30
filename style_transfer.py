import cv2, os
import numpy as np
from tqdm import tqdm


import cv2
import numpy as np

def extract_patches(image, patch_size, stride):
    height, width = image.shape[:2]
    patches = []
    for y in range(0, height - patch_size + 1, stride):
        for x in range(0, width - patch_size + 1, stride):
            patch = image[y:y + patch_size, x:x + patch_size]
            patches.append(patch)
    return np.array(patches)

def calculate_features(patch):
    gray_patch = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)
    mean_color = np.mean(gray_patch)
    std_dev = np.std(gray_patch)
    return mean_color, std_dev


def style_feature_precalculate(style_patches):
    style_patches_features = {}
    for sp_idx, sp_content in enumerate(style_patches):
        style_mean, style_std = calculate_features(sp_content)
        style_patches_features[sp_idx] = [style_mean, style_std] # (Mean, Std)
    
    return style_patches_features

"""
    Finding the best matched patch. 
    Calculate euclidean distance for the mean and std of style and content.
    Minimum distanced one is considered as best match.
"""
def best_matched_patch(content_patch, style_patches_features):
    feature_diff_list = []
    content_mean, content_std = calculate_features(content_patch)
    for idx_key in style_patches_features:
        spf_list = style_patches_features[idx_key]
        feature_diff = np.sum((content_mean - spf_list[0])**2 + (content_std - spf_list[1])**2)
        feature_diff_list.append(feature_diff)

    best_match_idx = np.argmin(feature_diff_list)

    return best_match_idx


"""
    Perform Style Transfer operation.
"""

def style_transfer(content_img, style_img, patch_size=5, stride=1):
    content_patches = extract_patches(content_img, patch_size, stride)
    style_patches = extract_patches(style_img, patch_size, stride)

    style_patches_features = style_feature_precalculate(style_patches)

    print(f"Total patch count: {len(content_patches)}")

    result_img = np.zeros_like(content_img)
    height, width = content_img.shape[:2]
    patch_h, patch_w = patch_size, patch_size


    for i, content_patch in tqdm(enumerate(content_patches)):
        best_match_idx = best_matched_patch(content_patch, style_patches_features)

        y = (i // (width // stride)) * stride
        x = (i % (width // stride)) * stride

        # Adjusting patch dimensions and slicing to handle edge.
        h = min(patch_h, content_img.shape[0] - y)
        w = min(patch_w, content_img.shape[1] - x)

        result_img[y:y + h, x:x + w] = style_patches[best_match_idx][:h, :w]

    # Handling overlapping regions
    overlap_counts = np.zeros_like(result_img)
    for patch in extract_patches(result_img, patch_size, stride=1):
        overlap_counts[y:y + patch_h, x:x + patch_w] += 1

    return result_img.astype(np.uint8) , overlap_counts
