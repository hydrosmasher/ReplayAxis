"""Evaluate fixed input rotations on the underwater manual audit frames."""
import argparse
import csv
from pathlib import Path
from statistics import median
import sys

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools/monocular"))
from reconstruct import detect_rotated, load_notebook

JOINTS = {"hip": (23, 24), "shoulder": (11, 12), "wrist": (15, 16), "cap": (0,)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video")
    parser.add_argument("model")
    parser.add_argument("--labels", type=Path, default=Path(__file__).with_name("underwater_manual_labels.csv"))
    parser.add_argument("--notebook", type=Path, default=Path("ReplayAxis_Markerless_TwoView.ipynb"))
    args = parser.parse_args()
    with args.labels.open() as stream:
        labels = list(csv.DictReader(stream))
    api = load_notebook(args.notebook)
    net = cv2.dnn.readNetFromONNX(args.model)
    cap = cv2.VideoCapture(args.video)
    frames = {}
    try:
        for index in sorted({int(row["frame"]) for row in labels}):
            cap.set(cv2.CAP_PROP_POS_FRAMES, index)
            ok, frame = cap.read()
            if not ok:
                raise ValueError(f"Could not read frame {index}.")
            frames[index] = frame
    finally:
        cap.release()
    for name in ("none", "clockwise", "counterclockwise"):
        output = {index: detect_rotated(api["detect_onnx_pose"], net, frame, name)
                  for index, frame in frames.items()}
        print(name)
        for landmark, ids in JOINTS.items():
            rows = [row for row in labels if row["landmark"] == landmark]
            distances = []
            for row in rows:
                target = float(row["x_384"])*5, float(row["y_216"])*5
                pose = output[int(row["frame"])]
                errors = [((x-target[0])**2+(y-target[1])**2)**.5
                          for j, (x, y, score) in pose.items() if j in ids and score >= .55]
                if errors:
                    distances.append(min(errors))
            print(landmark, f"{len(distances)}/{len(rows)}",
                  f"{median(distances):.1f} px" if distances and landmark != "cap" else "")


if __name__ == "__main__":
    main()
