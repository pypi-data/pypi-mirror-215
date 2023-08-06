def verify_images(img_1, img_2, threshold=0.0001):
    """
    Verify if two images are the same.
    :param img1: first image
    :param img2: second image
    :param threshold: the threshold to verify if two images are the same
    :return: True if the images are the same, False otherwise
    """
    import cv2
    import numpy as np
    import os

    if not os.path.isfile(img_1) and not os.path.isfile(img_2):
        raise FileNotFoundError()
    img_a = cv2.imread(img_1)
    img_b = cv2.imread(img_2)
    if img_a.shape != img_b.shape:
        return False
    if img_a.dtype != img_b.dtype:
        return False
    if img_a.dtype == np.uint8:
        return np.mean(np.abs(img_a - img_b)) < threshold
    else:
        return np.mean(np.abs(img_a - img_b)) < threshold * np.mean(img_a)
