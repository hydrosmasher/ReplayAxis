"""Check demo video identity and map each view to its calibration still."""
import argparse
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np


def blob_sha(path):
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def features(image, sift):
    points, descriptors = sift.detectAndCompute(image, None)
    return np.asarray([p.pt for p in points]), descriptors


def match(first, second, center):
    a, da = first
    b, db = second
    if da is None or db is None:
        return dict(matches=0, inliers=0)
    matcher = cv2.BFMatcher()
    candidates = matcher.knnMatch(da, db, k=2)
    pairs = [pair[0] for pair in candidates
             if len(pair) == 2 and pair[0].distance < .75 * pair[1].distance]
    if len(pairs) < 4:
        return dict(matches=len(pairs), inliers=0)
    src = np.asarray([a[m.queryIdx] for m in pairs])
    dst = np.asarray([b[m.trainIdx] for m in pairs])
    mapping, mask = cv2.findHomography(src, dst, cv2.RANSAC, 2.)
    if mapping is None:
        return dict(matches=len(pairs), inliers=0)
    keep = mask.ravel().astype(bool)
    projected = cv2.perspectiveTransform(src[None], mapping)[0]
    moved = cv2.perspectiveTransform(np.asarray([[center]], dtype=np.float64), mapping)[0, 0]
    return dict(matches=len(pairs), inliers=int(keep.sum()),
                median_inlier_error_px=float(np.median(np.linalg.norm(projected[keep] - dst[keep], axis=1))),
                center_offset_px=(moved - center).tolist())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("qca", type=Path)
    parser.add_argument("tree", type=Path, help="Upstream GitHub recursive tree JSON")
    parser.add_argument("stills", type=Path)
    parser.add_argument("videos", type=Path, nargs=4)
    args = parser.parse_args()
    tree = json.loads(args.tree.read_text())
    prefix = "Pose2Sim/Demo_SinglePerson/"
    upstream = {item["path"][len(prefix):]: item["sha"] for item in tree["tree"]
                if item["path"].startswith(prefix) and item["type"] == "blob"}
    cv2.setRNGSeed(82)
    sift = cv2.SIFT_create(nfeatures=3500)
    videos, stills, provenance = {}, {}, {}
    files = {"calibration/Calib.qca.txt": args.qca}
    for p in args.videos:
        files[f"videos/{p.name}"] = p
        still = args.stills / f"{p.stem}_ext.png"
        files[f"calibration/extrinsics/{still.name}"] = still
        image = cv2.imread(str(still), cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError(f"Could not read {still}")
        cap = cv2.VideoCapture(str(p))
        try:
            ok, frame = cap.read()
        finally:
            cap.release()
        if not ok:
            raise ValueError(f"Could not read {p}")
        center = (np.asarray(frame.shape[1::-1]) - 1) / 2
        videos[p.stem] = (features(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), sift), center)
        stills[p.stem] = features(image, sift)
    for key, path in files.items():
        actual = blob_sha(path)
        provenance[key] = dict(local_blob=actual, upstream_blob=upstream[key],
                               verified=actual == upstream[key])
    comparisons = {a: {b: match(f, g, center) for b, g in stills.items()}
                   for a, (f, center) in videos.items()}
    print(json.dumps(dict(upstream_commit=tree["sha"], opencv_version=cv2.__version__,
                          provenance=provenance, video_to_still=comparisons),
                     indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
