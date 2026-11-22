"""Exercise the paired-trial workflow on the public Pose2Sim demo clips."""
import argparse
from collections import Counter
import csv
import json
import os
from pathlib import Path
import sys

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "two_view_geometry"))
from replayaxis_geometry import load_notebook
from replayaxis_real import cameras_from_qca
from validate_manifest import validate


def metadata(path):
    cap = cv2.VideoCapture(str(path))
    try:
        if not cap.isOpened():
            raise ValueError(f"Cannot open {path}.")
        return [int(cap.get(key)) for key in (
            cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FRAME_COUNT
        )], cap.get(cv2.CAP_PROP_FPS)
    finally:
        cap.release()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("qca", "detector", "cam01", "cam02", "output"):
        parser.add_argument(name, type=lambda value: Path(value).resolve())
    parser.add_argument("--notebook", type=Path, default=Path("ReplayAxis_Markerless_TwoView.ipynb"))
    args = parser.parse_args()
    paths = (args.cam01, args.cam02)
    info = [metadata(path) for path in paths]
    if any(item != ([1080, 1920, 100], 60.) for item in info):
        parser.error("Expected the original 1080 × 1920, 100-frame, 60 fps demo clips.")
    api = load_notebook(args.notebook, extra_signatures=(
        "def replay_video_pair(", "class StreamingStereo:", "def reconstruct_sample(",
    ))
    qca = cameras_from_qca(args.qca)
    cameras = []
    for name in ("cam01", "cam02"):
        camera = qca[name]
        # Express the verified +4 px video-to-still crop in decoded intrinsics.
        camera["K"][0, 2] -= 4
        cameras.append(dict(image_size=[1080, 1920],
                            **{key: np.asarray(value).tolist() for key, value in camera.items()}))
    args.output.mkdir(parents=True, exist_ok=False)
    calibration = args.output / "camera_pair.json"
    calibration.write_text(json.dumps(dict(units="m", cameras=cameras), indent=2) + "\n")
    sync = args.output / "nominal_timestamps.csv"
    with sync.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(("camera", "frame_index", "time_ns"))
        for camera in ("A", "B"):
            writer.writerows((camera, i, round(i * 1e9 / 60)) for i in range(100))
    original = Path.cwd()
    try:
        os.chdir(args.output)
        frames = api["analyze"](*paths, calibration, duration=100 / 60, rate=60,
                                onnx_model=args.detector, timestamp_csv=sync)
    finally:
        os.chdir(original)
    timing = args.output / "ReplayAxis_Real_Clip_timing.json"
    timing_report = json.loads(timing.read_text())
    timing_report.update(pairing_mode="nominal equal frame index",
                         skew_source="synthetic timestamps derived from nominal 60 Hz")
    timing.write_text(json.dumps(timing_report, indent=2) + "\n")
    labels = "ReplayAxis_Real_Clip_joints.csv"
    manifest = args.output / "manifest.csv"
    header = Path(__file__).with_name("manifest_template.csv").read_text().strip().split(",")
    with manifest.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerow(("demo-trial", "demo-athlete", "train", "treadmill_demo", "",
                         "cam01", "cam02", *paths, calibration.name, sync.name,
                         labels, "two_view", labels))
    _, errors = validate(manifest)
    if errors:
        raise ValueError("\n".join(errors))
    with (args.output / labels).open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    statuses = Counter(row["status"] for row in rows)
    aligned = {tuple(frame["source_frames"]) for frame in frames}
    if aligned != {(i, i) for i in range(100)} or len(frames) != 100:
        raise ValueError("Did not export exactly one pair for each original frame.")
    if len(rows) != len(frames) * len(api["JOINTS"]) or not statuses["reconstructed"]:
        raise ValueError("Missing joint decisions or no reconstructed labels.")
    summary = dict(paired_frames=len(frames), label_rows=len(rows), statuses=statuses,
                   frames_with_3d=sum(bool(frame["points"]) for frame in frames),
                   timestamp_source="nominal frame index at 60 Hz",
                   reference_kind="two_view", coordinates="QCA venue metres",
                   opencv_version=cv2.__version__)
    report = json.dumps(summary, indent=2, allow_nan=False)
    (args.output / "rehearsal_summary.json").write_text(report + "\n")
    print(report)


if __name__ == "__main__":
    main()
