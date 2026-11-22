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
