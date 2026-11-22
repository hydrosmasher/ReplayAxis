"""Bracket a forward pool-surface crossing using per-frame calibration."""
import argparse
import json
import math
from pathlib import Path

import cv2

from pool_surface import calibrate


def bracket_crossings(frames, point_id, line_m, tolerance_m):
    if not all(map(math.isfinite, (line_m, tolerance_m))) or tolerance_m <= 0:
        raise ValueError("The line coordinate must be finite and tolerance positive.")
    checked = []
    crossings = []
    before = None
    previous = None
    for frame in frames:
        index, time_s, shot = frame["frame_id"], frame["time_s"], frame["shot_id"]
        if type(index) is not int or index < 0 or not math.isfinite(time_s) or not shot:
            raise ValueError("Each observation needs a frame index, time and shot ID.")
        if previous is not None:
            last_index, last_time, last_shot = previous
            if index <= last_index or time_s <= last_time:
                raise ValueError("Frame indices and times must increase strictly.")
            if index != last_index+1 or shot != last_shot:
                before = None
        previous = index, time_s, shot
        targets = [p for p in frame.get("surface_points", []) if p["id"] == point_id]
        if len(targets) > 1:
            raise ValueError(f"Duplicate target in frame {index}.")
        if not targets:
            before = None
            checked.append(dict(frame_id=index, status="target unavailable"))
            continue
        try:
            mapped = calibrate({**frame, "surface_points": targets}, tolerance_m)
        except (ValueError, KeyError, TypeError, cv2.error) as error:
            before = None
            checked.append(dict(frame_id=index, status="calibration withheld", reason=str(error)))
            continue
        along = mapped["surface_points"][0]["pool_xy_m"][0]
        row = dict(frame_id=index, time_s=time_s, shot_id=shot, along_lane_m=along)
        checked.append({**row, "check_errors_m": mapped["check_errors_m"]})
        if along < line_m-tolerance_m:
            before = row
        elif along > line_m+tolerance_m:
            if before is not None:
                crossings.append(dict(before=before, after=row))
            before = None
    return dict(point_id=point_id, line_m=line_m, margin_m=tolerance_m,
                crossings=crossings, observations=checked)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sequence", type=Path, help="JSON array of per-frame pool calibration inputs")
    parser.add_argument("--point-id", required=True)
    parser.add_argument("--line-m", type=float, default=25.)
    parser.add_argument("--tolerance-m", type=float, required=True)
    args = parser.parse_args()
    try:
        result = bracket_crossings(json.loads(args.sequence.read_text()), args.point_id,
                                   args.line_m, args.tolerance_m)
        print(json.dumps(result, indent=2, allow_nan=False))
    except (ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"Invalid crossing input: {error}\n")


if __name__ == "__main__":
    main()
