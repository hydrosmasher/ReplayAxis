# ReplayAxis: Feasibility of voice- and gesture-controlled 3D sports replay and motion forecasting from existing competition cameras

**Hrishikesh Karmalkar** · M.Sc. Data Science in Sports and Health, TU Dortmund University  
**Professor-review draft · 20 November 2026**

## Abstract

Elite competitions already use camera systems for broadcast, officiating, tracking, and biomechanics. This feasibility study asks which outputs from those systems could support an analyst-controlled spatial replay that also forecasts motion after observations end. We compare documented competition deployments, classify accessible inputs, and outline a reconstruction, interaction, and forecasting pipeline. We model resource and cost sensitivities for three deployment scales. The strongest candidate for auditable metric reconstruction is a short authorized interval with synchronized and calibrated multiview recordings. Provider tracks can support an animated replay where metadata and rights permit, while a switched broadcast imposes substantially weaker geometric constraints. Published immersive viewing demonstrations support the display concept, while research on spoken sports interaction motivates explicit correction of interpreted commands. Forecasts require separate causal evaluation and uncertainty reporting. The evidence supports a conditional offline pilot. Feed permissions, usable overlap, end-to-end performance, and a quoted budget remain open.

**Keywords:** sports biomechanics, multiview reconstruction, spatial replay, hand tracking, trajectory forecasting, feasibility

## 1. Introduction and research question

ReplayAxis is a proposed system that reuses video or tracking outputs from cameras already deployed at elite competitions. An analyst can pause, scrub, rotate the viewpoint, and inspect a measurement by voice, gesture, or conventional controls. A separate forecasting layer estimates plausible motion after an athlete or object is no longer visible to the usable cameras. The scene should show the distinction between recorded evidence, reconstructed motion, missing data, and predictions.

**Research question.** Under which feed-access, geometry, timing, software, display, and cost conditions could existing competition infrastructure support an auditable 3D replay and a separately validated forecast?

The contribution proposed here is a comparison of input-dependent capabilities, an explicit record linking displayed measurements to their source observations, and a feasibility evaluation plan. Free-viewpoint sports replay, multimodal interaction, and forecasting already have precedents. The paper treats their integration and evaluation as the candidate contribution.

## 2. Methods

This is a targeted feasibility study, using prior evidence assembled in the [technical brief](prior-work-feasibility.md), [evidence matrix](feasibility-evidence-matrix.md), and [reference-data review](reference-dataset-readiness.md), supplemented by competition operator reports and hardware documentation. Searches conducted through 20 November 2026 combined “sports free-viewpoint video”, “competition biomechanics high-speed camera”, “FIFA semi-automated offside tracking”, “mixed-reality sports spoken interaction”, “sports trajectory forecasting”, and “light-field display pricing”. Sources were selected for direct relevance to a system stage, a capture configuration, an empirical validation, or a cost input. Operator and vendor reports establish documented deployments or demonstrations. Peer-reviewed studies supply task-specific methods and results. Explicit assumptions are used for financial scenarios and analytical examples.

This review has no exhaustive screening or pooled estimates, and this draft reports no new competition, hardware or user-study results. Raw-feed access and prices without a public quote are treated as unresolved. Prototype evidence is restricted to synthetic software checks.

## 3. Existing infrastructure and access

| Deployment | Documented capability | Possible ReplayAxis input and access gap |
|---|---|---|
| London 2017 World Championships high-jump biomechanics [1] | Five high-speed cameras used for competition biomechanics, with calibrated measurement volumes. | A candidate for bounded post-event analysis if the operator can release original views, calibration, and timing. The public report establishes the setup. Raw archive access remains unconfirmed. |
| FIFA Qatar 2022 semi-automated offside [2] | Twelve roof-mounted tracking cameras record up to 29 points per player at 50 Hz. A separate ball sensor supplies data at 500 Hz. | Authorized timestamped player and ball tracks could drive skeletal replay. The deployment does not establish access to camera feeds, calibration, or officiating data. The ball sensor rate is distinct from camera frame rate. |
| Canon remote basketball demonstration [3] | Purpose-built volumetric capture delivered selectable viewpoints to mixed-reality viewers. | Strong presentation precedent for a dedicated venue stack. Generalization to ordinary broadcast cameras, access to underlying assets, and metrological accuracy remain unverified. |
| Hawk-Eye and Sony Beyond Sports [4] | Sony describes producing real-time 3D animation from in-game skeletal tracking. | Precedent for provider-track replay. Assess whether a specific partner can supply coordinate conventions, timestamps, quality outputs, and links to source views. |

Before a pilot, request a small authorized sample and document (i) the right to access it, (ii) permission to process it, (iii) permission to publish demonstrations or derived figures, and (iv) redistribution rules. These depend on the event and asset. The IOC archive guidance illustrates why public viewing does not settle research reuse [5]. No partner permission has been established here.

Four input tiers follow from this comparison:

