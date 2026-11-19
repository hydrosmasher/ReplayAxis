# Noisy external checks for ball reconstruction

Run `python3 research/benchmark/noisy_checks.py noisy-results.csv evidence.json` from the repository root. Two local runs produced byte-identical CSV and JSON outputs.

The experiment compares unweighted reprojection consensus, exclusion based on noisy external measurements, and weighting both consensus support and fitted coordinates. It uses 20 paired seeds, three horizontal pinhole layouts and 48 frames per seed. All conditions include 0.5 px image noise. The check samples timing and position error once per camera and sequence, with 0.08 ms and 2 mm Gaussian standard deviations. The illustrative normalization scales are 0.2 ms and 5 mm. These are simulation parameters.

| Wide layout | Policy | Ball frames recovered | MAE on frames all three policies recovered |
|---|---|---:|---:|
| Combined error | Residual only | 413/960 | 17.38 mm |
| Combined error | Exclusion | 955/960 | 9.54 mm |
| Combined error | Down-weighting | 779/960 | 10.41 mm |
| Borderline timing error | Residual only | 942/960 | 5.83 mm |
| Borderline timing error | Exclusion | 945/960 | 5.91 mm |
| Borderline timing error | Down-weighting | 960/960 | 5.56 mm |

The shared comparison uses 239 frames in the wide combined condition and 938 in the borderline condition. The CSV also reports error over each policy's recovered frames. In the clean condition, where cameras have no true timing or calibration bias, the hard rule still excludes 240 camera-frame observations per layout. Repeated observations share the same camera check, so these are not independent exclusions.

## Assistant evidence

The JSON includes two noise-free residual-only examples. In the first, all camera residuals were at most 0.39 px but the estimate was 3.87 mm from synthetic truth. Live recordings would lack this reference point. In the second, the estimator found an ambiguous consensus and withheld the position. The source frame IDs and pixels remain available; the current ambiguous result does not record the competing camera groups.

## Next decision

Compare graded or uncertainty-calibrated eligibility against both policies on held-out geometries and perturbation distributions. Record competing groups and score margins for ambiguous frames. Extend evidence replay to joint angles and speed after the ball-only policy study. Current results do not specify production thresholds or a single best policy.
