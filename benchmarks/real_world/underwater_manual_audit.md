# Underwater butterfly manual audit

Source and original replay command: [underwater butterfly pilot](underwater_butterfly_pilot.md). I visually inspected eight purposively sampled source frames (zero-based indices 40–150) and marked approximate positions on 384×216 display tiles. Coordinates are multiplied by five for scoring against original 1920×1080 pixels. Occluded and uncertain points were omitted. Shoulder, hip and wrist comparisons use the closest of the two exported sides because anatomical side was ambiguous in this view. These are single-rater, coarse observations on one clip.

| Manual landmark | Frames with an exported candidate | Median distance when exported |
| --- | ---: | ---: |
| Hip | 8/8 | 65.8 px |
| Shoulder | 4/4 | 321.6 px |
| Wrist | 2/8 | 264.1 px |
| Visible cap, checked for nose/head export only | 0/4 | — |

Cap center and detector nose are different landmarks, so cap labels are used only for a presence check. A visible cap does not imply the nose is visible. On these eight frames, direct inference at confidence 0.55 and replay export gave the same frame-level coverage for the four categories. Wrong placement and missed wrists are observable before any depth evaluation. This is a screening audit, not a population estimate or a 3D reference.

```sh
python benchmarks/real_world/score_underwater_labels.py underwater_replay.json benchmarks/real_world/underwater_manual_labels.csv
```
