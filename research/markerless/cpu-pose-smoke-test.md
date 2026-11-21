# CPU pose inference smoke test

The [decoder test](real-video-smoke-test.md) used two clips from the Pose2Sim v0.10.49 single-person demo. This follow-up uses the same inputs and an optional OpenCV DNN CPU backend with the fixed 640 × 640 [YOLOv8n-pose export](https://huggingface.co/Xenova/yolov8-pose-onnx/blob/main/yolov8n-pose.onnx). Model SHA-256: `04f6d2416266f2aba6c5ba8b26de33ed9eba3279f972ac02e33f9f1366547586`. Model weights and footage are obtained separately.

| Paced rate | Pairs | Pairs with at least one 3D joint | Mean processing | Over budget | Peak processing lag |
|---|---:|---:|---:|---:|---:|
| 20 Hz | 34 | 33 | 81.56 ms | 34 | 1,073.26 ms |
| 10 Hz | 17 | 16 | 74.42 ms | 0 | 0 ms |

Measured in one paced run per rate on Apple Silicon with Python 3.12.16 and OpenCV 4.14.0. In separate unpaced runs, mean processing was 70.35 ms at 20 Hz and 76.62 ms at 10 Hz. The unpaced 10 Hz run exceeded its 100 ms budget once. This is a short-clip smoke test, and the timing excludes startup and browser rendering.

Nominal start offsets were zero. Physical synchronization and the eight-pixel difference between encoded image width and the published calibration width remain unverified. Geometry and joint accuracy require an independent reference. Highest-score, single-person selection was used. The results do not establish multi-athlete tracking or continuous live performance.
