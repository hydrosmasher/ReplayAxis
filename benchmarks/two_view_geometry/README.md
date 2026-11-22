# Two-view geometry benchmark

From the repository root, install NumPy and OpenCV and run:

```sh
python benchmarks/two_view_geometry/replayaxis_geometry.py
```

Use `--videos path/to/cam01.mp4 path/to/cam02.mp4 ...` to screen all
pairs at the first frame. Real video used the four Pose2Sim single-person
demo clips. The footage is available from
[Pose2Sim](https://github.com/perfanalytics/pose2sim/tree/main/Pose2Sim/Demo_SinglePerson).
The checked-in results were generated with OpenCV 5.1.0 and NumPy 2.5.5.

The synthetic scene has a 1 m baseline, 60° true horizontal field of view,
250 noisy background correspondences, and one point moving laterally at
8 m/s. The same 500 image-space observations, sampled at 500 Hz with
0.75 px Gaussian noise per coordinate, are used in every comparison.
The known 1 m baseline lets this fixture express errors in centimetres
after reconstruction. The estimator itself still returns baseline units.

| Camera geometry | Samples accepted | Median 3D error | 95th percentile |
| --- | ---: | ---: | ---: |
| Known | 500/500 | 4.41 cm | 12.84 cm |
| Estimated, 60° assumed | 500/500 | 86.53 cm | 116.65 cm |

The field-of-view sweep varies only the assumed angle. High acceptance
and 250 inliers coexisted with substantial 3D error in this fixture.
One random seed and one point trajectory characterize this run.
The benchmark simulates observation timing and does not measure camera,
pose detector, or rendering performance at 500 Hz.

The automatic estimator withheld geometry for all six real pairs
because they produced 9–18 matches against the 20-match minimum.
This yields no real-video 3D error estimate. A follow-up can use
verified static correspondences and the supplied calibration to
compare estimates on identical athlete detections.

## Real footage with supplied calibration

Run from the repository root using the four original clips, Pose2Sim's
`calibration/Calib.qca.txt` and a fixed 640×640 YOLOv8n-pose ONNX export
with output shape 1×56×8400.

```sh
python benchmarks/two_view_geometry/replayaxis_real.py \
  path/to/Calib.qca.txt path/to/yolov8n-pose.onnx \
  path/to/cam01.mp4 path/to/cam02.mp4 path/to/cam03.mp4 path/to/cam04.mp4
```

The run sampled matching video indices 0 through 55 at five-frame intervals.
Source clips report 60 fps. Alignment by frame index was assumed and no
independent time synchronization or ground-truth athlete motion was supplied.
The supplied calibration was converted using the camera-axis and intrinsics
conventions of Pose2Sim's QCA converter and lengths were expressed in metres.
The static feature screen used a temporal median image, a low-variation mask,
mutual descriptor matching and a 2 px reference epipolar test. Passing
the epipolar test alone would not establish that a match was correct.
This is a reference-assisted benchmark, with calibration used to screen
matches and, where available, convert baseline-relative results to metres.

All six calibrated pairs produced 3D joint samples (58–99 per pair across
12 frame pairs). The stricter background screen retained 0–1 matches per
pair. The estimated path withheld every pair and no real-video 3D
disagreement can be computed. The calibrated counts measure coverage,
with no independent 3D accuracy assessment. See `real_results.json`.

Input SHA-256 values for this run:

| Input | SHA-256 |
| --- | --- |
| Calib.qca.txt | fd90e4bbae3278ef1dc0cdd42a34ee06bf88286f628a02c00a29407aa39e34c5 |
| yolov8n-pose.onnx | 04f6d2416266f2aba6c5ba8b26de33ed9eba3279f972ac02e33f9f1366547586 |
| cam01.mp4 | cf4f2816c86bea4bfbea255333d8626ff32a3ecabdab8b0fb147cea9167fde3a |
| cam02.mp4 | 94ff87cf978b8406e8aa36ab3c5362e72848994e87652f0dc7a33c315e8e0442 |
| cam03.mp4 | b8b329f832f178f27ecb78d024d5026b96c6adb36c387bfe2c0af85eab8a11ca |
| cam04.mp4 | b5c0e7863fd70d008e7178d3c556b045b0ea5f78fcd61ca548a0b2e807e641f7 |
