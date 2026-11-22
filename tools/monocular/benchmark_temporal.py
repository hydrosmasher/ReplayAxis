"""Compare both monocular depth modes with calibrated two-view reference estimates."""
import argparse
import json
from pathlib import Path
import sys

import cv2
import numpy as np

from reconstruct import lift, load_notebook

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "benchmarks/two_view_geometry"))
from replayaxis_real import cameras_from_qca, collect


def compare(observations, reference, confidence=.55):
    errors = {}
    for temporal in (False, True):
        for mirror in (False, True):
            poses = lift(observations, mirror=mirror, temporal=temporal, confidence=confidence)
            depth_errors = [abs(p[j][2]-q[j][2]) for p, q in zip(poses, reference)
                            for j in p.keys() & q.keys() if j not in (11, 12, 23, 24)]
            if not depth_errors:
                raise ValueError("No shared reference joints.")
            name = ("temporal" if temporal else "fixed")+("_mirrored" if mirror else "")
            errors[name] = dict(samples=len(depth_errors),
                                mean_absolute_depth_error=float(np.mean(depth_errors)),
                                median_absolute_depth_error=float(np.median(depth_errors)))
    return errors


def load_case(api, net, cameras, paths, *, metric_reference=False):
    known, views = [], []
    for path in paths:
        frames, poses = collect(path, net, api["detect_onnx_pose"])
        camera = cameras[path.stem]
        camera["image_size"] = frames[0].shape[::-1]
        known.append(camera)
        views.append([api["correct_pose_pixels"](p, camera) for p in poses])
    reference, torso_lengths = [], []
    for a, b in zip(*views):
        points = api["reconstruct"](a, b, known)["points"]
        if not {11, 12, 23, 24}.issubset(points):
            reference.append({})
            continue
        hips = (np.array(points[23])+points[24])/2
        shoulders = (np.array(points[11])+points[12])/2
        torso_lengths.append(np.linalg.norm(shoulders-hips))
        reference.append({j: known[0]["R"] @ (point-hips) for j, point in points.items()})
    if not torso_lengths:
        raise ValueError("No calibrated torso estimates.")
    scale = np.median(torso_lengths)
    if not metric_reference:
        reference = [{j: point/scale for j, point in row.items()} for row in reference]
    else:
        return views[0][:len(reference)], reference, float(scale)
    return views[0][:len(reference)], reference


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qca", type=Path)
    parser.add_argument("model", type=Path)
    parser.add_argument("camera_a", type=Path)
    parser.add_argument("camera_b", type=Path)
    parser.add_argument("--notebook", type=Path, default=Path("ReplayAxis_Markerless_TwoView.ipynb"))
    args = parser.parse_args()
    api = load_notebook(args.notebook)
    net = cv2.dnn.readNetFromONNX(str(args.model))
    cameras = cameras_from_qca(args.qca)
    observations, reference = load_case(api, net, cameras, (args.camera_a, args.camera_b))
    print(json.dumps({"frame_pairs": len(reference),
                      "scores_in_torso_lengths": compare(observations, reference)},
                     indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
