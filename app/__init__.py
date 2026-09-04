from __future__ import annotations

import os
import tempfile
from pathlib import Path

from flask import Flask

from .grub import GrubValidator
from .routes import api
from .store import ProjectStore


def create_app(*, data_dir: str | Path | None = None, iso_service=None, grub_validator=None) -> Flask:
    app = Flask(__name__)
    app.config.update(
        MAX_CONTENT_LENGTH=int(os.getenv("MAX_UPLOAD_BYTES", str(16 * 1024**3))),
        JSON_SORT_KEYS=False,
    )

    root = Path(data_dir or os.getenv("DATA_DIR", "/data"))
    project_store = ProjectStore(root, iso_service=iso_service)
    # Werkzeug's multipart parser uses tempfile for uploads larger than 500 KiB.
    # Keep those files on the persistent data volume instead of the small,
    # hardened /tmp tmpfs used by the container.
    tempfile.tempdir = str(project_store.upload_tmp_dir)
    app.extensions["project_store"] = project_store
    app.extensions["grub_validator"] = grub_validator or GrubValidator()
    app.register_blueprint(api)
    return app
