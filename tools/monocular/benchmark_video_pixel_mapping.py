"""Check explicit decoded-to-calibration pixel mappings on static landmarks."""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np

from benchmark_static_calibration import decoded_sizes, measure
from benchmark_temporal import cameras_from_qca


def calibration_sizes(qca):
    result = {}
    for camera in ET.parse(qca).findall("cameras/camera"):
        video = camera.find("fov_video")
        result[camera.get("serial")] = (
            int(video.get("right")) - int(video.get("left")) + 1,
            int(video.get("bottom")) - int(video.get("top")) + 1,
        )
    return result


def maps(sizes, calibrated):
    result = {name: {} for name in ("identity", "center_crop", "resize")}
    for name, (width, height) in sizes.items():
        cal_width, cal_height = calibrated[name]
        if height != cal_height:
            raise ValueError(f"{name}: this check requires matching frame heights.")
        result["identity"][name] = (1., 0.)
        result["center_crop"][name] = (1., (cal_width - width) / 2)
        result["resize"][name] = (cal_width / width, 0.)
    return result


def summarize(errors):
    distances = [value for pairs in errors.values() for pair in pairs.values() for value in pair]
    if not distances:
        raise ValueError("No shared static landmark observations.")
    return dict(distances=len(distances), median_px=float(np.median(distances)),
                max_px=float(np.max(distances)), landmarks=errors)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("development", type=Path)
    parser.add_argument("held_out", type=Path)
    parser.add_argument("qca", type=Path)
    parser.add_argument("videos", type=Path, nargs=4)
    args = parser.parse_args()
    cameras = cameras_from_qca(args.qca)
    calibrated = calibration_sizes(args.qca)
    datasets = {}
    for name, path in (("development", args.development), ("held_out", args.held_out)):
        labels = json.loads(path.read_text())
        sizes = decoded_sizes(args.videos, labels["source_frame"])
        datasets[name] = dict(
            decoded_sizes=sizes,
            scores={variant: summarize(measure(labels, sizes, cameras, mapping))
                    for variant, mapping in maps(sizes, calibrated).items()})
    print(json.dumps(dict(calibrated_sizes=calibrated, datasets=datasets),
                     indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
