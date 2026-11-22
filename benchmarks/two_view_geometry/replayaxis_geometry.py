"""Compare two-view geometry using the production functions in the root notebook."""
import argparse
from itertools import combinations
import json
from pathlib import Path

import cv2
import numpy as np


def load_notebook(path, extra_signatures=()):
    namespace = {"cv2": cv2, "np": np}
    notebook = json.loads(path.read_text())
    signatures = ("def triangulate(", "def estimate_stereo_geometry(") + extra_signatures
    for cell in notebook["cells"]:
        source = "".join(cell["source"])
        if cell["cell_type"] == "code" and any(s in source for s in signatures):
            exec(compile(source, str(path), "exec"), namespace)
    return namespace


def benchmark(api):
    rng = np.random.default_rng(82)
    cv2.setRNGSeed(82)
    width, height = 1280, 720
    focal = width / (2 * np.tan(np.deg2rad(30)))
    intrinsic = [[focal, 0, 639.5], [0, focal, 359.5], [0, 0, 1]]
    rotation = cv2.Rodrigues(np.array([.02, .10, -.01]))[0]
    known = [dict(K=intrinsic, R=np.eye(3), t=[0, 0, 0]),
             dict(K=intrinsic, R=rotation, t=[-1, 0, 0])]
    background = rng.uniform([-2, -1, 4], [2, 1, 12], (250, 3))
    time = np.arange(500) / 500
    speed = 8
    track = np.column_stack((speed * (time - .5),
                             .25 * np.sin(2 * np.pi * 3 * time),
                             8 + .3 * np.cos(2 * np.pi * 3 * time)))

    def observe(points, noise_px):
        pixels = np.array([[api["project"](p, c) for p in points] for c in known])
        return pixels + rng.normal(0, noise_px, pixels.shape) if noise_px else pixels

    static_pixels = observe(background, .35)
    moving_pixels = observe(track, .75)

    def score(cameras):
        errors = []
        for truth, a, b in zip(track, *moving_pixels):
            point, _ = api["triangulate"](a, b, *cameras)
            if point is not None:
                errors.append(100 * np.linalg.norm(point - truth))
        result = {"accepted": len(errors), "total": len(track)}
        if errors:
            result.update(median_cm=round(float(np.median(errors)), 2),
                          p95_cm=round(float(np.percentile(errors, 95)), 2))
        return result

    results = {"known_geometry": score(known), "estimated_geometry": {}}
    for fov in (50, 55, 60, 65, 70):
        try:
            estimate = api["estimate_stereo_geometry"](
                *static_pixels, [(width, height)] * 2, horizontal_fov_deg=fov)
            result = score(estimate["cameras"])
            result["pose_inliers"] = estimate["pose_inliers"]
        except ValueError as error:
            result = {"withheld": str(error)}
        results["estimated_geometry"][fov] = result
    return results


def screen_video_pairs(api, videos):
    results = {}
    for a, b in combinations(videos, 2):
        try:
            estimate = api["estimate_geometry_from_video"]([a, b], [0, 0], 60)
            result = {key: estimate[key] for key in
                      ("matched_points", "pose_inliers", "median_parallax_deg")}
        except ValueError as error:
            result = {"withheld": str(error)}
        results[f"{a.name} + {b.name}"] = result
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", type=Path, default=Path("ReplayAxis_Markerless_TwoView.ipynb"))
    parser.add_argument("--videos", type=Path, nargs="+", default=[])
    args = parser.parse_args()
    api = load_notebook(args.notebook)
    api["nearest_frame_index"] = lambda time, fps: round(time * fps)
    report = {"synthetic_500_hz": benchmark(api)}
    if args.videos:
        report["real_video_first_frame_screen"] = screen_video_pairs(api, args.videos)
    print(json.dumps(report, indent=2, allow_nan=False))
