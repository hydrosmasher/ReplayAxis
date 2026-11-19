"""Build a self-contained desktop-browser view of the synthetic evidence."""

import argparse
import json
from html import escape
from pathlib import Path

from benchmark import reconstruct
from explain_evidence import explain
from multiframe import FPS, project, scene


def observation_rows(observations, frame_ids):
    rows = []
    for view in observations:
        selected = view["frame_id"] in frame_ids
        marker = "In this group" if selected else "Outside this group"
        x, y = view["pixel"]
        residual = view.get("residual_px")
        residual_text = f"{residual:.3f}" if residual is not None else "Unavailable"
        values = (marker, view["camera_id"], view["frame_id"], f"{view['time_s']:.3f}",
                  f"{x:.2f}", f"{y:.2f}", residual_text, view.get("decision", "Unavailable"))
        cells = "".join(f"<td>{escape(str(value))}</td>" for value in values)
        style = ' class="selected"' if selected else ""
        rows.append(f"<tr{style}>{cells}</tr>")
    return "\n".join(rows)


def plot_observations(observations, frame_ids, scale_pixels=None):
    if not observations:
        return "<p>No pixel observations available.</p>"
    width, height, padding = 760, 280, 68
    pixels = scale_pixels if scale_pixels is not None else [view["pixel"] for view in observations]
    xs, ys = zip(*pixels)
    scale = min((width - 2 * padding) / max(max(xs) - min(xs), 1),
                (height - 2 * padding) / max(max(ys) - min(ys), 1))
    x_mid, y_mid = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    marks = []
    for view in observations:
        u, v = view["pixel"]
        x = width / 2 + (u - x_mid) * scale
        y = height / 2 + (v - y_mid) * scale
        frame = escape(view["frame_id"], quote=True)
        active = view["frame_id"] in frame_ids
        state = "included" if active else "excluded"
        description = escape(f"{view['frame_id']}, ({u:.2f}, {v:.2f}) px, {state}")
        label = escape(view["camera_id"])
        mark = (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="9"/>' if active else
                f'<rect x="{x - 8:.2f}" y="{y - 8:.2f}" width="16" height="16"/>')
        marks.append(f'<g class="{state}" data-frame="{frame}"><title>{description}</title>'
                     f'{mark}<text x="{x:.2f}" y="{y - 17:.2f}">{label}</text></g>')
    return f"""<figure class="camera-plot">
<svg viewBox="0 0 {width} {height}" role="img"
aria-label="Observed pixel coordinates on a shared image-coordinate scale">
<rect class="plot-area" x="45" y="20" width="690" height="220" rx="8"/>
<text class="axis-label" x="390" y="268">X increases right (px)</text>
<text class="axis-label" transform="translate(20 130) rotate(-90)">Y increases down (px)</text>
{"".join(marks)}
</svg>
<figcaption>Filled circles belong to the selected group. Outlined squares are outside it.
Each camera supplies its own image coordinates. The shared scale lets you compare membership.</figcaption>
</figure>"""


