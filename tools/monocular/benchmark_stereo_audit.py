"""Audit stereo rejections and one-frame sensitivity against disjoint views."""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

import cv2
import numpy as np

from benchmark_acceptance import JOINTS, score
from benchmark_temporal import cameras_from_qca, collect
from reconstruct import load_notebook


OFFSETS = ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1))
CONFIDENCE = .55


def audit_case(api, tracks, cameras, inputs, references, indices):
    a, b = inputs
    baseline = None
    sweeps = []
    for da, db in OFFSETS:
        decisions = [api["reconstruct"](tracks[a][i + da], tracks[b][i + db],
                                        [cameras[a], cameras[b]], confidence=CONFIDENCE)
                     for i in indices]
        sweeps.append({"offset_frames": [da, db], **score(
            [d["points"] for d in decisions], references, 1)})
        if da == db == 0:
            baseline = decisions

    rejected, low_by_camera, rejected_by_joint = Counter(), Counter(), Counter()
    largest = []
    for index, decision, reference in zip(indices, baseline, references):
        for joint in sorted(JOINTS & reference.keys()):
            evidence = decision["evidence"][joint]
            if joint not in decision["points"]:
                reason = decision["rejected"][joint]
                rejected[reason] += 1
                rejected_by_joint[str(joint)] += 1
                if reason == "low visibility":
                    for camera, key in zip(inputs, ("camera_a", "camera_b")):
                        detection = evidence[key]
                        if detection is None or detection[2] < CONFIDENCE:
                            low_by_camera[camera] += 1
                continue
            error = np.linalg.norm(np.asarray(decision["points"][joint]) - reference[joint])
            largest.append(dict(frame=index, joint=joint, error_m=float(error),
                                ray_angle_deg=evidence["ray_angle_deg"],
                                reprojection_px=evidence["reprojection_px"],
                                confidence=[evidence[key][2] for key in ("camera_a", "camera_b")]))
    return dict(rejections=dict(rejected), low_visibility_by_camera=dict(low_by_camera),
                rejections_by_joint=dict(rejected_by_joint),
                largest_errors=sorted(largest, key=lambda row: -row["error_m"])[:5],
                offset_sweep=sweeps)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qca", type=Path)
    parser.add_argument("detector", type=Path)
    parser.add_argument("videos", type=Path, nargs=4)
    parser.add_argument("--notebook", type=Path, default=Path("ReplayAxis_Markerless_TwoView.ipynb"))
    args = parser.parse_args()
    names = [path.stem for path in args.videos]
    if len(set(names)) != 4:
        parser.error("Provide four distinct camera views.")
    api = load_notebook(args.notebook)
    detector = cv2.dnn.readNetFromONNX(str(args.detector))
    cameras = cameras_from_qca(args.qca)
    tracks = {}
    for path in args.videos:
        frames, poses = collect(path, detector, api["detect_onnx_pose"], stride=1)
        camera = cameras[path.stem]
        camera["image_size"] = frames[0].shape[::-1]
        tracks[path.stem] = [api["correct_pose_pixels"](row, camera) for row in poses]
    indices = range(1, min(map(len, tracks.values())) - 1)
    if not indices:
        parser.error("At least three frames per view are required.")
    cases = []
    for pair_a in combinations(names, 2):
        pair_b = tuple(name for name in names if name not in pair_a)
        a, b = pair_b
        references = [api["reconstruct"](tracks[a][i], tracks[b][i],
                                          [cameras[a], cameras[b]])["points"] for i in indices]
        cases.append(dict(input_pair=pair_a, reference_pair=pair_b,
                          **audit_case(api, tracks, cameras, pair_a, references, indices)))
    print(json.dumps(dict(frame_indices=[indices.start, indices.stop - 1],
                          opencv_version=cv2.__version__, confidence_threshold=CONFIDENCE,
                          cases=cases), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
