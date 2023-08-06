"""
This module exposes various optical flow file formats and their read/write handlers.
"""

from __future__ import annotations

import re
from abc import ABCMeta, abstractmethod
from typing import NamedTuple

import cv2
import numpy as np
import numpy.typing as NP

from .format import FlowFormat
from .typings import PathType

cv2.setNumThreads(0)
cv2.ocl.setUseOpenCL(False)


class FlowTuple(NamedTuple):
    u: NP.NDArray[np.float64]
    v: NP.NDArray[np.float64]


_HANDLERS: dict[FlowFormat, _ReadWriter] = {}


def read_flow(path: PathType, **kwargs) -> FlowTuple:
    ffmt = FlowFormat.from_path(path)

    match ffmt:
        case h if h in _HANDLERS:
            _HANDLERS[h].read(path, **kwargs)
        case _:
            raise NotImplementedError(f"Flow file format {ffmt} write is not known/supported!")


def write_flow(path: PathType, flow: FlowTuple, **kwargs):
    ffmt = FlowFormat.from_path(path)

    match ffmt:
        case h if h in _HANDLERS:
            _HANDLERS[h].write(path, flow, **kwargs)
        case _:
            raise NotImplementedError(f"Flow file format {ffmt} write is not known/supported!")


class _ReadWriter(metaclass=ABCMeta):
    __slots__ = ()

    def __new__(cls):
        raise TypeError(f"Cannot instantiate {cls.__name__}!")

    def __init_subclass__(cls, /, format=None, **kwargs):
        global _HANDLERS

        super().__init_subclass__(**kwargs)
        if format is not None:
            _HANDLERS[format] = cls

    @classmethod
    @abstractmethod
    def read(cls, path: PathType) -> FlowTuple:
        ...

    @classmethod
    @abstractmethod
    def write(cls, path: PathType, flow: FlowTuple) -> None:
        ...


class FLOReadWriter(_ReadWriter):
    TAG_CHAR = np.array([202021.25], np.float32)

    @classmethod
    def read(cls, path: PathType) -> FlowTuple:
        """
        Read the optical flow from a .flo file.
        """
        with open(path, "rb") as f:
            magic = np.fromfile(f, np.float32, count=1)
            if FLOReadWriter.TAG_CHAR != magic:
                raise ValueError("Magic number incorrect. Invalid .flo file")
            else:
                w = np.fromfile(f, np.int32, count=1)
                h = np.fromfile(f, np.int32, count=1)
                data = np.fromfile(f, np.float32, count=2 * int(w) * int(h))

                # Reshape data into 3D array (columns, rows, bands)
                # The reshape here is for visualization, the original code is (w,h,2)
                uv = np.resize(data, (int(h), int(w), 2))

                return FlowTuple(uv[:, :, 0], uv[:, :, 1])

    @classmethod
    def write(cls, path: PathType, flow: FlowTuple) -> None:
        """
        Write the optical flow to a .flo file.

        Args:
            path (path): PathTypeto the file.
        """

        bands = 2

        assert flow.u.shape == flow.v.shape
        height, width = flow.u.shape

        with open(path, "wb") as f:
            # Write the header
            f.write(FLOReadWriter)

            np.array(width).astype(np.int32).tofile(f)
            np.array(height).astype(np.int32).tofile(f)

            # Arrange into matrix form
            tmp = np.zeros((height, width * bands))
            tmp[:, np.arange(width) * 2] = flow.u
            tmp[:, np.arange(width) * 2 + 1] = flow.v
            tmp.astype(np.float32).tofile(f)


class PTHReadWriter(_ReadWriter):
    """
    Write in PyTorch .pth format. Uses [UV, H, W] dimension order.
    """

    @classmethod
    def read(cls, path: PathType, **load_kwargs) -> FlowTuple:
        """
        Read the optical flow from a .pth file.
        """
        import torch

        uv = torch.load(path, map_location="cpu", **load_kwargs)
        return FlowTuple(uv[0, :, :].clone().numpy(), uv[1, :, :].clone().numpy())

    @classmethod
    def write(cls, path: PathType, flow: FlowTuple, **save_kwargs) -> None:
        """
        Write the optical flow to a .pth file.

        Args:
            path (path): PathTypeto the file.
        """
        import torch

        uv = torch.stack([torch.from_numpy(flow.u), torch.from_numpy(flow.v)], dim=0)
        torch.save(uv, path, **save_kwargs)


