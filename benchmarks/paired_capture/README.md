# Paired capture pilot for 2D-to-3D reconstruction

Collect a full video from each of two synchronized, calibrated cameras for
every repetition. Start with one movement family, 12–16 athletes, three
predefined variants and eight usable repetitions per variant per athlete.
That yields 288–384 paired trials. Keep complete movements and original
timestamps, with a short lead-in and lead-out. Record the intended variant
and optional plain-language prompt before the repetition.

1. Assign pseudonymous athlete IDs. Allocate athletes to train, validation
   and test before training. For a 12-athlete pilot, an initial allocation
   is 8/2/2. Treat the test results as a pilot signal given the small cohort.
2. Save the camera IDs, calibration for the decoded image coordinates and
   frame-level sync mapping. Recheck calibration after either camera moves.
   Record calibration and sync checks before accepting a session.
3. Export the synchronized 3D joints in metres and retain frame/joint validity
   flags and reprojection diagnostics. Store the coordinate frame and joint
   convention alongside each export. Preserve unusable frames as missing.
4. On a subset, collect an independent reference such as calibrated marker
   motion capture or triangulation from a separate camera pair. A single
   additional camera can check reprojection but does not provide independent
   3D on its own. Preserve reference provenance in the manifest.
5. Keep recordings, keys linking identities to athlete IDs, and annotations
   with identifying information in the approved study storage.

## Comparisons

Train or adapt a model on the full Camera A sequence and the 3D trajectory
from the synchronized pair. Compare video-only with video plus the intended
action, using the same recordings and athlete split. A separate two-view
condition measures the benefit of providing both angles at inference.
When scoring the two-view condition against labels made from those same
views, report agreement with those labels. Use independent reference
trials to evaluate accuracy for all three conditions.

Report hip-relative and venue-coordinate results separately. Prespecify
joint-specific tolerances for the intended analysis. Report the proportion
of eligible reference joints within tolerance, counting missing predictions
as failures, and report coverage alongside it. Summarize by athlete and
variant. Use 95% as the target and 90% as the minimum. This pilot does not
establish a population-wide pass rate.

## Manifest preflight

Create a CSV using the header in `manifest_template.csv`. Each row is one
recorded repetition. Use distinct camera IDs and separate video paths for
the two views. The synchronization file must map frames or timestamps
across views. Document the schema for your camera system with the dataset.
`reference_kind` is `two_view` or `independent_3d`. If both references are
available, keep the independent 3D export as `reference_3d` for that trial
and use `training_3d` for the paired-camera labels.

```sh
python benchmarks/paired_capture/validate_manifest.py pilot_manifest.csv
```

Paths are relative to the CSV directory or absolute. The preflight checks
manifest structure and file presence. It does not inspect synchrony,
calibration quality or trajectory contents.

## Rehearsal with the Pose2Sim demo

Run from the repository root with Python 3.10 or newer, OpenCV and NumPy.
Supply the original demo QCA, the fixed 640-square YOLOv8n-pose ONNX
export, both original clips and a new output directory.

```sh
python benchmarks/paired_capture/rehearse_pose2sim.py reference.qca yolov8n-pose.onnx cam01.mp4 cam02.mp4 paired_rehearsal
```

The script uses the notebook's production stereo and export path. It emits
the camera pair JSON, timestamp CSV, trial manifest, metric joint CSV, timing
report and replay HTML/JSON. It adjusts the principal point by the measured
horizontal crop for these clips only. The synchronization table is generated
from equal frame indices at the nominal 60 Hz. The saved timing report labels
those timestamps as synthetic. No camera clock or independent motion-capture
reference is available for this rehearsal.

The verified run paired all 100 frames. The joint CSV retained 1,300
decisions, including 747 reconstructed joints and 553 rejections.
Ninety-two frames contained at least one reconstructed joint.
The manifest preflight passed. See `rehearsal_summary.json`.
