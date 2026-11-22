"""Benchmark a ridge-regression depth lifter across camera groups."""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np

from benchmark_temporal import cameras_from_qca, load_case
from reconstruct import CHAINS, lift, load_notebook


def feature_rows(poses, joint, parent, index):
    frame = poses[index]
    local = np.subtract(frame[joint][:2], frame[parent][:2])
    neighboring = []
    for offset in (-1, 1):
        other_index = index+offset
        other = poses[other_index] if 0 <= other_index < len(poses) else {}
        available = joint in other and parent in other
        change = np.subtract(other[joint][:2], other[parent][:2])-local if available else [0, 0]
        neighboring.extend([*change, float(available)])
    identity = [float(joint == child) for _, child, _, _ in CHAINS]
    return [1., *identity, *frame[joint][:2], *local, frame[joint][2], *neighboring]


def prepare(observations, reference):
    fixed = lift(observations)
    temporal = lift(observations, temporal=True)
    parents = {child: parent for parent, child, _, _ in CHAINS}
    rows = []
    for index, (pose, ref) in enumerate(zip(fixed, reference, strict=True)):
        for joint in sorted(pose.keys() & ref.keys() & parents.keys()):
            rows.append((feature_rows(fixed, joint, parents[joint], index),
                         ref[joint][2], pose[joint][2], temporal[index][joint][2]))
    return np.asarray([r[0] for r in rows]), np.asarray([r[1:] for r in rows]).reshape(-1, 3)


def score(training, held_out):
    features, values = (np.concatenate(blocks) for blocks in zip(*training))
    target = values[:, 0]
    # A fixed penalty avoids tuning on the held-out views.
    penalty = np.eye(features.shape[1])*2
    penalty[0, 0] = 0
    weights = np.linalg.solve(features.T @ features+penalty, features.T @ target)
    results = []
    for x, y in held_out:
        predictions = np.column_stack((y[:, 1:], x @ weights))
        errors = np.abs(predictions-y[:, :1]).mean(axis=0)
        results.append(dict(samples=len(y), mean_absolute_depth_error={
            name: round(float(error), 6)
            for name, error in zip(("fixed", "temporal", "learned"), errors)}))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qca", type=Path)
    parser.add_argument("model", type=Path)
    parser.add_argument("cameras", type=Path, nargs=4)
    parser.add_argument("--notebook", type=Path, default=Path("ReplayAxis_Markerless_TwoView.ipynb"))
    args = parser.parse_args()
    api = load_notebook(args.notebook)
    net = cv2.dnn.readNetFromONNX(str(args.model))
    calibration = cameras_from_qca(args.qca)
    cases = {}
    for i, j in ((0, 1), (1, 0), (2, 3), (3, 2)):
        camera = args.cameras[i]
        cases[camera.stem] = prepare(*load_case(api, net, calibration, (camera, args.cameras[j])))
    group_a, group_b = list(cases)[:2], list(cases)[2:]
    results = {}
    for training, test in ((group_a, group_b), (group_b, group_a)):
        rows = score([cases[c] for c in training], [cases[c] for c in test])
        for view, metrics in zip(test, rows):
            results[view] = dict(training_views=training, **metrics)
    print(json.dumps(results, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
