# ReplayAxis comparator walkthrough

## Fixed reviewer task

Review left-knee flexion at an independently marked landing event in two trials. First show the measured value and the synchronized views. Then identify the exact source observations and calibration, determine whether an observation was rejected, and reproduce the value offline. Compare like with like: a three-point hip–knee–ankle angle and a segment-coordinate knee flexion angle can differ. Record definitions, axes, sign, filtering, alignment and units before comparing numbers.

| Workflow | What public evidence supports | What remains to verify |
|---|---|---|
| [Pose2Sim](https://github.com/perfanalytics/pose2sim/blob/main/README.md) | Likelihood-weighted triangulation, iterative camera exclusion based on reprojection error, aggregate camera-exclusion and error logs, and TRC exports. | Whether the exported artefacts retain accepted and rejected camera IDs for one specific 3D point, and how a downstream OpenSim angle can be traced back to those observations. |
| [Anipose](https://pmc.ncbi.nlm.nih.gov/articles/PMC8498918/) and [triangulation code](https://github.com/lambdaloop/anipose/blob/master/anipose/triangulate.py) | Offers calibration, filtered multiview pose, and visualization with video and tracked points. Source code enables inspection of underlying processing. | Whether a single UI selection can reveal the exact contributing observations, including filtering and rejection, and export the inputs needed to reproduce a selected derived angle. |
| [OpenCap](https://pmc.ncbi.nlm.nih.gov/articles/PMC10586693/) and [processing toolkit](https://github.com/opencap-org/opencap-processing) | Publishes a validated kinematics workflow and tools for scripted session download and post-processing. Treat it as a substantive reproducibility comparator. | Which session exports contain source 2D observations and synchronization metadata needed to independently regenerate a selected metric from the earliest available inputs. |
| [Theia3D + Visual3D](https://www.has-motion.com/wiki/doku.php?id=visual3d%3Adocumentation%3Athird-party%3Atheia) and [synchronized playback](https://wiki.has-motion.com/doku.php?id=visual3d%3Adocumentation%3Adialogs%3Aprocessing_video_in_visual3d) | C3D-based transfer of segment transforms and synchronized playback of video with motion capture. | Availability of per-camera observation and rejection records for a selected number. Public documentation checked here leaves this unknown. |

This is a documentation walkthrough. Product installations and hands-on feature comparisons remain outstanding. An undocumented feature stays unknown.

## First benchmark design

Use deterministic synthetic views of hip, knee, ankle and a projectile. Store ground truth separately from algorithm inputs. Inject one mislabeled knee observation and then replay the same case with one camera missing. Use calibrated triangulation to reconstruct each point and compute a simple unsigned knee flexion proxy as 180 degrees minus the angle between the knee-to-hip and knee-to-ankle vectors. Label it a geometric proxy throughout the report and compare it against the same expression evaluated on the ground truth.

For an independently repeatable case, store a metric definition, contributing frame IDs and timestamps, 2D coordinates, candidate and selected camera IDs, residuals, rejection reasons, camera matrices, units, algorithm identifier and numeric tolerance. Missing data and model estimates should be explicitly labeled. Keep fixture generation and scoring separate so that an estimator cannot read ground truth.

The same interface should support an intentionally wrong selection prompted by “compare this knee.” Verify recognition of the wrong side and one-step correction before testing headset hand tracking. This tests an assistant behavior apart from triangulation accuracy.

## Next decision

Implement and run the synthetic benchmark on a separate branch. If pointwise rejection is already exported end to end by a comparator, quantify whether the assistant improves error detection or correction. If no comparator exposes that workflow in the reviewed configuration, test whether the ReplayAxis export makes independent recomputation possible with a small reference script. Verify performance on licensed real data later. No hardware or purchase decision follows from this documentation pass alone.
