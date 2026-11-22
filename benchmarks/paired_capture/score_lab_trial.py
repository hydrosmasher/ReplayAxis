"""Score metric joint positions against an explicitly aligned 3D reference."""
import argparse
from collections import defaultdict
import csv
import json
import math
from pathlib import Path


COLUMNS = {"source_frame_a", "joint", "status", "x_m", "y_m", "z_m"}


def read_positions(path):
    positions = {}
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not COLUMNS.issubset(reader.fieldnames or []):
            raise ValueError(f"{path.name}: required columns: {', '.join(sorted(COLUMNS))}")
        for line, row in enumerate(reader, start=2):
            try:
                key = int(row["source_frame_a"]), row["joint"].strip()
                if key[0] < 0 or not key[1] or key in positions:
                    raise ValueError("empty joint, negative frame index, or duplicate frame/joint")
                status = row["status"].strip()
                if not status:
                    raise ValueError("empty status")
                point = None
                if status == "reconstructed":
                    point = tuple(float(row[column]) for column in ("x_m", "y_m", "z_m"))
                    if not all(map(math.isfinite, point)):
                        raise ValueError("non-finite coordinates")
                positions[key] = point
            except (TypeError, AttributeError, ValueError) as error:
                raise ValueError(f"{path.name}, row {line}: {error}") from error
    return positions


def summarize(errors, tolerances_m):
    eligible = len(errors)
    observed = sorted(error for error in errors if error is not None)
    return {
        "eligible": eligible,
        "scored": len(observed),
        "coverage": len(observed) / eligible,
        "within_tolerance": {
            f"{tol * 100:g}_cm": {
                "passes": sum(error <= tol for error in observed),
                "rate": sum(error <= tol for error in observed) / eligible,
            } for tol in tolerances_m
        },
    }


def score(reference, predicted, tolerances_m):
    if not any(value is not None for value in reference.values()):
        raise ValueError("Reference has no eligible metric coordinates.")
    joints = defaultdict(list)
    for key, target in reference.items():
        if target is None:
            continue
        estimate = predicted.get(key)
        joints[key[1]].append(math.dist(target, estimate) if estimate is not None else None)
    return {
        "overall": summarize([error for errors in joints.values() for error in errors], tolerances_m),
        "per_joint": {joint: summarize(errors, tolerances_m)
                      for joint, errors in sorted(joints.items())},
        "predicted_only_keys": len(predicted.keys() - reference.keys()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    parser.add_argument("predictions", type=Path, nargs="+")
    parser.add_argument("--tolerance-cm", type=float, nargs="+", required=True)
    parser.add_argument("--reference-kind", choices=("independent_3d", "two_view"), required=True)
    args = parser.parse_args()
    if any(not math.isfinite(v) or v <= 0 for v in args.tolerance_cm):
        parser.error("Tolerances must be finite and positive.")
    names = [path.stem for path in args.predictions]
    if len(set(names)) != len(names):
        parser.error("Prediction files must have distinct stems.")
    try:
        reference = read_positions(args.reference)
        results = {name: score(reference, read_positions(path),
                               [v / 100 for v in args.tolerance_cm])
                   for name, path in zip(names, args.predictions)}
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(dict(reference_kind=args.reference_kind, coordinate_units="m",
                          results=results), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
