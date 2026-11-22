# Underwater butterfly — real single-camera pilot

Source: [Butterfly stroke from underwater](https://commons.wikimedia.org/wiki/File:Butterfly_stroke_from_underwater.webm), filmed by It is a wonderful world, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The benchmark uses the original 1080p WebM unchanged (SHA-256: `8fea4373c5fe50cc0eb02e13646b1e01ddf30b3572971e4979f98acbf67135bb`). No source media is embedded in the repository. This is a separate swimming recording from the Phelps race.

Run the fixed-prior baseline with the same ONNX detector as the terrestrial benchmark:

```sh
python tools/monocular/reconstruct.py butterfly.webm yolov8n-pose.onnx --frames 1000 --output underwater_replay.html
```

| Measure | Result |
| --- | ---: |
| Decoded frames | 356 at nominal 25 fps |
| Frames with any exported pose | 236 (66.3%) |
| Frames with all 13 landmarks | 37 (10.4%) |
| Exported head landmark | 42 (11.8%) |
| Exported left / right wrist | 131 / 146 |
| Total exported joint samples | 2,429 |
| Longest interval with no pose | 13 frames |
| Longest uninterrupted run with any pose | 26 frames |

Coverage is measured after confidence screening and the reconstruction's required hips and parent joints. It is not detector accuracy. Labels were not manually verified and no synchronized calibrated reference was available for this recording. The result checks transfer of the existing detection-and-replay pipeline. It does not score the learned depth model, establish 3D accuracy, or provide metric swimmer trajectory estimates.

Next: annotate head, shoulders, hips and wrists in representative frames across a stroke cycle and check errors and misses against the detector. Improve the 2D tracks before comparing depth models on synchronized underwater footage.
