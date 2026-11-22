"""Export an exploratory, single-shot 3D replay from real video."""
import argparse
import json
import math
from pathlib import Path
from statistics import median

import cv2


# Parent-first tree. Sibling shoulders and hips share a depth plane.
CHAINS = ((11, 0, .48, -1), (11, 13, .52, -1), (13, 15, .46, -1),
          (12, 14, .52, -1), (14, 16, .46, -1),
          (23, 25, .66, -1), (25, 27, .63, 1),
          (24, 26, .66, -1), (26, 28, .63, 1))


def load_notebook(path):
    api = {}
    for cell in json.loads(path.read_text())["cells"]:
        source = "".join(cell["source"])
        if cell["cell_type"] == "code" and (
                "def triangulate(" in source or "def detect_onnx_pose(" in source):
            exec(compile(source, str(path), "exec"), api)
    return api


def temporal_offsets(samples, preferred_sign, cues):
    """Select signed offsets for each contiguous run with a two-state path search."""
    offsets = {}
    start = 0
    while start < len(samples):
        if samples[start] is None:
            start += 1
            continue
        end = start + 1
        while end < len(samples) and samples[end] is not None:
            end += 1
        costs = [0., 0.]
        links = []
        for index in range(start, end):
            current = samples[index]
            previous = samples[index-1] if index > start else current
            next_costs, parents = [], []
            for state, sign in enumerate((preferred_sign, -preferred_sign)):
                other_sign = -sign
                stay = costs[state] + (current-previous)**2
                switch = costs[1-state] + (sign*current-other_sign*previous)**2
                parent = state if stay <= switch else 1-state
                parents.append(parent)
                next_costs.append(min(stay, switch) + .08*current**2*(sign != cues[index]))
            links.append(parents)
            costs = next_costs
        state = int(costs[1] < costs[0])
        for index in range(end-1, start-1, -1):
            offsets[index] = samples[index]*preferred_sign*(1-2*state)
            state = links[index-start][state]
        start = end
    return offsets


def lift(observations, mirror=False, confidence=.55, temporal=False):
    """Use weak perspective and segment priors to produce one of two depth hypotheses."""
    clean = [{j: p for j, p in obs.items()
              if len(p) == 3 and all(map(math.isfinite, p)) and p[2] >= confidence}
             for obs in observations]
    trunk_lengths = []
    for p in clean:
        if all(j in p for j in (11, 12, 23, 24)):
            trunk_lengths.append(math.hypot(*[(p[11][k]+p[12][k]-p[23][k]-p[24][k])/2
                                               for k in (0, 1)]))
    if not trunk_lengths or median(trunk_lengths) < 5:
        raise ValueError("No reliable torso scale. Use a shot with visible shoulders and hips.")
    scale = median(trunk_lengths)
    frames, planar = [], []
    for p in clean:
        points = {}
        if 23 in p and 24 in p:
            cx, cy = ((p[23][k]+p[24][k])/2 for k in (0, 1))
            points = {j: [(value[0]-cx)/scale, (value[1]-cy)/scale, 0.]
                      for j, value in p.items()}
        planar.append(points)
        frames.append({j: point.copy() for j, point in points.items()
                       if j in (11, 12, 23, 24)})
    bend_anchors = {15: 11, 16: 12, 27: 23, 28: 24}
    for parent, child, length, sign in CHAINS:
        samples, cues = [], []
        for frame, p in zip(frames, planar):
            depth, cue = None, sign
            if parent in frame and child in p:
                dx, dy = (p[child][k]-p[parent][k] for k in (0, 1))
                depth = math.sqrt(max(0., length*length-dx*dx-dy*dy))
                anchor = bend_anchors.get(child)
                if anchor in p:
                    ax, ay = (p[parent][k]-p[anchor][k] for k in (0, 1))
                    area = ax*dy-ay*dx
                    if abs(area) > .025:
                        cue = sign * (1 if area > 0 else -1)
            samples.append(depth)
            cues.append(cue)
        offsets = (temporal_offsets(samples, sign, cues) if temporal else
                   {i: sign*depth for i, depth in enumerate(samples) if depth is not None})
        for i, depth in offsets.items():
            frames[i][child] = [*planar[i][child][:2],
                                frames[i][parent][2]+depth*(-1 if mirror else 1)]
    return frames


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path, help="Local source file containing a single continuous shot")
    parser.add_argument("model", type=Path, help="Fixed 640x640 YOLOv8n-pose ONNX export")
    parser.add_argument("--notebook", type=Path, default=Path("ReplayAxis_Markerless_TwoView.ipynb"))
    parser.add_argument("--output", type=Path, default=Path("estimated_replay.html"))
    parser.add_argument("--start-frame", type=int, default=0)
    parser.add_argument("--frames", type=int, default=120)
    parser.add_argument("--mirror-depth", action="store_true")
    parser.add_argument("--temporal", action="store_true", help="Use the experimental temporal depth path")
    args = parser.parse_args()
    if args.frames < 1 or args.start_frame < 0:
        parser.error("frame count must be positive and start frame must be nonnegative")
    api = load_notebook(args.notebook)
    net = cv2.dnn.readNetFromONNX(str(args.model))
    capture = cv2.VideoCapture(str(args.video))
    observations = []
    try:
        fps = capture.get(cv2.CAP_PROP_FPS)
        if not capture.isOpened() or not math.isfinite(fps) or fps <= 0:
            raise ValueError("Could not establish a nominal frame rate.")
        if args.start_frame:
            capture.set(cv2.CAP_PROP_POS_FRAMES,args.start_frame)
        for _ in range(args.frames):
            ok, image = capture.read()
            if not ok:
                break
            observations.append(api["detect_onnx_pose"](net, image))
    finally:
        capture.release()
    poses = lift(observations, mirror=args.mirror_depth, temporal=args.temporal)
    frames = []
    for index, (pose, obs) in enumerate(zip(poses, observations), args.start_frame):
        frames.append(dict(time=index/fps, source_frames=[index, None], points=pose,
                           rejected={j: "Unavailable" for j in api["JOINTS"] if j not in pose},
                           evidence={j: {"camera_a": obs[j]} for j in pose}))
    payload = dict(title="Estimated 3D · single camera · relative pose only",
                   units="torso", depth="mirrored hypothesis" if args.mirror_depth else "prior hypothesis",
                   depth_method="temporal bend prior" if args.temporal else "fixed prior",
                   timeline="nominal FPS", rate=fps, frames=frames, bones=api["BONES"], joints=api["JOINTS"])
    data = json.dumps(payload, allow_nan=False)
    viewer = api["VIEWER"].replace("Landmarks reconstructed", "Landmarks estimated")
    viewer = viewer.replace("'Reconstructed'", "'Estimated · depth inferred'")
    args.output.write_text(viewer.replace("__DATA__", data.replace("<", r"\u003c")), encoding="utf-8")
    args.output.with_suffix(".json").write_text(data, encoding="utf-8")
    print(f"Estimated pose on {sum(bool(p) for p in poses)}/{len(poses)} real frames.")


if __name__ == "__main__":
    main()
