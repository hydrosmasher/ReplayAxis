# Real-video decoder smoke test

ReplayAxis notebook baseline: `befea3570711391f66046410179ad975e9bb524b`. Test host: Apple Silicon, macOS 27.2.1, Python 3.12.16, and OpenCV 4.14.0. Source: [Pose2Sim 0.10.49 single-person demo](https://github.com/perfanalytics/pose2sim/tree/v0.10.49/Pose2Sim/Demo_SinglePerson). The published wheel SHA-256 matched `403e0dc4065898ba6a595e72a8970950310979253d60e24c2e00b16b36bf21e1`. The two input MP4s and calibration matched the corresponding wheel entries byte for byte.

## Results

Each input has 100 recorded frames at 60 fps and decodes to 1080 × 1920. ReplayAxis requested two seconds at 20 samples per second, starting at nominal zero offsets for both clips. OpenCV decoded the selected images and the production incremental pairing path received empty landmark sets. Six of the 40 requested samples fell past the end of both clips.

| Mode | Pairs emitted | Mean processing | Max processing | Samples over 50 ms |
|---|---:|---:|---:|---:|
| Unpaced | 34 | 4.54 ms | 22.51 ms | 0 |
| Paced | 34 | 7.04 ms | 18.06 ms | 0 |

The paced run recorded zero processing deadline lag. Neither run found missing one-sided views or nominal timestamp skew above 12 ms. These timings cover decoding and frame pairing in this one clip pair. MediaPipe 0.10.35 aborted while opening its pose graph after CPU delegate initialization, with a graphics-service error. No pose inference, reconstruction accuracy, or live-camera latency was measured.

## Interpretation

Zero nominal timestamp skew comes from the file frame indices and equal nominal frame rates. The physical synchronization of the recorded actions was unverified. The Qualisys calibration specifies 1088 × 1920. Confirm the mapping of the eight horizontal pixels before treating the calibration as valid for these decoded frames. The next full test requires a working pose backend, verified timing and image geometry, and an independent distance or joint reference. The repository contains the test findings only.
