"""Explain a synthetic replay result using only its exported evidence."""

import argparse
import json
from pathlib import Path


def explain(case):
    result = case["result"]
    consensus = result["consensus"]
    candidates = consensus["candidates"]
    details = {"status": result["status"], "reason": consensus["reason"],
               "score_metric": consensus["score_metric"],
               "score_margin": consensus["score_margin"],
               "inlier_threshold_px": consensus["inlier_threshold_px"]}
    if result["status"] == "ambiguous" and consensus["reason"] == "tied_top_groups":
        score = candidates[0]["score"]
        groups = [group for group in candidates if group["score"] == score]
        labels = ", ".join("–".join(group["camera_ids"]) for group in groups)
        message = (f"Position withheld: {labels} tied at {score} inlier cameras "
                   f"under the {details['inlier_threshold_px']:g} px reprojection rule.")
    elif result["status"] == "ambiguous":
        groups = []
        message = "Position withheld: no candidate camera group met the reprojection rule."
    elif result["status"] == "inconsistent_refit":
        groups = candidates[:1]
        message = "Position withheld: the selected group exceeded the reprojection threshold after refitting."
    elif result["status"] == "reconstructed":
        groups = candidates[:1]
        label = "–".join(groups[0]["camera_ids"])
        message = (f"Position reconstructed from {label} under the reprojection rule. "
                   "Camera agreement does not establish position accuracy.")
    else:
        raise ValueError(f"Unsupported reconstruction status: {result['status']}")
    return {**details, "message": message, "camera_groups": groups}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    cases = json.loads(args.evidence.read_text(encoding="utf-8"))
    print(json.dumps([{"case": case["case"], **explain(case)} for case in cases],
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
