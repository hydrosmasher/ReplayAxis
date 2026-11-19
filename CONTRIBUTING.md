# Branching workflow

Keep `main` as the reviewed project baseline. Create short-lived branches from current `main` when work begins, open a pull request for each focused change, and merge it after review. Start new branches from the updated `main`.

| Branch | Scope | Start when |
|---|---|---|
| `research/prior-art` | Literature, competitor and patent evidence | First research pass |
| `research/capture-and-display` | Camera feasibility and rendering comparisons | Requirements are ready to compare |
| `feat/synthetic-benchmark` | Known-motion fixtures and numerical evaluation | Benchmark outputs and tolerances are defined |
| `feat/reconstruction` | Multiview pose and object tracks | Session contracts and baseline fixtures are ready |
| `feat/spatial-replay` | Playback and interaction | A usable replay bundle exists |
| `research/motion-forecasting` | Prediction baselines and evaluation protocols | Reconstruction baseline and ground truth are available |
| `build/distribution` | Release packaging and dependency inventory | The supported release targets are defined |

This repository is public. Use synthetic or appropriately licensed examples and keep athlete recordings, credentials and confidential research material out of the repository.
