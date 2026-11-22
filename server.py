import mimetypes
import threading
from pathlib import Path

from flask import Flask, abort, render_template, send_file
from waitress import create_server


VIDEO_EXTENSIONS = {".mp4", ".m4v", ".webm", ".mov", ".mkv", ".avi"}


def create_app(movie_folder):
    app = Flask(__name__)
    root = Path(movie_folder).resolve()

    def get_video(filename):
        try:
            video = (root / filename).resolve()
            video.relative_to(root)
        except (ValueError, OSError):
            abort(403)

        if not video.is_file():
            abort(404)
        if video.suffix.lower() not in VIDEO_EXTENSIONS:
            abort(403)
        return video

    @app.route("/")
    def index():
        movies = sorted(
            (file.relative_to(root).as_posix()
             for file in root.rglob("*")
             if file.is_file() and file.suffix.lower() in VIDEO_EXTENSIONS),
            key=str.lower,
        )
        return render_template("index.html", movies=movies)

    @app.route("/video/<path:filename>")
    def stream_video(filename):
        video = get_video(filename)
        return send_file(
            video,
            mimetype=mimetypes.guess_type(video.name)[0] or "application/octet-stream",
            conditional=True,
            as_attachment=False,
        )

    return app


class MediaServer:
    def __init__(self):
        self.server = None
        self.thread = None
        self.app = None

    def start(self, movie_folder, host="0.0.0.0", port=8080):
        if self.server:
            return
        app = create_app(movie_folder)
        server = create_server(app, host=host, port=port, threads=8)
        thread = threading.Thread(target=server.run, daemon=True)
        thread.start()
        self.app = app
        self.server = server
        self.thread = thread

    def stop(self):
        if self.server:
            self.server.close()
            self.server = None
            self.thread = None
            self.app = None
