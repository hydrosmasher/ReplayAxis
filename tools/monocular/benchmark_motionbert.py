"""Compare MotionBERT-Lite and ReplayAxis on identical dense 2D tracks."""
import argparse
from functools import partial
import hashlib
import json
from pathlib import Path
import sys

import cv2
import numpy as np

from benchmark_acceptance import score
from benchmark_temporal import cameras_from_qca, load_case
from reconstruct import lift, load_notebook


CHECKPOINT_SHA256 = "9811155371db4ca5d20f31a36a232d41012e12e1333882888a564d741861148f"
H36M = {0: 9, 11: 11, 12: 14, 13: 12, 14: 15, 15: 13, 16: 16,
        23: 4, 24: 1, 25: 5, 26: 2, 27: 6, 28: 3}
LEFT = [4, 5, 6, 11, 12, 13]
RIGHT = [1, 2, 3, 14, 15, 16]


def prepare(observations):
    # Approximate Halpe-only landmarks from the shared COCO detections.
    data = np.zeros((len(observations), 17, 3), dtype=np.float32)
    for i, row in enumerate(observations):
        for joint, value in row.items():
            if joint in H36M:
                data[i, H36M[joint]] = value
    for output, a, b in ((0, 1, 4), (8, 11, 14), (7, 0, 8), (10, 8, 9)):
        valid = (data[:, a, 2] > 0) & (data[:, b, 2] > 0)
        data[valid, output] = (data[valid, a] + data[valid, b]) / 2
        data[valid, output, 2] = np.minimum(data[valid, a, 2], data[valid, b, 2])
    visible = data[..., 2] > 0
    xy = data[..., :2]
    if not visible.any():
        raise ValueError("No visible detections.")
    low, high = xy[visible].min(axis=0), xy[visible].max(axis=0)
    extent = np.max(high - low)
    if extent <= 0:
        raise ValueError("Zero extent for 2D track.")
    xy[visible] = (xy[visible] - (low + high) / 2) * 2 / extent
    return data


def flip(data):
    result = data.copy()
    result[..., LEFT + RIGHT, :] = data[..., RIGHT + LEFT, :]
    result[..., 0] *= -1
    return result


def predict(model, torch, observations):
    data = prepare(observations)
    with torch.inference_mode():
        original = model(torch.from_numpy(data[None])).numpy()[0]
        reflected = model(torch.from_numpy(flip(data)[None])).numpy()[0]
    pose = (original + flip(reflected)) / 2
    hips = (pose[:, 1] + pose[:, 4]) / 2
    shoulders = (pose[:, 11] + pose[:, 14]) / 2
    torso = np.linalg.norm(shoulders - hips, axis=1)
    visible = np.all(data[:, [1, 4, 11, 14], 2] >= 0.55, axis=1)
    scale = np.median(torso[visible]) if visible.any() else np.nan
    if not np.isfinite(scale) or scale <= 0:
        raise ValueError("No reliable MotionBERT torso scale.")
    normalized = (pose - hips[:, None]) / scale
    return [{joint: frame[index] for joint, index in H36M.items()}
            if row else {} for frame, row in zip(normalized, observations)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="MotionBERT upstream source directory")
    parser.add_argument("checkpoint", type=Path)
    parser.add_argument("qca", type=Path)
    parser.add_argument("detector", type=Path)
    parser.add_argument("camera_a", type=Path)
    parser.add_argument("camera_b", type=Path)
    parser.add_argument("--notebook", type=Path, default=Path("ReplayAxis_Markerless_TwoView.ipynb"))
    args = parser.parse_args()
    if hashlib.sha256(args.checkpoint.read_bytes()).hexdigest() != CHECKPOINT_SHA256:
        parser.error("MotionBERT-Lite checkpoint SHA-256 mismatch.")
    sys.path.insert(0, str(args.source.resolve()))
    import torch
    from lib.model.DSTformer import DSTformer

    torch.set_num_threads(4)
    model = DSTformer(norm_layer=partial(torch.nn.LayerNorm, eps=1e-6))
    checkpoint = torch.load(args.checkpoint, map_location="cpu", weights_only=True)
    model.load_state_dict({k.removeprefix("module."): v for k, v in checkpoint["model_pos"].items()})
    model.eval()
    api = load_notebook(args.notebook)
    net = cv2.dnn.readNetFromONNX(str(args.detector))
    cameras = cameras_from_qca(args.qca)
    cases = []
    for a, b in ((args.camera_a, args.camera_b), (args.camera_b, args.camera_a)):
        observations, reference, torso = load_case(
            api, net, cameras, (a, b), metric_reference=True, stride=1)
        fixed = lift(observations)
        temporal = lift(observations, temporal=True)
        learned = predict(model, torch, observations)
        common = [{j: target[j] for j in target.keys() & f.keys() & t.keys() & m.keys()}
                  for target, f, t, m in zip(reference, fixed, temporal, learned)]
        methods = dict(fixed=fixed, temporal=temporal, motionbert_lite=learned)
        cases.append(dict(input_camera=a.stem, reference_partner=b.stem,
                          frame_pairs=len(reference), torso_m=torso,
                          all_eligible={k: score(v, reference, torso) for k, v in methods.items()},
                          common_joints={k: score(v, common, torso) for k, v in methods.items()}))
    print(json.dumps(dict(checkpoint_sha256=CHECKPOINT_SHA256, torch_version=torch.__version__,
                          opencv_version=cv2.__version__, source_frame_stride=1,
                          scale_source="reference torso length",
                          cases=cases), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
