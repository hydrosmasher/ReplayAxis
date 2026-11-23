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
