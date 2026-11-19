# Research agenda

## Before hardware

- Compare free-viewpoint replay, markerless biomechanics, mixed-reality sports analytics and athlete/equipment tracking. Document closest academic papers, deployments, products and patent families. Record unverified product capabilities as unknown.
- Define the contribution to test: select a measurement in spatial replay, inspect the supporting source frames and estimate quality, then regenerate it using a versioned session package.
- Model camera synchronization, exposure, projected target size, coverage and occlusion. Test synthetic sprint and cricket trajectories with known ground truth. Compare capture requirements for football, swimming, figure skating and skiing separately.
- Compare desktop baseline, headset hand tracking, light field and swept-volume displays. Test gesture command semantics in software before evaluating sensor accuracy and display readability.
- Specify local-first packaging, versioned data contracts, synthetic regression fixtures, dependency and model licenses, and independent rebuild criteria. Discuss commercial IP and athlete data use with TU Dortmund before publication or recruitment.

## Future motion forecasting

Support two tasks explicitly: reconstructing temporarily unobserved motion within a recording and forecasting beyond the last trustworthy observation. Record the observation cutoff, forecast horizon, model version, predicted alternatives and uncertainty. Retain observed and inferred data lineage during playback and export.

Start with constant-velocity and physics baselines. Later compare temporal ML and DL models using masked views and held-out future segments with reference trajectories. Split data by athlete and session to reduce leakage, stratify evaluation by sport and motion phase, and measure position, joint-angle and event-timing errors alongside uncertainty calibration. Track failure after external events such as a deflection, landing or push-off, and suppress forecasts when evidence is insufficient or uncertainty is too high. Forecast accuracy and supported horizons remain research outcomes.
