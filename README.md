# ReplayAxis

Research and software for gesture-controlled 3D sports motion analysis. ReplayAxis will link measurements to synchronized camera evidence and support reproducible analysis across sports.

## Project handoff

- [Work done to date](docs/work-done.md) summarizes the research, feasibility studies and synthetic benchmark.
- [Next work and checkpoints](docs/next-milestones.md) lists the research steps and their completion criteria.
- [Final project goals](docs/final-goals.md) defines thesis and longer-term outcomes.

Start with the [thesis feasibility brief](docs/thesis-feasibility-brief.md) for supervisor discussion. The [synthetic benchmark](research/benchmark/) includes the evidence view and sample notebook.

## Project phases

1. **Research and software feasibility.** Review prior art, products and patents. Model camera timing, exposure and geometry. Compare spatial displays, software licenses and distribution options. Validate the design with synthetic motion and appropriately licensed datasets.
2. **Evidence-linked replay.** Reconstruct timestamped body, ball and equipment tracks. Provide synchronized source views, confidence flags and exports. Validate measurements by sport and task before making support claims.
3. **Motion forecasting.** Evaluate ML and deep learning to estimate plausible motion beyond the observed time window or capture volume. Compare with simple kinematic and sport-specific physics baselines. Report error and uncertainty by forecast horizon, sport and event. Keep out-of-view estimates and forecasts visually distinct from evidence-backed reconstruction.

Hardware procurement, installation, and athlete capture are deferred pending the research and software feasibility review. Athlete studies and commercial release require separate validation and applicable permissions.

See [the research agenda](docs/research-agenda.md) and [branching workflow](CONTRIBUTING.md).
