window.findReplayCases = (query, cases) => {
  const normalize = (value) => value.normalize("NFD").replace(/\p{Diacritic}/gu, "")
    .toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
  const words = " " + normalize(query) + " ";
  const contains = (value) => words.includes(" " + normalize(value) + " ");
  const matching = cases.flatMap(([title], index) => {
    const [athlete, event] = title.split(" · ");
    const surname = athlete.split(" ").at(-1);
    return contains(athlete) || contains(surname) ? [{athlete, event, index}] : [];
  });
  if (new Set(matching.map(({athlete}) => athlete)).size > 1) return matching.map(({index}) => index);
  const scored = matching.map(({event, index}) => ({
    index,
    score: normalize(event).split(" ").filter(word => word.length >= 4 && contains(word)).length,
  }));
  const bestScore = Math.max(...scored.map(({score}) => score));
  return scored.filter(({score}) => score === bestScore).map(({index}) => index);
};

window.answerReplayQuestion = (input, {name, notes, hasPilot, hasSource, replay, namedCase = false}) => {
  const question = input.trim()
    .replace(/^(?:replay\s*axis|jarvis)\b[,:]?\s*/i, "")
    .replace(/^(?:please\s+)?ask\s+/i, "")
    .toLowerCase();
  const result = (message, source = "ReplayAxis case catalog") => ({message, source});
  const measurementLimits = "No validated metric velocity, acceleration, or 3D ball trajectory is available for this case.";
  if (/\b(?:speed|velocity|acceleration|ball track|ball trajectory|measur(?:e|ed|ing|ements?)|metric|accuracy|accurate)\b/.test(question)) {
    return result(measurementLimits, "Case validation status");
  }
  if (/\b(?:angle|angles|cameras?|views?|depth|calibrat\w*|triangulat\w*)\b/.test(question)) {
    return result(hasPilot
      ? "Akhtar’s 3D estimate uses one broadcast view and a body prior for depth. A second view of the same delivery has not been verified."
      : "This case has no verified camera geometry or triangulated reconstruction in this demo.", "Case validation status");
  }
  if (/\b(?:current replay|loaded replay|which replay|what (?:am i|is the viewer) (?:watching|showing))\b/.test(question)) {
    return result(replay === "akhtar"
      ? "The viewer is set to the Akhtar single-camera pose pilot."
      : "The viewer is set to the underwater butterfly pilot. It uses separate footage from the Phelps benchmark cases.", "Replay selection");
  }
  if (/\b(?:forecast\w*|predict\w*)\b/.test(question)) {
    return result("This demo contains estimated poses within the source clips. A validated beyond-camera forecast is not available.", "ReplayAxis demo scope");
  }
  if (/\b(?:fps|frame rate|missing frames|frame count)\b/.test(question)) {
    return result(hasPilot
      ? "The Akhtar pilot uses 25 fps broadcast footage. Seventeen of its 19 frames contain usable joints."
      : "The catalog does not provide a verified source frame rate or reconstructed frame count for this case.", "Case validation status");
  }
  if (/\b(?:source|footage|video|clip|timestamp|when|where)\b/.test(question)) {
    return result(name + ". " + notes + (hasSource ? " Select this case to open its Watch source footage link." : ""));
  }
  if (namedCase || /\b(?:case|pilot|reconstruct\w*|estimated|limitations|validated)\b/.test(question)) {
    return result(name + ". " + notes + " " + (hasPilot
      ? "An unvalidated monocular body-pose pilot is available for 14.00–14.72 seconds."
      : "This case has a catalog entry. Its 3D reconstruction is pending."));
  }
  return result("I can answer questions about the selected case, footage, camera views, reconstruction, or measurement limits. Try “Is there a second camera angle?”", "Assistant help");
};
