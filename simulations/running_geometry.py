"""Idealized running geometry sensitivity. Run with Python 3 and NumPy."""
import numpy as np

rng = np.random.default_rng(204)
n = 2000
focal = 1500.
target = np.array([0., 0., 1.])
hip = np.array([0., 0., 1.05])
knee = np.array([.12, 0., .63])
ankle = knee + np.array([-.18, 0., -.37])
points = np.array([hip, knee, ankle])
points = points + rng.uniform([-1, -.5, -.05], [1, .5, .05], size=(n, 1, 3))
velocity = np.array([[5, 0, 0], [6, 0, .5], [8, 0, 1.]])

def angle(p):
    u, v = p[:, 0] - p[:, 1], p[:, 2] - p[:, 1]
    u, v = u[:, [0, 2]], v[:, [0, 2]]
    c = (u*v).sum(-1)/(np.linalg.norm(u, axis=-1)*np.linalg.norm(v, axis=-1))
    return 180 - np.degrees(np.arccos(np.clip(c, -1, 1)))

def run(azimuth, px, ms, deg):
    matrices, observations = [], []
    for az in np.radians(azimuth):
        c = np.array([10*np.sin(az), -10*np.cos(az), 2.])
        z = target-c
        z /= np.linalg.norm(z)
        x = np.cross(z, [0, 0, 1])
        x /= np.linalg.norm(x)
        y = np.cross(z, x)
        r = np.array([x, y, z])
        skew = rng.normal(0, ms/1000, size=(n, 1, 1))
        q = (points + velocity*skew - c)@r.T
        uv = q[..., :2]/q[..., 2:] + rng.normal(0, px/focal, size=(n, 3, 2))
        theta = rng.normal(0, np.radians(deg), size=n)
        yaw = np.zeros((n, 3, 3))
        yaw[:, 0, 0] = yaw[:, 2, 2] = np.cos(theta)
        yaw[:, 0, 2] = np.sin(theta)
        yaw[:, 2, 0] = -np.sin(theta)
        yaw[:, 1, 1] = 1
        rr = yaw@r
        p = np.concatenate([rr, -(rr@c)[..., None]], axis=-1)
        matrices.append(uv[..., None]*p[:, None, 2:3, :] - p[:, None, :2, :])
    a = np.concatenate(matrices, axis=2)
    _, _, v = np.linalg.svd(a, full_matrices=False)
    xyz = v[..., -1, :3]/v[..., -1, 3:]
    pos = np.linalg.norm(xyz-points, axis=-1)*1000
    err = np.abs(angle(xyz)-angle(points))
    print(len(azimuth), px, ms, deg, *(round(x, 2) for x in (
        np.median(pos), np.quantile(pos,.95), err.mean(), np.quantile(err,.95))))

for az in ((-15, 15), (-45, 45), (-60, -20, 20, 60)):
    for px, ms, deg in ((1,0,0),(3,0,0),(3,2,.1),(3,10,.1)):
        run(az, px, ms, deg)
