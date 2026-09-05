from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


RELEASES_URL = "https://releases.ubuntu.com/"
MAX_METADATA_BYTES = 2 * 1024**2


class UbuntuReleaseError(RuntimeError):
    pass


@dataclass(frozen=True)
class UbuntuIso:
    edition: str
    version: str
    name: str
    url: str
    sha256: str


class UbuntuReleaseService:
    def __init__(self, base_url: str = RELEASES_URL, opener=urlopen) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.opener = opener

    def _open(self, url: str, *, timeout: int):
        request = Request(url, headers={"User-Agent": "ubuntu-builder/1.0"})
        try:
            response = self.opener(request, timeout=timeout)
        except OSError as exc:
            raise UbuntuReleaseError(f"Could not reach Canonical's Ubuntu releases service: {exc}") from exc
        final_host = (urlparse(response.geturl()).hostname or "").lower()
        if final_host != "releases.ubuntu.com" and not final_host.endswith(".releases.ubuntu.com"):
            response.close()
            raise UbuntuReleaseError("Canonical redirected the ISO download to an unexpected host")
        return response

    def _read_text(self, url: str) -> str:
        with self._open(url, timeout=30) as response:
            payload = response.read(MAX_METADATA_BYTES + 1)
        if len(payload) > MAX_METADATA_BYTES:
            raise UbuntuReleaseError("Canonical's release metadata is unexpectedly large")
        try:
            return payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise UbuntuReleaseError("Canonical's release metadata is not valid UTF-8") from exc

    @staticmethod
    def _version_key(version: str) -> tuple[int, ...]:
        return tuple(int(part) for part in version.split("."))

    def resolve_latest(self, edition: str) -> UbuntuIso:
        if edition not in {"desktop", "server"}:
            raise ValueError("Edition must be desktop or server")

        index = self._read_text(self.base_url)
        versions = set(re.findall(r'href=["\'](\d+\.\d+(?:\.\d+)?)/["\']', index))
        if not versions:
            raise UbuntuReleaseError("Canonical's release index contains no numbered Ubuntu releases")
        version = max(versions, key=self._version_key)
        release_url = urljoin(self.base_url, f"{version}/")
        sums = self._read_text(urljoin(release_url, "SHA256SUMS"))
        suffix = "desktop-amd64.iso" if edition == "desktop" else "live-server-amd64.iso"
        expected_name = f"ubuntu-{version}-{suffix}"
        checksum = None
        for line in sums.splitlines():
            parts = line.split()
            if len(parts) == 2 and parts[1].lstrip("*") == expected_name:
                checksum = parts[0].lower()
                break
        if not checksum or not re.fullmatch(r"[0-9a-f]{64}", checksum):
            raise UbuntuReleaseError(f"Canonical does not list {expected_name} in SHA256SUMS")
        return UbuntuIso(
            edition=edition,
            version=version,
            name=expected_name,
            url=urljoin(release_url, expected_name),
            sha256=checksum,
        )

    def download_latest(self, store, edition: str, *, max_bytes: int) -> dict:
        image = self.resolve_latest(edition)
        with self._open(image.url, timeout=60) as response:
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > max_bytes:
                raise UbuntuReleaseError("The latest Ubuntu ISO exceeds MAX_UPLOAD_BYTES")
            return store.set_base_iso(
                response,
                image.name,
                expected_sha256=image.sha256,
                max_bytes=max_bytes,
            )
