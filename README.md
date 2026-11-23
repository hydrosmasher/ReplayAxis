# ReplayAxis

Research and software for 3D sports motion analysis.

- [Sports case demo and assistant](ReplayAxis_Demo.html)
- [Two-view reconstruction notebook](ReplayAxis_Markerless_TwoView.ipynb)
- Feasibility paper in [PDF](ReplayAxis_Feasibility_Assesment_First_Draft.pdf) and [Word](ReplayAxis_Feasibility_Assesment_First_Draft.docx)

The sports demo links to footage and hosts the Akhtar and underwater butterfly pose pilots in one viewer.

## ReplayAxis Assistant

Start the demo with `python3 serve_demo.py` and open the printed link.
The assistant answers supported questions in the browser using the selected
case and documented validation limits. Example questions include “What does
this case show?”, “Is there a second camera angle?”, and “Can I measure ball
speed?” The response identifies its evidence source. Unsupported questions
receive guidance on supported topics. Ask “Does Akhtar have a second
camera angle?” from any case, or say “select Phelps butterfly finish” to
switch cases. If a name matches multiple events, the assistant lists them. A separate, fixed command list controls
the viewer. The web server only serves demo files.

## Branches

Keep the current demo, reconstruction notebook, and paper on `main`. Save the previous working `main` commit to `checkpoints` before publishing a replacement. Keep exploratory scripts, validation results, and project handoff in the research archive.

### Replay controls

Open the demo through `python3 serve_demo.py` for the 3D controls. Type
or say `play`, `pause`, `next frame`, `previous frame`, `rewind`, `half speed`,
`normal speed`, `zoom in`, `zoom out`, `reset view`, `mark joint`, or
`replay status`. Say `load Akhtar` or `load butterfly` to load a pilot.
Replay commands are handled locally and the viewer confirms the result.
Say or type `frame 10` for a one-based replay frame, `source frame 350` for
a camera A frame, or `go to 14.4 seconds` for the nearest recorded frame at
that source timestamp. The viewer pauses on a match and reports the actual
source time. Requests outside the loaded replay leave playback alone.
Use **Start microphone** for one utterance at a time and optionally begin with
“ReplayAxis.” **Speak replies** enables browser speech synthesis. The question
handler itself runs locally, and browser speech recognition may use an online
provider.

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
