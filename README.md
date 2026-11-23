# ReplayAxis

Research and software for 3D sports motion analysis.

- [Sports case demo and assistant](ReplayAxis_Demo.html)
- [Two-view reconstruction notebook](ReplayAxis_Markerless_TwoView.ipynb)
- Feasibility paper in [PDF](ReplayAxis_Feasibility_Assesment_First_Draft.pdf) and [Word](ReplayAxis_Feasibility_Assesment_First_Draft.docx)

The sports demo links to footage and hosts the Akhtar and underwater butterfly pose pilots in one viewer.

## Local OpenJarvis assistant

The demo works directly from the HTML file for case browsing and local navigation commands. Free-text questions use the chat API from [OpenJarvis](https://github.com/open-jarvis/OpenJarvis). Install and configure a local model using the [OpenJarvis documentation](https://open-jarvis.github.io/OpenJarvis/getting-started/installation/), then run these in separate terminals:

```sh
jarvis serve --host 127.0.0.1 --port 8000 --agent simple
python3 serve_demo.py --jarvis-port 8000 --model qwen3:8b
```

Use the model ID available in your OpenJarvis instance. Open the demo URL printed by the server. The replay pilots also work with this server when OpenJarvis is offline. Only the typed question and selected case text go to OpenJarvis. The assistant has no access to the camera footage, research files, or measurement pipeline. Replay navigation uses the explicit local commands listed under `help`.

## Branches

Keep the current demo, reconstruction notebook, and paper on `main`. Save the previous working `main` commit to `checkpoints` before publishing a replacement. Keep exploratory scripts, validation results, and project handoff in the research archive.

### Replay controls

Open the demo through the local server for the 3D assistant controls. Type
or say `play`, `pause`, `next frame`, `previous frame`, `reset view`, or
`mark joint`. These commands go directly to the viewer. OpenJarvis handles
free-text case questions when its server is running.

Use **Voice** in a browser that supports speech recognition. The browser
may use its speech provider. Use **Enable camera gestures** to load the
MediaPipe model and grant camera access. Hand inference runs in the browser.
Open palm plays and closed fist pauses. Disable gestures to release the camera.

The underwater butterfly pilot uses a separate video from the Phelps case and shows
estimated single-camera relative pose. Its source is
[Butterfly stroke from underwater](https://commons.wikimedia.org/wiki/File:Butterfly_stroke_from_underwater.webm)
by It is a wonderful world, CC BY-SA 4.0. The bundled pilot trajectory
is provided under the same license. The 16 catalog entries still need their
own validated 3D reconstructions.

### Broadcast case pilot

Select **Shoaib Akhtar · Bouncer** and choose **Load Akhtar pose pilot**.
The demo bundles estimated joint coordinates from frames 350–368 (14.00–14.72 s)
of the linked Cricket Australia review clip, sampled at its source rate of 25 fps.
A crop isolates the bowler. The markerless detector finds 2D joints, and a fixed
body prior supplies estimated depth in a hip-relative coordinate system. Missing
observations remain missing. Seventeen frames contain some accepted joints.
The replay includes no broadcast video, ball track, metric scale, or validated
accuracy. The same playback, voice-command, and gesture controls target this replay.
