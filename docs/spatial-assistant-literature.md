# ReplayAxis spatial assistant — second literature pass

19 November 2026 · Research branch · Software-only design

## Interaction reference

Use the JARVIS scenes in Iron Man as an interaction reference for ReplayAxis: analysts speak while pointing, the scene changes in response, and an assistant can explain what is on screen. ReplayAxis retains its own identity, voice and interface. Public-facing descriptions should use “multimodal spatial sports-analysis assistant.”

**Target interaction.** The analyst points at an athlete's knee and says “Compare this at landing with the previous trial.” ReplayAxis highlights the selected athlete, anatomical side, metric, event and reference trial before drawing an aligned overlay. “Show your evidence” reveals the source frames, accepted and rejected 2D observations, and the calculation that produced the comparison. If landing is uncertain, show the supported candidates and offer a direct correction. If footage ends, show any forecast as a distinct, optional layer once forecasting is validated.

## Papers and design consequences

| Source | What it contributes | ReplayAxis implication and next step |
|---|---|---|
| [Bolt, Put-That-There, SIGGRAPH 1980](https://doi.org/10.1145/800250.807503) | Combines pointing and speech to ground references in spatial graphics. | Resolve “this” with the pointing target at the time it was uttered. Test mismatched speech and pointing, competing joints, and stale selection. |
| [Srinivasan et al., DataBreeze, IEEE TVCG](https://pubmed.ncbi.nlm.nih.gov/32149639/) | Combines speech and direct manipulation for flexible data exploration. | Use speech for semantic tasks such as comparing trials. Use direct input for spatial selection and precise scrubbing. Route both through the same operations and test handoff between modalities. |
| [Narechania et al., NL4DV, IEEE TVCG](https://pubmed.ncbi.nlm.nih.gov/33048704/) | Converts natural-language data questions into analytic specifications and demonstrates ambiguity interfaces. | Parse object, metric, time/event, comparison and desired display into a typed action. Test the mapping independently of speech recognition or any language model. |
| [Lee et al., Who’s That Player?, IEEE VIS 2026](https://study.ieeevis.org/year/2026/program/content/a6a811db-f906-4dea-bae8-5a160321102e/) | Closest interaction precedent. XR soccer system exposes how spoken references about entities, locations, time and metrics were resolved. Its 16-person study reported improved inspectability on most measured dimensions, while repair occurred in only 38% of misaligned externalization trials. | Add direct correction next to each inferred field, such as “left knee → right knee” and “first landing → final landing.” Test both whether users notice a mismatch and whether they repair it. Voice-controlled sports XR alone is established. |
| [Lin et al., The Ball Is in Our Court](https://pubmed.ncbi.nlm.nih.gov/37022362/) | Sports visualization design lessons from working with different groups of sports experts. | Study biomechanics analysts and coaches separately from the athletes whose motion appears in the viewer. Pilot tasks with realistic time pressure and ambiguous footage. |
| [Cordeil et al., IATK, IEEE VR 2019](https://digital.library.adelaide.edu.au/items/93e8dc6c-b596-429c-bf83-ac1ad4dea8ab) | Immersive analytics authoring and exploration toolkit implemented in Unity. | Use as an implementation precedent for coordinated views and spatial charts. Keep the first prototype desktop-based and evaluate whether the 3D scene needs an embedded trajectory, a separate plot, or both. |
| [Karashchuk et al., Anipose, Cell Reports 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8498918/) | Combines calibration, filtering and a visualization of source video, tracked keypoints and annotations. Substantive overlap with the ReplayAxis evidence-view concept. | Add Anipose to the comparator walkthrough. Check direct metric-to-observation links, rejected observations, saved calibration and the ability to independently reproduce a selected measurement. |
| [Callahan et al., VisTrails, SIGMOD 2006](https://sci.utah.edu/~csilva/papers/sigmod2006.pdf) | Scientific workflow provenance for reproducible visualizations. | Store a replayable record of input identifiers, processing parameters, operation history and results. Verify that a clean environment can regenerate a chosen metric and plot. |
| [Ingwersen et al., Two Views Are Better than One, CVPR Workshops 2025](https://openaccess.thecvf.com/content/CVPR2025W/CVSPORTS/papers/Ingwersen_Two_Views_Are_Better_than_One_Monocular_3D_Pose_Estimation_CVPRW_2025_paper.pdf) | Studies multiview consistency in pose estimation and evaluates on SportsPose. | Candidate for later sparse-view evaluation. Start with deterministic calibrated triangulation, then quantify the effect of losing views before testing learned methods. |
| [Zhu et al., MotionBERT, ICCV 2023](https://openaccess.thecvf.com/content/ICCV2023/papers/Zhu_MotionBERT_A_Unified_Perspective_on_Learning_Human_Motion_Representations_ICCV_2023_paper.pdf) | Learns temporal motion representations using 2D-to-3D lifting. | Consider for pose reconstruction when observations are incomplete. Future unobserved motion requires a separate causal forecasting benchmark with withheld ground truth. |

## Software-only prototype and evaluation

1. **Specify the command vocabulary.** Begin with play/pause, seek to event, select joint or object, compare two trials, show evidence, and correct selection. Represent an action with explicit trial, object, anatomical side, time or event, measurement definition and a reference trial where applicable.
2. **Make interpretation visible.** Show the resolved action before comparison. Give ambiguous fields an immediate correction affordance. Compare text-only, simulated pointing plus text, and the same interface with the interpreted action exposed. In later hardware trials, match task, display and information access across controller and gesture modes.
3. **Bind explanations to measurements.** Calculate metrics in the analysis engine. The assistant reports values, units, observation identifiers and quality flags returned by that engine. Distinguish command ambiguity from measurement uncertainty. Use scripted responses before adding a language model so either part can be evaluated independently.
4. **Construct a ground-truth scenario.** Use two synthetic landings, a wrong-side distractor and one camera with a corrupted knee observation. Record which interpretation should occur and whether the analyst corrects an intentionally wrong one. A second scenario with a projectile tests the same action and evidence format on a different kind of track.
5. **Record outcomes.** Log correct intent resolution, correction rate conditional on a wrong interpretation, task time, and error detection. Separately score independent metric reproduction to a declared tolerance. Assess gesture accuracy and speech recognition under realistic conditions later.

## Decision triggers and next literature pass

- If showing the interpreted action improves detection but people rarely correct it, prioritize one-step repair and compare with the interpretation-only design.
- If users can verify the metric but independent reproduction fails, make the missing inputs explicit before expanding spatial interaction. If Anipose or another comparator already implements the full workflow, test measurable reviewer benefits or narrow to cross-sport portability.
- Once the typed actions and evidence record work with synthetic tracks, evaluate speech input and a conventional desktop 3D view. Specialist displays and athlete recording remain deferred.
- Search IEEE VIS, ACM CHI/UIST and IEEE ISMAR for spoken XR analytics, ambiguous deixis, multimodal repair, sports replay and intelligibility. Follow citations from Lee et al. For the reconstruction lane, compare Anipose, OpenCap and Theia3D + Visual3D using one identical measurement task and explicitly flag unknown capabilities.

This is a targeted research pass. The prototype and its tests remain proposed. Public academic evidence does not settle worldwide novelty.
