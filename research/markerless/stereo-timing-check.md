# Stereo timing check on the demo clips

This follows the [CPU pose smoke test](cpu-pose-smoke-test.md) on Pose2Sim v0.10.49's cam01 and cam02 videos (60 fps). The offset convention is camera B frame = camera A frame + offset. The sweep tested −8 to +8 frames while retaining camera A frames 8–91 for every candidate. It used the same OpenCV DNN pose model and held provisional camera geometry fixed. For both views, detections had to meet the 0.55 landmark confidence threshold. The score was the median of the mean two-camera reprojection residual per triangulatable joint. The production 10 px rejection cutoff was disabled for scoring so large residuals remained visible.

| Camera A window | Best B offset | Median at best offset | Median at zero offset | Joint pairs at best offset |
|---|---:|---:|---:|---:|
| Frames 8–49 | +2 frames | 5.632 px | 6.808 px | 541 |
| Frames 50–91 | −2 frames | 7.596 px | 8.555 px | 539 |
| Frames 8–91 | 0 frames | 7.398 px | 7.398 px | 1,079 |

At +1 frame, the full-window score was 7.404 px, only 0.006 px higher than the zero-offset score. The two halves prefer opposite offsets. This sweep does not identify a reliable synchronization correction or establish drift. Landmark error, movement geometry, and the unverified mapping from 1088 calibration columns to 1080 encoded columns can affect the scores. Keep the nominal offsets unchanged. A shared timing event and verified image mapping are required before the independent known-distance check.
