import cv2
import numpy as np
import torch

from .networks.models import MattingModule
from .networks.transforms import trimap_transform, normalise_image
from .utils import read_image, read_trimap, convert, concatenate

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def np_to_torch(x, permute=True):
    if permute:
        return torch.from_numpy(x).permute(2, 0, 1)[None, :, :, :].float().to(device)
    else:
        return torch.from_numpy(x)[None, :, :, :].float().to(device)


def scale_input(x: np.ndarray, scale: float, scale_type) -> np.ndarray:
    """ Scales inputs to multiple of 8. """
    h, w = x.shape[:2]
    h1 = int(np.ceil(scale * h / 8) * 8)
    w1 = int(np.ceil(scale * w / 8) * 8)
    x_scale = cv2.resize(x, (w1, h1), interpolation=scale_type)
    return x_scale


def inference(model: MattingModule, image: str, trimap: str) -> [np.ndarray]:
    """ Predict alpha, foreground and background.
        Parameters:
        image_np -- the image in rgb format between 0 and 1. Dimensions: (h, w, 3)
        trimap_np -- two channel trimap, first background then foreground. Dimensions: (h, w, 2)
        Returns:
        fg: foreground image in rgb format between 0 and 1. Dimensions: (h, w, 3)
        bg: background image in rgb format between 0 and 1. Dimensions: (h, w, 3)
        alpha: alpha matte image between 0 and 1. Dimensions: (h, w)
    """
    image_np = read_image(image)
    trimap_np = read_trimap(trimap)

    h, w = trimap_np.shape[:2]
    image_scale_np = scale_input(image_np, 1.0, cv2.INTER_LANCZOS4)
    trimap_scale_np = scale_input(trimap_np, 1.0, cv2.INTER_LANCZOS4)

    with torch.no_grad():
        image_torch = np_to_torch(image_scale_np)
        trimap_torch = np_to_torch(trimap_scale_np)

        trimap_transformed_torch = np_to_torch(
            trimap_transform(trimap_scale_np), permute=False)
        image_transformed_torch = normalise_image(
            image_torch.clone())

        output = model(
            image_torch,
            trimap_torch,
            image_transformed_torch,
            trimap_transformed_torch)
        output = cv2.resize(
            output[0].cpu().numpy().transpose(
                (1, 2, 0)), (w, h), cv2.INTER_LANCZOS4)

    alpha = output[:, :, 0]
    fg = output[:, :, 1:4]
    bg = output[:, :, 4:7]

    alpha[trimap_np[:, :, 0] == 1] = 0
    alpha[trimap_np[:, :, 1] == 1] = 1
    fg[alpha == 1] = image_np[alpha == 1]
    bg[alpha == 0] = image_np[alpha == 0]

    fg = convert(fg, 0, 255, np.uint8)
    bg = convert(bg, 0, 255, np.uint8)
    alpha = convert(alpha, 0, 255, np.uint8)
    composite = concatenate(fg, alpha)

    return fg, bg, alpha, composite