1. **Calibrated and synchronized individual camera feeds.** Candidate for metric 3D within observed overlapping views. Record lens settings, timestamps, frame drops, exposure, coordinate calibration and different-camera visibility.
2. **Multiview footage with incomplete metadata.** Candidate for limited reconstruction after alignment and calibration checks. Report benchmark error before presenting metric 3D.
3. **Provider tracks.** Candidate for spatial animation with good timestamped track access. Pixel-level auditability depends on what the provider exposes.
4. **Switched broadcast or single view.** Candidate for 2D analysis and explicitly approximate 3D overlays. Camera cuts and hidden views can leave metric depth or motion unidentifiable.

## 4. Technical feasibility

### 4.1 Reconstruction and replay

A practical offline path is ingest → time and geometry calibration → athlete or object association → 2D estimation → 3D reconstruction → provenance export → human review. Triangulation depends on usable view separation and correctly matched observations [6]. For rectified stereo, depth is approximately focal length × baseline divided by disparity. The [analytical capture envelope](analytical-capture-envelope.md) shows that doubling depth under fixed assumptions quadruples first-order depth uncertainty. At 40 m/s, a 0.2 ms offset corresponds to 8 mm of physical travel. This is a motion scale whose effect on reconstruction depends on geometry.

First implement or evaluate a timestamped skeleton and ball trajectory with source views, model version, calibration version, estimator decisions and uncertainty. Compare measurement results with an independent reference. Treat photorealistic free-viewpoint video as a separate rendering track. Published sports free-viewpoint work and dynamic Gaussian reconstruction offer visual precedents [7, 8]. Rendering fidelity and biomechanical accuracy need different tests.

For an initial body-motion benchmark, estimate sagittal knee flexion at force-defined running initial contact. Use the same reference time for both estimates, then assess error from candidate event detection separately. BioCV documents synchronized video, markers, and force plates, but access and trial-level video-to-reference timing require verification [9]. For ball motion, assess position over independently referenced pre-bounce flight and report error and coverage by flight phase. The independent commercial-tracking versus Vicon tennis study is a protocol precedent. The cricket reference remains unresolved [10].

### 4.2 Human interaction and spatial display

The analyst needs pause, frame stepping, scrubbing, viewpoint changes, object or joint selection, and the ability to ask why a measure was withheld. Speech can carry semantic intent while pointing identifies a location. Every ambiguous command should expose the interpreted athlete, side, event and metric and offer an explicit correction. The spoken XR soccer study by Lee et al. reported improved inspectability on most measured dimensions, with repair in 38% of misaligned trials under visible interpretation [11]. This argues for measuring successful correction as a distinct outcome.

| Display path | Availability evidence | Evaluation role |
|---|---|---|
| Desktop 3D | Existing synthetic evidence viewer in this repository | Baseline for frame selection, uncertainty inspection, and measurement reproduction. |
| Headset mixed reality | Meta documents hand tracking in Unity [12]. | Personal spatial view. Measure command interpretation, gesture false activation, usability, and motion-to-display delay. |
| Glasses-free light field | Looking Glass lists a 16-inch unit at US$3,000, with availability requiring confirmation [13]. | Shared lab viewing. Verify viewing cone, label readability, multi-observer behavior, and external tracking integration. |

Use “spatial replay” as the platform-independent term. Specify the actual optical modality when discussing a holographic display. For an interaction study, compare matched evidence across desktop and spatial conditions, and isolate gesture effects by comparing hands with conventional controls on the same platform.

### 4.3 Forecasting after visibility ends

An offline reconstruction may use later observations to bridge a gap. A causal forecast may only use inputs at or before the forecast cutoff. Evaluate these separately, with a documented cutoff and no leakage across athletes, games, or deliveries. Start with constant velocity and sport-specific physics baselines, then compare a probabilistic sequence model where training data and scope permit. MoFlow provides a precedent for sports-agent trajectory forecasting on NBA data [14]. Articulated pose and fast-object flight require distinct evidence.

Report position or joint error by horizon, prediction coverage, interval calibration, and the frequency of withholding. Near impacts, unseen contact or a change in player intent can produce different futures from the same observed history. Show forecasts in a visually separate layer and state the horizon and uncertainty.

## 5. Financial feasibility

The model compares budgets for an existing desktop research setup, an offline multiview pilot, and an offline venue-scale study. It assumes reuse of installed cameras where suitable and separates capture access from compute. Given N feeds at R Mb/s for T hours, decimal ingest is about 0.45 × N × R × T GB. Divide total camera-feed hours from scene hours when profiling the actual pipeline. The GPU multiplier below is defined per scene-hour, with all input views included.

| Scenario | Feeds × Mb/s × scene hours | Ingest | Assumed GPU-hours per scene-hour | GPU-hours | Illustrative compute + one month of input storage |
|---|---:|---:|---:|---:|---:|
| Research clip | 4 × 15 × 0.5 | 13.5 GB | 4 | 2 | €3.34 |
| Offline pilot | 12 × 25 × 2 | 270 GB | 12 | 24 | €42.75 |
| Venue-scale study | 24 × 50 × 8 | 4,320 GB | 30 | 240 | €468.00 |

