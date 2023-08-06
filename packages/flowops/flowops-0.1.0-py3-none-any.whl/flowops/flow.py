from __future__ import annotations

import enum
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional

import numpy as np
import numpy.typing as NP
from typing_extensions import Self

from . import io, warp

__all__ = ["Flow", "NormalFlow", "FlowColor"]


class FlowColor(enum.Enum):
    RGB = enum.auto()
    BGR = enum.auto()


class FlowMixin:
    u: NP.NDArray[np.float64]
    v: NP.NDArray[np.float64]

    @property
    def shape(self) -> tuple[int, int]:
        return self.u.shape

    @property
    def r(self) -> np.float64:
        """
        Returns the maximum flow magnitude.
        """
        return np.sqrt(np.square(self.u) + np.square(self.v))

    def as_tuple(self) -> io.FlowTuple:
        """
        Returns the flow as a UV tuple
        """
        return io.FlowTuple(self.u, self.v)

    def __eq__(self, other: FlowMixin | io.FlowTuple) -> bool:
        return np.array_equal(self.u, other.u) and np.array_equal(self.v, other.v)


@dataclass(slots=True, frozen=True, eq=False, unsafe_hash=True)
class Flow(FlowMixin):
    """
    Optical flow dataclass with horizontal (``u``) and vertical (``v``) flow components.
    """

    u: NP.NDArray[np.float64]
    v: NP.NDArray[np.float64]

    def __post_init__(self):
        assert self.u.ndim == 2, "Flow components must have two dimensions!"
        assert self.u.shape == self.v.shape, "Flow components must have the same shape!"

    @classmethod
    def from_tuple(cls, uv: io.FlowTuple, **kwargs) -> Self:
        """
        Initialize from a UV tuple.
        """
        return cls(uv.u, uv.v, **kwargs)

    @classmethod
    def from_hw2(cls, flow_uv: np.ndarray, *, max_flow: Optional[float] = None, **kwargs) -> Self:
        """
        Initialize from a flow image of shape [H,W,2].
        """
        assert flow_uv.ndim == 3, "input flow must have three dimensions"
        assert flow_uv.shape[2] == 2, "input flow must have shape [H,W,2]"

        if max_flow is not None:
            flow_uv = np.clip(flow_uv, 0, max_flow)

        u = flow_uv[:, :, 0]
        v = flow_uv[:, :, 1]

        return cls(u, v, **kwargs)

    def as_hw2(self) -> NP.NDArray[np.float64]:
        """
        Returns the flow as a flow image of shape [H,W,2].
        """
        return np.stack((self.u, self.v), axis=-1)

    @classmethod
    def from_2hw(cls, flow_uv: np.ndarray, *args, **kwargs) -> Self:
        return cls.from_hw2(flow_uv.transpose(1, 2, 0), *args, **kwargs)

    def as_2hw(self) -> NP.NDArray[np.float64]:
        return self.as_hw2().transpose(2, 0, 1)

    def write(self, path: Path | str, ffmt: Optional[io.FlowFormat] = None, *args, **kwargs) -> None:
        """
        Write the optical flow to a file.
        """

        return io.write_flow(path, self.as_tuple(), ffmt=ffmt, *args, **kwargs)

    @classmethod
    def read(cls, path: Path | str, ffmt: Optional[io.FlowFormat] = None) -> Self:
        """
        Read the optical flow from a file.
        """

        flow = io.read_flow(path, ffmt=ffmt)

        return cls.from_tuple(flow)

    def normalize(self, r_max: Optional[float], *, eps=1e-8) -> NormalFlow:
        """
        Normalize flow components to [-1,1] range.
        No default value for `r_max` is provided to encourage explicit auto-scaling.
        """

        if r_max is None:
            r_max = np.max(self.r)

        r_max = r_max + eps

        U = self.u / r_max
        V = self.v / r_max

        return NormalFlow(U, V)

    def warp_backward(self, image: np.ndarray, **kwargs) -> np.ndarray:
        return warp.warp_backward(image, self.as_tuple(), **kwargs)

    def warp_forward(self, image: np.ndarray, **kwargs) -> np.ndarray:
        return warp.warp_forward(image, self.as_tuple(), **kwargs)