def render_case(index, case, answer, *, scale_pixels=None, title=None):
    result = case["result"]
    consensus = result["consensus"]
    groups = answer["camera_groups"]
    if answer["status"] != result["status"] or any(
            group not in consensus["candidates"] for group in groups):
        raise ValueError(f"Explanation differs from evidence for {case['case']}")
    title = title or {"biased_accepted": "Accepted position", "withheld": "Withheld position"}.get(
        case["case"], case["case"])
    margin = consensus["score_margin"]
    margin_text = str(margin) if margin is not None else "Unavailable"
    panels = []
    for group_index, group in enumerate(groups or [None]):
        group_id = f"case-{index}-group-{group_index}"
        frames = set(group["frame_ids"]) if group else set()
        if not frames.issubset(view["frame_id"] for view in result["observations"]):
            raise ValueError(f"Unknown source frame in {case['case']}")
        if group:
            label = escape("–".join(group["camera_ids"]))
            checked = " checked" if group_index == 0 else ""
            control = (f'<input type="radio" name="case-{index}" id="{group_id}"{checked}>'
                       f'<label for="{group_id}">{label} · {group["score"]} inliers</label>')
        else:
            control = ""
        rows = observation_rows(result["observations"], frames)
        plot = plot_observations(result["observations"], frames, scale_pixels)
        panels.append(f"""<div class="group">{control}
<div class="observations" tabindex="0">
{plot}
<table>
<caption>Source observations</caption>
<thead><tr><th>Membership</th><th>Camera</th><th>Frame ID</th><th>Time (s)</th>
<th>X (px)</th><th>Y (px)</th><th>Result residual (px)</th><th>Estimator decision</th></tr></thead>
<tbody>{rows}</tbody></table></div></div>""")
    return f"""<section aria-labelledby="heading-{index}">
<h2 id="heading-{index}">{escape(title)}</h2>
<p>{escape(answer["message"])}</p>
<dl><div><dt>Reconstruction status</dt><dd>{escape(result["status"])}</dd></div>
<div><dt>Consensus score margin</dt><dd>{margin_text}</dd></div></dl>
<fieldset><legend>Camera group</legend>{"".join(panels)}</fieldset></section>"""


def trajectory(cases):
    """Plot the estimated horizontal position without bridging missing frames."""
    positions = [case["result"]["point_m"] for case in cases]
    observed_x = [point[0] for point in positions if point is not None]
    if not observed_x:
        return "<p>No trajectory positions were reconstructed.</p>"
    lower, upper = min(observed_x), max(observed_x)
    if lower == upper:
        lower, upper = lower - 0.5, upper + 0.5
    first_time, last_time = cases[0]["time_s"], cases[-1]["time_s"]
    timespan = last_time - first_time or 1
    segments, marks = [], []
    previous = None
    for index, (case, point) in enumerate(zip(cases, positions)):
        x = 80 + 640 * (case["time_s"] - first_time) / timespan
        y = 155 if point is None else 145 - 120 * (point[0] - lower) / (upper - lower)
        if point is None:
            description = f"Frame {index + 1}: position withheld"
            marker = (f'<path class="gap" d="M{x-5:.2f} {y-5} l10 10 '
                      'm-10 0 l10 -10"/>')
            previous = None
        else:
            description = f"Frame {index + 1}: estimated X {point[0]:.3f} m"
            marker = f'<circle class="estimate" cx="{x:.2f}" cy="{y:.2f}" r="5"/>'
            if previous is not None:
                px, py, prior_index = previous
                segments.append(f'<line class="segment" data-from="{prior_index}" data-to="{index}" '
                                f'x1="{px:.2f}" y1="{py:.2f}" x2="{x:.2f}" y2="{y:.2f}"/>')
            previous = (x, y, index)
        active = " active" if index == 0 else ""
        pressed = "true" if index == 0 else "false"
        name = escape(description, quote=True)
        marks.append(f'<g class="trajectory-frame{active}" data-frame-index="{index}" '
                     f'role="button" tabindex="0" aria-label="{name}" aria-pressed="{pressed}" '
                     'aria-controls="timeline-frames">'
                     f'<title>{escape(description)}</title>'
                     f'<circle class="hit-target" cx="{x:.2f}" cy="{y:.2f}" r="18"/>'
                     f'<line class="cursor" x1="{x:.2f}" x2="{x:.2f}" y1="18" y2="167"/>'
                     f'{marker}<text x="{x:.2f}" y="188">{case["time_s"] * 1000:.1f}</text></g>')
    return f"""<figure class="trajectory">
<h3>Ball trajectory</h3>
<svg id="trajectory-plot" viewBox="0 0 760 220" role="group"
aria-label="Estimated horizontal ball position in metres over time, with withheld frames marked">
<rect class="plot-area" x="65" y="18" width="670" height="149" rx="8"/>
<text x="57" y="30" text-anchor="end">{upper:.2f}</text>
<text x="57" y="150" text-anchor="end">{lower:.2f}</text>
<text x="22" y="88" transform="rotate(-90 22 88)" text-anchor="middle">X (m)</text>
{"".join(segments)}{"".join(marks)}
<text x="400" y="211">Time (ms)</text>
</svg>
<figcaption>Select a point or cross to view its frame evidence. Crosses mark withheld frames. Their vertical placement does not represent a position.</figcaption>
</figure>"""


