# ReplayAxis endpoint validation protocols

19 November 2026 · Research draft

This draft follows the [BioCV and ball-data audit](biocv-timing-and-ball-data-audit.md) and [capture envelope](analytical-capture-envelope.md). The protocols define measurements and analysis. Performance and acceptance thresholds are pending.

## Protocol A — Sagittal knee flexion at running initial contact

**Question.** How much disagreement arises from estimating the angle at the reference contact time, and how much does the candidate's own event timing add?

1. **Qualify trials.** Use primary BioCV running trials with synchronized video, marker trajectories and a usable single-foot force-plate contact inside the surveyed common volume. Log calibration version, side, available cameras, missing markers, video/marker/force rates, clock mapping and alignment method. Tag LED-confirmed, median-corrected and unknown alignment separately when distinguishable. Check use terms through the [Bath archive](https://doi.org/10.15125/BATH-01258).
2. **Define the reference event.** Map analog force time to the marker and video clocks. Before comparing outcomes, freeze the vertical-force threshold, persistence rule, baseline correction and event-pairing window. Log the threshold and filter delay. Confirm the correct limb and resolve simultaneous or ambiguous contacts independently of candidate outputs. Retain candidate misses in coverage counts. The [BioCV data paper](https://doi.org/10.1038/s41597-024-04077-3) documents the trigger, LED alignment and fallback.
3. **Match the angle.** Use the same sagittal angle convention, anatomical definitions, side and sign. Record whether the candidate or reference needs interpolation, and keep interpolation inside bracketed valid observations. Explicitly label geometric landmark angles if an anatomical match cannot be established. Freeze filtering settings before evaluating the held-out sample.
4. **Report the decomposition.** For force-defined contact time t_ref and candidate contact time t_est, calculate timing error t_est − t_ref. Matched-time angle error is θ_est(t_ref) − θ_ref(t_ref). The timing-induced shift in the candidate series is θ_est(t_est) − θ_est(t_ref). Their event-level angle terms add to the end-to-end error θ_est(t_est) − θ_ref(t_ref); their aggregate absolute errors do not necessarily add. Report matched-time coverage and end-to-end coverage separately.
5. **Test alignment sensitivity.** Recalculate matched-time error at symmetric offsets of ±1, ±2 and ±5 ms where interpolation is supported. These are sensitivity scenarios, not estimated BioCV alignment errors. Stratify by alignment method and report by athlete and speed where available. Quantify repeatability and avoid treating repeated strides as independent when estimating agreement. [Bland and Altman on repeated measurements](https://pubmed.ncbi.nlm.nih.gov/17613642/).

## Protocol B — Visible pre-bounce cricket ball position

**Question.** How closely does a candidate system locate the ball centre throughout the visible pre-bounce interval of a bounded, calibrated volume?

1. **Qualify the reference.** Require raw synchronized candidate views plus a separately calibrated, time-aligned 3D ball-centre reference through the shared volume. Document reference precision, timing residuals and spatial registration using independent checks. Assess the reference at relevant speeds and positions. A radar speed estimate can corroborate velocity, while a court-plane landing label can benchmark landing. Neither supplies airborne XYZ. Use the simultaneous optical comparison in [Eassom et al.](https://doi.org/10.1177/17543371251381488) as a protocol precedent.
2. **Freeze the comparison.** Define the eligible capture volume, pre-bounce start/end, inclusions and visibility criteria from reference or independent annotations. Define early/middle/late bins as thirds of a predetermined pre-bounce interval in reference time. Record observed overlap per bin. Determine transforms and timing offsets from calibration or alignment checks and lock them before evaluating the scored deliveries. Interpolate only within supported reference intervals, with a documented maximum gap. Keep occluded, out-of-volume, missed, and excluded samples auditable.
3. **Score and report.** At eligible reference timestamps, compute signed XYZ differences in a documented coordinate system and Euclidean position error for matched estimates. Report bias per axis, median and 95th percentile distance, and coverage per bin. In addition to visibility counts, count reference-eligible opportunities withheld by the candidate, and report candidate visibility exclusions relative to the full reference interval. Summarize by delivery and account for repeated frames when reporting uncertainty. Record timing and registration sensitivity without extrapolating past bounce.
4. **Grade substitutes.** Synthetic trajectories with exact truth test modeling sensitivity. Stereo-derived labels can benchmark monocular estimates or aid diagnostic checks. If candidate and reference share the same observations or calibration errors, record that dependence. A performance claim about real metric 3D flight requires the independent reference above. The previous audit did not identify one available to ReplayAxis.

## Decision before collection or analysis

Fix the minimum useful difference, acceptable error, required coverage and reference uncertainty before evaluating held-out trials. Document empirical evidence and sensitivity assumptions separately. For BioCV, dataset access and trial-level timing checks remain pending. For cricket, a suitable reusable reference or an independently instrumented collection design remains pending.

**Next research step.** Turn these protocols into a preregistration-ready decision table with explicit pass, investigate and stop criteria. Track which thresholds need coach input or an independent reference uncertainty estimate.
