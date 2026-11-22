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
