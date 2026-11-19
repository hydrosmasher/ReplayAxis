# ReplayAxis pre-hardware error budget

19 November 2026 · Research only · Initial sensitivity analysis

This memo asks what capture and reference errors a later trial would need to quantify. All example inputs and provisional limits below are engineering assumptions for sensitivity analysis. They are neither published acceptance limits nor measured ReplayAxis performance.

## Define one endpoint per task

| Task | Primary endpoint | Independent comparator | Report with the error |
|---|---|---|---|
| Running | Sagittal knee flexion at initial contact during a defined straight-running trial. Match side, axes, sign, and anatomical model. | Synchronized marker-based kinematics with initial contact identified independently, for example by force plate. Quantify reference repeatability and event alignment. | Signed bias, absolute error, RMSE, limits of agreement, and valid results per attempted contact. Also report the flexion waveform separately. |
| Cricket | 3D ball-center position at reference timestamps over visible pre-bounce flight inside a surveyed volume. | Independently calibrated 3D optical reference with an independently checked clock and spatial registration. Radar can corroborate a documented speed component or speed estimate. It does not independently establish 3D position. | Per-axis bias, 3D distance error by flight phase, and reconstructed frames per eligible reference frame. Record visibility and abstention. |

## Sensitivity model

- **Camera geometry.** In ideal rectified stereo, depth Z = fB/d, with focal length f in pixels, baseline B in metres, and disparity d in pixels. Linearized depth uncertainty is uZ ≈ Z² ud/(fB). For two independent 0.5 px localization uncertainties, ud ≈ 0.707 px. With f = 1600 px and B = 3 m, the depth component alone is 14.7 mm at 10 m and 58.9 mm at 20 m. Near-perfect pixel agreement can coexist with weak depth conditioning. Actual 3D error requires the full camera model and sensitivity across the volume. Increasing baseline can trade shared visibility for better geometry. [Hartley and Sturm](https://doi.org/10.1006/cviu.1997.0547).
- **Synchronization.** At 40 m/s, 0.2 ms of clock offset corresponds to 8 mm of ball travel. This is a displacement scale, not a bound on reconstructed 3D error. An 8 mm timing allocation would imply roughly 0.2 ms only in a direct position-versus-time model with unit gain. Multi-camera reconstruction may respond differently. Measure exposure-time alignment, systematic offsets, drift and jitter with an independent timing reference. A 1 ms exposure spans about 40 mm of travel at that speed. Blur length is not centroid error, and exposure and frame period are different inputs. [Albl et al.](https://openaccess.thecvf.com/content_cvpr_2017/poster/2003_POSTER.pdf).
- **Knee event and geometry.** If local flexion changes at an illustrative 450°/s, a 2 ms error in initial-contact timing shifts an event angle by about 0.9°. As an order-of-magnitude localization example, a transverse 10 mm endpoint error over a 0.4 m segment corresponds to about 1.43° of segment-direction error. Flexion combines two segments with a shared knee landmark, so the two errors can correlate. A tracked hip–knee–ankle proxy and an anatomically defined flexion angle require a mapping and verification before comparing values.
- **Calibration and reference.** Reserve distinct terms for camera intrinsics, extrinsics, reference spatial registration, and repeatability of the reference itself. Propagate shared inputs with covariance. Evaluate systematic biases and occlusions separately. Use independent check points or motion throughout the calibrated volume and repeat the reference procedure. [JCGM Guide, §5](https://www.bipm.org/documents/20126/2071204/JCGM_100_2008_E.pdf).

## Worked allocations to test, not specifications

For arithmetic illustration, each cell below is an assumed standard uncertainty in the endpoint or a direct-model proxy. Root-sum-square applies only under the stated independent, zero-mean approximation. The ball calculation is for one position component, not 3D Euclidean trajectory error. It omits systematic bias and dropout. The real model should use a Jacobian and covariance matrix or Monte Carlo sampling, and report uncertainty alongside bias and coverage.

| Contribution | Ball component | Knee angle at contact |
|---|---:|---:|
| Localization and geometry | 15 mm | 2.0° |
| Timing | 8 mm | 0.9° |
| Calibration and registration | 10 mm | 1.0° |
| Reference uncertainty | 8 mm | 1.5° |
| Illustrative combined standard uncertainty | 21.3 mm | 2.84° |

The 15 mm ball allocation is plausible under the example stereo assumptions at approximately 10 m. At 20 m the same localization and geometry assumption alone already exceeds it. For the knee, the allocations are hypothetical. Marker placement, soft-tissue motion, model conventions, occlusion, and event labeling can introduce errors beyond the geometric proxy.

## Literature constraints and funding gate

- Pose2Sim reported a 4.1° running mean across joint angles and degrees of freedom in one participant. It does not support a 4.1° initial-contact knee threshold. In competition long jump, knee outcome errors varied with the exact metric. Extract the matching event, motion phase and error statistic before proposing a knee acceptance threshold. [Pose2Sim](https://doi.org/10.3390/s22072712) · [Cronin et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC10796501/).
- Eassom et al. reported 36.8 mm mean spatial separation between commercial tennis tracking and aligned Vicon trajectories, with larger separation mid-flight. That is a cross-system 3D result from a different sport. It cannot be directly compared with the assumed single-axis budget here. Use its alignment and phase-specific validation design. [Eassom et al.](https://doi.org/10.1177/17543371251381488).
- Before a funding proposal, define a coaching decision, its minimum useful difference, the allowed error and coverage, and a defensible reference. Then test the model across working distances, view overlap, and systematic timing or calibration offsets. Record infeasible configurations as well as feasible ones. These checks do not require purchasing equipment.

**Next research pass.** Find running-validation studies reporting sagittal knee flexion specifically at initial contact and ball-validation studies with phase-resolved separation and reference repeatability. Record which inputs are measured, modeled or unreported. Then draw an evidence-based capture feasibility envelope and identify the most consequential unknowns for a later validation trial.