class PKLReadWriter(_ReadWriter):
    @classmethod
    def read(cls, path: PathType) -> FlowTuple:
        """
        Read the optical flow from a .pkl file.
        """
        import pickle

        with open(path, "rb") as f:
            u, v = pickle.load(f)

        return FlowTuple(u, v)

    @classmethod
    def write(cls, path: PathType, flow: FlowTuple) -> None:
        """
        Write the optical flow to a .pkl file.

        Args:
            path (path): PathTypeto the file.
        """
        import pickle

        with open(path, "wb") as f:
            pickle.dump((flow.u, flow.v), f)


class PFMReadWriter(_ReadWriter):
    @classmethod
    def read(cls, path: PathType) -> FlowTuple:
        with open(path, "rb") as file:
            color = None
            width = None
            height = None
            scale = None
            endian = None

            header = file.readline().rstrip()
            if header == b"PF":
                color = True
            elif header == b"Pf":
                color = False
            else:
                raise RuntimeError("Not a PFM file.")

            dim_match = re.match(rb"^(\d+)\s(\d+)\s$", file.readline())
            if dim_match:
                width, height = map(int, dim_match.groups())
            else:
                raise Exception("Malformed PFM header.")

            scale = float(file.readline().rstrip())
            if scale < 0:  # little-endian
                endian = "<"
                scale = -scale
            else:
                endian = ">"  # big-endian

            data = np.fromfile(file, endian + "f")
        shape = (height, width, 3) if color else (height, width)

        data = np.reshape(data, shape)
        data = np.flipud(data)

        return data

    @classmethod
    def write(cls, path: PathType, flow: FlowTuple) -> None:
        raise NotImplementedError("PFM write is not implemented!")


class RawReadWriter(_ReadWriter):
    @classmethod
    def read(cls, path: PathType) -> FlowTuple:
        uv = np.load(path)
        assert uv.ndim == 3
        # if uv.shape[0] == 2:
        #     return FlowUV(uv[0, :, :], uv[1, :, :])
        if uv.shape[2] == 2:
            return FlowTuple(uv[:, :, 0], uv[:, :, 1])
        else:
            raise ValueError(f"Invalid shape for raw flow file: {uv.shape}!")

    @classmethod
    def write(cls, path: PathType, flow: FlowTuple) -> None:
        np.save(path, np.stack([flow.u, flow.v], axis=0))


class KITTIReadWriter(_ReadWriter):
    @classmethod
    def read_with_valid(cls, path: PathType) -> tuple[FlowTuple, np.ndarray]:
        flow = cv2.imread(path, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_COLOR)

        assert flow.ndim == 3
        assert flow.shape[2] == 3

        flow = flow[:, :, ::-1].astype(np.float32)
        flow, valid = flow[:, :, :2], flow[:, :, 2]
        flow = (flow - 2**15) / 64.0

        return FlowTuple(flow[:, :, 0], flow[:, :, 1]), valid

    @classmethod
    def read_disp(cls, path: PathType) -> tuple[FlowTuple, np.ndarray]:
        disp = cv2.imread(path, cv2.IMREAD_ANYDEPTH)
        disp = disp.astype(np.float32) / 256.0
        valid = disp > 0.0
        flow = np.stack([-disp, np.zeros_like(disp)], -1)

        return flow, valid

    @classmethod
    def read(cls, path: PathType) -> FlowTuple:
        flow, _ = KITTIReadWriter.read_with_valid(path)

        return flow

    @classmethod
    def write(cls, path: PathType, flow: FlowTuple) -> None:
        uv = np.stack([flow.u, flow.v], axis=-1)
        uv = 64.0 * uv + 2**15
        valid = np.ones([uv.shape[0], uv.shape[1], 1])
        uv = np.concatenate([uv, valid], axis=-1).astype(np.uint16)
        cv2.imwrite(path, uv[..., ::-1])
