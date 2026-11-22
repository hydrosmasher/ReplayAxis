# Underwater rotation check

See the [manual audit](underwater_manual_audit.md) for the labeling and scoring conventions. Run `check_rotation.py` with the same clip, model and notebook. Its optional `--labels underwater_rotation_holdout.csv` argument selects six newly labeled frames later in the same clip. Scores use confidence 0.55 before lifting.

| Input | Held-out wrist coverage | Wrist median error | Held-out shoulder coverage | Cap-visible head coverage |
| --- | ---: | ---: | ---: | ---: |
| Original | 2/4 | 194.1 px | 1/4 | 0/2 |
| Clockwise | 4/4 | 1,071.7 px | 4/4 | 1/2 |
| Counterclockwise | 4/4 | 21.2 px | 4/4 | 0/2 |

The later frames are from the same swimmer and clip. Counterclockwise rotation
was chosen on the earlier eight frames. The full replay with that rotation
had 300/356 partial or complete poses compared with 236/356 unrotated. Complete
poses fell from 37 to 15 and exported heads from 42 to 29. The results support
a wrist tracking improvement on this sample and leave the head unresolved.
The default remains unrotated. Use `reconstruct.py --rotation counterclockwise`
for reproducing the embedded case browser pilot.
