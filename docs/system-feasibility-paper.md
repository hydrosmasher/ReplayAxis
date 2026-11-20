# ReplayAxis feasibility paper

## System definition

ReplayAxis is a proposed voice- and gesture-operated spatial replay and analysis system for elite sports. It starts with recordings or derived data from camera systems already deployed at high-level competitions. Its output is a time-varying 3D replay that a human can pause, scrub, change viewpoint and inspect. A separate forecasting layer estimates plausible motion after an athlete or object is no longer observable. The analyst must be able to distinguish recorded views, reconstructed states, gaps and forecasts.

The first deliverable is a publishable feasibility paper covering financial, hardware and software capabilities and availability, including access to existing footage. The running knee-angle work is an illustrative measurement study within the wider project. The synthetic benchmark contributes evidence about reconstruction failure modes and traceability. It cannot establish venue-scale readiness.

**Working title:** ReplayAxis: Feasibility of Voice- and Gesture-Controlled 3D Sports Replay and Motion Forecasting from Existing Competition Cameras

**Central question:** Under which feed-access, camera-geometry, timing, computing, display and cost conditions can an existing elite-sport camera installation support a human-inspectable 3D replay and a separately qualified forecast after visibility ends?

## Evidence scenarios

| Input actually available | Initial paper assessment |
|---|---|
| Synchronized raw multiview ISO feeds with calibration and timestamps | Strongest candidate for reconstruction inside the observed overlap. Determine which views cover which athletes/objects, timestamp integrity, frame rate, exposure, resolution, lens calibration and accessibility. |
| Multiview feeds with incomplete metadata | Test whether calibration/synchronization can be recovered to task-specific tolerances before making metric claims. Scope to short, well-observed intervals. |
| Vendor 3D skeletal or object tracks | Can support an animated spatial replay if timestamps, coordinates and rights are sufficient. Assess provenance, uncertainty and source-video links separately. Photorealistic replay requires additional visual inputs. |
| Public switched or single-view broadcast | Useful for assessing availability, 2D analysis, or explicitly approximate 3D estimates. Camera cuts, hidden views and unknown calibration can make metric 3D underdetermined. Rights to access an asset, process it, publish derivatives and redistribute it should be tracked separately. |

Documented production anchors: [FIFA 2022 offside tracking](https://inside.fifa.com/en/innovation/world-cup-2022/semi-automated-offside-technology) describes 12 dedicated tracking cameras at 50 Hz and a separate ball sensor. [Sony's strategy presentation](https://www.sony.com/en/SonyInfo/IR/library/presen/strategy/pdf/2024/speech_E.pdf) describes animating Hawk-Eye skeletal information through Beyond Sports. [Canon's 2026 basketball demonstration](https://global.canon/en/news/2026/20260925.html) demonstrates selectable spatial viewpoints using a purpose-built volumetric and MR stack. [World Athletics high-jump biomechanics](https://worldathletics.org/download/download?filename=5ab60373-2030-4712-9efe-0b2985386bdd.pdf) documents five high-speed cameras and competition calibration. These are deployment precedents, not evidence that raw feeds or licenses are available to ReplayAxis. Check terms for the exact archive or event. [IOC archive-content example](https://www.olympics.com/ioc/faq/using-the-content-of-this-website/is-it-possible-to-use-the-content-texts-images-or-films-on-www-olympic-org).

## Paper methods and deliverables

| Workstream | Evidence to extract | Publishable output |
|---|---|---|
| Competition infrastructure and access | Separate competition, broadcast, officiating and dedicated volumetric feeds. Record operator, permissions status, fields of view, timing, geometry, export metadata and unknowns. | Deployment/access matrix and minimum eligible feed specification. |
| 3D reconstruction and rendering | Compare markerless skeletal replay, tracked-object trajectories and photorealistic volumetric replay. Extract errors, coverage, output reproducibility, GPU throughput and retained observation-level evidence. | Methods matrix with separate visual and metric claims. Use the existing knee and ball work as concrete validation cases. |
| Voice, gesture and display | Compare desktop control, headset MR with hand tracking, glasses-free light-field displays, and true volumetric display where supported. Compare modality, field of view, users, latency and integration. Define pause, scrubbing, viewpoint, measurement selection and a correction path for misunderstood commands. | Human-in-the-loop requirements and device capability table. Define “holographic” by the actual display modality. [Meta hand tracking](https://developers.meta.com/vr/documentation/unity/unity-handtracking-overview/) · [Looking Glass](https://checkout.lookingglassfactory.com/products/16-lightfield-display/). |
| After-camera forecasting | Distinguish retrospective interpolation using later observations from causal forecasting using only prior observations. Compare constant-velocity/physics baselines with learned probabilistic models. Score error, usable coverage, uncertainty calibration and horizon. | Forecast design and limits by sport and motion regime. Exact future motion is generally unobservable. [MoFlow sports-agent precedent](https://openaccess.thecvf.com/content/CVPR2025/html/Fu_MoFlow_One-Step_Flow_Matching_for_Human_Trajectory_Forecasting_via_Implicit_CVPR_2025_paper.html). |
| Financial feasibility | Model research setup, offline pilot, and venue-scale operation. Include feed/license charges, labor, GPU time, storage, transfer, display, SDK/support and any missing capture components. Check pricing, quote availability, region, currency, tax and date. | Low/base/high scenarios with formulas, one-time and recurring costs, and sensitivity to uncertain costs. Mark rights and vendor fees unknown until quoted. |

### Initial cost-model sanity check

For N encoded feeds at R megabits/s each and T hours, decimal ingest is approximately 0.45 × N × R × T GB, excluding overhead. An illustrative 12 feeds at 25 Mb/s each produce about 135 GB/hour. These bitrates are assumptions and do not describe the FIFA deployment. Compute cost depends on clip-hours times measured GPU-hours per clip-hour times the regional unit price. Storage, egress, engineering effort and permissions remain separate. [EC2 On-Demand pricing reference](https://www.aws.eu/ec2/pricing/on-demand/).

Use a dated search and extraction log covering academic papers, federation sources, vendor specifications and price pages. Tag each claim as measured, vendor-demonstrated, analytically modeled or unresolved. Report an evidence-based boundary for offline replay first. Live operation is a separate latency and cost scenario. An unpriced rights dependency stays unknown rather than being entered as zero.

## Completion criteria

The paper identifies which capabilities have been demonstrated, which existing input configurations plausibly support the proposed workflow, what those configurations would cost under stated assumptions, and what controlled validation is still required. The present document is a paper plan with preliminary evidence. Venue access, data reuse, end-to-end performance, forecasting accuracy and a priced deployment remain open.

Next research task: build the deployment and access matrix using World Athletics biomechanics, FIFA/Hawk-Eye and Canon as the first three documented cases, then connect each to an offline-pilot cost scenario.
