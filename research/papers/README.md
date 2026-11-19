# Research paper archive

Use `YEAR_FirstAuthor_ShortTitle.pdf` for local filenames. The [catalog](catalog.json) records 22 sources, including one alternate version of Anipose. Direct PDF URLs are included when identified. Landing pages can link to author manuscripts or require authorized access. A license field indicates the article's verified redistribution license. An empty license entry means public redistribution has not been cleared. Public reading access, the article PDF license, software licenses and dataset terms are separate.

| Filename | Source | Public redistribution |
|---|---|---|
| `2023_Uhlrich_OpenCap.pdf` | [PDF](https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1011462&type=printable) | CC BY 4.0 |
| `2024_Cronin_OpenPose_Long_Jump.pdf` | [PDF](https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2023.1298003/pdf) | CC BY 4.0 |
| `2021_Pagnon_Pose2Sim_Part_1_Robustness.pdf` | [PDF](https://www.mdpi.com/1424-8220/21/19/6530/pdf) | CC BY 4.0 |
| `2022_Pagnon_Pose2Sim_Part_2_Accuracy.pdf` | [PDF](https://www.mdpi.com/1424-8220/22/7/2712/pdf) | CC BY 4.0 |
| `2026_Lee_Whos_That_Player.pdf` | [PDF](https://arxiv.org/pdf/2608.00876) | Review needed |
| `2024_Cheng_VisCourt.pdf` | [PDF](https://yulingyun.com/wp-content/uploads/2025/02/Cheng_2024_VisCourt.pdf) | Review needed |
| `1980_Bolt_Put_That_There.pdf` | [PDF](https://www.media.mit.edu/speech/papers/1980/bolt_SIGGRAPH80_put-that-there.pdf) | Review needed |
| `2023_Ingwersen_SportsPose.pdf` | [PDF](https://openaccess.thecvf.com/content/CVPR2023W/CVSports/papers/Ingwersen_SportsPose_-_A_Dynamic_3D_Sports_Pose_Dataset_CVPRW_2023_paper.pdf) | Review needed |
| `2025_Ingwersen_Two_Views_Are_Better_Than_One.pdf` | [PDF](https://openaccess.thecvf.com/content/CVPR2025W/CVSPORTS/papers/Ingwersen_Two_Views_Are_Better_than_One_Monocular_3D_Pose_Estimation_CVPRW_2025_paper.pdf) | Review needed |
| `2023_Zhu_MotionBERT.pdf` | [PDF](https://openaccess.thecvf.com/content/ICCV2023/papers/Zhu_MotionBERT_A_Unified_Perspective_on_Learning_Human_Motion_Representations_ICCV_2023_paper.pdf) | Review needed |
| `2025_Fu_MoFlow.pdf` | [PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Fu_MoFlow_One-Step_Flow_Matching_for_Human_Trajectory_Forecasting_via_Implicit_CVPR_2025_paper.pdf) | Review needed |
| `2006_Callahan_VisTrails.pdf` | [PDF](https://sci.utah.edu/~csilva/papers/sigmod2006.pdf) | Review needed |
| `2006_Grau_Free_Viewpoint_Sports.pdf` | [PDF](https://freeviewpointvideo.co.uk/Publications/Papers/Grau06IBC.pdf) | Review needed |
| `2024_Wu_4D_Gaussian_Splatting.pdf` | [PDF](https://openaccess.thecvf.com/content/CVPR2024/papers/Wu_4D_Gaussian_Splatting_for_Real-Time_Dynamic_Scene_Rendering_CVPR_2024_paper.pdf) | Review needed |
| `2019_Iskakov_Learnable_Triangulation.pdf` | [PDF](https://openaccess.thecvf.com/content_ICCV_2019/papers/Iskakov_Learnable_Triangulation_of_Human_Pose_ICCV_2019_paper.pdf) | Review needed |
| `2020_Karashchuk_Anipose_Preprint.pdf` | [PDF](https://www.biorxiv.org/content/10.1101/2020.05.26.117325v1.full.pdf) | Review needed |
| `2021_Karashchuk_Anipose.pdf` | [Article page](https://pmc.ncbi.nlm.nih.gov/articles/PMC8498918/) | Review needed |
| `2021_Srinivasan_DataBreeze.pdf` | [Article page](https://pubmed.ncbi.nlm.nih.gov/32149639/) | Review needed |
| `2021_Narechania_NL4DV.pdf` | [Article page](https://pubmed.ncbi.nlm.nih.gov/33048704/) | Review needed |
| `2019_Cordeil_IATK.pdf` | [Article page](https://digital.library.adelaide.edu.au/items/93e8dc6c-b596-429c-bf83-ac1ad4dea8ab) | Review needed |
| `2023_Lin_The_Ball_Is_in_Our_Court.pdf` | [Article page](https://pubmed.ncbi.nlm.nih.gov/37022362/) | Review needed |
| `2024_Simultaneous_In_Air_And_Underwater_Swimming_Kinematics.pdf` | [Article page](https://www.sciencedirect.com/science/article/pii/S0021929024001556) | Review needed |

## Local download

From the repository root on this branch, run:

```sh
python3 research/papers/download.py ~/Downloads/ReplayAxis-papers
```

Append `--redistributable-only` to fetch just the four articles identified as CC BY 4.0. A publisher may require manual browser download. Verify the title and PDF integrity before committing a file and retain the original PDF intact, including copyright and license notices. The catalog supplies source attribution and filenames. Record byte size and SHA-256 for each archived copy once downloaded.

## Research update — reconstruction baseline

- [Pagnon et al., Pose2Sim Part 1: Robustness](https://doi.org/10.3390/s21196530) varies capture and processing conditions for walking, running and cycling. Use its camera-count and calibration perturbations to design separate synthetic failure modes for ReplayAxis.
- [Pagnon et al., Pose2Sim Part 2: Accuracy](https://doi.org/10.3390/s22072712) evaluates sports kinematics accuracy. Reuse the comparison idea at a small scale: one selected joint angle against a reference, with explicit error and event timing. Avoid transferring study accuracy to different movement or camera setups.
- [Iskakov et al., Learnable Triangulation](https://openaccess.thecvf.com/content_ICCV_2019/html/Iskakov_Learnable_Triangulation_of_Human_Pose_ICCV_2019_paper.html) provides a multiview learned comparator. Establish a deterministic baseline first. A learned method should earn its place by improving accuracy and retaining a usable record of the measurement's inputs.

**Next decision.** Compare Pose2Sim with Anipose, OpenCap and the Theia3D/Visual3D workflow using the same knee-angle scenario. If one already supplies the full evidence trail, prioritize a measurable assistant benefit such as faster correction of a wrong limb or detection of a bad camera contribution. If the gap persists, define the export contract and test independent recomputation on synthetic data.
