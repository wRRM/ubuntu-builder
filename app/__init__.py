from __future__ import annotations

import os
from pathlib import Path

from flask import Flask

from .routes import api
from .store import ProjectStore


def create_app(*, data_dir: str | Path | None = None, iso_service=None) -> Flask:
    app = Flask(__name__)
    app.config.update(
        MAX_CONTENT_LENGTH=int(os.getenv("MAX_UPLOAD_BYTES", str(16 * 1024**3))),
        JSON_SORT_KEYS=False,
    )

    root = Path(data_dir or os.getenv("DATA_DIR", "/data"))
    app.extensions["project_store"] = ProjectStore(root, iso_service=iso_service)
    app.register_blueprint(api)
    return app

