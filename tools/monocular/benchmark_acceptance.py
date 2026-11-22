"""Report empirical position/depth tolerances and missing coverage."""
import argparse
import json
import math
from pathlib import Path

import cv2
import numpy as np

from benchmark_temporal import cameras_from_qca, load_case
from reconstruct import CHAINS, lift, load_notebook


JOINTS = {child for _, child, _, _ in CHAINS}
PASS_RATES = (90, 95)
TOLERANCES_M = (0.05, 0.10, 0.20)


def score(predictions, reference, scale, joints=JOINTS):
    errors = []
    eligible = 0
    for predicted, actual in zip(predictions, reference, strict=True):
        for joint in sorted(joints & actual.keys()):
            eligible += 1
            if joint in predicted and np.isfinite(predicted[joint]).all():
                errors.append(np.asarray(predicted[joint]) * scale - actual[joint])
    scores = {"reference_samples": eligible, "scored_samples": len(errors),
              "coverage": len(errors) / eligible if eligible else None}
    differences = np.asarray(errors).reshape(-1, 3)
    for name, values in (("position", np.linalg.norm(differences, axis=1)),
                         ("depth", np.abs(differences[:, 2]))):
        ranked = np.sort(values)
        scores[name] = {
            "tolerance_m_at_pass_rate_on_scored": {
                str(rate): float(ranked[math.ceil(len(ranked) * rate / 100) - 1])
                if len(ranked) else None for rate in PASS_RATES
            },
            "reference_pass_rate_at_tolerance_m": {
                str(limit): float(np.count_nonzero(values <= limit) / eligible)
                if eligible else None for limit in TOLERANCES_M
            },
        }
    return scores


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
    observations, reference, torso = load_case(
        api, net, cameras_from_qca(args.qca), (args.camera_a, args.camera_b),
        metric_reference=True)
    results = {}
    for name, temporal in (("fixed", False), ("temporal", True)):
        results[name] = score(lift(observations, temporal=temporal), reference, torso)
    print(json.dumps(dict(input_camera=args.camera_a.stem, reference_partner=args.camera_b.stem,
                          frame_pairs=len(reference), source_frame_stride=5,
                          scale_source="reference torso length", torso_m=torso,
                          baselines=results), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
