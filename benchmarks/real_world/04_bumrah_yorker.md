# Case 04 — Jasprit Bumrah bowls Ollie Pope

India vs England, second Test, Visakhapatnam, day two (3 February 2024).
The dismissal is logged at 27.5 in England's first innings.

- [Footage and event report](https://www.wisden.com/series/england-in-india-2023-24/cricket-news/jasprit-bumrah-destroys-ollie-popes-stumps-with-lethal-reverse-swinging-yorker)
- [Ball-by-ball record](https://mlb.cricbuzz.com/player-match-performance/match/78635/player/11691/batting?inningsId=2)
- [Match report](https://www.bbc.co.uk/sport/cricket/68171311)

## Reconstruction protocol

Track the bowler and the ball independently. Include the batter for occlusion
and context. Mark the release bracket (last frame in hand to first frame
separate), the pitch contact bracket if visible, and first stump contact.
Leave frames unobserved when the ball is hidden or blurred beyond annotation.

Start with 2D tracks on a continuous, real-time broadcast angle. Preserve
frame timestamps and flag cuts, slow motion and replay duplicates. If a
second angle covers the same delivery, establish matching timing before
using it for triangulation. Pitch markings and stump geometry can constrain
the camera estimate. A ground-plane mapping alone cannot recover the
height of the airborne ball.

The 3D ball path, swing displacement and metric release speed require
validated timing, camera geometry and uncertainty estimates. A
single-angle fit may be shown as an estimate with its assumptions.
There are no measured trajectories or speed estimates for this case yet.
