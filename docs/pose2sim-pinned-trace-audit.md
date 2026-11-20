# Pose2Sim 0.10.49 trace audit

20 November 2026 · Static source audit

**Pin.** Pair the [PyPI 0.10.49 distribution](https://pypi.org/project/pose2sim/0.10.49/) with the upstream [v0.10.49 source tag](https://github.com/perfanalytics/pose2sim/tree/v0.10.49). The tag resolves and its [packaging manifest](https://github.com/perfanalytics/pose2sim/blob/v0.10.49/pyproject.toml) includes `Demo_SinglePerson/**`. The tagged [demo configuration](https://github.com/perfanalytics/pose2sim/blob/v0.10.49/Pose2Sim/Demo_SinglePerson/Config.toml) was retrieved. The source declares BSD-3-Clause. No separate permission for reuse or redistribution of the demo participant media was verified. The released wheel could not be inspected because the local environment could not resolve PyPI. Package inclusion here is verified from the build configuration, with the wheel's exact contents and hash still pending.

## Where the evidence chain stops

| Layer | Verified from the tag | What a runtime audit must establish |
|---|---|---|
| Frame and processing configuration | Demo config declares automatic frame-range selection, synchronization options, a 0.3 2D likelihood cutoff for triangulation and an interpolation gap parameter of 20 frames. | Recover the effective runtime settings, actual frame range, and source-to-synced frame mapping for the selected trial. |
| Camera decisions | [Triangulation source](https://github.com/perfanalytics/pose2sim/blob/v0.10.49/Pose2Sim/triangulation.py) constructs an excluded-camera ID list per person, keypoint and frame. It carries those lists through trimming and aggregates camera exclusion counts. | Check output directories and any relevant modes for the original per-keypoint ID lists and how camera indices map to source views. Internal availability creates a plausible instrumentation point. |
| Reported trajectory and angle | The audited triangulation implementation writes TRC coordinates and uses the exclusion counts in its recap. In the inspected path, no separate point-level rejection export was identified. The demo walkthrough then runs filtering, marker augmentation and kinematics. | Recover the actual model, inverse-kinematics configuration and processing window. Recalculate one angular sample from a verified processed trajectory, then trace its input landmarks through filtering/interpolation and triangulation. |

**Decision.** The earliest unresolved link in the camera portion is the mapping from one reported landmark sample to exported per-view decisions and original observations. This is a static finding for one pinned path. No selected knee angle was generated or reproduced in this pass, and other export modes were not exhaustively tested. A configured demo without a force-defined contact cannot establish validity at the thesis endpoint.

**Next checkpoint.** Obtain and hash the pinned wheel in an authorized environment, inspect its exact demo manifest and any bundled media notices, then run one permitted trial. First score angle-from-processed-inputs reproducibility. Next see whether original-camera lineage is recoverable from standard outputs or requires an instrumented rerun.
