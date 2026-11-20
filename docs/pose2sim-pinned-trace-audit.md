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

## Release retrieval and published results follow-up

| Source | Confirmed | Status |
|---|---|---|
| [PyPI wheel, 0.10.49](https://pypi.org/project/pose2sim/0.10.49/#files) | Published SHA-256: `403e0dc4065898ba6a595e72a8970950310979253d60e24c2e00b16b36bf21e1`. | Publisher digest recorded. Local retrieval retry failed at DNS, so it has not been compared with downloaded bytes. |
| [Zenodo source snapshot](https://zenodo.org/records/21287875) | Independent distribution route for the same tagged release. The archive is a source ZIP. | Local retrieval also failed at DNS. Source archive contents and media notices remain unverified. |
| [Pose2Sim accuracy study](https://doi.org/10.3390/s22072712), Data Availability and Appendix A | Provides published running angle comparisons and links the code. | The availability statement provides no trial-level data bundle. Plots can guide comparator selection, but do not provide the matched TRC, model/settings, and MOT angle sample needed for numerical reproduction. |

### Evidence required for the first executed trace

Capture the wheel digest and manifest, and record permitted use of demo media. For the chosen trial, retain the effective configuration and versions, post-processing TRC actually supplied to inverse kinematics, scaled OpenSim model, inverse-kinematics task weights and time range, and reported MOT. Match one sagittal knee coordinate by name, units and timestamp. Rerun from those processed inputs, compare to a tolerance declared beforehand, and separately inventory how the underlying camera decisions and synchronization mapping can be recovered. Record this as traceability on a sample, with thesis-endpoint validity reserved for a qualified force-defined running reference.

**Outcome.** Artifact identity and the limits of the publication-only route are documented. Exact demo manifest, media permissions, and numeric reproduction are still pending.
