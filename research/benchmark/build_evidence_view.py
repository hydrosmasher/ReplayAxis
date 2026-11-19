"""Build a self-contained desktop-browser view of the synthetic evidence."""

import argparse
import json
from html import escape
from pathlib import Path


def observation_rows(observations, frame_ids):
    rows = []
    for view in observations:
        selected = view["frame_id"] in frame_ids
        marker = "In this group" if selected else "Outside this group"
        x, y = view["pixel"]
        residual = view.get("residual_px")
        residual_text = f"{residual:.3f}" if residual is not None else "Unavailable"
        values = (marker, view["camera_id"], view["frame_id"], f"{view['time_s']:.3f}",
                  f"{x:.2f}", f"{y:.2f}", residual_text)
        cells = "".join(f"<td>{escape(str(value))}</td>" for value in values)
        style = ' class="selected"' if selected else ""
        rows.append(f"<tr{style}>{cells}</tr>")
    return "\n".join(rows)


def render_case(index, case, answer):
    result = case["result"]
    consensus = result["consensus"]
    groups = answer["camera_groups"]
    if answer["status"] != result["status"] or any(
            group not in consensus["candidates"] for group in groups):
        raise ValueError(f"Explanation differs from evidence for {case['case']}")
    title = {"biased_accepted": "Accepted position", "withheld": "Withheld position"}.get(
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
        panels.append(f"""<div class="group">{control}
<div class="observations" tabindex="0">
<table>
<caption>Source observations</caption>
<thead><tr><th>Membership</th><th>Camera</th><th>Frame ID</th><th>Time (s)</th>
<th>X (px)</th><th>Y (px)</th><th>Result residual (px)</th></tr></thead>
<tbody>{rows}</tbody></table></div></div>""")
    return f"""<section aria-labelledby="heading-{index}">
<h2 id="heading-{index}">{escape(title)}</h2>
<p>{escape(answer["message"])}</p>
<dl><div><dt>Reconstruction status</dt><dd>{escape(result["status"])}</dd></div>
<div><dt>Consensus score margin</dt><dd>{margin_text}</dd></div></dl>
<fieldset><legend>Camera group</legend>{"".join(panels)}</fieldset></section>"""


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
</style></head><body><main><h1>ReplayAxis evidence review</h1>
<p>Select a camera group to highlight its synthetic source observations.</p>
{sections}</main></body></html>
"""
    with args.output.open("x", encoding="utf-8") as output:
        output.write(html)


if __name__ == "__main__":
    main()
