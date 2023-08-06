__appname__ = "FBA Matting"
__version__ = "1.0.0"

from .inference import inference
from .networks import build_model
from .networks.transforms import trimap_transform, normalise_image

