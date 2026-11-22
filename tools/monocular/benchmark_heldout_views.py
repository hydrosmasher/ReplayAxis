"""Compare monocular and stereo pose against two disjoint calibrated views."""
import argparse
from itertools import combinations
import json
from pathlib import Path

import cv2
import numpy as np

from benchmark_acceptance import score
from benchmark_motionbert import CHECKPOINT_SHA256, load_model, predict
from benchmark_temporal import cameras_from_qca, collect
from reconstruct import lift, load_notebook


TORSO = {11, 12, 23, 24}


def centered(row, rotation):
    if not {23, 24}.issubset(row):
        return {}
    hips = (np.asarray(row[23]) + row[24]) / 2
    return {j: rotation @ (value - hips) for j, value in row.items()}


def torso_scale(rows):
    lengths = []
    for row in rows:
        if TORSO.issubset(row):
            shoulders = (np.asarray(row[11]) + row[12]) / 2
            lengths.append(np.linalg.norm(shoulders))
    return float(np.median(lengths)) if lengths else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source", "checkpoint", "qca", "detector"):
        parser.add_argument(name, type=Path)
    parser.add_argument("videos", type=Path, nargs=4)
    parser.add_argument("--notebook", type=Path, default=Path("ReplayAxis_Markerless_TwoView.ipynb"))
    args = parser.parse_args()
    names = [path.stem for path in args.videos]
    if len(set(names)) != 4:
        parser.error("Provide four distinct camera names.")
    api = load_notebook(args.notebook)
    model, torch = load_model(args.source, args.checkpoint)
    detector = cv2.dnn.readNetFromONNX(str(args.detector))
    cameras = cameras_from_qca(args.qca)
    tracks = {}
    for name, path in zip(names, args.videos):
        frames, poses = collect(path, detector, api["detect_onnx_pose"], stride=1)
        cameras[name]["image_size"] = frames[0].shape[::-1]
        tracks[name] = [api["correct_pose_pixels"](p, cameras[name]) for p in poses]
    frame_count = min(map(len, tracks.values()))
    tracks = {name: poses[:frame_count] for name, poses in tracks.items()}
    mono = {name: predict(model, torch, poses) for name, poses in tracks.items()}
    fixed = {name: lift(poses) for name, poses in tracks.items()}
    stereo = {pair: [api["reconstruct"](a, b, [cameras[name] for name in pair])["points"]
                     for a, b in zip(*(tracks[name] for name in pair))]
              for pair in combinations(names, 2)}
    cases = []
    for inputs, values in stereo.items():
        held_out = tuple(name for name in names if name not in inputs)
        raw_reference = stereo[held_out]
        venue = score(values, raw_reference, 1)
        fold = dict(input_pair=inputs, reference_pair=held_out, stereo_venue=venue, poses=[])
        cases.append(fold)
        for view in inputs:
            rotation = cameras[view]["R"]
            reference = [centered(row, rotation) for row in raw_reference]
            torso = torso_scale(reference)
            if torso is None:
                fold["pose_unavailable"] = "Held-out pair has no usable torso scale."
                break
            two_view = [centered(row, rotation) for row in values]
            methods = {"fixed": (fixed[view], torso), "motionbert_lite": (mono[view], torso),
                       "calibrated_stereo": (two_view, 1)}
            common = [{j: target[j] for j in target.keys() & a.keys() & b.keys() & c.keys()}
                      for target, a, b, c in zip(reference, fixed[view], mono[view], two_view)]
            fold["poses"].append(dict(monocular_view=view, reference_torso_m=torso,
                              all_eligible={k: score(p, reference, s) for k, (p, s) in methods.items()},
                              common_joints={k: score(p, common, s) for k, (p, s) in methods.items()}))
    print(json.dumps(dict(frame_pairs=frame_count, frame_matching="equal source frame index",
                          checkpoint_sha256=CHECKPOINT_SHA256, opencv_version=cv2.__version__,
                          torch_version=torch.__version__, cases=cases), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
