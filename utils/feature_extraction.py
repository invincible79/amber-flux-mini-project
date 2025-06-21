import cv2
import numpy as np
import os

def compute_histogram(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not read image at path: {image_path}. Please ensure the file exists and is a valid image.")
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                        [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist

def compute_all_histograms(folder):
    vectors = []
    for img in sorted(os.listdir(folder)):
        path = os.path.join(folder, img)
        try:
            vec = compute_histogram(path)
            vectors.append((img, vec))
        except FileNotFoundError as e:
            print(f"Skipping file: {e}")
    return vectors
