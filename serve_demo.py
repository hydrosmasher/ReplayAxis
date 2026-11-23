"""Serve the ReplayAxis demo and its local assets."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class DemoHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        if self.path.split("?", 1)[0] not in {
            "/ReplayAxis_Demo.html", "/replay/viewer.html",
            "/replay/ReplayAxis_Butterfly_Pilot.json", "/replay/ReplayAxis_Akhtar_Pilot.json",
            "/replay_controls.js", "/replay_assistant.js",
        }:
            self.send_error(404)
            return None
        return super().send_head()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("Specify a port between 1 and 65535.")
    directory = Path(__file__).resolve().parent
    with ThreadingHTTPServer(("127.0.0.1", args.port),
                             partial(DemoHandler, directory=str(directory))) as server:
        print(f"http://127.0.0.1:{server.server_port}/ReplayAxis_Demo.html", flush=True)
        server.serve_forever()


if __name__ == "__main__":
    main()
