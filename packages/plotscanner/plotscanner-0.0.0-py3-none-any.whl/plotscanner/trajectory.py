import numpy as np
import cv2 as cv
from collections import defaultdict
import logging


def _find_center(vec):
    """
    Find the center of a vector.

    Args:
        vec: A numpy array representing the vector.

    Returns:
        A float representing the center of the vector.
    """
    return np.median(vec)


def normalize(img):
    """
    Normalize an image to 0-255.

    Args:
        img: A numpy array representing the image.

    Returns:
        A numpy array representing the normalized image.
    """
    return np.interp(img, (img.min(), img.max()), (0, 255)).astype(np.uint8)


def fit_trajectory_using_median(traj, T, img):
    """
    Fit a trajectory using the median.

    Args:
        traj: A defaultdict representing the trajectory.
        T: A tuple representing the transformation.
        img: A numpy array representing the image.

    Returns:
        A list of tuples representing the trajectory.
    """
    (sX, sY), (offX, offY) = T
    res = []
    r, _ = img.shape

    # x, y = zip(*sorted(traj.items()))
    # logging.info((xvec, ys))

    for k in sorted(traj):
        x = k

        vals = np.array(traj[k])

        # For each x, we may multiple pixels in column of the image which might
        # be y. Usually experience is that the trajectories are close to the
        # top rather to the bottom. So we discard call pixel which are below
        # the center of mass (median here)
        # These are opencv pixles. So there valus starts from the top. 0
        # belogs to top row. Therefore > rather than <.
        avg = np.median(vals)
        vals = vals[np.where(vals >= avg)]
        if len(vals) == 0:
            continue

        # Still we have multiple candidates for y for each x.
        # We find the center of these points and call it the y for given x.
        y = _find_center(vals)
        cv.circle(img, (x, int(y)), 1, 255, -1)
        x1 = (x - offX) / sX
        y1 = (r - y - offY) / sY
        res.append((x1, y1))

    # sort by x-axis.
    return sorted(res)


def _valid_px(val: int) -> int:
    """
    Ensure that a pixel value is within the valid range.

    Args:
        val: An integer representing the pixel value.

    Returns:
        An integer representing the valid pixel value.
    """
    return min(max(0, val), 255)


def find_trajectory(img: np.ndarray, pixel: int, T):
    """
    Find the trajectory of a pixel in an image.

    Args:
        img: A numpy array representing the image.
        pixel: An integer representing the pixel value.
        T: A tuple representing the transformation.

    Returns:
        result: A list of tuples representing the trajectory.
        img: A numpy array representing the image.
    """
    logging.info(f"Extracting trajectory for color {pixel}")
    assert (
            img.min() <= pixel <= img.max()
    ), f"{pixel} is outside the range: [{img.min()}, {img.max()}]"

    # Find all pixels which belongs to a trajectory.
    o = 6
    _clower, _cupper = _valid_px(pixel - o // 2), _valid_px(pixel + o // 2)

    Y, X = np.where((img >= _clower) & (img <= _cupper))
    traj = defaultdict(list)
    for x, y in zip(X, Y):
        traj[x].append(y)

    assert traj, "Empty trajectory"

    # this is a simple fit using median.
    new = np.zeros_like(img)
    res = fit_trajectory_using_median(traj, T, new)
    return res, np.vstack((img, new))
