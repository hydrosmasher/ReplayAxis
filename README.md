# ReplayAxis

Research and software for 3D sports motion analysis.

- [Sports case demo and assistant](ReplayAxis_Demo.html)
- [Interactive synthetic 3D replay](ReplayAxis_3D_Example.html)
- [Two-view reconstruction notebook](ReplayAxis_Markerless_TwoView.ipynb)
- Feasibility paper in [PDF](ReplayAxis_Feasibility_Assesment_First_Draft.pdf) and [Word](ReplayAxis_Feasibility_Assesment_First_Draft.docx)

The sports case demo links to footage. The synthetic example illustrates 3D replay and manual joint marking. Sport-specific reconstructions are pending.

## Local OpenJarvis assistant

The demo works directly from the HTML file for case browsing and local navigation commands. Free-text questions use the chat API from [OpenJarvis](https://github.com/open-jarvis/OpenJarvis). Install and configure a local model using the [OpenJarvis documentation](https://open-jarvis.github.io/OpenJarvis/getting-started/installation/), then run these in separate terminals:

```sh
jarvis serve --host 127.0.0.1 --port 8000 --agent simple
python3 serve_demo.py --jarvis-port 8000 --model qwen3:8b
```

Use the model ID available in your OpenJarvis instance. Open the demo URL printed by the server. Only the typed question and selected case text go to OpenJarvis. The assistant has no access to the camera footage, research files, or measurement pipeline. Replay navigation uses the explicit local commands listed under `help`.

## Branches

Keep the current demos and paper on `main`. Save the previous working `main` commit to `checkpoints` before publishing a replacement. Keep exploratory scripts, validation results, and project handoff in the research archive.

### Replay controls

Open the demo through the local server for the 3D assistant controls. Type
or say `play`, `pause`, `next frame`, `previous frame`, `reset view`, or
`mark joint`. These commands go directly to the viewer. OpenJarvis handles
free-text case questions when its server is running.

Use **Voice** in a browser that supports speech recognition. The browser
may use its speech provider. Use **Enable camera gestures** to load the
MediaPipe model and grant camera access. Hand inference runs in the browser.
Open palm plays and closed fist pauses. Disable gestures to release the camera.

The synthetic replay and the underwater butterfly pilot exercise the same
controls. The pilot is a separate video from the Phelps case and shows
estimated single-camera relative pose. Its source is
[Butterfly stroke from underwater](https://commons.wikimedia.org/wiki/File:Butterfly_stroke_from_underwater.webm)
by It is a wonderful world, CC BY-SA 4.0. The bundled pilot trajectory
is provided under the same license. The 16 catalog entries still need their
own validated 3D reconstructions.
