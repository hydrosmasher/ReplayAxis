"""Compare stature and scene-based torso scale in a controlled pinhole fixture."""
import json

import cv2
import numpy as np


def project(points, rotation, translation, camera):
    pixels, _ = cv2.projectPoints(points, rotation, translation, camera, None)
    return pixels.reshape(-1, 2)


def benchmark():
    rng = np.random.default_rng(20261122)
    camera = np.array([[960., 0, 640], [0, 960, 360], [0, 0, 1]])
    rotation = np.array([0.12, 0.25, 0.04])
    anchors = np.array([[-2., -1.5], [0, -1.5], [2, -1.5],
                        [-2, 1.5], [0, 1.5], [2, 1.5]])
    anchor_xyz = np.column_stack((anchors, np.zeros(len(anchors))))
    cases = []
    for distance in (5., 10.):
        translation = np.array([0., 0., distance])
        anchor_px = project(anchor_xyz, rotation, translation, camera)
        for offset in (0., 0.5, 1.5):
            errors = []
            for _ in range(200):
                truth = rng.uniform(0.45, 0.53)
                height_scale = 1.93 * 0.34
                x = rng.uniform(-1.4, 1.4)
                hip = np.array([x, 0.3, offset])
                shoulder = hip + truth * np.array([0.2, -np.sqrt(0.96), 0])
                joints_px = project(np.array([hip, shoulder]), rotation, translation, camera)
                # Estimation receives only scene dimensions and noisy image locations.
                homography, _ = cv2.findHomography(
                    anchor_px + rng.normal(0, 1, anchor_px.shape), anchors)
                noisy_joints = joints_px + rng.normal(0, 2, joints_px.shape)
                plane_joints = cv2.perspectiveTransform(noisy_joints[None], homography)[0]
                scene_scale = np.linalg.norm(plane_joints[1] - plane_joints[0])
                combined_scale = (height_scale + scene_scale) / 2
                errors.append(np.abs([height_scale - truth, scene_scale - truth,
                                      combined_scale - truth]))
            cases.append(dict(camera_translation_z_m=distance, plane_offset_m=offset,
                              trials=len(errors), mean_absolute_error_m=dict(zip(
                                  ("height_only", "scene_only", "equal_weight"),
                                  np.mean(errors, axis=0), strict=True))))
    return dict(seed=20261122, height_prior_m=1.93, torso_to_height=0.34,
                anchor_noise_std_px=1, joint_noise_std_px=2, cases=cases)


if __name__ == "__main__":
    print(json.dumps(benchmark(), indent=2, allow_nan=False))
