# ReplayAxis threshold worksheet and reference checklist

19 November 2026 · Research only · Draft for elicitation

Use one completed worksheet per endpoint and intended use. The examples are discussion prompts. Numerical thresholds remain open. Transfer justified limits to the [preregistration decision table](preregistration-decision-table.md) before viewing held-out results.

## 1. Elicit what the measurement would change

| Prompt | Running knee flexion at initial contact | Pre-bounce cricket ball position |
|---|---|---|
| Example decision | A coach decides whether a runner changed knee flexion after a technique cue and whether to keep the cue. | A bowling coach decides whether a delivery's visible path moved enough toward a planned line to change the next drill. |
| Scope to record | Athlete population, speed range, strike pattern, side, angle convention and whether the comparison uses a known contact time or ReplayAxis detection. | Delivery type, speed range, capture volume, early/middle/late phases and the direction of change that matters. |
| Smallest useful difference | What angular change in degrees would change your decision? Does this apply to one contact or an average across repeated contacts? | What spatial change in millimetres would change your decision, along which direction and during which phase? |
| Consequences of error | What would happen if a real change were missed, or if the display implied a change that did not occur? | What would happen if the display moved the path to the wrong side of a target line? Would an uncertain trajectory be more useful if visibly flagged or withheld? |
| Coverage | How many eligible contacts can be withheld before feedback becomes unreliable? Are misses near particular foot-strike patterns more consequential? | How many eligible positions can be withheld per phase? How long can a contiguous gap be before interpretation breaks down? |

Use paired examples at several candidate differences, including unchanged cases, without revealing the nominal difference initially. Use simulated or consent-cleared materials. Record each person's decision, rationale and uncertainty before discussing discrepancies. Capture who was consulted, date, role, exact task, and any disagreement. A coach's directional decision may justify an additional directional outcome. Keep that separate from the original 3D error gate and specify it before evaluation.

## 2. Record the limits with their owners

| Field | Value to fill | Required basis |
|---|---|---|
| Minimum useful difference and decision context | ___ | Coach or intended analyst responses and example tasks |
| Maximum primary error, statistic and units | ___ | Study lead's justification relating the metric to the intended decision |
| Minimum coverage and longest usable gap, if applicable | ___ | Intended workflow, separately for required flight phases |
| Own-event timing and end-to-end limits, if applicable | ___ | Intended use and observed angle sensitivity to timing |
| Maximum independent reference uncertainty | ___ | Allocation justified against the primary error limit and documented measured uncertainty |
| Sample size, interval method, decision-rule version | ___ | Pilot precision and planned athlete- or delivery-level analysis |
| Approver, source, freeze date and unresolved assumptions | ___ | Study record before held-out scoring |

A minimum useful difference and a maximum measurement error are distinct quantities. In particular, a comparison of two trials introduces uncertainty from both estimates and any shared bias. Record how the proposed limits protect the intended decision. Keep the illustrative values in the [capture envelope](analytical-capture-envelope.md) as sensitivity examples.

## 3. Qualify the independent reference

Mark each item **verified**, **pending**, or **fails**, and cite the file, measurement, or protocol that supports it.

- [ ] **Scope and access.** Intended analysis is permitted, relevant motions and speeds are covered, and required raw data and timing metadata are available.
- [ ] **Independence.** List any shared observations, calibration targets, alignment inputs or model assumptions. Evaluate what errors could be shared; references that reuse the candidate views cannot independently validate those views.
- [ ] **Repeatability.** Repeat reference measurements or use an appropriate check artefact across the scored volume and relevant speed conditions. Record the number of repetitions, spread, spatial bias and uncertainty method.
- [ ] **Spatial registration.** Fix units, coordinate systems and transform. Measure residuals at independent check points spanning the near, far and edge regions. Record the transform and its version.
- [ ] **Temporal alignment.** Record exposure timestamp convention, sampling rates, trigger/clock mapping, drift and residual timing uncertainty. Document interpolation support and gaps. Estimate alignment without optimizing on scored samples.
- [ ] **Running endpoint.** Verify force channel and force-defined initial contact, side assignment, marker-derived anatomical convention and alignment stratum. Separate LED-verified, median-corrected and unknown trials where possible, and document supported timing precision before testing own-event performance. [BioCV audit](biocv-timing-and-ball-data-audit.md).
- [ ] **Ball endpoint.** Verify an independent 3D ball-centre reference across visible pre-bounce samples in the shared volume. Document overlap, reference uncertainty and gaps for each predeclared flight phase. [Endpoint protocol](endpoint-validation-protocols.md).

**Decision record.** Record the intended claim, status, evidence owner, missing inputs and resolution for each endpoint. Keep the status at investigate when evidence is pending. Use the preregistration decision table when a reference check fails or when confidence bounds can be evaluated.

**Next research step.** Build the thesis feasibility brief around the decision table, use cases and unresolved evidence, with separate evidence for reconstruction, spatial playback, spoken interaction and forecasting.
