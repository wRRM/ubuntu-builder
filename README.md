# Ubuntu ISO Builder

A local web application for creating a customized, bootable Ubuntu ISO. Upload a source ISO, stage files at paths in the ISO filesystem, edit the GRUB configuration files found in the image, then download the result.

The build runs entirely inside Docker and does **not** need `--privileged`, loop devices, or host mounts. It uses `xorriso` boot-image replay so the same Compose setup works with Docker Engine on Linux and Docker Desktop on Windows.

## Install and start it

Requirements:

- Docker Engine 24+ with the Compose plugin, or Docker Desktop
- Enough Docker storage for the source ISO, output ISO, and temporary build data (allow roughly 3× the ISO size)

The public image is published for Linux AMD64 at `ghcr.io/wrrm/ubuntu-builder`.

```bash
docker pull ghcr.io/wrrm/ubuntu-builder:latest
docker compose up -d
```

Open [http://localhost:8080](http://localhost:8080). Stop the service with `docker compose down`; uploaded data and output images remain in the `builder_data` named volume.

### Windows

Run the same command from PowerShell in this directory:

```powershell
docker pull ghcr.io/wrrm/ubuntu-builder:latest
docker compose up -d
```

Using a named volume avoids Windows/Linux bind-mount permission and path differences. No WSL-specific setup is required when Docker Desktop is using Linux containers.

## Workflow

1. Upload an Ubuntu `.iso`, or download the latest released Ubuntu Desktop/Server AMD64 ISO directly from Canonical. Official downloads are checked against Canonical's `SHA256SUMS`. The server then validates the image with `xorriso` and discovers every `grub.cfg` and `loopback.cfg` in the image.
2. Add files. They are staged immediately at the root of the ISO using their filenames.
3. Select and edit any discovered GRUB configuration, then save it. `grub-script-check` validates the syntax before changes are accepted.
   The **Autoinstall** button on a selected `grub.cfg` adds the `autoinstall` kernel argument to every Ubuntu installer boot entry, selects the first menu entry containing `Install Ubuntu`, sets a hidden zero-second timeout for direct boot, validates the result, and saves it. When `/autoinstall.yaml` is staged at the ISO root, Subiquity discovers it from the installation medium.
4. Choose an output name, build, and download the new ISO.

Uploaded sources, staged files, edits, build status, and an undownloaded output image survive container restarts. After a successful build, the source ISO and staged files are deleted automatically. The completed ISO is deleted after its download response finishes, so persistent container storage does not accumulate old images.

The interface uses Swedish by default. Use the language control in the header to switch to English; the choice is saved in the browser.

## Important path distinction

This tool injects files into the **ISO filesystem**. It does not modify Ubuntu's installed root filesystem, which is normally stored in `casper/filesystem.squashfs`. This is ideal for autoinstall data, boot-time assets, firmware, scripts consumed from the installation media, and similar use cases.

Modifying the SquashFS root requires an additional unpack/chroot/repack workflow and is intentionally outside this project's current scope.

## Configuration

Copy `.env.example` to `.env` to override defaults:

| Variable | Default | Purpose |
| --- | ---: | --- |
| `WEB_PORT` | `8080` | Host port bound to `127.0.0.1` |
| `MAX_UPLOAD_BYTES` | `17179869184` | Maximum HTTP request size (16 GiB) |

To access the UI from another machine, deliberately change the Compose port binding from `127.0.0.1` to an appropriate interface and put authentication/TLS in front of it. The app itself has no user accounts.

## Security and boot behavior

- The container runs as UID/GID `10001`, drops all Linux capabilities, sets `no-new-privileges`, and uses a read-only root filesystem.
- Source ISOs are never changed in place. Builds use a temporary output and publish it atomically when complete.
- Paths are normalized and traversal with `..` is rejected.
- GRUB edits and injected files can still make an image unbootable. Keep the original ISO and test outputs in a VM before using physical media.
- Boot catalog, El Torito, and system-area settings are replayed from the source image. Replacing signed EFI executables or other verified boot assets can invalidate Secure Boot expectations.

## Development and tests

Create an environment and run the unit/API suite:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/pytest -q
```

Container checks:

```bash
docker compose -f compose.yaml -f compose.dev.yaml config
docker compose -f compose.yaml -f compose.dev.yaml build
docker compose -f compose.yaml -f compose.dev.yaml up -d
docker compose ps
```

For a full acceptance test, upload an official Ubuntu ISO, add a small marker file, change a harmless GRUB timeout, build it, and boot the output in a VM. Unit tests mock `xorriso`; they verify storage, path-safety, API, editing, and orchestration rather than firmware bootability.
