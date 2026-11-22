"""Compare manual wrist marks and detector pixels on the audited frame."""
import argparse
from itertools import combinations
import json
from pathlib import Path

import cv2
import numpy as np

from benchmark_temporal import cameras_from_qca
from reconstruct import load_notebook


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("labels", "qca", "detector"):
        parser.add_argument(name, type=Path)
    parser.add_argument("videos", type=Path, nargs=4)
    parser.add_argument("--notebook", type=Path, default=Path("ReplayAxis_Markerless_TwoView.ipynb"))
    args = parser.parse_args()
    labels = json.loads(args.labels.read_text())
    joint = labels["joint"]
    api = load_notebook(args.notebook)
    net = cv2.dnn.readNetFromONNX(str(args.detector))
    cameras = cameras_from_qca(args.qca)
    pixels = {"detector": {}, "manual": {}}
    views = {}
    for path in args.videos:
        name = path.stem
        cap = cv2.VideoCapture(str(path))
        try:
            cap.set(cv2.CAP_PROP_POS_FRAMES, labels["source_frame"])
            ok, frame = cap.read()
        finally:
            cap.release()
        if not ok:
            raise ValueError(f"Cannot decode requested frame from {path}.")
        camera = cameras[name]
        camera["image_size"] = frame.shape[1], frame.shape[0]
        manual = labels["pixels"][name]
        detected = api["detect_onnx_pose"](net, frame)[joint]
        views[name] = dict(manual_px=manual, detection=detected,
                           disagreement_px=float(np.linalg.norm(np.asarray(manual) - detected[:2])))
        for method, point in (("detector", detected), ("manual", [*manual, 1.])):
            pixels[method][name] = api["correct_pose_pixels"]({joint: point}, camera)[joint][:2]
    results = {}
    for method, observations in pixels.items():
        pair_results = {}
        accepted, diagnostic = {}, {}
        for a, b in combinations(observations, 2):
            details = {}
            point, status = api["triangulate"](observations[a], observations[b],
                                                cameras[a], cameras[b], float("inf"), details)
            if point is not None:
                diagnostic[a, b] = np.asarray(point)
                if max(details["reprojection_px"]) <= 10:
                    accepted[a, b] = np.asarray(point)
                else:
                    status, point = "reprojection error", None
            pair_results[f"{a}+{b}"] = dict(point_m=point, rejection=status if point is None else None,
                                            **details)
        disagreement = {}
        for a, b in combinations(accepted, 2):
            if not set(a) & set(b):
                disagreement[f"{'+'.join(a)} vs {'+'.join(b)}"] = float(
                    np.linalg.norm(accepted[a] - accepted[b]))
        primary = (("cam01", "cam02"), ("cam03", "cam04"))
        raw_delta = None
        if all(pair in diagnostic for pair in primary):
            raw_delta = float(np.linalg.norm(diagnostic[primary[0]] - diagnostic[primary[1]]))
        results[method] = dict(pairs=pair_results, disjoint_disagreement_m=disagreement,
                               primary_disagreement_without_pixel_gate_m=raw_delta)
    print(json.dumps(dict(source_frame=labels["source_frame"], joint=joint, views=views,
                          comparisons=results), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
