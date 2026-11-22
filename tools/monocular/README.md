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


## Learned depth benchmark

From the repository root, run:

```sh
python tools/monocular/benchmark_learned.py Calib.qca.txt yolov8n-pose.onnx cam01.mp4 cam02.mp4 cam03.mp4 cam04.mp4
```

The ridge model predicts joint depth relative to the hips using joint identity,
normalized 2D position, segment direction, fixed-prior depth and changes
in the projected segment across adjacent sampled frames. Train on views
01–02 and evaluate on 03–04, then reverse the groups. The penalty is fixed.
All three methods are scored on identical shared joints.

Mean depth error was lower than both baselines in two of four held-out
views. Full per-view results are in `learned_results.json`. The folds
share the same athlete, motion and times, so this measures transfer
between camera groups within one recording. The reference is calibrated
two-view triangulation, not independent motion capture. The learned model
is a benchmark only and is not enabled in the replay CLI.


## Optional athlete-height prior

Provide both `--athlete-height-m` and `--torso-to-height` to express
body-relative estimates in metres under a stated stature and proportion
assumption. The ratio is shoulder midpoint to hip midpoint divided by
standing stature. Prefer a measured ratio for the athlete when available.
For example, `--athlete-height-m 1.93 --torso-to-height 0.34` gives
0.6562 m per torso length. The 0.34 ratio is illustrative, not an observed
Phelps measurement.

The replay JSON records these assumptions under `body_scale_prior` and
uses `body_prior_m` to identify the coordinate units. This multiplies the
estimated coordinates by a single clip-wide factor. It does not resolve
camera depth, reshape limb proportions, establish a pool coordinate system
or produce a race distance. The prior was smoke-tested on 10 Pose2Sim
frames, with identical 2D evidence and expected scaling across 124 joint
samples. No Phelps frames were processed in that test.


## Body-scale sensitivity

Run `python tools/monocular/benchmark_height.py Calib.qca.txt yolov8n-pose.onnx cam02.mp4 cam01.mp4 --assumed-height-m 1.93 --ratios .30 .34 .38`.
The example stature is a sensitivity input and is not a measurement of the
Pose2Sim subject. The calibrated comparison uses hip-centered camera
coordinates and only joints shared by both estimates. In this run it
used 26 shared head and limb samples from 12 frame pairs.

| Scale input | Mean 3D error | Mean absolute depth error |
| --- | ---: | ---: |
| 1.93 m × 0.30 | 0.251 m | 0.205 m |
| 1.93 m × 0.34 | 0.306 m | 0.204 m |
| 1.93 m × 0.38 | 0.368 m | 0.202 m |
| Reference torso length (~0.484 m) | 0.216 m | 0.208 m |

The reference scale uses calibrated triangulation, not independently
measured anatomy. Errors are body-relative. The example measures sensitivity
to scale on one recording and does not evaluate Phelps or swimming.

## Scene-based scale and out-of-plane bias

Run `python tools/monocular/benchmark_scene_scale.py` with NumPy and OpenCV.
The seeded synthetic fixture fits an image-to-metre homography using six
known planar landmarks. It estimates torso length from the projected hip
and shoulder midpoints without access to the simulated camera parameters.
It compares this with the previous illustrative stature prior and a fixed
equal-weight average. See `scene_scale_results.json` for 1,200 trials.

On the landmark plane, scene-only torso length MAE was 1.3–2.5 cm.
At a 1.5 m offset away from the plane, it rose to 6.6–11.7 cm.
The illustrative stature prior overestimates every simulated torso, so
improvements from averaging at large offsets reflect cancellation of
opposing biases in this fixture. These scores are torso length errors,
not 3D joint or depth errors.

Before using this in swimming, annotate dimensioned landmarks in a
fixed camera shot and check them on withheld landmarks. An above-water
homography applies to its landmark plane. Underwater validation needs
separate reference observations and a model of refraction if the rays
cross the air–water interface.

## Acceptance thresholds

Run `python tools/monocular/benchmark_acceptance.py reference.qca yolov8n-pose.onnx cam02.mp4 cam01.mp4` from the repository root. Swap the camera order to reproduce the second case in `acceptance_results.json`.

The scorer reports nearest-rank 90% and 95% error thresholds on scored joints.
Fixed-tolerance pass rates count missing predictions as failures among eligible
reference joints. Coverage uses that same reference denominator. The two
directions share one motion and one two-view triangulation reference, with
26 eligible samples each across 12 frame pairs. Input pixels are undistorted
using known intrinsics and metric scale comes from the reference torso,
so this is a depth baseline with reference assistance. Scores are hip-relative.

For the learned comparison, use dense matched source frames and identical
2D detector tracks for both methods. Follow the official MotionBERT
[inference guide](https://github.com/Walter0807/MotionBERT/blob/main/docs/inference.md)
and verify the joint mapping, depth axis and scale before feeding predictions
to the same scorer. MotionBERT inference was not run for this result.
