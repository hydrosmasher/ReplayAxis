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

## MotionBERT-Lite comparison on dense tracks

Use a Python environment with PyTorch 2.8, NumPy and OpenCV. Obtain
[upstream source at 705d3a9](https://github.com/Walter0807/MotionBERT/tree/705d3a95354db8bdb696b3492e47a3b5537174ff)
and the author's [Lite weights](https://huggingface.co/walterzhu/MotionBERT/blob/main/checkpoint/pose3d/FT_MB_lite_MB_ft_h36m_global_lite/best_epoch.bin).
The benchmark checks the published checkpoint SHA-256 before loading it.
The checkpoint and upstream source are external dependencies.

```sh
python tools/monocular/benchmark_motionbert.py /path/to/MotionBERT /path/to/best_epoch.bin reference.qca yolov8n-pose.onnx cam02.mp4 cam01.mp4
```

Both camera directions use the first 60 consecutive frames. All methods
receive the same undistorted YOLO detections for the input camera only.
The MotionBERT adapter maps COCO joints to Human3.6M, approximates the
landmarks absent in COCO, normalizes the clip and averages inference with
a horizontally flipped pass. Predictions are centered at the hip midpoint
and scaled to the triangulated median torso length for each comparison.
No per-joint fit or rotation alignment is applied. This experiment tests
pose under reference-assisted scale and lens correction. It keeps separate
scores for all eligible reference samples and for joints all methods estimate.
Both views observe the same performance and share one two-view reference.

Results are in `motionbert_results.json`. All methods scored the same 175
eligible joint samples per view. MotionBERT gained at the illustrative
5 cm threshold (34 vs. 24 fixed-baseline passes in camera 02, and 15 vs. 12
in camera 01). Its 95% error thresholds were 40.9 cm and 49.5 cm,
respectively. The best existing baseline on each view reached 48.5 cm
and 44.6 cm at 95%. These results do not establish a general improvement
or qualify the model for metric analysis.

## Disjoint-camera benchmark

Run `benchmark_heldout_views.py` from the repository root with the same
MotionBERT source, checkpoint, QCA and ONNX detector as above, followed by
all four Pose2Sim clips in camera-number order. The JSON reports all six
directed input/reference pair splits across the first 60 source frames.
Equal frame indices are assumed to correspond. Hardware timing was not
independently verified. The disjoint reference uses the same detector and
calibration source, so agreement is not ground-truth motion-capture accuracy.

Hip-relative scores compare stereo to each input camera's fixed and
MotionBERT estimates on shared joints. Monocular metric scale comes from the
held-out reference torso. Venue scores compare stereo directly in the
calibrated world frame. The all-eligible pass rates count missing joints
as failures. Clips that cannot supply a held-out torso scale still report
venue results. The compared joint set matches the acceptance benchmark.

Where all methods had overlapping joints, stereo achieved 65.3–73.1%
within 10 cm and 3.8–15.3% within 5 cm. Counting missing estimates, its best
hip-relative pass rates were 37.9% and 8.9%, respectively. Its best venue
pass rates were 26.9% and 5.0%.

## Stereo rejection and timing audit

Run `python tools/monocular/benchmark_stereo_audit.py reference.qca yolov8n-pose.onnx cam01.mp4 cam02.mp4 cam03.mp4 cam04.mp4`.
The reference pair stays fixed at source frames 1–58. Each input camera is
shifted individually by one source frame in either direction, with the same
reference denominator for every trial. Scores are in venue coordinates.

The equal-index baseline rejected 790 reference-eligible joint comparisons
across the six directed splits. Of these, 749 failed the reprojection gate
and 41 failed the visibility gate. Counts are comparisons, with joints
repeated across splits. The largest pair disagreement was 98.6 cm despite
subpixel residuals in one pair. The best 10 cm pass rate was 39.5% after a
one-frame shift, versus 26.3% at equal indices for that split. Best offsets
varied across splits, so the sweep is a sensitivity check and does not
establish a timing correction. See `stereo_audit_results.json` for per-camera
visibility, per-joint rejections and frame-level outliers.

## Manual review of the frame 10 left-wrist outlier

Run from the repository root:

```sh
python tools/monocular/benchmark_wrist_labels.py tools/monocular/frame10_wrist_labels.json reference.qca yolov8n-pose.onnx cam01.mp4 cam02.mp4 cam03.mp4 cam04.mp4
```

The labels are approximate single-pass hand–forearm junction marks on source
frame 10, in original image pixels. They differ from the detector by
10.5–31.6 px. Manual substitution made cam01–cam02 fail the existing 10 px
per-view gate. Removing that gate for diagnosis only, the disjoint pair
disagreement was 1.039 m for manual marks versus 0.986 m for detections.
This checks one frame and does not identify whether timestamps, pixel
geometry, calibration, or visible landmark interpretation drives the
remaining disagreement. The results JSON preserves the individual pixel
residuals, including the failed pairs.

## Static calibration spot check

```sh
python tools/monocular/benchmark_static_calibration.py tools/monocular/static_landmarks.json reference.qca cam01.mp4 cam02.mp4 cam03.mp4 cam04.mp4
```

Approximate manual treadmill landmarks were selected on frame 0, using
432 × 768 image previews cropped from row 350. The script maps the preview
coordinates back to decoded pixels, corrects lens distortion and computes
the distance from each observed point to its predicted epipolar line.
The paired distances in the results JSON are ordered by camera name.
No calibration parameters are estimated from these annotations.

Cameras 01 and 02 decoded to 1080 × 1920; Cameras 03 and 04 decoded to
1088 × 1920. The QCA video fields span 1088 × 1920 in all views.
Distances ranged from 0.2 to 40.3 px across 10 comparisons of three landmarks.
The test uses approximate marks, including rims viewed from different
angles. It establishes that static correspondence discrepancies merit
investigation, without identifying a specific calibration or export fault.

## Decoded pixel mapping check

Run from the repository root:

```sh
python tools/monocular/benchmark_video_pixel_mapping.py tools/monocular/static_landmarks.json tools/monocular/static_landmarks_holdout.json reference.qca cam01.mp4 cam02.mp4 cam03.mp4 cam04.mp4
```

The script compares identity, symmetric horizontal crop, and horizontal
resize mappings into the QCA video field. The center-crop hypothesis adds
four pixels to x for 1080-wide views. The resize hypothesis scales x using
pixel centers. Both leave the 1088-wide views unchanged. The test uses
three original features and two separately annotated roller housings.

Median epipolar distance on the original marks was 11.79 px (identity),
11.59 px (crop), and 11.27 px (resize). All three gave 87.51 px median on
the separate marks. Several roller correspondences have very large errors
and should be independently verified. The test does not support adopting
either mapping. The identical 40.35 px maximum on the original marks is
from cameras 03 and 04, whose decoded dimensions already match the QCA.
