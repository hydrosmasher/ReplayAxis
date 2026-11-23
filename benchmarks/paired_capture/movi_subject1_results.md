# MoVi Subject 1, round S2
Both Grasshopper AVI files matched the MD5 values published by Borealis (file IDs 85651 and 85704, dataset DOI 10.5683/SP2/JRHDRN). The run decoded all 2,763 frames per camera and sampled every fifth frame. Frame zero was excluded to support the offset sensitivity check. The second motion-capture array was used with nominal sample index 4 × video frame. Exact clock alignment was not independently verified. Missing estimates count as failures. The reference markers are wrist and ankle joint centers.

| Joint | Eligible | Reconstructed | Within 5 cm | Within 10 cm | Median error, reconstructed |
|---|---:|---:|---:|---:|---:|
| Left wrist | 548 | 243 | 114 | 224 | 5.24 cm |
| Right wrist | 540 | 452 | 310 | 417 | 3.93 cm |
| Left ankle | 545 | 480 | 331 | 459 | 3.98 cm |
| Right ankle | 551 | 502 | 402 | 474 | 3.40 cm |
| Total | 2184 | 1677 | 1157 | 1574 | |

A shift of the reference by one video frame in either direction did not improve the pooled pass rates. Valid reference counts differed slightly by offset. This is a single-trial result. The left wrist was the largest coverage gap. Earlier visual review of eight partially downloaded frames suggested that it is often hidden in the PG2 side view.

## Left-wrist confidence sensitivity

On the same 548 eligible samples, lowering confidence from 0.55 to 0.35 increased reconstruction from 243 to 322, 5 cm passes from 114 to 151, and 10 cm passes from 224 to 281. Reprojection rejections rose from 66 to 138 and low-visibility rejections fell from 239 to 88. At 0.55, 225 samples fell below threshold in PG2 and 14 in PG1. The production default remains 0.55.

## Offline interpolation of short left-wrist gaps

Infer both views at 30 fps and reconstruct observed anchors using the selected confidence threshold. Interpolate only bounded gaps of at most the listed number of missing frames. Score the same 548 nominally aligned reference samples used above. No motion-capture value is used for interpolation. Missing estimates count as failures. Results apply to this trial only.

| Confidence | Max missing frames | Eligible | Reconstructed or filled | Within 5 cm | Within 10 cm |
|---|---:|---:|---:|---:|---:|
| 0.55 | 0 | 548 | 243 | 114 | 224 |
| 0.55 | 3 | 548 | 274 | 126 | 250 |
| 0.55 | 6 | 548 | 290 | 135 | 262 |
| 0.55 | 12 | 548 | 313 | 140 | 276 |
| 0.35 | 0 | 548 | 322 | 151 | 281 |
| 0.35 | 3 | 548 | 347 | 156 | 298 |
| 0.35 | 6 | 548 | 368 | 165 | 310 |
| 0.35 | 12 | 548 | 412 | 168 | 324 |

The 0.35 threshold with gaps of up to 12 frames recovered the most estimates, but only 14 of the 44 additional fills relative to the six-frame limit were within 10 cm. This is an offline sensitivity analysis. Production settings were not changed.
