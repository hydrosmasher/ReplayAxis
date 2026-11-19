# ReplayAxis thesis feasibility brief

19 November 2026 · Supervisor discussion draft · Research only

**Proposed thesis title:** ReplayAxis: Evidence-linked 3D sports replay and validation of a running knee-angle measurement

**Recommendation:** Scope the thesis to one controlled running measurement and its reproducibility. Use pre-bounce cricket flight as a transfer question with a separate evidence gate. Prior work supports the feasibility of the constituent techniques. Integrated accuracy and analyst benefit still need to be measured.

## Thesis question and contribution

**Primary question.** In a calibrated capture volume, how well does a markerless multicamera workflow estimate sagittal knee flexion at independently force-defined running initial contact, and can a reviewer reproduce a selected estimate from its recorded camera observations, calibration and processing decisions?

Report matched-time angle MAE, bias and usable-contact coverage against a qualified reference. Treat candidate event detection as a separately reported extension. For reproducibility, attempt offline regeneration of a selected result using an export with timestamps, camera and frame IDs, 2D observations, accepted or rejected view decisions, calibration revision, angle convention, configuration and software version. Freeze the numerical reproducibility tolerance and the scoring procedure before held-out evaluation. Document where comparators expose equivalent evidence. This is a candidate integration and evaluation contribution. Novelty and patent scope remain open.

## Evidence by capability

| Capability | What prior evidence demonstrates | Proposed place in the thesis |
|---|---|---|
| Markerless 3D reconstruction | Calibrated views establish geometric observability under adequate visibility and non-degenerate geometry. Pose2Sim shows controlled running precedent. Competition long jump shows that fast capture can still produce poor agreement on discrete endpoints. [Triangulation](https://doi.org/10.1006/cviu.1997.0547) · [Pose2Sim](https://doi.org/10.3390/s22072712) · [Long jump](https://pmc.ncbi.nlm.nih.gov/articles/PMC10796501/). | Primary validation, with one movement, one anatomical convention and an independent event. Report where the method withholds a measurement. |
| Spatial replay | Sports free-viewpoint reconstruction and Canon's mixed-reality basketball demonstration establish that selectable viewpoints can be presented. Canon's report is vendor evidence for viewing capability. [Grau et al.](https://freeviewpointvideo.co.uk/Publications/Papers/Grau06IBC.pdf) · [Canon](https://global.canon/en/news/2026/20260925.html). | Define the evidence presentation around the measured trajectory and synchronized views. Photorealistic volumetric rendering is optional later work. |
| Measurement provenance | Anipose combines video and keypoints. Visual3D presents synchronized video and motion capture. Patent material describes camera-linked event metadata and structured exports. [Anipose](https://pmc.ncbi.nlm.nih.gov/articles/PMC8498918/) · [Visual3D](https://wiki.has-motion.com/doku.php?id=visual3d%3Adocumentation%3Adialogs%3Aprocessing_video_in_visual3d) · [US12627844B2](https://patents.google.com/patent/US12627844B2/en). | Walk an identical measurement through the closest comparator. Evaluate whether a reviewer can regenerate the result and identify unsupported estimates. |
| Spoken and gestural interaction | Voice with spatial pointing has precedent. A sports XR study shows that visible interpretations can help inspection, while correction remained incomplete. [Bolt](https://doi.org/10.1145/800250.807503) · [Lee et al.](https://arxiv.org/abs/2608.00876). | Use the JARVIS inspiration as a design direction. Any later interaction experiment should test whether users can verify and correct a selected athlete, body part or event, with matched information available in the baseline. |
| Forecasting beyond observation | Sports-agent forecasting has probabilistic precedent. Different futures can share the same observational history. [MoFlow](https://openaccess.thecvf.com/content/CVPR2025/html/Fu_MoFlow_One-Step_Flow_Matching_for_Human_Trajectory_Forecasting_via_Implicit_CVPR_2025_paper.html). | Future research. Separate offline gap filling from causal forecasts, report uncertainty by horizon, and compare with simple baselines. Keep forecast output visibly distinct from measured or reconstructed evidence. |

## Decision path for a funding proposal

| Decision | Current evidence | What moves it forward |
|---|---|---|
| Can the knee endpoint be tested with existing data? | **Investigate.** BioCV has calibrated 200 Hz video, marker tracks and force data. Video-to-marker alignment may use paired LEDs or a median correction. The archive requires access approval. | Confirm eligible running contacts, angle convention and per-trial alignment. Compare at the force-defined time first and report own-event error separately. [BioCV audit](biocv-timing-and-ball-data-audit.md). |
| Can ball accuracy be established with existing data? | **Investigate.** Tennis research shows an independent optical comparison design. The screened sources have not yielded a reusable cricket dataset with an independent 3D airborne reference. | Require synchronized views and independently calibrated 3D reference through the same visible pre-bounce interval. Otherwise retain cricket as a transfer feasibility discussion. [Endpoint protocols](endpoint-validation-protocols.md). |
| Are error and coverage sufficient for a coaching decision? | **Open.** Existing geometry and timing figures are illustrative sensitivity allocations. | Elicit the minimum useful change, measure reference uncertainty and freeze error and coverage rules before held-out scoring. Require confidence bounds to meet the prespecified limits. [Capture envelope](analytical-capture-envelope.md) · [Threshold worksheet](threshold-worksheet-and-reference-checklist.md) · [Decision table](preregistration-decision-table.md). |

A defensible funding request would identify the endpoint, use case, qualified reference or collection design, capture volume, and error sources that dominate within that volume. The first budget should target the measurement and reference requirements. A spatial display question can be assessed after the measurement and interaction tasks are defined.

## Supervisor decisions

1. Is the primary contribution the measurement-validation study, the reproducibility workflow, or both with one designated primary?
2. Is controlled running an acceptable first context? If BioCV alignment cannot be qualified, should the scope narrow to reference-timed angle agreement under documented timing strata, or move to another dataset?
3. Is cricket appropriate as a separate transfer question pending reference access?
4. Which coaching use case and independent reference would justify a later pilot and budget?

This brief synthesizes existing evidence and proposes a bounded scope. It is neither a systematic literature review nor a record of measured ReplayAxis performance.
