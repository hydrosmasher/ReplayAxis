# ReplayAxis

Research and software for 3D sports motion analysis.

- [Sports case demo and assistant](ReplayAxis_Demo.html)
- [Two-view reconstruction notebook](ReplayAxis_Markerless_TwoView.ipynb)
- Feasibility paper in [PDF](ReplayAxis_Feasibility_Assesment_First_Draft.pdf) and [Word](ReplayAxis_Feasibility_Assesment_First_Draft.docx)

The sports demo links to footage and hosts the Akhtar and underwater butterfly pose pilots in one viewer.

## Local OpenJarvis assistant

The demo works directly from the HTML file for case browsing and local navigation commands. Free-text questions use the chat API from [OpenJarvis](https://github.com/open-jarvis/OpenJarvis). Install and configure a local model using the [OpenJarvis documentation](https://open-jarvis.github.io/OpenJarvis/getting-started/installation/), then run these in separate terminals:

```sh
jarvis serve --host 127.0.0.1 --port 8000 --model qwen3:8b
python3 serve_demo.py --jarvis-port 8000 --model qwen3:8b
```

Use the model ID available in your OpenJarvis instance. Open the demo URL printed by the server. The replay pilots also work with this server when OpenJarvis is offline. Only the typed question and selected case text go to OpenJarvis. The assistant has no access to the camera footage, research files, or measurement pipeline. Replay navigation uses the explicit local commands listed under `help`.

## Branches

Keep the current demo, reconstruction notebook, and paper on `main`. Save the previous working `main` commit to `checkpoints` before publishing a replacement. Keep exploratory scripts, validation results, and project handoff in the research archive.

### Replay controls

Open the demo through `python3 serve_demo.py` for the 3D controls. Type
or say `play`, `pause`, `next frame`, `previous frame`, `rewind`, `half speed`,
`normal speed`, `zoom in`, `zoom out`, `reset view`, `mark joint`, or
`replay status`. Say `load Akhtar` or `load butterfly` to load a pilot.
Replay commands are handled locally and the viewer confirms the result.
Use **Start microphone** for one utterance at a time. The optional “Jarvis”
prefix works in a command, and **Speak replies** enables browser speech
synthesis. Start spoken questions with “ask” to send the transcript to
local OpenJarvis. **Check OpenJarvis** checks whether the server lists the
configured model. Browser speech recognition may use an online provider.

**Enable camera gestures** loads the MediaPipe model and requests camera
access. Recognition runs in the browser. Open palm plays, fist pauses,
thumbs-up steps forward and thumbs-down steps back. Hold the gesture briefly
and release to repeat. Disable gestures to stop the camera.

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

#### Second-angle review

The primary [Cricket Australia feature](https://www.cricket.com.au/videos/2965060)
cuts from a close-up of Akhtar's approach at about 13.6 s to the end-on
release view by 13.8 s. It cuts to a fielder by 15.4 s. Those cuts do
not provide overlapping views of the release.

A low, behind-batter shot around 32–33.5 s shows an approach, then cuts
to another end-on delivery around 34 s. At 15.2 s Ponting crouches as he
evades the ball; around 35 s he stays upright and brings his bat across
his body. Treat this later sequence as a different delivery and exclude
it from the first delivery's stereo pair. The [official YouTube upload](https://www.youtube.com/watch?v=jdrItizhcRA)
has the same feature title and is an alternate source for review. The local
copy decoded only through 40.08 s, so later footage remains unreviewed.

For a new candidate, verify delivery identity using the broadcast sequence
and the batter's response, then align the bowler's front-foot contact,
release, and (when visible) bounce. Require distinct views with overlapping
frames around release and independently check the camera geometry before
triangulation. The current pilot remains a single-view estimate.
