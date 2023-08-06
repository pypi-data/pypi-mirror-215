import cv2
import numpy as np


def convert(img, target_type_min, target_type_max, target_type):
    imin = img.min()
    imax = img.max()

    a = (target_type_max - target_type_min) / (imax - imin)
    b = target_type_max - a * imax
    new_img = (a * img + b).astype(target_type)
    return new_img


def concatenate(image, mask):
    mask = mask[:, :, None]
    return np.concatenate([image, mask], axis=2, dtype=np.uint8)


def read_image(name):
    return (cv2.imread(name) / 255.0)[:, :, ::-1]


def read_trimap(name):
    trimap_im = cv2.imread(name, 0) / 255.0
    h, w = trimap_im.shape
    trimap_np = np.zeros((h, w, 2))
    trimap_np[trimap_im == 1, 1] = 1
    trimap_np[trimap_im == 0, 0] = 1
    return trimap_np
