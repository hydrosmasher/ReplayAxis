# Single-measurement provenance comparison

20 November 2026 · Documentation and source-code review

## Common task

Starting from a displayed left sagittal knee-flexion value, ask an independent reviewer to recover the force-defined running contact time, source camera/frame observations, calibration and synchronization revisions, view decisions, filtering or interpolation, anatomical angle convention, and executable model and settings. Then ask the reviewer to recompute the same reported value. Keep the numerical recomputation tolerance separate from agreement against a reference. A three-point geometric knee angle is a different endpoint from an anatomical segment angle.

| Workflow | Recoverable steps documented publicly | What still needs a one-trial check |
|---|---|---|
| [Pose2Sim](https://github.com/perfanalytics/pose2sim/blob/main/README.md) and OpenSim | Configured 2D input, likelihood-weighted triangulation, reprojection-based camera exclusion, interpolation and TRC trajectory output followed by model kinematics. | Starting at one OpenSim angle sample, can a reviewer recover source-frame mapping, exact accepted and excluded camera IDs for each contributing landmark, gap-fill status, and the model/IK settings without guessing? Aggregate exclusion statistics alone cannot answer this. |
| [Anipose](https://anipose.readthedocs.io/en/stable/tutorial.html) | The tutorial exposes camera calibration, 2D tracks and triangulated 3D CSV outputs. This can support an upstream reconstruction audit. | Verify the exact camera membership and decision reason at a selected landmark/frame. Any separately computed anatomical joint angle and force event need their own provenance. |
| [OpenCap Core](https://github.com/opencap-org/opencap-core) and [session downloader](https://github.com/opencap-org/opencap-processing/blob/main/utils.py) | Core documents video-to-marker-to-OpenSim kinematics. The downloader code includes camera mapping, calibration, model metadata, and options for videos and synchronized outputs. | Exercise one permitted sample. Inventory whether 2D tracks, frame/temporal mapping, confidence, view decisions and processing versions are present in the standard export or must be recovered by rerunning. |
| [Theia3D + Visual3D](https://www.has-motion.com/wiki/doku.php?id=visual3d%3Adocumentation%3Athird-party%3Atheia) | Segment-transform/C3D handoff and [model-based angle calculation](https://wiki.has-motion.com/doku.php?id=visual3d%3Adocumentation%3Apipeline%3Amodel_based_data_commands%3Acompute_model_based_data) can support checking the downstream angle from the model and its conventions. | Verify whether the upstream per-camera pixels, timing, selection and pipeline decisions can be exported and connected to the selected segment transforms. Vendor-specific access and software versions matter. |

An unverified cell is an open question. The review does not indicate that a capability is absent. Documentation and code were reviewed without running the comparator products.

## How to record the audit

1. Pin the tool versions and identify one permitted running trial, the event time, limb and angle convention. Use the same task for every tool that supports it. Log any incompatible model or event definition.
2. For each required input, record **available in exported files**, **recoverable with a rerun**, **outside this workflow**, or **unverified**. Save the artifact name and record key or timestamp. An archetypal chain is angle sample → contact timestamp → segment transforms and processing window → 3D landmarks → per-camera 2D observations and decisions.
3. Give the reviewer the bundle and a fixed numerical tolerance. Record whether the angle can actually be regenerated, the first missing dependency, whether the frame is observed or interpolated, additional manual steps, and whether a missing measurement is identified correctly.
4. Interpret any measured comparison in the approved scope. A comparator with a complete trace supports studying review effort and error detection. An incomplete trace supports investigating a more explicit evidence bundle. Both outcomes require a hands-on audit before any differentiation claim.

**Next checkpoint.** Start with Pose2Sim and OpenCap as documented reconstruction-to-kinematics comparators. Find permitted sample bundles and check the artifact chain above. BioCV access and supervisor approval remain separate decisions.
