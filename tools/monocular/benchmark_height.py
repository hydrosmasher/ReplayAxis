"""Evaluate body-scale sensitivity against a calibrated two-view reference."""
import argparse
import json
import math
from pathlib import Path

import cv2
import numpy as np

from benchmark_temporal import cameras_from_qca, load_case
from reconstruct import CHAINS, lift, load_notebook


def compare(observations, reference, reference_torso_m, height_m, ratios):
    poses = lift(observations)
    evaluated = {child for _, child, _, _ in CHAINS}
    pairs = [(pose[j], actual[j]) for pose, actual in zip(poses, reference, strict=True)
             for j in sorted(pose.keys() & actual.keys() & evaluated)]
    if not pairs:
        raise ValueError("No common joints in the monocular and calibrated poses.")
    prediction, target = np.asarray(pairs).transpose(1, 0, 2)
    results = []
    for label, ratio, scale in [
        *(("assumed stature and ratio", ratio, height_m*ratio) for ratio in ratios),
        ("reference torso scale", None, reference_torso_m),
    ]:
        error = prediction*scale-target
        results.append(dict(scale_source=label, torso_to_height=ratio,
                            metres_per_torso=scale, samples=len(pairs),
                            mean_3d_error_m=float(np.linalg.norm(error, axis=1).mean()),
                            mean_absolute_depth_error_m=float(np.abs(error[:, 2]).mean())))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qca", type=Path)
    parser.add_argument("model", type=Path)
    parser.add_argument("camera_a", type=Path)
    parser.add_argument("camera_b", type=Path)
    parser.add_argument("--assumed-height-m", type=float, required=True)
    parser.add_argument("--ratios", type=float, nargs="+", required=True)
    parser.add_argument("--notebook", type=Path, default=Path("ReplayAxis_Markerless_TwoView.ipynb"))
    args = parser.parse_args()
    if not math.isfinite(args.assumed_height_m) or args.assumed_height_m <= 0:
        parser.error("Assumed height must be finite and positive.")
    if any(not 0 < ratio < 1 for ratio in args.ratios):
        parser.error("Ratios must be between zero and one.")
    api = load_notebook(args.notebook)
    net = cv2.dnn.readNetFromONNX(str(args.model))
    camera_a, camera_b = args.camera_a, args.camera_b
    observations, reference, torso = load_case(api, net, cameras_from_qca(args.qca),
                                               (camera_a, camera_b), metric_reference=True)
    report = dict(input_camera=camera_a.stem, reference_camera=camera_b.stem,
                  assumed_stature_m=args.assumed_height_m, frame_pairs=len(reference),
                  reference_torso_m=torso, results=compare(observations, reference, torso,
                                                          args.assumed_height_m, args.ratios))
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
