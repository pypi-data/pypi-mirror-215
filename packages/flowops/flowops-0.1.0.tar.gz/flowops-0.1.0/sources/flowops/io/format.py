from enum import Enum

from .typings import PathType
from .utils import get_ext


class FlowFormat(Enum):
    FLO = ".flo"  # .flo (Middlebury FLO format)
    PFM = ".pfm"  # .pfm (Portable Float Map)
    PNG = ".png"  # .png (KITTI FLOW 2015 format)
    PTH = ".pth"  # .pth (PyTorch, as a tuple of Tensors)
    PKL = ".pkl"  # .pkl (Pickle, as a NumPy array)

    @staticmethod
    def from_path(path: PathType):
        return FlowFormat(get_ext(path))