The last column uses assumed rates of €1.50 per GPU-hour and €0.025 per GB-month. These are sensitivity inputs, not provider quotes or measured performance. At half and double the assumed compute rate, the pilot subtotal becomes €24.75 and €78.75 respectively. Each additional retained copy adds storage, while training, rendering intermediates, requests, transfer, engineering, technical support, taxes, hardware, and rights are outside the subtotal. Egress and regional billing should be checked with the chosen provider [15]. The light-field list price is a separate USD hardware anchor. Its shipping, local tax, tracking equipment and integration are unresolved.

A funding-grade estimate requires partner terms or quotes and measured throughput for an authorized clip. Report one-time versus recurring costs. Unknown footage, SDK and support fees must remain explicit. Live replay would also require real-time throughput, latency targets, resilience, and a separate network and operations budget.

## 6. Feasibility judgment and validation gates

A short offline pilot is plausible if authorized ISO feeds or suitably documented tracks can be obtained. A claim of accurate 3D reconstruction from ordinary broadcast footage cannot be generalized across venues. A live, photorealistic, multi-sport system with dependable post-visibility forecasts remains an upper-scope research programme.

| Gate | Evidence needed |
|---|---|
| Feed eligibility | An authorized sample, timestamps and calibration or an independently checked recovery procedure, and adequate overlap for the selected task. |
| Metric validation | Prespecified matched-time error and coverage, a qualified independent reference, and one angle or position reproduced independently from its exported evidence. |
| Human review | Correct selection and correction of athlete, body part, or event, including inspection of disputed and withheld estimates. |
| Forecast | A causal holdout comparison with a simple baseline and measured uncertainty by horizon. |
| Budget | Partner quote or written access terms, measured processing time, dated display and compute quotes, and separate offline and live scenarios. |

The existing ReplayAxis benchmark demonstrates the mechanics of showing a camera-consensus decision, uncertainty gaps, and source observations in synthetic data. It motivates the evidence export without establishing competition accuracy. The immediate study should start with one bounded capture volume, one body-motion endpoint, and one reproducible replay example. Ball forecasting and wider spatial deployment can be qualified alongside this study once their reference data and access conditions are documented.

## References

1. World Athletics. [2017 World Championships men’s high-jump biomechanical report](https://worldathletics.org/download/download?filename=5ab60373-2030-4712-9efe-0b2985386bdd.pdf).
2. FIFA. [Semi-automated offside technology at Qatar 2022](https://inside.fifa.com/en/innovation/world-cup-2022/semi-automated-offside-technology).
3. Canon. [Real-time remote sports viewing through volumetric video and MR](https://global.canon/en/news/2026/20260925.html), 2026.
4. Sony Group. [Corporate Strategy Meeting FY2024 presentation](https://www.sony.com/en/SonyInfo/IR/library/presen/strategy/pdf/2024/speech_E.pdf).
5. IOC. [Use of Olympic website content](https://www.olympics.com/ioc/faq/using-the-content-of-this-website/is-it-possible-to-use-the-content-texts-images-or-films-on-www-olympic-org).
6. Hartley R, Sturm P. [Triangulation](https://doi.org/10.1006/cviu.1997.0547). Computer Vision and Image Understanding, 1997.
7. Grau O et al. [A free-viewpoint video system for visualisation of sport scenes](https://freeviewpointvideo.co.uk/Publications/Papers/Grau06IBC.pdf), 2006.
8. Lin Y et al. [Gaussian-Flow: 4D reconstruction with dynamic 3D Gaussian particle](https://openaccess.thecvf.com/content/CVPR2024/html/Lin_Gaussian-Flow_4D_Reconstruction_with_Dynamic_3D_Gaussian_Particle_CVPR_2024_paper.html). CVPR, 2024.
9. Evans M et al. [Synchronised video, motion capture and force plate dataset for validating markerless human movement analysis](https://doi.org/10.1038/s41597-024-04077-3). Scientific Data, 2024.
10. Eassom A et al. [Validation of spatiotemporal tennis ball trajectory tracking technology](https://doi.org/10.1177/17543371251381488), 2025.
11. Lee C et al. [Who’s That Player? Externalizing query interpretation in spoken XR sports interaction](https://arxiv.org/abs/2608.00876), 2026.
12. Meta. [Hand tracking overview for Unity](https://developers.meta.com/vr/documentation/unity/unity-handtracking-overview/).
13. Looking Glass Factory. [16-inch Light Field Display](https://checkout.lookingglassfactory.com/products/16-lightfield-display/).
14. Fu Y et al. [MoFlow: One-step flow matching for human trajectory forecasting](https://openaccess.thecvf.com/content/CVPR2025/html/Fu_MoFlow_One-Step_Flow_Matching_for_Human_Trajectory_Forecasting_via_Implicit_CVPR_2025_paper.html). CVPR, 2025.
15. Amazon Web Services. [S3 pricing](https://aws.amazon.com/s3/pricing/) and [EC2 On-Demand pricing](https://aws.amazon.com/ec2/pricing/on-demand/).
