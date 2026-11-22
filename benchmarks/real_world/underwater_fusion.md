# Underwater detection fusion

This compares the same 356-frame [underwater butterfly clip](underwater_butterfly_pilot.md) under three input conditions. Run the original replay command with `--rotation fused` to reproduce the combined run. The default stays unrotated.

| Mode | Any pose | All 13 joints | Exported head |
| --- | ---: | ---: | ---: |
| Original | 236 | 37 | 42 |
| Counterclockwise | 300 | 15 | 29 |
| Fused | 317 | 48 | 61 |

The fused mode runs the detector twice. It chooses the detection with
the stronger torso scores, then merges joints only if the detections agree
on the torso within a fraction of its apparent length. This is a single-
swimmer heuristic. Scores are detector scores, not calibrated probabilities.
Fewer than two overlapping torso anchors prevent merging the detections.

On the six previously labeled later frames (see [rotation check](underwater_rotation.md)),
fused wrist coverage was 4/4 with 18.3 px median error, compared with
4/4 and 21.2 px for rotation alone. Hip error rose from 58.5 to 90.1 px.
It still exported no head landmark on either cap-visible frame. Increased
coverage is not verified accuracy, and this reused sample cannot establish
generalization. A second clip with independently labeled joints and a
calibrated depth reference is still needed.
