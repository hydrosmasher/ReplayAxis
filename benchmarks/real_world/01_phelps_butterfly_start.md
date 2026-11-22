# Case 01 — Michael Phelps, butterfly start to 25 m

**Event:** London 2012 men's 100 m butterfly final, 3 August 2012. **Target:** Michael Phelps, lane 4.

- [Official Olympic race replay](https://www.youtube.com/watch?v=X7bj_LUIY7Y)
- [Official results book, swimming](https://www.usaswimming.org/docs/default-source/timesdocuments/meet-results/olympic-games/2012-olympic-games.pdf)

## Footage status

Public broadcast reference identified. Synchronized independent feeds covering lane 4 from the start through 25 m, original capture timestamps and camera calibration remain unverified. A cut or slow-motion replay is insufficient evidence that frames correspond to the same instant. Keep the source URL in the repository and use authorized source files for processing.

## Annotation and measurement

- Define the race-time origin by the start signal. Record each view's original frame index and presentation timestamp. Split at edits and exclude repeated or retimed frames unless the original clock can be recovered.
- Label feet leaving the block, first hand entry, head breakout and head crossing the 25 m plane. Establish that plane with surveyed pool geometry or independently verified markings.
- Register the camera views in pool coordinates, with +x down the lane and +z upward. Model refraction for views that cross the water surface. Use synchronized overlapping views for triangulation and report gaps when the athlete is obscured.
- Store the tracked point by name. A pelvis midpoint trajectory can describe swimmer translation. Head position defines the 25 m endpoint. Record position (m), velocity (m/s) and acceleration (m/s²) on the capture timeline, along with visibility and uncertainty. Compute derivatives on contiguous valid samples with a documented smoothing window and report sensitivity to that window. Derive direction from velocity and withhold direction when speed is indistinguishable from zero.
- Allow frame-by-frame pause. Show source timestamps and distinguish measured observations, estimated frames and unavailable intervals. A slowed replay adds no capture samples.

## Gate for accepting a metric 3D result

Require two synchronized views of the same interval with enough overlap and verified scale. Validate pool geometry against held-out landmarks and report coverage per race phase. Quantitative 3D results are pending that evidence. The broadcast alone is a reference for phase labeling and possible image-plane tracking.


## Underwater viewer requirement

Show a shaded, semi-transparent water surface fixed in pool coordinates.
Keep the athlete and tracked landmarks legible on both sides of the surface
during entry and breakout. Use the same plane in 3D, side and overhead views.
Expose a visibility toggle for inspection. If the surface height is estimated,
label it as estimated and keep it separate from the pose prediction.


## Broadcast review

Use the player interval 3:17–3:36 for acquisition review. At 3:22 the
swimmers are set on the blocks. At 3:26 the broadcast shows an underwater
side view with a race clock near 3.5 s. At 3:34 it shows an overhead view
with surfacing swimmers and a race clock near 11.4 s. These are player
time cues, with no verified frame-accurate start or 25 m crossing.

The cut from the starting blocks to underwater and then overhead changes
viewpoint. The underwater shot shows multiple swimmers at different
apparent depths. Lane 4 identity needs to be checked per shot before
extracting keypoints. The opening broadcast interval can be used to
annotate observable motion, with separate per-shot tracks. Simultaneous
view overlap and the pool-fixed 25 m plane remain unverified.
