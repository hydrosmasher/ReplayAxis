# Independent camera checks in a synthetic sweep

Run the experiment with `python3 research/benchmark/capture_policy.py capture-policy.csv` from the repository root. Two runs produced identical CSV output in the tested environment.

The sweep compares three horizontal parallel-camera layouts, six input conditions and two eligibility policies across 20 paired noise seeds. The independent-check arm receives exact simulated timing and position errors for camera D. It removes D before reconstruction when either synthetic threshold is exceeded. These deliberately chosen thresholds and exact measurements model an idealized check, not deployed metrology or hardware acceptance criteria. Deterministic conditions repeat the same trajectory, while seeds change localization noise in stochastic conditions.

| Combined corruption | Ball coverage, residual only → independent check | Ball position MAE | Knee proxy MAE |
|---|---|---|---|
| Wide | 426/960 → 957/960 | 17.84 → 5.71 mm | 0.74 → 1.00° |
| Narrow | 426/960 → 957/960 | 66.74 → 20.31 mm | 2.81 → 3.99° |
| Asymmetric | 349/960 → 955/960 | 21.40 → 6.73 mm | 0.92 → 1.22° |

Combined corruption applies 0.5 ms skew and 5 mm camera position error to D plus 0.5 px localization noise across cameras. MAEs compare each policy's available estimates and can cover different frames. In the wide case, angle coverage increased from 913/960 to 952/960. The asymmetric layout's estimated speed MAE increased from 1.06 to 1.16 m/s while adjacent-pair coverage increased from 122/940 to 930/940. Metric-level comparisons are necessary.

Narrow and wide layouts had identical ball coverage under 1 px noise alone, but 28.75 mm versus 8.11 mm ball MAE. Residual agreement alone does not reveal how geometry amplifies position error.

## Next experiment

Replace exact external measurements with noisy estimates, track calibration and sync eligibility separately from reprojection decisions, and test soft weighting versus camera exclusion by track. Compare policies on common frames as well as reporting overall coverage. Add per-frame evidence for one misleading accepted observation and one withheld result so the assistant can explain both outcomes.
