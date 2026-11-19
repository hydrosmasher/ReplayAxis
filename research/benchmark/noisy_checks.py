"""Compare camera policies using noisy external checks and paired frames."""

import argparse
import csv
import itertools
import json
import math
import random
import statistics
from pathlib import Path

from benchmark import reconstruct, residual
from capture_policy import LAYOUTS
from multiframe import FPS, FRAME_COUNT, project, scene

CALIBRATION = {"focal_px": 1000, "inlier_threshold_px": 2}
POLICIES = ("residual_only", "exclude", "downweight")
CONDITIONS = {"clean": (0, 0, 0.5), "borderline": (0.1, 0, 0.5),
              "combined": (0.5, 5, 0.5)}
SEEDS = range(20)


def weighted_fit(views):
    weights = [view["weight"] for view in views]
    total = sum(weights)
    centre = sum(w * view["camera_x_m"] for w, view in zip(weights, views)) / total
    u = sum(w * view["pixel"][0] for w, view in zip(weights, views)) / total
    v = sum(w * view["pixel"][1] for w, view in zip(weights, views)) / total
    offsets = [view["camera_x_m"] - centre for view in views]
    variance = sum(w * dx * dx for w, dx in zip(weights, offsets))
    slope = sum(w * dx * (view["pixel"][0] - u)
                for w, dx, view in zip(weights, offsets, views)) / variance
    if slope >= 0:
        raise ValueError("Nonpositive inferred depth")
    focal = CALIBRATION["focal_px"]
    depth = -focal / slope
    return [centre + u * depth / focal, v * depth / focal, depth]


def soft_estimate(views):
    candidates = {}
    for pair in itertools.combinations(views, 2):
        try:
            seed = weighted_fit(pair)
        except ValueError:
            continue
        accepted = [v for v in views if residual(seed, v, 1000) <= 2]
        if len(accepted) >= 2:
            key = tuple(v["camera_id"] for v in accepted)
            candidates[key] = accepted
    ranked = sorted(candidates.values(), key=lambda group: sum(v["weight"] for v in group),
                    reverse=True)
    if not ranked or (len(ranked) > 1 and math.isclose(
            sum(v["weight"] for v in ranked[0]), sum(v["weight"] for v in ranked[1]),
            abs_tol=1e-9)):
        return {"status": "ambiguous", "point_m": None, "observations": views}
    point = weighted_fit(ranked[0])
    evidence = [{**v, "residual_px": residual(point, v, 1000),
                 "decision": "accepted" if v in ranked[0] else "rejected"} for v in views]
    if any(v["residual_px"] > 2 for v in evidence if v["decision"] == "accepted"):
        return {"status": "inconsistent_refit", "point_m": None, "observations": evidence}
    return {"status": "reconstructed", "point_m": point, "observations": evidence}


def observations(cameras, time_s, frame, skew_ms, bias_mm, noise_px, rng):
    views = []
    for camera, x in cameras.items():
        is_d = camera == "D"
        ball = scene(time_s + (skew_ms / 1000 if is_d else 0))["ball"]
        pixel = project(ball, x + (bias_mm / 1000 if is_d else 0), 1000)
        views.append({"camera_id": camera, "camera_x_m": x, "time_s": time_s,
                      "frame_id": f"{camera}:{frame}",
                      "pixel": [p + rng.gauss(0, noise_px) for p in pixel]})
    return views


def sample(cameras, parameters, seed):
    skew_ms, bias_mm, noise_px = parameters
    image_rng = random.Random(seed)
    check_rng = random.Random(10000 + seed)
    # One independent check per camera and trial, with noisy offset measurements.
    checks = {}
    for camera in cameras:
        timing = (skew_ms if camera == "D" else 0) + check_rng.gauss(0, 0.08)
        location = (bias_mm if camera == "D" else 0) + check_rng.gauss(0, 2)
        severity = max(abs(timing) / 0.2, abs(location) / 5)
        checks[camera] = {"skew_ms": timing, "bias_mm": location, "severity": severity}
    for frame in range(FRAME_COUNT):
        time_s = frame / FPS
        views = observations(cameras, time_s, frame, *parameters, image_rng)
        yield time_s, views, checks


def evaluate(views, checks):
    eligible = [v for v in views if checks[v["camera_id"]]["severity"] <= 1]
    weighted = [{**v, "weight": 1 / (1 + checks[v["camera_id"]]["severity"] ** 2)}
                for v in views]
    return {"residual_only": reconstruct(views, CALIBRATION),
            "exclude": reconstruct(eligible, CALIBRATION),
            "downweight": soft_estimate(weighted)}


def run():
    for layout, cameras in LAYOUTS.items():
        for condition, parameters in CONDITIONS.items():
            errors = {policy: {} for policy in POLICIES}
            excluded = 0
            for seed in SEEDS:
                for frame, (time_s, views, checks) in enumerate(sample(cameras, parameters, seed)):
                    truth = scene(time_s)["ball"]
                    excluded += sum(c["severity"] > 1 for c in checks.values())
                    for policy, result in evaluate(views, checks).items():
                        if result["point_m"] is not None:
                            errors[policy][seed, frame] = 1000 * math.dist(result["point_m"], truth)
            shared = set.intersection(*(set(values) for values in errors.values()))
            for policy, values in errors.items():
                yield {"layout": layout, "condition": condition, "policy": policy,
                       "frames": len(SEEDS) * FRAME_COUNT, "recovered": len(values),
                       "mae_mm": statistics.mean(values.values()) if values else None,
                       "common_frames": len(shared),
                       "common_mae_mm": statistics.mean(values[k] for k in sorted(shared)) if shared else None,
                       "camera_frame_exclusions": excluded if policy == "exclude" else 0}


def examples():
    for label, skew_ms in (("biased_accepted", 0.1), ("withheld", 0.5)):
        cameras = LAYOUTS["wide"]
        views = observations(cameras, 0, 0, skew_ms, 0, 0, random.Random(0))
        result = reconstruct(views, CALIBRATION, include_consensus=True)
        truth = scene(0)["ball"]
        point = result["point_m"]
        if label == "biased_accepted":
            assert point is not None and math.dist(point, truth) > 0.001
            assert all(v["decision"] == "accepted" for v in result["observations"])
        else:
            assert result["status"] == "ambiguous"
            assert result["consensus"]["reason"] == "tied_top_groups"
            assert result["consensus"]["score_margin"] == 0
        yield {"case": label, "track": "ball", "calibration": CALIBRATION,
               "simulated_camera_d_skew_ms": skew_ms, "reference_point_m": truth,
               "result": result, "error_mm": None if point is None else 1000 * math.dist(point, truth)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("examples_path", type=Path)
    args = parser.parse_args()
    rows = list(run())
    cases = list(examples())
    with args.csv_path.open("x", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    with args.examples_path.open("x") as output:
        json.dump(cases, output, indent=2, allow_nan=False)
        output.write("\n")


if __name__ == "__main__":
    main()