@dataclass(slots=True, frozen=True, eq=False, unsafe_hash=True)
class NormalFlow(FlowMixin):
    u: NP.NDArray[np.float64]
    v: NP.NDArray[np.float64]

    def __post_init__(self):
        for w in (self.u, self.v):
            assert (w >= -1.0).all() and (w <= 1.0).all(), "Flow components must be in [-1,1] range!"

    def render(self, cfmt=FlowColor.BGR) -> NP.NDArray[np.uint8]:
        """
        Render flow as an image.
        """
        flow_image = np.zeros((self.u.shape[0], self.u.shape[1], 3), np.uint8)
        ncols = self.colorwheel.shape[0]
        rad = np.sqrt(np.square(self.u) + np.square(self.v))
        a = np.arctan2(-self.v, -self.u) / np.pi
        fk = (a + 1) / 2 * (ncols - 1)
        k0 = np.floor(fk).astype(np.int32)
        k1 = k0 + 1
        k1[k1 == ncols] = 0
        f = fk - k0
        for i in range(self.colorwheel.shape[1]):
            tmp = self.colorwheel[:, i]
            col0 = tmp[k0] / 255.0
            col1 = tmp[k1] / 255.0
            col = (1 - f) * col0 + f * col1
            idx = rad <= 1
            col[idx] = 1 - rad[idx] * (1 - col[idx])
            col[~idx] = col[~idx] * 0.75  # out of range

            match cfmt:
                case FlowColor.RGB:
                    ch_idx = i
                case FlowColor.BGR:
                    ch_idx = 2 - i
                case _:
                    raise NotImplementedError(f"Color format {cfmt} is not known/supported!")
            flow_image[:, :, ch_idx] = np.floor(255 * col)
        return flow_image

    @staticmethod
    @lru_cache()
    def _make_colorwheel() -> NP.NDArray[np.float64]:
        """
        Generates a color wheel for optical flow visualization as in Baker et al. "A Database and Evaluation
        Methodology for Optical Flow" (ICCV, 2007)

        Paper: http://vision.middlebury.edu/flow/flowEval-iccv07.pdf
        """

        RY = 15
        YG = 6
        GC = 4
        CB = 11
        BM = 13
        MR = 6

        ncols = RY + YG + GC + CB + BM + MR
        colorwheel = np.zeros((ncols, 3))
        col = 0

        # RY
        colorwheel[0:RY, 0] = 255
        colorwheel[0:RY, 1] = np.floor(255 * np.arange(0, RY) / RY)
        col = col + RY
        # YG
        colorwheel[col : col + YG, 0] = 255 - np.floor(255 * np.arange(0, YG) / YG)
        colorwheel[col : col + YG, 1] = 255
        col = col + YG
        # GC
        colorwheel[col : col + GC, 1] = 255
        colorwheel[col : col + GC, 2] = np.floor(255 * np.arange(0, GC) / GC)
        col = col + GC
        # CB
        colorwheel[col : col + CB, 1] = 255 - np.floor(255 * np.arange(CB) / CB)
        colorwheel[col : col + CB, 2] = 255
        col = col + CB
        # BM
        colorwheel[col : col + BM, 2] = 255
        colorwheel[col : col + BM, 0] = np.floor(255 * np.arange(0, BM) / BM)
        col = col + BM
        # MR
        colorwheel[col : col + MR, 2] = 255 - np.floor(255 * np.arange(MR) / MR)
        colorwheel[col : col + MR, 0] = 255
        return colorwheel

    @property
    def colorwheel(self) -> NP.NDArray[np.float64]:
        """
        Returns the colorwheel used for flow visualization.
        """
        return self._make_colorwheel()

    def write(self, path: io.PathType, *args, **kwargs) -> None:
        from PIL import Image

        ext = io.get_ext(path)
        if ext not in (".png", ".jpg", ".jpeg"):
            raise NotImplementedError(f"NormalFlow write does not support '{ext}' files!")

        image = self.render(*args, **kwargs, cfmt=FlowColor.RGB)
        Image.fromarray(image).save(path)

    @classmethod
    def read(cls, path: io.PathType, ffmt: Optional[io.FlowFormat] = None) -> Self:
        raise NotImplementedError("NormalFlow read is not supported!")
