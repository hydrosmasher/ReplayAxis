"""Measure static epipolar error using manually matched treadmill landmarks."""
import argparse
from itertools import combinations
import json
from pathlib import Path

import cv2
import numpy as np

from benchmark_temporal import cameras_from_qca
from replayaxis_real import relative_camera


def epipolar_errors(a, b, cam_a, cam_b):
    rotation, translation = relative_camera(cam_a, cam_b)
    x, y, z = translation
    cross = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    fundamental = np.linalg.inv(cam_b["K"]).T @ cross @ rotation @ np.linalg.inv(cam_a["K"])
    lines = fundamental @ a, fundamental.T @ b
    numerator = abs(b @ lines[0])
    return [float(numerator / np.linalg.norm(line[:2])) for line in lines[::-1]]


def decoded_sizes(videos, frame_index):
    sizes = {}
    for path in videos:
        cap = cv2.VideoCapture(str(path))
        try:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ok, frame = cap.read()
        finally:
            cap.release()
        if not ok:
            raise ValueError(f"Cannot decode annotation frame from {path}.")
        sizes[path.stem] = [frame.shape[1], frame.shape[0]]

    return sizes


def measure(labels, sizes, cameras, pixel_maps=None):
    results = {}
    canvas = np.asarray(labels["annotation_canvas"])
    for landmark, views in labels["landmarks"].items():
        points = {}
        for name, (x, y) in views.items():
            size = np.asarray(sizes[name])
            canvas_point = np.array([x, y + labels["crop_top"]])
            pixel = (canvas_point + .5) * size / canvas - .5
            if pixel_maps is not None:
                scale, shift = pixel_maps[name]
                pixel[0] = (pixel[0] + .5) * scale - .5 + shift
            cam = cameras[name]
            corrected = cv2.undistortPoints(pixel.reshape(1, 1, 2), cam["K"],
                                            np.asarray(cam["dist"]), P=cam["K"])[0, 0]
            points[name] = np.r_[corrected, 1.]
        results[landmark] = {
            f"{a}+{b}": epipolar_errors(points[a], points[b], cameras[a], cameras[b])
            for a, b in combinations(points, 2)}
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("labels", type=Path)
    parser.add_argument("qca", type=Path)
    parser.add_argument("videos", type=Path, nargs=4)
    args = parser.parse_args()
    labels = json.loads(args.labels.read_text())
    cameras = cameras_from_qca(args.qca)
    sizes = decoded_sizes(args.videos, labels["source_frame"])
    results = measure(labels, sizes, cameras)
    print(json.dumps(dict(decoded_sizes=sizes, landmarks=results), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
