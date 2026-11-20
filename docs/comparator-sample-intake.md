# Pose2Sim and OpenCap sample intake

20 November 2026 · Documentation and source audit

The [single-measurement comparison](single-measurement-provenance.md) requires a permitted sample and a chain from an angle back to its per-camera observations. This pass verified the entry points, an actual Pose2Sim demo configuration file and the OpenCap downloader source. It did not run either pipeline or validate participant media permissions.

| Check | Pose2Sim | OpenCap |
|---|---|---|
| Official sample lead | Installed `Pose2Sim/Demo_SinglePerson` walkthrough. The official repository contains its [configuration](https://github.com/perfanalytics/pose2sim/blob/main/Pose2Sim/Demo_SinglePerson/Config.toml). | The [Core README](https://github.com/opencap-org/opencap-core) links an [example session](https://app.opencap.ai/session/7272a71a-e70a-4794-a253-39e11cb7542c). Its locally reprocessed workflow documents an authentication path. |
| Verified processing evidence | Demo configuration includes frame range and synchronization settings. The [walkthrough](https://github.com/perfanalytics/pose2sim/blob/main/README.md) describes calibration, 2D pose, synchronization, triangulation, filtering, marker augmentation, and kinematics. | [Downloader source](https://github.com/opencap-org/opencap-processing/blob/main/utils.py) contains paths for camera mapping, calibration, model/metadata, marker and IK files, settings, and synchronized video retrieval. These are code capabilities, with session-specific contents still unverified. |
| First missing link for one-angle reproduction | The exact output records mapping a chosen angle time through the processing window and 3D landmarks to contributing or excluded source cameras remain unverified. | It remains unverified whether the demo session exposes downloadable 2D tracks, original-to-synchronized frame mapping and per-observation selection decisions. |
| Permission and scope | Official packaging offers a sample entry point. Confirm the included media and their terms at the pinned release before retrieving or republishing them. | A linked example session and a code license do not establish media use or redistribution terms. Confirm authorized access and permitted use before downloading or reprocessing. |

## Proposed first hands-on check

1. Start with the Pose2Sim demo and document the pinned release, sample-specific terms, environment, and hashes of inputs actually used. Inventory the bundled files before running.
2. Pick a single documented valid knee angle sample. The sample can assess traceability even if it lacks an independently force-defined running contact. Such an audit cannot establish validity for the thesis endpoint.
3. Attempt two reproductions separately. First recompute the reported angle from the processed trajectory and model/settings. Then trace that trajectory back through filtering or interpolation, calibration and timing, 2D coordinates and per-camera decisions. Mark the first missing artifact in each path and record whether a rerun can recover it.
4. Repeat with a permitted OpenCap export. Keep files and permissions session-specific, and use a local copy or a documented read-only path for the audit. Record unknowns rather than inferring capabilities from the absence of an output.

**Decision.** Use Pose2Sim as the first local sample candidate, and OpenCap as the second after confirming its session access and terms. Exact sample contents and offline angle regeneration remain untested. No conclusion on product differentiation follows yet.
