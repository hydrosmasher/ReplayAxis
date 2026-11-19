# BioCV access and timing audit, and ball-flight reference search

19 November 2026 · Research only

## BioCV documentation audit

- **Access.** The [University of Bath archive](https://researchdata.bath.ac.uk/1258/) provides access on request with explicit terms. It describes research-purpose use and restricts redistribution. Participant archives are typically about 15 GB each. The archive is the source of record for access terms. No request, download or redistribution was performed in this pass.
- **Manifest.** The [data paper](https://doi.org/10.1038/s41597-024-04077-3), Data Records and Table 5, describes 15 participant TAR archives, a calibration update, and missing-marker notes. Trial folders contain per-camera video and marker files. The paper describes raw and processed marker C3Ds and event CSVs in frame and seconds forms. Verify actual analog force channel availability, sample rate, units and sample indexing in a primary running trial after access. Video-only secondary trials cannot support the reference angle comparison.
- **Timing.** The nine video cameras shared a hardware frame trigger, also routed to Qualisys. The authors nevertheless found inconsistent end-of-recording delays and used paired visible/IR LEDs to correct video-to-marker alignment. When the LED was unavailable, they used a median end-frame correction and visual verification. Force was recorded in Qualisys Track Manager and synchronized to marker data within that system. This preserves the distinction between camera-to-camera agreement and video-to-reference alignment. The documented correction procedure supplies no verified per-trial bound at the proposed 2 ms allocation.
- **Interpretation.** At 200 Hz the video interval is 5 ms. Selecting the nearest regularly spaced video sample alone can leave up to 2.5 ms of quantization, before residual alignment error. At the earlier illustrative 450 degrees/s this corresponds to about 1.13 degrees. Interpolating a continuous angle estimate at a force-defined instant may help with sample-grid effects. It does not remove unknown offsets.

### Trial intake after authorized access

Start with one primary running archive and the calibration update. Check trial identifiers, camera frame counts and timestamp interpretation, raw and processed marker units, event CSV agreement, force plate mapping and whether the LED correction method is recorded per trial. Compare an LED-aligned trial and any median-corrected trial as separate timing strata if identifiable. Record missing markers, dropped frames and whether a force-defined single-foot contact lies inside the common camera volume. If per-trial alignment is not identifiable, use BioCV for controlled angle and timing sensitivity and withhold a sub-2-ms evidence claim.

## Expanded fast-ball data search

| Candidate | What it supplies | Fit for pre-bounce 3D validation |
|---|---|---|
| [Calandre et al. table-tennis study](https://ailb-web.ing.unimore.it/icpr/media/posters/12025.pdf) | 29 real sequences, two synchronized 240 fps cameras and stereo-triangulated 3D positions. The estimator is monocular. | Best documented substitute found for testing a monocular method against stereo. It is a table-tennis precedent, and the stereo result is not a third-system independent reference for a stereo estimator using those same images. Reusable raw files, license and position uncertainty were not verified. |
| [MUVY](https://pmc.ncbi.nlm.nih.gov/articles/PMC13333307/) | User-generated multi-view sports scenes including cricket, grouped by event. | Candidate for qualitative visibility and viewpoint diversity. No independent airborne 3D ball reference was identified in the documentation screened. |
| [SpinDOE](https://cogsys-tuebingen.github.io/spindoe/) | Dataset and method for spin estimation from a patterned table-tennis ball. | Useful spin and tracking precedent. The project page does not establish the independent metric 3D flight reference needed here. |
| [Eassom et al. tennis protocol](https://doi.org/10.1177/17543371251381488) | Simultaneous commercial tracking and Vicon in a shared court volume. | Strong design precedent for independent comparison with aligned optical tracks. Raw data are unavailable for reuse according to the journal. |

The screened sources do not establish a reusable independent cricket reference spanning visible pre-bounce flight. Look for datasets and supplementary material from ball-tracking, sports engineering and vision robotics groups. Record frame-level synchronization, calibration and usable overlap, reference independence, uncertainty, licensing and event coverage before ranking them.

**Next research step.** Draft the two endpoint validation protocols from the evidence now available, including a BioCV timing sensitivity plan and a substitute-data versus independent-reference decision for ball flight. Keep quantitative hardware and procurement gates provisional until those checks are supported.
