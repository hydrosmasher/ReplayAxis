# Synthetic measurement provenance benchmark

Run with Python 3.10+ and no external dependencies.

```sh
python3 research/benchmark/benchmark.py evidence.json
python3 research/benchmark/benchmark.py evidence.json --verify
```

The export records camera calibration, source frame IDs, timestamps, pixel observations, residuals, camera decisions and a geometric knee-flexion proxy. The estimator receives observations and calibration only. The verifier uses synthetic ground truth to score the result and checks that rerunning the estimator on the serialized inputs reproduces the saved results.

| Scenario | Verified result |
|---|---|
| Clean four-camera frame | Joint positions, ball centre and angle match synthetic truth within the test tolerance. |
| Camera D shifted 60 pixels for knee and ball | Camera D rejected for those tracks. Joint angle and ball position recovered. |
| Camera C missing | Remaining clean views recover the positions and angle. |
| Camera C missing and D corrupted | Knee and ball estimates withheld as ambiguous. Their downstream measurements are unavailable. |

The simulation uses one frame, perfectly calibrated parallel pinhole cameras and a 2 px consensus threshold. The angle is a three-point geometric proxy. It uses no anatomical coordinate convention. The ball fixture tests position, with trajectory and speed deferred until multiple timestamps exist. Same-code recomputation verifies serialization and deterministic behavior on the tested environment. Separate implementation and environment verification remain open.

## Next experiment

Add multiple frames and independent metric recomputation, then sweep sync skew, pixel noise and calibration error. Measure false camera rejection, angle error, position error and abstention. Use the resulting evidence record for a desktop assistant interaction that explains a rejected view and lets an analyst inspect the contributing observations.
