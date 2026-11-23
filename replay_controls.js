(() => {
  const replay = document.getElementById("replay");
  const answer = document.getElementById("assistant-answer");
  const form = document.getElementById("assistant-form");
  const question = document.getElementById("assistant-question");
  const video = document.getElementById("gesture-camera");
  const gestureButton = document.getElementById("gesture");
  const commands = new Set(["play", "pause", "next frame", "previous frame", "reset view", "mark joint"]);
  const localServer = ["127.0.0.1", "localhost"].includes(location.hostname);

  window.replayControl = (action) => {
    if (!commands.has(action)) return false;
    if (!localServer) {
      answer.textContent = "Open the local demo server to control 3D replay with the assistant.";
      return true;
    }
    replay.contentWindow.postMessage({type: "replayaxis-control", action}, location.origin);
    answer.textContent = "Replay command sent: " + action;
    return true;
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
  listen.onclick = () => {
    if (!SpeechRecognition) {
      answer.textContent = "Voice recognition is unavailable in this browser. Type a command instead.";
      return;
    }
    const speech = new SpeechRecognition();
    speech.lang = "en-US";
    speech.onresult = (event) => {
      question.value = event.results[0][0].transcript;
      form.requestSubmit();
    };
    speech.onerror = () => { answer.textContent = "Voice recognition could not complete."; };
    speech.onend = () => { listen.disabled = false; };
    try {
      speech.start();
      listen.disabled = true;
      answer.textContent = "Listening…";
    } catch {
      answer.textContent = "Voice recognition could not start.";
    }
  };

  let stream = null;
  let recognizer = null;
  let timer = null;
  const stopGestures = () => {
    clearInterval(timer);
    timer = null;
    stream?.getTracks().forEach((track) => track.stop());
    stream = null;
    video.srcObject = null;
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
      gestureButton.textContent = "Disable camera gestures";
      answer.textContent = "Camera gestures on. Open palm plays. Fist pauses.";
      let lastTime = -1;
      let lastGesture = "";
      let repeated = 0;
      timer = setInterval(() => {
        if (video.readyState < 2 || video.currentTime === lastTime) return;
        lastTime = video.currentTime;
        try {
          const result = recognizer.recognizeForVideo(video, performance.now()).gestures[0]?.[0];
          const label = result?.score >= 0.75 ? result.categoryName : "";
          repeated = label === lastGesture ? repeated + 1 : 1;
          lastGesture = label;
          if (repeated !== 3) return;
          if (label === "Open_Palm") window.replayControl("play");
          if (label === "Closed_Fist") window.replayControl("pause");
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
  window.addEventListener("pagehide", stopGestures);
})();
