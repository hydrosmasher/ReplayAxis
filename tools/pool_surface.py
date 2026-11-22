"""Fit a pool-surface homography for one frame and audit its metric error."""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np


def coordinates(rows, field):
    points = np.asarray([row[field] for row in rows], dtype=float)
    if points.shape != (len(rows), 2) or not np.isfinite(points).all():
        raise ValueError(f"Expected finite coordinate pairs for {field}.")
    return points


def map_points(matrix, pixels):
    homogeneous = np.column_stack((pixels, np.ones(len(pixels)))) @ matrix.T
    if np.any(np.abs(homogeneous[:, 2]) <= 1e-10):
        raise ValueError("A point maps to the projective horizon.")
    return homogeneous[:, :2]/homogeneous[:, 2:]


def fit_surface(anchors, checks, tolerance_m):
    if len(anchors) < 4 or len(checks) < 2:
        raise ValueError("Supply at least four fitted anchors and two independent check points.")
    if not np.isfinite(tolerance_m) or tolerance_m <= 0:
        raise ValueError("Check-point tolerance must be positive.")
    pixels = coordinates(anchors, "pixel")
    pool = coordinates(anchors, "pool_m")
    check_pixels = coordinates(checks, "pixel")
    check_pool = coordinates(checks, "pool_m")
    for fit, held_out in ((pixels, check_pixels), (pool, check_pool)):
        if len({tuple(x) for x in np.vstack((fit, held_out))}) != len(fit)+len(held_out):
            raise ValueError("Landmarks must be distinct across fit and check sets.")
    matrix, _ = cv2.findHomography(pixels, pool, method=0)
    if matrix is None or not np.isfinite(matrix).all() or np.linalg.matrix_rank(matrix) != 3:
        raise ValueError("Pool landmarks cannot define a nondegenerate surface mapping.")
    errors = np.linalg.norm(map_points(matrix, check_pixels)-check_pool, axis=1)
    if errors.max() > tolerance_m:
        raise ValueError(f"Pool check-point error reached {errors.max():.3f} m, above tolerance.")
    return matrix, errors


def calibrate(payload, tolerance_m):
    matrix, errors = fit_surface(payload["anchors"], payload["checks"], tolerance_m)
    points = payload.get("surface_points", [])
    mapped = []
    if points:
        pixels = coordinates(points, "pixel")
        hull = cv2.convexHull(coordinates(payload["anchors"], "pixel").astype(np.float32))
        for point, pixel, pool in zip(points, pixels, map_points(matrix, pixels)):
            if cv2.pointPolygonTest(hull, tuple(pixel), False) < 0:
                raise ValueError("Surface point lies outside the fitted landmark footprint.")
            mapped.append({"id": point["id"], "pool_xy_m": pool.tolist()})
    return {"frame_id": payload["frame_id"], "image_to_pool": matrix.tolist(),
            "check_errors_m": errors.tolist(), "surface_points": mapped}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("landmarks", type=Path)
    parser.add_argument("--tolerance-m", type=float, required=True)
    args = parser.parse_args()
    try:
        result = calibrate(json.loads(args.landmarks.read_text()), args.tolerance_m)
    except (ValueError, KeyError, TypeError, cv2.error) as error:
        parser.exit(2, f"Calibration withheld: {error}\n")
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
