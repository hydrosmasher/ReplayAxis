# Pool-surface calibration

Run `python tools/pool_surface.py frame_landmarks.json --tolerance-m 0.2`
with OpenCV and NumPy. Use a tolerance justified by annotation uncertainty
and the intended measurement. The command reports held-out errors in metres
and withholds its mapping if any check exceeds the supplied tolerance.

The input JSON contains `frame_id`, `anchors` and `checks`. Each anchor
and check has `pixel: [u,v]` and `pool_m: [along_lane,across_pool]`.
Use at least four noncollinear fit landmarks and two independently labeled
check landmarks from the water surface, with visible features around the
region of interest. Coordinates are in one image frame. Optional
`surface_points` entries have `id` and `pixel`. Only points within the
fit landmark footprint are mapped. Keep a stable convention for lane
direction and origin, such as metres from the start wall.

Calibrate each moving-camera frame independently or validate explicitly
that a mapping can be carried between frames. Only apply it to points that
lie on the water surface. Do not treat a cap above or below that plane
as an exact surface point. The shaded viewer waterline can use the same
pool frame, with the plane at z = 0 when that convention is adopted.

A synthetic geometry check recovered the 25 m line to numerical precision,
rejected a displaced held-out landmark, and rejected a point beyond the
anchor footprint. The London 2012 footage has not yet supplied verified
metric landmarks. No 25 m crossing, waterline registration, or speed has
been measured from that footage.


## Bracket a 25 m crossing

Pass a JSON array of per-frame calibration objects to:

```sh
python tools/pool_crossing.py sequence.json --point-id cap --line-m 25 --tolerance-m 0.2
```

In each object, add a strictly increasing integer `frame_id`, real
presentation time `time_s` in seconds, and a nonempty `shot_id` shared
only by consecutive frames in the same shot. Use a stable point ID and
include it only when the landmark represents the water surface. Along-lane
coordinates must increase toward the finish. The tool brackets a forward
crossing using the last point below and first point above the line's
tolerance band. It does not interpolate a timestamp or infer one across
missing frames, failed calibration or camera cuts. The tolerance band is
a caller-selected margin, not a statistical confidence interval.

Synthetic checks cover the bracket and rejection cases. The two London
overhead samples remain approximate screen points with no calibrated
pool coordinates or exact frame timestamps, so no race time is reported.
