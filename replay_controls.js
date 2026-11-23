(() => {
  const replay = document.getElementById("replay");
  const answer = document.getElementById("assistant-answer");
  const form = document.getElementById("assistant-form");
  const question = document.getElementById("assistant-question");
  const video = document.getElementById("gesture-camera");
  const gestureButton = document.getElementById("gesture");
  const devices = document.getElementById("jarvis-devices");
  const spoken = document.getElementById("spoken-replies");
  const commands = new Set([
    "play", "pause", "next frame", "previous frame", "rewind", "reset view",
    "half speed", "normal speed", "zoom in", "zoom out", "mark joint", "replay status",
  ]);
  const catalog = new Set(["next", "previous", "status", "help", "show footage", "load akhtar", "load butterfly"]);
  const aliases = new Map([
    ["resume", "play"], ["start replay", "play"], ["play replay", "play"],
    ["stop", "pause"], ["pause replay", "pause"], ["step forward", "next frame"],
    ["step back", "previous frame"], ["last frame", "previous frame"],
    ["next case", "next"], ["previous case", "previous"], ["case status", "status"],
    ["go to start", "rewind"], ["restart replay", "rewind"], ["slow down", "half speed"],
    ["reset camera", "reset view"],
    ["open akhtar", "load akhtar"], ["open butterfly", "load butterfly"],
  ]);
  const normalize = (input) => {
    const words = input.trim().toLowerCase().replace(/^jarvis(?:[,:]+|\s+|$)\s*/, "")
      .replace(/^please\s+/, "").replace(/[.!?]+$/, "").replace(/\s+please$/, "").trim();
    return aliases.get(words) ?? words;
  };
  window.normalizeReplayCommand = normalize;
  const localServer = location.hostname === "127.0.0.1";
  const reply = (message, aloud = true) => {
    answer.textContent = message;
    if (aloud && spoken.checked && window.speechSynthesis && window.SpeechSynthesisUtterance) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(message);
      utterance.lang = "en-US";
      window.speechSynthesis.speak(utterance);
    }
  };
  window.jarvisReply = reply;
  let sequence = 0;
  let pending = null;
  window.addEventListener("message", (event) => {
    if (event.origin !== location.origin || event.source !== replay.contentWindow ||
        event.data?.type !== "replayaxis-result" || !pending || event.data.id !== pending.id ||
        typeof event.data.message !== "string") return;
    clearTimeout(pending.timer);
    reply(event.data.message, pending.aloud);
    pending = null;
  });
  window.replayControl = (action, aloud = true) => {
    if (!commands.has(action)) return false;
    if (!localServer) {
      reply("Open the local demo server to control 3D replay.");
      return true;
    }
    if (pending) clearTimeout(pending.timer);
    const id = ++sequence;
    const timer = setTimeout(() => {
      pending = null;
      reply("The replay did not respond. Wait for it to load, then try again.", false);
    }, 2000);
    pending = {id, timer, aloud};
    replay.contentWindow.postMessage({type: "replayaxis-control", action, id}, location.origin);
    return true;
  };
  document.getElementById("check-jarvis").onclick = async () => {
    if (!localServer) { reply("Open the local demo server to check OpenJarvis."); return; }
    devices.textContent = "Checking OpenJarvis…";
    try {
      const response = await fetch("/api/assistant/status", {signal: AbortSignal.timeout(5000)});
      const status = await response.json();
      devices.textContent = status.message;
    } catch {
      devices.textContent = "Could not check OpenJarvis.";
    }
  };
  document.getElementById("load-pilot").onclick = () => {
    if (!localServer) {
      answer.textContent = "Open the local demo server to load the butterfly pilot.";
      return;
    }
    replay.src = "replay/viewer.html?replay=butterfly";
  };

  document.getElementById("load-case-replay").onclick = () => {
    if (!localServer) {
      answer.textContent = "Open the local demo server to load the Akhtar pose pilot.";
      return;
    }
    replay.src = "replay/viewer.html?replay=akhtar";
  };

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const listen = document.getElementById("listen");
  let speech = null;
  listen.onclick = () => {
    if (speech) { speech.abort(); return; }
    if (!SpeechRecognition) {
      reply("Voice recognition is unavailable in this browser. Type a command instead.");
      return;
    }
    window.speechSynthesis?.cancel();
    const session = new SpeechRecognition();
    speech = session;
    session.lang = "en-US";
    session.onresult = (event) => {
      const transcript = event.results[0][0].transcript.trim();
      const command = normalize(transcript);
      question.value = transcript;
      if (commands.has(command) || catalog.has(command) || /^ask\s+\S/.test(command)) form.requestSubmit();
      else reply("I didn’t recognize that command. Say help for commands, or start a question with ask.", false);
    };
    session.onerror = (event) => {
      if (event.error !== "aborted") reply("Microphone recognition: " + event.error + ".", false);
    };
    session.onend = () => {
      speech = null;
      listen.textContent = "Start microphone";
      listen.setAttribute("aria-pressed", "false");
      if (answer.textContent === "Listening…") reply("Microphone stopped.", false);
    };
    try {
      session.start();
      listen.textContent = "Stop microphone";
      listen.setAttribute("aria-pressed", "true");
      reply("Listening…", false);
    } catch {
      session.onend();
      reply("Voice recognition could not start.", false);
    }
  };

  let stream = null;
  let recognizer = null;
  let timer = null;
  const gestures = new Map([
    ["Open_Palm", "play"], ["Closed_Fist", "pause"],
    ["Thumb_Up", "next frame"], ["Thumb_Down", "previous frame"],
  ]);
  const stopGestures = () => {
    clearInterval(timer);
    timer = null;
    stream?.getTracks().forEach((track) => track.stop());
    stream = null;
    video.srcObject = null;
    video.hidden = true;
    gestureButton.setAttribute("aria-pressed", "false");
    recognizer?.close();
    recognizer = null;
    gestureButton.textContent = "Enable camera gestures";
  };
  gestureButton.onclick = async () => {
    if (stream) {
      stopGestures();
      answer.textContent = "Camera gestures off.";
      return;
    }
    if (!localServer || !navigator.mediaDevices?.getUserMedia) {
      answer.textContent = "Camera gestures require the local demo server and browser camera support.";
      return;
    }
    gestureButton.disabled = true;
    answer.textContent = "Loading hand-gesture recognition…";
    try {
      const base = "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.21";
      const {FilesetResolver, GestureRecognizer} = await import(base + "/vision_bundle.mjs");
      const files = await FilesetResolver.forVisionTasks(base + "/wasm");
      recognizer = await GestureRecognizer.createFromOptions(files, {
        baseOptions: {modelAssetPath: "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"},
        runningMode: "VIDEO", numHands: 1,
      });
      stream = await navigator.mediaDevices.getUserMedia({video: true, audio: false});
      video.srcObject = stream;
      await video.play();
      video.hidden = false;
      gestureButton.setAttribute("aria-pressed", "true");
      gestureButton.textContent = "Disable camera gestures";
      answer.textContent = "Camera gestures on.";
      let lastTime = -1;
      let lastGesture = "";
      let repeated = 0;
      let latched = false;
      timer = setInterval(() => {
        if (video.readyState < 2 || video.currentTime === lastTime) return;
        lastTime = video.currentTime;
        try {
          const result = recognizer.recognizeForVideo(video, performance.now()).gestures[0]?.[0];
          const label = result?.score >= 0.75 && gestures.has(result.categoryName) ? result.categoryName : "";
          repeated = label === lastGesture ? repeated + 1 : 1;
          lastGesture = label;
          if (repeated !== 3) return;
          if (!label) { latched = false; return; }
          if (latched) return;
          latched = true;
          window.replayControl(gestures.get(label), false);
        } catch {
          stopGestures();
          answer.textContent = "Gesture recognition stopped. Typed and voice controls are still available.";
        }
      }, 125);
    } catch {
      stopGestures();
      answer.textContent = "Camera or gesture model unavailable. Typed and voice controls are still available.";
    } finally {
      gestureButton.disabled = false;
    }
  };
  window.addEventListener("pagehide", () => {
    speech?.abort();
    window.speechSynthesis?.cancel();
    stopGestures();
  });
})();
