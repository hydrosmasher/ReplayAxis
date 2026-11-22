"""Reference-assisted two-view comparison on Pose2Sim Demo_SinglePerson."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import cv2
import numpy as np

from replayaxis_geometry import load_notebook


def cameras_from_qca(path):
    cameras = {}
    for item in ET.parse(path).findall("cameras/camera"):
        intr, ext = item.find("intrinsic"), item.find("transform")
        focal_x, focal_y, center_x, center_y = [
            float(intr.get(key)) / 64 for key in
            ("focalLengthU", "focalLengthV", "centerPointU", "centerPointV")]
        k = np.array([[focal_x, 0, center_x], [0, focal_y, center_y], [0, 0, 1]])
        orientation = np.array([[float(ext.get(f"r{i}{j}")) for j in (1, 2, 3)]
                                for i in (1, 2, 3)])
        r = np.diag([1, -1, -1]) @ orientation
        center = np.array([float(ext.get(key)) / 1000 for key in "xyz"])
        dist = [float(intr.get(key)) / 64 for key in (
            "radialDistortion1", "radialDistortion2",
            "tangentalDistortion1", "tangentalDistortion2")]
        cameras[item.get("serial")] = dict(K=k, R=r, t=-r @ center, dist=dist)
    return cameras


def collect(path, net, detect):
    cap = cv2.VideoCapture(str(path))
    frames, poses = [], []
    try:
        for index in range(60):
            ok, image = cap.read()
            if not ok:
                break
            if index % 5 == 0:
                frames.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
                poses.append(detect(net, image))
    finally:
        cap.release()
    if not frames:
        raise ValueError(f"Could not read {path}")
    return frames, poses


def relative_camera(a, b):
    r = b["R"] @ a["R"].T
    t = b["t"] - r @ a["t"]
    return r, t


def background_features(frames):
    # Low temporal variation excludes most moving foreground pixels.
    stack = np.stack(frames)
    mask = (np.ptp(stack, axis=0) <= 24).astype(np.uint8) * 255
    mask = cv2.erode(mask, np.ones((9, 9), np.uint8))
    image = np.median(stack, axis=0).astype(np.uint8)
    keypoints, descriptors = cv2.SIFT_create(nfeatures=6000).detectAndCompute(image, mask)
    return np.array([kp.pt for kp in keypoints]), descriptors


def verified_matches(a_features, b_features, a, b):
    points_a, da = a_features
    points_b, db = b_features
    r, t = relative_camera(a, b)
    x, y, z = t
    cross = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    f = np.linalg.inv(b["K"]).T @ cross @ r @ np.linalg.inv(a["K"])
    matcher = cv2.BFMatcher(cv2.NORM_L2)

    def ratio_matches(first, second):
        return {m.queryIdx: m.trainIdx for m, n in matcher.knnMatch(first, second, k=2)
                if m.distance < .88 * n.distance}

    if da is None or db is None or min(len(da), len(db)) < 2:
        return np.empty((0, 2)), np.empty((0, 2))
    forward, reverse = ratio_matches(da, db), ratio_matches(db, da)
    pairs = [(i, j) for i, j in forward.items() if reverse.get(j) == i]
    if not pairs:
        return np.empty((0, 2)), np.empty((0, 2))
    ia, ib = np.asarray(pairs).T
    raw = [points_a[ia], points_b[ib]]
    homogeneous = []
    for points, cam in zip(raw, (a, b)):
        clean = cv2.undistortPoints(points, cam["K"], np.asarray(cam["dist"]), P=cam["K"])
        homogeneous.append(np.column_stack((clean.reshape(-1, 2), np.ones(len(points)))))
    pa, pb = homogeneous
    lines_b, lines_a = pa @ f.T, pb @ f
    residual = abs(np.sum(pb * lines_b, axis=1))
    keep = residual <= 2 * np.minimum(np.linalg.norm(lines_a[:, :2], axis=1),
                                      np.linalg.norm(lines_b[:, :2], axis=1))
    return raw[0][keep], raw[1][keep]


def compare(api, poses, known, estimated=None):
    r, t = relative_camera(*known)
    baseline = np.linalg.norm(t)
    known_count = estimated_count = 0
    differences = []
    for a, b in zip(*poses):
        known_points = api["reconstruct"](
            api["correct_pose_pixels"](a, known[0]),
            api["correct_pose_pixels"](b, known[1]), known)["points"]
        known_count += len(known_points)
        if estimated is None:
            continue
        est_points = api["reconstruct"](a, b, estimated)["points"]
        estimated_count += len(est_points)
        for joint in known_points.keys() & est_points.keys():
            reference = known[0]["R"] @ known_points[joint] + known[0]["t"]
            differences.append(100 * np.linalg.norm(reference - baseline * np.array(est_points[joint])))
    result = {"frame_pairs": min(map(len, poses)), "reference_joints": known_count}
    if estimated is not None:
        result.update(estimated_joints=estimated_count, common_joints=len(differences))
    if differences:
        result.update(median_disagreement_cm=float(np.median(differences)),
                      p95_disagreement_cm=float(np.percentile(differences, 95)))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qca", type=Path)
    parser.add_argument("model", type=Path)
    parser.add_argument("videos", type=Path, nargs="+")
    parser.add_argument("--notebook", type=Path, default=Path("ReplayAxis_Markerless_TwoView.ipynb"))
    args = parser.parse_args()
    cv2.setRNGSeed(82)
    api = load_notebook(args.notebook, extra_signatures=("def detect_onnx_pose(",))
    net = cv2.dnn.readNetFromONNX(str(args.model))
    cameras = cameras_from_qca(args.qca)
    data = {}
    for path in args.videos:
        frames, poses = collect(path, net, api["detect_onnx_pose"])
        cameras[path.stem]["image_size"] = frames[0].shape[::-1]
        data[path.stem] = background_features(frames), poses
    report = {}
    for a, b in combinations(data, 2):
        known = [cameras[a], cameras[b]]
        points_a, points_b = verified_matches(data[a][0], data[b][0], *known)
        result = {"reference_screened_matches": len(points_a)}
        estimated = None
        try:
            estimate = api["estimate_stereo_geometry"](
                points_a, points_b, [c["image_size"] for c in known], horizontal_fov_deg=36)
            estimated = estimate["cameras"]
            result["pose_inliers"] = estimate["pose_inliers"]
        except ValueError as error:
            result["withheld"] = str(error)
        result.update(compare(api, [data[a][1], data[b][1]], known, estimated))
        report[f"{a} + {b}"] = result
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
