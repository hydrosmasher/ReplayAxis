"""Sweep capture errors for the synthetic parallel-camera benchmark."""

import argparse
import csv
import math
import random
import statistics
from pathlib import Path

from benchmark import estimate, flexion, project


FPS = 240
FRAME_COUNT = 48
TRACKS = ("hip", "knee", "ankle", "ball")


def scene(time_s):
    phase = 2 * math.pi * 3 * time_s
    knee = [0.2 + 2 * time_s, 0.3 + 0.1 * math.sin(phase), 5]
    hip = [knee[0] - 0.1, knee[1] + 0.4, 5.1]
    ankle = [knee[0] + 0.25 * math.cos(phase), knee[1] - 0.35, 5.12]
    ball = [-2 + 40 * time_s, 0.8 + 2 * time_s - 4.905 * time_s**2, 4.7]
    return dict(zip(TRACKS, (hip, knee, ankle, ball)))


def summarize(skew_ms, noise_px, calibration_mm):
    # Reuse the same noise sequence across levels for paired comparisons.
    rng = random.Random(42)
    cameras = {"A": -2, "B": -1, "C": 1, "D": 2}
    calibration = {"focal_px": 1000, "inlier_threshold_px": 2}
    errors = {track: [] for track in ("ball_mm", "angle_deg", "speed_m_s")}
    rejected = 0
    ambiguous_tracks = 0
    observations_with_decision = 0
    previous = None
    for frame in range(FRAME_COUNT):
        time_s = frame / FPS
        truth = scene(time_s)
        inputs = {track: [] for track in TRACKS}
        for camera, x in cameras.items():
            actual_time = time_s + skew_ms / 1000 if camera == "D" else time_s
            actual_x = x + calibration_mm / 1000 if camera == "D" else x
            for track, point in scene(actual_time).items():
                pixel = [value + noise_px * rng.gauss(0, 1)
                         for value in project(point, actual_x, calibration["focal_px"])]
                inputs[track].append({"camera_id": camera, "camera_x_m": x,
                                      "frame_id": f"{camera}:{frame}", "time_s": time_s,
                                      "pixel": pixel})
        result = estimate(inputs, calibration)
        for track in result["tracks"].values():
            ambiguous_tracks += track["point_m"] is None
            for observation in track["observations"]:
                decision = observation.get("decision")
                observations_with_decision += decision is not None
                rejected += decision == "rejected"
        ball = result["tracks"]["ball"]["point_m"]
        angle = result["knee_flexion_proxy_deg"]
        if angle is not None:
            errors["angle_deg"].append(abs(angle - flexion(*(truth[k] for k in TRACKS[:3]))))
        if ball is not None:
            errors["ball_mm"].append(1000 * math.dist(ball, truth["ball"]))
            if previous is not None:
                speed = FPS * math.dist(ball, previous)
                speed_truth = FPS * math.dist(truth["ball"], scene((frame - 1) / FPS)["ball"])
                errors["speed_m_s"].append(abs(speed - speed_truth))
        previous = ball

    row = {"skew_ms": skew_ms, "noise_px_sd": noise_px, "calibration_mm": calibration_mm,
           "frames": FRAME_COUNT, "ambiguous_tracks": ambiguous_tracks,
           "rejected_views": rejected, "views_with_decision": observations_with_decision}
    for metric, values in errors.items():
        row[f"{metric}_n"] = len(values)
        row[f"{metric}_mae"] = statistics.mean(values) if values else None
        row[f"{metric}_max"] = max(values) if values else None
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    settings = [(0, 0, 0), *((n, 0, 0) for n in (0.1, 0.5, 1, 2)),
                *((0, n, 0) for n in (0.25, 0.5, 1, 2)),
                *((0, 0, n) for n in (2, 5, 10, 20)), (0.5, 0.5, 5), (1, 1, 10)]
    rows = [summarize(*setting) for setting in settings]
    clean = rows[0]
    if any(clean[f"{metric}_max"] > 1e-8 for metric in ("ball_mm", "angle_deg", "speed_m_s")):
        raise RuntimeError("Clean fixture exceeded numerical tolerance")
    if clean["speed_m_s_n"] != FRAME_COUNT - 1:
        raise RuntimeError("Clean fixture did not produce all adjacent speed samples")
    with args.output.open("x", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
