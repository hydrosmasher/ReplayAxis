# ReplayAxis analytical capture envelope

19 November 2026 · Research only

This extends the [error budget](pre-hardware-error-budget.md) and [endpoint review](endpoint-validation-evidence.md). It tests only whether illustrative component allocations are internally compatible with particular geometry and timing assumptions. Coaching thresholds, achievable calibration, and measured performance remain pending. No equipment specifications are implied.

## Rectified stereo geometry

Depth sensitivity is approximated by uZ = Z² ud/(fB), where Z is depth, B is baseline, f = 1600 px, and ud = √2 × 0.5 px under independent equal per-view localization uncertainties. The target column solves B ≥ Z² ud/(f × 0.015 m) for the provisional 15 mm depth-only allocation. The model assumes ideal parallel geometry, usable overlap, and correctly matched points. Focal length and localization uncertainty must be evaluated together with field of view and target pixel size. [Hartley and Sturm, Triangulation](https://doi.org/10.1006/cviu.1997.0547).

| Depth (m) | Depth uncertainty, 1.5 m baseline (mm) | 3 m baseline (mm) | 6 m baseline (mm) | Baseline for 15 mm (m) |
|---:|---:|---:|---:|---:|
| 5 | 7.4 | 3.7 | 1.8 | 0.74 |
| 10 | 29.5 | 14.7 | 7.4 | 2.95 |
| 15 | 66.3 | 33.1 | 16.6 | 6.63 |
| 20 | 117.9 | 58.9 | 29.5 | 11.79 |

A 3 m baseline reaches approximately 10.1 m under these assumptions. A 6 m baseline reaches approximately 14.3 m. Neither statement accounts for occlusion, atypical triangulation angles or calibration error. For 20 m, an algebraic result of 11.79 m baseline does not establish viable shared coverage. A later geometry assessment should compare shorter capture zones, optical scale, and oblique viewpoints across the actual volume.

## Fast-ball timing

The model v × |Δt| gives physical travel over the timestamp offset. The last column inverts the provisional 8 mm allocation. Treat this as a timing sensitivity under unit gain, since the mapping from camera time error to triangulated position depends on direction and geometry.

| Ball speed (m/s) | 0.1 ms (mm) | 0.2 ms (mm) | 0.5 ms (mm) | Offset corresponding to 8 mm (ms) |
|---:|---:|---:|---:|---:|
| 20 | 2.0 | 4.0 | 10.0 | 0.400 |
| 30 | 3.0 | 6.0 | 15.0 | 0.267 |
| 40 | 4.0 | 8.0 | 20.0 | 0.200 |
| 50 | 5.0 | 10.0 | 25.0 | 0.160 |

At 10 m with a 3 m baseline and 40 m/s with 0.2 ms offset, the illustrative depth and timing allocations both fit. At 15 m with the same baseline, depth fails. At 50 m/s with the same offset, the timing proxy fails. These are separate component checks. Their alignment, covariance and biases must be modeled before calculating total 3D error. Exposure and rolling-shutter readout are separate timing inputs. [JCGM uncertainty guide](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf).

## Knee flexion at initial contact

Use the local magnitude of angular velocity, not running speed as a substitute. The first-order timing term is |dθ/dt| × |Δt|. Rates are illustrative and should be extracted at contact from independent reference waveforms stratified by running speed, side and foot-strike pattern.

| Local angular rate (°/s) | 1 ms (°) | 2 ms (°) | 4 ms (°) | Offset corresponding to 0.9° (ms) |
|---:|---:|---:|---:|---:|
| 150 | 0.15 | 0.30 | 0.60 | 6.00 |
| 300 | 0.30 | 0.60 | 1.20 | 3.00 |
| 450 | 0.45 | 0.90 | 1.80 | 2.00 |
| 600 | 0.60 | 1.20 | 2.40 | 1.50 |

At an illustrative rate of 450°/s, 2 ms consumes the full timing component. Separately estimate error on a force-defined reference timestamp and the candidate's own event timestamp. The first evaluates angle agreement at matched time; the second includes event detection error. [Point-of-contact high-speed running study](https://doi.org/10.3390/s24175718).

## Reference readiness before a budget decision

| Endpoint | Required evidence |
|---|---|
| Both | Independent spatial check points across near, far and edge regions. Common time reference with independently measured alignment uncertainty, drift, exposure convention and frame drop log. Separate calibration and validation targets. |
| Pre-bounce ball | Independent 3D reference tracking through early, middle and late flight. Record reference repeatability at the relevant speeds and positions, along with the usable overlap between both systems. Keep bounce and extrapolation separate. |
| Knee at contact | Synchronized force-based event definition and marker-based joint angles with a matched model, side and sign. Document timing alignment and between-session repeatability, then report matched-time and end-to-end errors with coverage. |

**Next research pass.** Compare candidate reference datasets and collection protocols against this checklist. Seek explicit uncertainty, shared volume and timestamp semantics. Use that evidence to narrow the feasible task and volume before proposing a budget.
