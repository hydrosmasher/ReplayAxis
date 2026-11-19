"""Reproduce synthetic multiview measurements with Python's standard library."""

import argparse
import itertools
import json
import math
from pathlib import Path


def mean(values):
    return sum(values) / len(values)


def project(point, camera_x, focal_px):
    x, y, z = point
    return [focal_px * (x - camera_x) / z, focal_px * y / z]


def triangulate(views, focal_px):
    """Fit the pinhole model for parallel cameras on a horizontal baseline."""
    centre = mean([view["camera_x_m"] for view in views])
    average_u = mean([view["pixel"][0] for view in views])
    offsets = [view["camera_x_m"] - centre for view in views]
    baseline_variance = sum(offset ** 2 for offset in offsets)
    if baseline_variance <= 0:
        raise ValueError("At least two distinct camera positions are required")
    slope = sum(offset * (view["pixel"][0] - average_u)
                for view, offset in zip(views, offsets)) / baseline_variance
    if slope >= 0:
        raise ValueError("Observations do not yield a positive depth")
    depth = -focal_px / slope
    return [centre + average_u * depth / focal_px,
            mean([view["pixel"][1] for view in views]) * depth / focal_px,
            depth]


def residual(point, view, focal_px):
    return math.dist(project(point, view["camera_x_m"], focal_px), view["pixel"])


def reconstruct(views, calibration):
    focal_px = calibration["focal_px"]
    threshold_px = calibration["inlier_threshold_px"]
    candidates = {}
    for pair in itertools.combinations(views, 2):
        try:
            seed = triangulate(pair, focal_px)
        except ValueError:
            continue
        inliers = [view for view in views if residual(seed, view, focal_px) <= threshold_px]
        if len(inliers) >= 2:
            candidates[tuple(view["camera_id"] for view in inliers)] = inliers
    ranked = sorted(candidates, key=len, reverse=True)
    if not ranked or (len(ranked) > 1 and len(ranked[0]) == len(ranked[1])):
        return {"status": "ambiguous", "point_m": None, "observations": views}
    accepted = candidates[ranked[0]]
    point = triangulate(accepted, focal_px)
    evidence = []
    for view in views:
        error = residual(point, view, focal_px)
        evidence.append({**view, "residual_px": error,
                         "decision": "accepted" if view in accepted else "rejected",
                         "reason": "selected_consensus" if view in accepted else "outside_consensus"})
    if any(item["residual_px"] > threshold_px for item in evidence if item["decision"] == "accepted"):
        return {"status": "inconsistent_refit", "point_m": None, "observations": evidence}
    return {"status": "reconstructed", "point_m": point, "observations": evidence}


def flexion(hip, knee, ankle):
    thigh = [a - b for a, b in zip(hip, knee)]
    shin = [a - b for a, b in zip(ankle, knee)]
    cosine = sum(a * b for a, b in zip(thigh, shin)) / (math.hypot(*thigh) * math.hypot(*shin))
    return 180 - math.degrees(math.acos(max(-1, min(1, cosine))))


def estimate(observations, calibration):
    tracks = {name: reconstruct(views, calibration) for name, views in observations.items()}
    joints = [tracks[name]["point_m"] for name in ("hip", "knee", "ankle")]
    angle = flexion(*joints) if all(point is not None for point in joints) else None
    return {"tracks": tracks, "knee_flexion_proxy_deg": angle}


def benchmark():
    calibration = {"model": "parallel-pinhole-horizontal", "focal_px": 1000,
                   "principal_point_px": [0, 0], "inlier_threshold_px": 2,
                   "camera_x_m": {"A": -2, "B": -1, "C": 1, "D": 2}}
    truth = {"hip": [0.1, 0.7, 5.1], "knee": [0.2, 0.3, 5],
             "ankle": [0.45, -0.05, 5.12], "ball": [-0.1, 0.8, 4.7]}
    cases = {}
    for scenario in ("clean", "corrupted_view", "missing_view", "corrupted_and_missing"):
        observations = {}
        for name, point in truth.items():
            views = []
            for camera, camera_x in calibration["camera_x_m"].items():
                if scenario in ("missing_view", "corrupted_and_missing") and camera == "C":
                    continue
                pixel = project(point, camera_x, calibration["focal_px"])
                if scenario in ("corrupted_view", "corrupted_and_missing") and camera == "D" and name in ("knee", "ball"):
                    pixel[0] += 60
                views.append({"camera_id": camera, "camera_x_m": camera_x,
                              "frame_id": f"{camera}:120", "time_s": 0.5, "pixel": pixel})
            observations[name] = views
        result = estimate(observations, calibration)
        cases[scenario] = {"inputs": observations, "result": result}
    return {"schema_version": 1, "algorithm": "pair-consensus-parallel-pinhole-v1",
            "metric": "180 degrees minus geometric hip-knee-ankle angle",
            "calibration": calibration, "cases": cases, "synthetic_truth_m": truth}


def verify(record):
    truth = record["synthetic_truth_m"]
    expected_angle = flexion(truth["hip"], truth["knee"], truth["ankle"])
    for name, case in record["cases"].items():
        reproduced = estimate(case["inputs"], record["calibration"])
        if name == "corrupted_and_missing":
            assert reproduced["knee_flexion_proxy_deg"] is None
            assert reproduced["tracks"]["ball"]["status"] == "ambiguous"
        else:
            assert abs(reproduced["knee_flexion_proxy_deg"] - expected_angle) < 1e-8
            for track, target in truth.items():
                assert math.dist(reproduced["tracks"][track]["point_m"], target) < 1e-8
        assert reproduced == case["result"]
    rejected = record["cases"]["corrupted_view"]["result"]["tracks"]["knee"]["observations"]
    assert [view["camera_id"] for view in rejected if view["decision"] == "rejected"] == ["D"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        verify(json.loads(args.path.read_text()))
        print("Verified four scenarios and exact replay from exported observations.")
        return
    with args.path.open("x") as output:
        json.dump(benchmark(), output, indent=2, allow_nan=False)
        output.write("\n")


if __name__ == "__main__":
    main()
