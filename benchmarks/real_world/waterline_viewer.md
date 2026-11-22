# Waterline in the 3D viewer

The notebook's replay export accepts an optional horizontal water surface.
Supply it only with registered pool-space poses. The current viewer uses Y
as the vertical axis (positive down), with X and Z running along the plane.
For pool coordinates with Z positive up, convert both the pose and surface
to the viewer's convention before exporting.

```python
export_view(
    frames, "Registered swimming replay", "swimming_replay", rate=25,
    water_surface={
        "y": 0.0,
        "x_bounds": [0.0, 25.0],
        "z_bounds": [-1.25, 1.25],
        "estimated": False,
    },
)
```

The bounds above are illustrative. The surface is a translucent reference
plane drawn behind the athlete and annotations. It stays in world coordinates
while the pose animates or the view orbits. At an edge-on angle it appears
as a line. The Waterline checkbox toggles the plane, and estimated planes
carry an explicit label. Exports with no water surface preserve the existing
controls and behavior.

This renders a supplied surface. The [London 2012 case](01_phelps_butterfly_start.md)
still needs a pool-registered pose and a verified surface position.
