"""Compare reprojection-only consensus with an idealized external camera check."""

import argparse
import csv
from pathlib import Path

from multiframe import summarize


LAYOUTS = {
    "wide": {"A": -2, "B": -1, "C": 1, "D": 2},
    "narrow": {"A": -0.5, "B": -0.25, "C": 0.25, "D": 0.5},
    "asymmetric": {"A": -2, "B": -0.2, "C": 0.4, "D": 1.5},
}
CONDITIONS = {
    "clean": (0, 0, 0),
    "noise_only": (0, 1, 0),
    "small_skew": (0.1, 0, 0),
    "borderline_skew": (0.5, 0, 0),
    "calibration_bias": (0, 0, 10),
    "combined": (0.5, 0.5, 5),
}
SEEDS = range(20)
METRICS = ("ball_mm", "angle_deg", "speed_m_s")


def run():
    for name, cameras in LAYOUTS.items():
        for condition, parameters in CONDITIONS.items():
            skew_ms, _, bias_mm = parameters
            for policy in ("residual_only", "ideal_external_check"):
                # Simulate exact measurements from an independent timing/calibration
                # check. These deliberately chosen limits are not hardware tolerances.
                exclude = policy == "ideal_external_check" and (skew_ms > 0.05 or bias_mm > 4)
                runs = [summarize(*parameters, seed=seed, cameras=cameras, exclude_camera_d=exclude)
                        for seed in SEEDS]
                row = {"layout": name, "condition": condition, "policy": policy,
                       "runs": len(runs), "camera_d_excluded": int(exclude),
                       "frames": sum(run["frames"] for run in runs)}
                for metric in METRICS:
                    count = sum(run[f"{metric}_n"] for run in runs)
                    row[f"{metric}_n"] = count
                    row[f"{metric}_mae"] = (
                        sum(run[f"{metric}_mae"] * run[f"{metric}_n"]
                            for run in runs if run[f"{metric}_n"]) / count if count else None
                    )
                yield row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rows = list(run())
    for baseline, checked in zip(rows[::2], rows[1::2]):
        if not checked["camera_d_excluded"]:
            assert all(baseline[field] == checked[field] for field in baseline if field != "policy")
        if checked["condition"] == "clean":
            assert checked["ball_mm_n"] == checked["frames"]
            assert checked["ball_mm_mae"] < 1e-8
    with args.output.open("x", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
