# Endpoint-matched validation evidence

19 November 2026 · Research only

This targeted pass asks for markerless sagittal knee flexion at the instant of initial contact, and independent 3D ball-position error split by flight phase. It supplements the [pre-hardware error budget](pre-hardware-error-budget.md). Search terms combined running, markerless, knee flexion, initial contact, force plate, ball trajectory, Vicon, and flight phase. This is a scoping pass using accessible papers and abstracts.

| Source | What matches | What remains unresolved |
|---|---|---|
| [Van Hooren et al., 2023](https://doi.org/10.1111/sms.14319) | Compares DeepLabCut and OpenPose sagittal running kinematics against a marker-based reference at 2.78 and 3.33 m/s. | The retrieved evidence establishes a running comparator at these speeds. It does not establish a speed-matched initial-contact error for the proposed ReplayAxis workflow. Extract any event-specific estimates separately from waveform errors. |
| [de Borba et al., 2026](https://doi.org/10.1123/jab.2026-0021) | OpenCap versus marker-based motion capture during treadmill running and walking. Abstract describes sagittal angle waveforms, range of motion, and spatiotemporal variables. | The abstract does not furnish the required initial-contact knee-angle error. Agreement on the whole waveform or range of motion cannot fill that cell. |
| [High-speed running point-of-contact IMU validation, 2024](https://doi.org/10.3390/s24175718), Table 1 and discussion | Exact event and sagittal knee-angle outcome during running at 12–18 km/h. Uses force-plate timing and an optoelectronic comparator. Reports overestimation of knee flexion exceeding 7° for the tested IMU system. | The sensor modality differs. Use the event and comparison design, not the reported error as a camera-based requirement or expected result. |
| [Eassom et al., tennis ball trajectory validation](https://doi.org/10.1177/17543371251381488), public abstract and data statement | Simultaneous commercial tracking and Vicon, followed by space/time alignment. Mean spatial separation 36.8 mm, with greater separation mid-flight than near landing. | Exact phase-specific magnitudes and reference repeatability could not be verified from accessible material. The journal reports that raw data cannot be shared. The overall separation cannot serve as a cricket tolerance or as the reference system's uncertainty. |
| [Sanders, cricket tracking](https://drpaulfelton.com/wp-content/uploads/2022/08/2019-sanders-factors-affecting-performance-in-elite-finger-spin-bowlers.pdf), §3.4 | Documents real match tracking with six 340 Hz cameras and describes how ground contact can occur between samples. | Provides a capture precedent. Independent phase-specific position error remains unverified. Bounce timing and contact location need separate validation from visible pre-bounce position. |

## Consequence for the proposed feasibility envelope

The numerical limits in the earlier error budget stay provisional. Neither a waveform-wide knee error nor overall inter-system tennis separation supplies a defensible acceptance limit for the chosen endpoint.

- **Running.** Compare candidate and reference angles at the same force-defined contact timestamp to isolate angle disagreement. Report the candidate system's own contact-timing error separately, then report end-to-end angle error at its own detected event. Keep speed, foot-strike pattern, and anatomical angle convention explicit. Report bias, per-athlete agreement and usable-contact coverage.
- **Ball.** Define pre-bounce phase bins in reference time before evaluation. Preserve clearly visible early-, mid-, and late-flight samples and publish counts and withheld coverage in each bin. Use independently verified spatial and temporal alignment, with estimated alignment and reference uncertainty. Score 3D vector error and absolute distance separately. Bounce prediction and line-call error are distinct outcomes.
- **What would justify an upper bound.** An agreed minimum useful difference for a specific decision, a repeatable independent reference, and endpoint-matched agreement measured in a representative volume. An error reported in another sport, modality or motion phase is a sensitivity scenario.

## Next research decision

Convert the provisional geometry and timing inputs into an analytical capture envelope for representative distances and subject speeds. Attach a reference-readiness checklist to each endpoint and label acceptance thresholds as pending. Continue citation chaining for endpoint-matched optical studies and look for licensable synchronized reference data with documented uncertainty.