def timeline():
    """Render a scripted timing fault in a short synthetic ball sequence."""
    cameras = {"A": -2, "B": -1, "C": 1, "D": 2}
    calibration = {"focal_px": 1000, "inlier_threshold_px": 2}
    skews_ms = (0, 0.1, 0.5, 0.5, 1, 0.1, 0)
    cases = []
    for frame, skew_ms in enumerate(skews_ms):
        time_s = frame / FPS
        observations = []
        for camera, position in cameras.items():
            capture_time = time_s + (skew_ms / 1000 if camera == "D" else 0)
            pixel = project(scene(capture_time)["ball"], position, calibration["focal_px"])
            observations.append({"camera_id": camera, "camera_x_m": position,
                                 "frame_id": f"{camera}:{frame}", "time_s": time_s, "pixel": pixel})
        cases.append({"case": f"sequence-{frame}", "time_s": time_s, "skew_ms": skew_ms,
                      "result": reconstruct(observations, calibration, include_consensus=True)})
    shared_pixels = [view["pixel"] for case in cases for view in case["result"]["observations"]]
    panels = []
    options = []
    labels = []
    for frame, case in enumerate(cases):
        answer = explain(case)
        label = f"Frame {frame + 1} · {case['time_s'] * 1000:.2f} ms"
        result = case["result"]
        if result["status"] != "reconstructed":
            state = "Withheld"
        elif any(view.get("decision") == "rejected" for view in result["observations"]):
            state = "Reconstructed with a rejected view"
        else:
            state = "Reconstructed"
        labels.append(f"{label} · {state}")
        options.append(f'<option value="{frame}" label="{state}"></option>')
        panel = render_case(f"timeline-{frame}", case, answer, scale_pixels=shared_pixels, title=label)
        hidden = " hidden" if frame else ""
        panels.append(f'<div data-label="{labels[-1]}"{hidden}>'
                      f'<p>Simulated camera D offset: {case["skew_ms"]:g} ms</p>{panel}</div>')
    return f"""<div class="timeline" aria-labelledby="timeline-heading">
<h2 id="timeline-heading">Synthetic frame sequence</h2>
<label for="frame-scrubber">Frame</label>
<input type="range" id="frame-scrubber" min="0" max="{len(cases) - 1}" value="0"
list="frame-ticks" aria-describedby="frame-label">
<datalist id="frame-ticks">{"".join(options)}</datalist>
<output id="frame-label" for="frame-scrubber" aria-live="polite">{labels[0]}</output>
{trajectory(cases)}
<div id="timeline-frames">{"".join(panels)}</div></div>"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    cases = json.loads((directory / "assistant-evidence-cases.json").read_text(encoding="utf-8"))
    answers = json.loads((directory / "assistant-explanations.json").read_text(encoding="utf-8"))
    by_case = {answer["case"]: answer for answer in answers}
    sections = "".join(render_case(index, case, by_case[case["case"]])
                       for index, case in enumerate(cases))
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ReplayAxis evidence review</title>
<style>
:root {{color-scheme:dark;font:16px/1.55 system-ui;color:#e5edf8;background:#0b1220}}
body {{margin:0}} main {{max-width:1040px;margin:auto;padding:2rem 1rem}}
h1,h2,p {{margin:0 0 .7rem}} h1 {{font-size:clamp(2rem,5vw,3rem)}}
section {{background:#121e30;border:1px solid #324459;border-radius:12px;padding:1.25rem;margin:1.25rem 0}}
dl {{display:flex;gap:1.5rem;flex-wrap:wrap}} dt,caption {{color:#acbfd5}} dd {{margin:0;font-weight:600}}
fieldset {{border:1px solid #43546b;border-radius:8px;margin:0;padding:.8rem;min-width:0}}
.group {{display:contents}} label {{display:inline-block;padding:.3rem .6rem;margin-right:.5rem;cursor:pointer}}
input {{accent-color:#78e2db}} input:checked+label {{color:#8df6ed;font-weight:700}}
input:not(:checked)~.observations {{display:none}}
.observations {{overflow:auto;margin:.6rem 0}}
table {{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}}
caption {{text-align:left;margin:.2rem 0}}
th,td {{padding:.45rem .6rem;text-align:left;white-space:nowrap;border-bottom:1px solid #3b4a5c}}
.selected {{background:#153c43}} .selected td:first-child {{font-weight:700;color:#9ff8ef}}
.camera-plot {{margin:.7rem 0 1rem}} .camera-plot svg {{display:block;width:100%;height:auto}}
.camera-plot figcaption {{color:#acbfd5;font-size:.9rem}}
.plot-area {{fill:#0b1527;stroke:#43546b}}
.camera-plot text {{text-anchor:middle;fill:#e5edf8;font:600 16px system-ui}}
.camera-plot .axis-label {{fill:#acbfd5;font-size:14px}}
.timeline {{margin:1.4rem 0 2rem}} .timeline input[type=range] {{width:min(100%,24rem);vertical-align:middle}}
.timeline output {{display:block;font-weight:600;margin:.4rem 0 .75rem}}
.trajectory {{margin:.75rem 0 1rem}}
.trajectory h3 {{margin:0}}
.trajectory svg {{display:block;width:100%;height:auto}}
.trajectory figcaption,.trajectory text {{color:#acbfd5;fill:#acbfd5;font-size:14px}}
.trajectory text:not([text-anchor]) {{text-anchor:middle}}
.trajectory .segment,.trajectory .gap {{stroke:#8df6ed;stroke-width:2}}
.trajectory .estimate {{fill:#8df6ed}}
.trajectory .cursor {{visibility:hidden;stroke:#ffd185;stroke-dasharray:4 4}}
.trajectory .hit-target {{fill:transparent;stroke:transparent;stroke-width:2;cursor:pointer}}
.trajectory-frame {{cursor:pointer}}
.trajectory-frame:focus-visible .hit-target {{stroke:#fff;stroke-dasharray:3 2}}
.trajectory .active .cursor {{visibility:visible}}
.trajectory .active .estimate {{fill:#ffd185;stroke:#ffd185;stroke-width:4}}
.trajectory .active .gap {{stroke:#ffd185;stroke-width:3}}
.included circle {{fill:#8df6ed;stroke:#1c7779;stroke-width:2}}
.excluded rect {{fill:none;stroke:#acbfd5;stroke-width:2}}
</style></head><body><main><h1>ReplayAxis evidence review</h1>
<p>Select a camera group to highlight its synthetic source observations.</p>
{timeline()}
<h2>Reference cases</h2>
{sections}</main>
<script>
const scrubber = document.getElementById("frame-scrubber");
const label = document.getElementById("frame-label");
const frames = [...document.getElementById("timeline-frames").children];
const trajectoryFrames = [...document.querySelectorAll(".trajectory-frame")];
function showFrame() {{
    const index = Number(scrubber.value);
    frames.forEach((frame, position) => {{ frame.hidden = position !== index; }});
    trajectoryFrames.forEach((mark, position) => {{
        const active = position === index;
        mark.classList.toggle("active", active);
        mark.setAttribute("aria-pressed", String(active));
    }});
    label.textContent = frames[index].dataset.label;
    scrubber.setAttribute("aria-valuetext", label.textContent);
}}
for (const mark of trajectoryFrames) {{
    function selectFrame() {{
        scrubber.value = mark.dataset.frameIndex;
        showFrame();
    }}
    mark.addEventListener("click", selectFrame);
    mark.addEventListener("keydown", event => {{
        if (event.key === "Enter" || event.key === " ") {{
            event.preventDefault();
            selectFrame();
        }}
    }});
}}
scrubber.addEventListener("input", showFrame);
showFrame();
</script></body></html>
"""
    with args.output.open("x", encoding="utf-8") as output:
        output.write(html)


if __name__ == "__main__":
    main()
