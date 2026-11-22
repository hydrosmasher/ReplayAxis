"""Measure the impact of the Pose2Sim video center crop on calibrated stereo."""
import argparse
from itertools import combinations
import json
from pathlib import Path

import cv2
import numpy as np

from benchmark_acceptance import score
from benchmark_heldout_views import centered
from benchmark_temporal import cameras_from_qca, collect
from benchmark_video_pixel_mapping import calibration_sizes, maps
from reconstruct import load_notebook


def reconstruct_pairs(api, cameras, observations, sizes, mapping):
    corrected = {}
    for name, frames in observations.items():
        scale, shift = mapping[name]
        camera = {**cameras[name], "image_size": sizes[name]}
        corrected[name] = [
            api["correct_pose_pixels"]({
                j: [(x + .5) * scale - .5 + shift, y, confidence]
                for j, (x, y, confidence) in pose.items()}, camera)
            for pose in frames]
    return {
        (a, b): [api["reconstruct"](first, second, [cameras[a], cameras[b]])["points"]
                 for first, second in zip(corrected[a], corrected[b])]
        for a, b in combinations(corrected, 2)}


def shared_references(reference, other):
    return [{j: point for j, point in a.items() if j in b} for a, b in zip(reference, other)]


def wrist_gap(pairs):
    a = pairs["cam01", "cam02"][10].get(15)
    b = pairs["cam03", "cam04"][10].get(15)
    return float(np.linalg.norm(np.asarray(a) - b)) if a is not None and b is not None else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qca", type=Path)
    parser.add_argument("detector", type=Path)
    parser.add_argument("videos", type=Path, nargs=4)
    parser.add_argument("--notebook", type=Path, default=Path("ReplayAxis_Markerless_TwoView.ipynb"))
    args = parser.parse_args()
    paths = sorted(args.videos)
    names = [path.stem for path in paths]
    if names != ["cam01", "cam02", "cam03", "cam04"]:
        parser.error("Provide the four named Pose2Sim demo clips.")
    api = load_notebook(args.notebook)
    detector = cv2.dnn.readNetFromONNX(str(args.detector))
    cameras = cameras_from_qca(args.qca)
    calibrated = calibration_sizes(args.qca)
    sizes, observations = {}, {}
    for path in paths:
        frames, poses = collect(path, detector, api["detect_onnx_pose"], stride=1)
        sizes[path.stem] = frames[0].shape[::-1]
        observations[path.stem] = poses
    count = min(map(len, observations.values()))
    if count <= 10:
        parser.error("At least 11 frames are required for the wrist diagnostic.")
    observations = {name: poses[:count] for name, poses in observations.items()}
    mappings = maps(sizes, calibrated)
    baseline = reconstruct_pairs(api, cameras, observations, sizes, mappings["identity"])
    crop = reconstruct_pairs(api, cameras, observations, calibrated, mappings["center_crop"])
    cases = []
    for pair in baseline:
        heldout = tuple(name for name in names if name not in pair)
        comparisons = {}
        rotation = cameras[pair[0]]["R"]
        for mode in ("venue", "hip_relative"):
            a_ref, b_ref = baseline[heldout], crop[heldout]
            a_pred, b_pred = baseline[pair], crop[pair]
            if mode == "hip_relative":
                a_ref, b_ref, a_pred, b_pred = [
                    [centered(row, rotation) for row in sequence]
                    for sequence in (a_ref, b_ref, a_pred, b_pred)]
            comparisons[mode] = {
                "identity": dict(native=score(a_pred, a_ref, 1),
                                 shared=score(a_pred, shared_references(a_ref, b_ref), 1)),
                "center_crop": dict(native=score(b_pred, b_ref, 1),
                                    shared=score(b_pred, shared_references(b_ref, a_ref), 1))}
        cases.append(dict(input_pair=pair, heldout_pair=heldout, metrics=comparisons))
    print(json.dumps(dict(frames=count, opencv_version=cv2.__version__,
                          horizontal_offset_px={name: mapping[1] for name, mapping
                                                in mappings["center_crop"].items()},
                          frame10_left_wrist_gap_m={"identity": wrist_gap(baseline),
                                                    "center_crop": wrist_gap(crop)},
                          cases=cases), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
