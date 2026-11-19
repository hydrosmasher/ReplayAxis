# Work done to date

Status snapshot · 19 November 2026

ReplayAxis is at the research and software feasibility stage. The proposed thesis focuses on running knee flexion at force-defined initial contact and whether a selected measurement can be independently reproduced from its recorded evidence.

| Area | Completed work and where to find it |
|---|---|
| Prior art | Mapped academic, commercial and patent precedents for reconstruction, spatial replay, interaction, forecasting and measurement provenance. See the [prior-work brief](prior-work-feasibility.md), [comparator walkthrough](comparator-walkthrough.md), and [spatial-assistant literature](spatial-assistant-literature.md). |
| Feasibility | Documented published performance and limitations, modeled geometry and timing sensitivity, and defined what the running and cricket endpoints would require. See the [evidence matrix](feasibility-evidence-matrix.md), [error budget](pre-hardware-error-budget.md), and [capture envelope](analytical-capture-envelope.md). |
| Data and validation | Identified BioCV as a controlled running candidate and examined its timing and access restrictions. Screened ball-flight datasets and defined both validation protocols, decision gates and threshold elicitation. See the [dataset audit](biocv-timing-and-ball-data-audit.md), [protocols](endpoint-validation-protocols.md), [decision table](preregistration-decision-table.md) and [threshold worksheet](threshold-worksheet-and-reference-checklist.md). |
| Synthetic benchmark | Built deterministic camera-consensus and error-sensitivity experiments, including timing, calibration, localization noise and alternative camera policies. Added a seven-frame evidence viewer, trajectory gaps, selectable camera groups, frame comparisons and text/JSON exports. See the [benchmark folder](../research/benchmark/) and [sample analysis notebook](../research/benchmark/compare_camera_decisions.ipynb). |
| Thesis framing | Wrote a supervisor-facing proposal that distinguishes the primary measurement study, cricket transfer question, spatial and spoken interface, and forecasting. See the [thesis feasibility brief](thesis-feasibility-brief.md). |
| Papers | Organized research links, naming and reuse status in the [paper catalog](../research/papers/). PDF acquisition and redistribution review remain pending. |

The software checks established deterministic synthetic behavior and simulated interactions. Live browser behavior and real-athlete accuracy remain unverified. BioCV access and trial-level timing, an independent cricket reference, numerical acceptance limits, novelty and analyst benefit remain open. No new capture or hardware purchase was part of this checkpoint.
