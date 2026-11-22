# Single-camera estimated replay

Run from the repository root with a local, continuous video shot and a fixed
640×640 YOLOv8n-pose ONNX export (output 1×56×8400). Install NumPy and OpenCV.

```sh
python tools/monocular/reconstruct.py shot.mp4 yolov8n-pose.onnx --frames 120 --output estimated_replay.html
```

Open the HTML to pause, step through source frames, orbit the estimated
skeleton and inspect the tracked joints. The JSON contains one estimate
per decoded frame. Run with `--mirror-depth` and a separate output path
to inspect a reflected solution with identical image-plane coordinates.

This baseline subtracts the hip midpoint, scales by median apparent torso
length and estimates bone depth offsets from a fixed segment-length prior.
The depth signs come from a default hypothesis. Where a projected segment
exceeds its prior, its depth offset is zero. Missing joints remain missing.
This preserves the observed image plane but does not model perspective,
body rotation, water refraction, scene translation or camera motion.
Timeline values assume constant nominal FPS. Distances are torso-relative,
and metric speed, acceleration and change of direction are unavailable.

## Real video smoke test

Pose2Sim Demo_SinglePerson `cam02.mp4`, frames 0–49, using the model recorded
in the two-view benchmark README. The prototype returned estimates for all
50 frames and 641 joint samples. The reflected run changed depth for 194
samples while preserving every image-plane coordinate. This checks
execution and exposes ambiguity. Accuracy has not been measured here.

The London 2012 Phelps broadcast is the first target case. No decoded Phelps
frames were used in this run. The next iteration should test a
swimming-aware detector and temporal lifting on a continuous race shot,
then score aligned pose and depth against calibrated real footage.

## Experimental temporal depth

Add `--temporal` to the replay command. This mode chooses signs for the
inferred depth offsets over contiguous runs using a two-state search.
Its cost combines changes in depth offset and a weak image-plane
bend cue. That cue is a heuristic, does not observe depth directly,
and can change with viewpoint. Visibility gaps are never filled.

Run against the same QCA file, model and videos used by the two-view
benchmark:

```sh
python tools/monocular/benchmark_temporal.py Calib.qca.txt yolov8n-pose.onnx cam02.mp4 cam01.mp4
```

| Single-camera input | Reference pair | Shared joint samples | Fixed depth MAE | Temporal depth MAE |
| --- | --- | ---: | ---: | ---: |
| cam01 | cam01 + cam02 | 26 | .565 | .552 |
| cam02 | cam02 + cam01 | 26 | .429 | .477 |
| cam03 | cam03 + cam04 | 16 | .432 | .477 |
| cam04 | cam04 + cam03 | 16 | .731 | .527 |

Each run used 12 sampled frame pairs from the same Pose2Sim performance.
The benchmark undistorts both views, triangulates a reference, subtracts
the hip midpoint, expresses depth in torso lengths, and scores shared
head and limb joints. It also reports reflected hypotheses to expose
sign ambiguity. Calibrated triangulation is a proxy reference and uses
the same 2D detections. These comparisons are neither independent subjects
nor motion-capture ground truth. The fixed estimator remains the default.
