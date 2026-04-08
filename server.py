#!/usr/bin/env python3
"""
Building Directory — local dev server
--------------------------------------
Place this file in the same folder as:
  - building-directory.html
  - nightjar_interior.stl   (or whatever you set STL_FILE to in the HTML)

Then run:
  python server.py

And open:
  http://localhost:8000/building-directory.html

To use a different port:
  python server.py 9000
"""

import http.server
import socketserver
import sys
import os
import webbrowser
from functools import partial

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Allow local fetch of STL files
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, format, *args):
        # Quieter logging — only show non-asset requests
        path = args[0].split()[1] if args else ""
        if any(path.endswith(ext) for ext in (".js", ".css", ".ico", ".png", ".woff2")):
            return
        print(f"  {self.address_string()}  {format % args}")


print(f"\n  Building Directory server")
print(f"  ─────────────────────────────────")
print(f"  Serving:  {DIRECTORY}")
print(f"  Open:     http://localhost:{PORT}/building-directory.html")
print(f"  Stop:     Ctrl+C\n")

url = f"http://localhost:{PORT}/building-directory.html"

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
