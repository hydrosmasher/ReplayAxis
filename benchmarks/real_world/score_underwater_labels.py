"""Score exported underwater joint locations against approximate manual points."""
import argparse
import csv
import json
from collections import defaultdict
from math import hypot
from pathlib import Path
from statistics import median

JOINTS = {"hip": ("23", "24"), "shoulder": ("11", "12"), "wrist": ("15", "16")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("replay", type=Path)
    parser.add_argument("labels", type=Path)
    args = parser.parse_args()
    frames = {f["source_frames"][0]: f for f in json.loads(args.replay.read_text())["frames"]}
    rows = defaultdict(list)
    cap_visible = []
    with args.labels.open(newline="") as stream:
        for row in csv.DictReader(stream):
            frame = frames[int(row["frame"])]
            if row["landmark"] == "cap":
                cap_visible.append("0" in frame["points"])
                continue
            target = float(row["x_384"])*5, float(row["y_216"])*5
            candidates = [frame["evidence"][j]["camera_a"] for j in JOINTS[row["landmark"]]
                          if j in frame["points"]]
            errors = [hypot(x-target[0], y-target[1]) for x, y, _ in candidates]
            rows[row["landmark"]].append(min(errors) if errors else None)
    for name, distances in rows.items():
        available = [d for d in distances if d is not None]
        print(name, f"{len(available)}/{len(distances)} exported",
              f"{median(available):.1f} px median when exported" if available else "")

    if cap_visible:
        print(f"head exported on {sum(cap_visible)}/{len(cap_visible)} cap-visible frames")


if __name__ == "__main__":
    main()
