from __future__ import annotations

import hashlib
import io

import pytest

from app.ubuntu import UbuntuReleaseError, UbuntuReleaseService


class FakeResponse(io.BytesIO):
    def __init__(self, payload: bytes, url: str, *, content_length: int | None = None) -> None:
        super().__init__(payload)
        self.url = url
        self.headers = {}
        if content_length is not None:
            self.headers["Content-Length"] = str(content_length)

    def geturl(self) -> str:
        return self.url

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        self.close()


def fake_opener(payloads: dict[str, bytes]):
    def open_request(request, timeout):
        assert timeout in {30, 60}
        payload = payloads[request.full_url]
        return FakeResponse(payload, request.full_url, content_length=len(payload))

    return open_request


def release_payloads(edition: str = "desktop", iso: bytes = b"official-iso") -> dict[str, bytes]:
    suffix = "desktop-amd64.iso" if edition == "desktop" else "live-server-amd64.iso"
    name = f"ubuntu-26.04.1-{suffix}"
    checksum = hashlib.sha256(iso).hexdigest()
    return {
        "https://releases.ubuntu.com/": (
            b'<a href="24.04.4/">24.04.4/</a><a href="26.04/">26.04/</a>'
            b'<a href="26.04.1/">26.04.1/</a><a href="noble/">noble/</a>'
        ),
        "https://releases.ubuntu.com/26.04.1/SHA256SUMS": f"{checksum} *{name}\n".encode(),
        f"https://releases.ubuntu.com/26.04.1/{name}": iso,
    }


def test_resolves_latest_numbered_desktop_release():
    service = UbuntuReleaseService(opener=fake_opener(release_payloads()))
    image = service.resolve_latest("desktop")
    assert image.version == "26.04.1"
    assert image.name == "ubuntu-26.04.1-desktop-amd64.iso"
    assert image.url == "https://releases.ubuntu.com/26.04.1/ubuntu-26.04.1-desktop-amd64.iso"


def test_resolves_latest_server_release():
    service = UbuntuReleaseService(opener=fake_opener(release_payloads("server")))
    image = service.resolve_latest("server")
    assert image.name == "ubuntu-26.04.1-live-server-amd64.iso"


def test_rejects_redirect_away_from_canonical():
    def redirected(_request, timeout):
        assert timeout == 30
        return FakeResponse(b"index", "https://example.test/releases/")

    service = UbuntuReleaseService(opener=redirected)
    with pytest.raises(UbuntuReleaseError, match="unexpected host"):
        service.resolve_latest("desktop")
