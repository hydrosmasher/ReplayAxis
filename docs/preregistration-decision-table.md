# ReplayAxis preregistration decision table

19 November 2026 · Research draft for review

This draft turns the [endpoint validation protocols](endpoint-validation-protocols.md) into decision rules. Numerical thresholds, sample-size targets and reference qualifications remain open. A pass applies to the prespecified endpoint, capture volume and population represented by the data.

## Freeze before scoring

| Input | Knee flexion at running initial contact | Visible pre-bounce cricket ball position | Evidence owner |
|---|---|---|---|
| Intended use and minimum useful difference | Define the coaching decision and smallest useful change in angle. Decide whether own-event timing is required. | Define the decision and the smallest useful spatial difference over the flight segment. | Coach or intended analyst, documented by study lead |
| Primary error limit | Upper bound for matched-time absolute angle error. Add a separate timing and end-to-end angle limit if own-event use is in scope. | Upper limit for 95th percentile Euclidean error in each prespecified flight bin. | Study lead and domain expert, justified against intended use |
| Coverage and minimum information | Minimum proportion of reference contacts scored and minimum independent athletes and eligible contacts. | Minimum coverage in each bin plus minimum independent deliveries and eligible opportunities per bin. | Study lead with intended users; sample size based on pilot precision |
| Reference qualification | Maximum admissible angle and alignment uncertainty, with force-event definition and anatomical convention frozen. | Maximum admissible 3D reference and alignment uncertainty, with a separate calibration and registration check across the scored volume. | Reference-system operator or data custodian, supported by measured checks |
| Evaluation rules | Freeze athlete partition, event pairing, angle definition, interpolation rules, missing-data handling and estimators. | Freeze delivery partition, eligible volume and timestamps, early/middle/late bins, interpolation limits and continuity rules. | Study lead before held-out evaluation |

Suggested knee primary statistic is MAE at force-defined contact, with per-athlete reporting and clustered uncertainty. Ball primary statistic is the 95th percentile distance within each flight bin, with delivery-clustered uncertainty. Freeze aggregation weights, interval method and confidence level before scoring. Treat all required flight bins as a joint gate and account for uncertainty across those bins when making a single pass claim. Pilot and tune on different athletes or deliveries from those used for final evaluation.

## Decision rules

| Gate | Pass | Investigate | Stop the claim |
|---|---|---|---|
| Reference readiness | Access permits the intended use, the independent reference covers the endpoint, and measured uncertainty meets the prespecified limit. | Access, uncertainty, or alignment metadata are unresolved but could be verified. Isolate timing strata and run sensitivity checks. | Reference remains inaccessible, lacks independence for the claim, or cannot satisfy the reference budget after the planned checks. Continue only as a diagnostic or narrow the endpoint and start a new evaluation. |
| Knee matched-time angle | Upper confidence bound for the primary error is at or below its limit and lower confidence bound for coverage is at or above its minimum. | Error or coverage interval crosses its limit, or the planned sample lacks enough independent athletes. | With a qualified reference and adequate data, the lower confidence bound for error exceeds the limit, or the upper confidence bound for coverage falls below its minimum. |
| Knee own-event use, if required | Timing and end-to-end angle meet their own error and coverage gates in addition to matched-time agreement. | Alignment sensitivity makes it unclear whether disagreement comes from detection, reference timing or the angle estimate. | A required own-event gate clearly fails. A separately passed matched-time result only supports review at a known contact time. |
| Ball phase-specific accuracy and coverage | Error and coverage confidence bounds meet their limits in every prespecified required bin. | A bin is underpowered, has unresolved reference gaps, or crosses either threshold. | A required bin clearly fails either bound with adequate reference and data. Keep any narrower phase claim conditional on a separate prespecified evaluation. |

Use all reference-eligible contacts or timestamps as the coverage denominator, including candidate misses and withheld estimates. Calculate error on matched results and present it with coverage. Report reference attrition separately. Lock decision rules before held-out results are viewed and record any subsequent changes as exploratory. A pass supports considering a scoped validation or funding step. It does not validate general deployment.

## Current status

**Knee: investigate.** BioCV is a strong candidate. Access, trial-level synchronization evidence, and qualified contact counts are pending. The 2 ms figure in the earlier sensitivity study is an illustrative allocation, not an acceptance threshold. [BioCV audit](biocv-timing-and-ball-data-audit.md).

**Ball: investigate, with the independent accuracy claim gated.** No eligible reusable cricket reference has been identified in the scan. Synthetic and shared-view reference data remain useful for sensitivity work. The prior 15 mm depth and 8 mm timing figures are modeled components, not tolerances for 3D flight. [Capture envelope](analytical-capture-envelope.md).

**Next research step.** Draft a short threshold-elicitation worksheet with example coaching decisions for each endpoint and a separate reference uncertainty checklist. Leave numbers open until supported by domain judgment or measurements.
