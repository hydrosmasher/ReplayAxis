"""Check paired-video collection manifests before model training."""
import argparse
from collections import Counter
import csv
from pathlib import Path


FILES = ("video_a", "video_b", "calibration", "synchronization", "training_3d", "reference_3d")
FIELDS = {"trial_id", "athlete_id", "split", "variant", "prompt", "camera_a_id",
          "camera_b_id", "reference_kind", *FILES}
SPLITS = {"train", "validation", "test"}
REFERENCES = {"two_view", "independent_3d"}


def validate(path):
    trials, clips, athlete_splits, counts, errors = set(), set(), {}, Counter(), []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        missing = FIELDS - set(header)
        if missing or len(header) != len(set(header)):
            return counts, [f"Invalid columns. Missing: {', '.join(sorted(missing)) or 'none'}."]
        for line, raw in enumerate(reader, start=2):
            if None in raw or any(value is None for value in raw.values()):
                errors.append(f"Row {line}: column count differs from the header.")
                continue
            row = {field: value.strip() for field, value in raw.items()}
            empty = [field for field in sorted(FIELDS - {"prompt"}) if not row[field]]
            if empty:
                errors.append(f"Row {line}: empty {', '.join(empty)}.")
                continue
            trial, athlete, split = (row[key] for key in ("trial_id", "athlete_id", "split"))
            if trial in trials:
                errors.append(f"Row {line}: repeated trial {trial}.")
            trials.add(trial)
            previous = athlete_splits.setdefault(athlete, split)
            if previous != split:
                errors.append(f"Row {line}: athlete {athlete} appears across splits.")
            if split not in SPLITS or row["reference_kind"] not in REFERENCES:
                errors.append(f"Row {line}: unknown split or reference kind.")
            if row["camera_a_id"] == row["camera_b_id"]:
                errors.append(f"Row {line}: two distinct camera IDs are required.")
            paths = {field: (path.parent / row[field]).resolve() for field in FILES}
            for field, item in paths.items():
                if not item.is_file():
                    errors.append(f"Row {line}: missing file for {field}.")
            for field in ("video_a", "video_b"):
                if paths[field] in clips:
                    errors.append(f"Row {line}: video already assigned to a camera or trial.")
                clips.add(paths[field])
            if row["reference_kind"] == "independent_3d" and paths["reference_3d"] == paths["training_3d"]:
                errors.append(f"Row {line}: independent reference uses the training label file.")
            counts[split] += 1
    if not trials:
        errors.append("No recorded trials.")
    return counts, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    counts, errors = validate(args.manifest)
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    for split in sorted(counts):
        print(f"{split}: {counts[split]} trials")


if __name__ == "__main__":
    main()
