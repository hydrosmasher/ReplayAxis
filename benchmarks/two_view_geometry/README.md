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
