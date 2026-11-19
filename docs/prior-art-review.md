# ReplayAxis prior-art review — first pass

**Date:** 19 November 2026  
**Scope:** Public academic full texts and abstracts, vendor documentation, and patent publications. This is a targeted scoping pass. It establishes overlap and defines the next searches. It does not establish worldwide novelty or freedom to operate.

## Question and proposed falsification test

Can an analyst select an individual 3D sports measurement, inspect the exact contributing 2D observations and rejected views, and regenerate the number from an export in a separate environment? Does this help the analyst identify a faulty measurement compared with synchronized video and 3D review alone?

The same evidence contract should cover a body joint and a fast object. A hand-controlled interface is a separate experimental variable. If an existing workflow performs this end to end, benchmark the difference in reproducibility or reviewer accuracy before claiming a contribution.

## Evidence matrix

| Evidence | Publicly documented capability | Implication and next action |
|---|---|---|
| [Grau et al., A Free-Viewpoint Video System for Visualization of Sport Scenes](https://journal.smpte.org/periodicals/SMPTE%20Motion%20Imaging%20Journal/116/5-6/14/) | Multicamera sports reconstruction and viewpoint changes, including visual-hull and view-dependent approaches. | Treat free-viewpoint sports replay as established. Extract visibility and rendering failures for the synthetic benchmark. |
| [Canon, 2026 MR demonstration](https://global.canon/en/news/2026/20260925.html) and [Arcturus Sports](https://arcturus.studio/page/sports/) | Canon demonstrated selectable volumetric MR views of basketball. Arcturus advertises interactive spatial replay with pause, rewind and viewpoint changes. Vendor evidence describes these capabilities. | Assess capture ingest and frame-level inspectability. Ask whether displayed measures are linked to reproducible metric computations. Public descriptions reviewed here leave that question open. |
| [Theia integration with Visual3D](https://www.has-motion.com/wiki/doku.php?id=visual3d%3Adocumentation%3Athird-party%3Atheia), [Visual3D synchronized video](https://wiki.has-motion.com/doku.php?id=visual3d%3Adocumentation%3Adialogs%3Aprocessing_video_in_visual3d), [SIMI Motion](https://www.zhaw.ch/en/engineering/institute-zentren/imes/infrastruktur/translate-to-en-ueberblick-ueber-alle-pruefmaschinen-messverfahren-und-laboreinrichtungen/translate-to-en-simi-motion) | Theia segment outputs can feed downstream motion analysis via C3D. Visual3D plays synchronized motion capture and video. | Closest lab comparator. Inspect whether a selected angle can reveal contributing camera observations, confidence after rejection, exact reference frame and the settings needed for independent reproduction. |
| [Cheng et al., VisCourt, UIST 2024](https://doi.org/10.1145/3654777.3676466) | Mixed-reality basketball tactics training includes movement-based playback and viewpoint control, with a user evaluation. | Spatial interaction for sport is established. Compare identical measurement tasks with standard controls and hand input. Preserve an additional synchronized 2D comparison with equivalent information. |
| [Cronin et al., competitive long-jump analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC10796501/) | Two 200 Hz views and OpenPose were compared with manual SIMI digitization. The study reported generally poor agreement for discrete outcomes. | Acquisition speed alone is insufficient. Compare event timing, joint-angle error, missing data, and failure at key phases separately. |
| [Uhlrich et al., OpenCap](https://pmc.ncbi.nlm.nih.gov/articles/PMC10586693/) | Validated estimation of kinematics and dynamics from smartphone footage for the tasks in that study. | Use as a validation-method reference. Track angles and timings separately because each requires a suitable reference and can fail differently. |
| [Ingwersen et al., SportsPose](https://openaccess.thecvf.com/content/CVPR2023W/CVSports/papers/Ingwersen_SportsPose_-_A_Dynamic_3D_Sports_Pose_Dataset_CVPRW_2023_paper.pdf) | 24 participants, seven hardware-synchronized views, 90 fps and 3D pose data. [Dataset access](https://christianingwersen.github.io/SportsPose/download.html) requires an application and license review. | Candidate body-motion benchmark. Check actual files, calibration and terms before use. Keep a fully synthetic baseline for independent reproduction and fast projectile testing. |
| [Fu et al., MoFlow, CVPR 2025](https://openaccess.thecvf.com/content/CVPR2025/papers/Fu_MoFlow_One-Step_Flow_Matching_for_Human_Trajectory_Forecasting_via_Implicit_CVPR_2025_paper.pdf) | Forecasts trajectories and evaluates on NBA SportVU among other datasets. | Sports trajectory prediction has precedent. Keep player trajectory, 3D articulated pose, and projectile forecasts separate. Defer model work until ground-truth coverage and leakage controls exist. |

## Patent triage

- [EP4327902A1, Sports metaverse](https://data.epo.org/publication-server/rest/v1.2/patents/EP4327902NWA1/document.pdf). Published European application. Claim 1 describes client-side neural rendering using previously fitted participant parameters and streamed positional and pose data from a live event. Review this family if a live photorealistic client renderer enters scope.
- [US12627844B2, Video-based analytics platform](https://patents.google.com/patent/US12627844B2/en). The description explicitly includes synchronized frame indexing, event confidence, camera-source identifiers and structured exports. That is material overlap with broad claims about evidence-linked replay. Record the distinction between disclosed embodiments and the issued claims. Before commercialization, map independent claims and verify territorial status and related family members in official registers. An independently reproducible measurement package is a research hypothesis, and offline processing alone does not settle legal scope.

## Search log and follow-up protocol

The first pass used public web searches on 19 November 2026 and opened the closest paper and patent evidence available. Representative query strings follow.

1. `sports 3D biomechanical analysis synchronized video joint angle Theia3D Visual3D Simi markerless evidence`
2. `VisCourt ACM 3654777 3676466 mixed reality basketball gesture training study`
3. `Canon 2026 volumetric video MR real-time sports Arcturus HoloSuite sports`
4. `EP4327902A1 sports metaverse US12627844B2 athlete equipment claims patents`
5. `SportsPose dataset official GitHub license non commercial download calibration sports pose Ingwersen`

For the next pass, rerun narrower queries in ACM DL, IEEE Xplore, PubMed, OpenAlex, Espacenet and USPTO. Search for `measurement provenance`, `video overlay`, `manual correction`, `reprojection error`, `kinematic uncertainty` and `reproducible biomechanics` independently. Follow citations from OpenCap, Visual3D-related studies and the identified patents. Deduplicate by DOI or patent family and log inclusion criteria, dates, full-text access, and unresolved claims.

## Next steps and decision triggers

| Sequence | Task | Decision it informs |
|---|---|---|
| 1 | Document one reference walkthrough for Theia3D + Visual3D, SIMI and OpenCap from manuals, papers and public demos. Check camera evidence, accepted/rejected views, uncertainty, provenance export and independent recalculation. Record undocumented features as unknown. | If an existing workflow covers the full task, narrow the thesis to reviewer error detection or cross-sport portability and test that directly. |
| 2 | Define a measurement contract containing source frame IDs, synchronized timestamps, 2D points and residuals, camera calibration, units, algorithm/version, filtering settings and quality flags. | Decide whether measurements can be reproduced without vendor software. |
| 3 | Prototype a deterministic synthetic test with one moving body joint and one projectile. Compare clean data, camera skew, occlusion and calibration error. Record error against known truth and export exact contributing inputs. | Validate the theory and identify which capture specifications actually constrain accuracy. |
| 4 | Identify permitted real datasets and record camera geometry, capture rates, reference quality and licenses. | Decide whether a software-only validation can address each task or whether later lab capture is necessary. |
| 5 | Compare display and gesture paths once the measurements and reviewer tasks are defined. | Decide whether hand input or a specialist display merits a later evaluation. |

Hardware and participant recording remain deferred. In later forecasting work, evaluate withheld in-recording gaps separately from future predictions after the last observation. Report performance by forecast horizon before deciding which estimates to show.
