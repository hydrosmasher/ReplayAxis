# Multiframe capture error sweep

The synthetic sequence uses four parallel pinhole cameras, 48 frames at 240 fps, a ball with a 40 m/s horizontal velocity component, and a moving lower-body fixture. One camera has controlled timing or calibration error. Pixel noise is independent Gaussian noise with one fixed pseudorandom seed reused across conditions. The estimator uses the existing 2 px threshold. A position estimate is compared with truth at nominal frame time. Ball speed is the magnitude of the adjacent-frame displacement divided by the frame interval, scored only when both adjacent estimates exist. Angle is the benchmark's geometric proxy.

| Condition | Ball frames recovered | Ball position MAE | Interpretation |
|---|---:|---:|---|
| Clean | 48/48 | Numerical precision | Baseline also recovered all 47 adjacent speed samples. |
| 0.1 ms skew | 48/48 | 4.87 mm | All observations accepted despite position bias. |
| 0.5 ms skew | 0/48 | — | The consensus rule abstained on all ball frames. |
| 1 ms skew | 48/48 | Numerical precision | The bad ball views were rejected. The knee proxy still had 0.26° mean absolute error. |
| 1 px noise SD | 37/48 | 10.48 mm | Ball-speed MAE was 1.94 m/s across 28 valid adjacent pairs. |
| 10 mm camera-position bias | 48/48 | 12.12 mm | All observations accepted despite calibration bias. |
| 0.5 ms skew, 0.5 px noise SD, 5 mm bias | 19/48 | 19.14 mm | Speed available for just 12/47 adjacent pairs. |

Errors apply to recovered estimates. An empty error cell in the CSV denotes no samples. Rejection counts cover observations with a decision. Ambiguous tracks are counted separately. The simulated response to skew is non-monotonic: borderline inconsistencies can produce tied selections, while a larger deviation can isolate a single bad view. These are fixture results and cannot be used as camera acceptance limits.

The CSV was reproduced byte for byte in two runs on one environment. The next experiment is to run repeated seeds and varied camera geometry, report coverage together with accuracy, and compare reprojection-only checks with explicit synchronization and calibration bounds. Export per-frame evidence for selected failure cases so the assistant can explain what happened. Longer-interval speed estimation should be compared against the adjacent-frame baseline before using speed in reviewer tasks.
