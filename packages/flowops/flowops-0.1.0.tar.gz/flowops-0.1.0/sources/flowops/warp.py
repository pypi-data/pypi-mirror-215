from __future__ import annotations

import numpy as np
import numpy.typing as NP

__all__ = ["warp_backward", "warp_forward"]


def warp_backward(image: np.ndarray, flow: tuple[np.ndarray, np.ndarray]) -> NP.NDArray[np.float]:
    """
    Warp an image backward in time using a flow field. This is the inverse of forward_warp, but much less expensive.
    """

    import cv2

    flow_x, flow_y = flow

    h, w = image.shape[:2]

    map_x, map_y = np.meshgrid(np.arange(w), np.arange(h))
    map_x = map_x.astype(np.float32) + flow_x
    map_y = map_y.astype(np.float32) + flow_y

    return cv2.remap(image, map_x, map_y, interpolation=cv2.INTER_NEAREST)


def warp_forward(image: np.ndarray, flow: tuple[np.ndarray, np.ndarray], *, k=4) -> NP.NDArray[np.float]:
    """
    Compute the forward warp of an image using k-nearest neighbors for interpolation.
    """

    from scipy.spatial import KDTree

    flow_x, flow_y = flow

    first_image_3d = image[..., np.newaxis] if image.ndim == 2 else image
    height, width, _ = first_image_3d.shape

    coord = np.mgrid[:height, :width]
    grid = coord.transpose(1, 2, 0).reshape((width * height, 2))

    gy, gx = coord.astype(flow_x.dtype)
    gy += flow_y
    gx += flow_x

    warped_points = np.asarray((gy.flatten(), gx.flatten())).T
    kdt = KDTree(warped_points)

    distance, neighbor = kdt.query(grid, k=k, workers=-1, eps=0.1)

    y, x = neighbor // width, neighbor % width

    neigbor_values = first_image_3d[(y, x)]

    if k == 1:
        image_warped = neigbor_values
    else:
        weights = np.exp(-distance[..., np.newaxis])
        normalizer = np.sum(weights, axis=1)

        image_warped = np.sum(neigbor_values * weights, axis=1)
        image_warped = (image_warped / normalizer).astype(image.dtype)

    return image_warped.reshape(image.shape)
