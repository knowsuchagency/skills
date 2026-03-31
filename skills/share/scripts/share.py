# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx"]
# ///
"""Upload files to Zipline."""

import argparse
import mimetypes
import os
import subprocess
import sys
from pathlib import Path

import httpx

DEFAULT_ZIPLINE_URL = "https://zipline.knowsuchagency.ai"


def load_from_env_or_fnox(key: str) -> str | None:
    value = os.environ.get(key)
    if value:
        return value
    result = subprocess.run(
        ["fnox", "get", key],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload files to Zipline")
    parser.add_argument("files", nargs="+", help="File path(s) to upload")
    parser.add_argument("--url", default=None, help="Zipline server URL (default: env/fnox ZIPLINE_URL or built-in)")
    parser.add_argument("--expires", default=None, help="Auto-delete after duration (e.g. 1d, 7d)")
    parser.add_argument("--password", default=None, help="Password-protect the file")
    parser.add_argument("--max-views", type=int, default=None, help="Delete after N views")
    parser.add_argument("--format", default=None, choices=["random", "date", "uuid", "name", "gfycat", "random-words"], dest="name_format")
    parser.add_argument("--original-name", action="store_true", help="Preserve original filename")
    parser.add_argument("--folder", default=None, help="Folder ID to place files in")
    args = parser.parse_args()

    zipline_url = args.url or load_from_env_or_fnox("ZIPLINE_URL") or DEFAULT_ZIPLINE_URL
    token = load_from_env_or_fnox("ZIPLINE_TOKEN")
    if not token:
        print("Error: ZIPLINE_TOKEN not found in environment or fnox", file=sys.stderr)
        sys.exit(1)

    headers: dict[str, str] = {"Authorization": token}
    if args.expires:
        headers["x-zipline-deletes-at"] = args.expires
    if args.password:
        headers["x-zipline-password"] = args.password
    if args.max_views is not None:
        headers["x-zipline-max-views"] = str(args.max_views)
    if args.name_format:
        headers["x-zipline-format"] = args.name_format
    if args.original_name:
        headers["x-zipline-original-name"] = "true"
    if args.folder:
        headers["x-zipline-folder"] = args.folder

    files = []
    for path_str in args.files:
        path = Path(path_str)
        if not path.is_file():
            print(f"Error: {path} is not a file", file=sys.stderr)
            sys.exit(1)
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        files.append(("file", (path.name, path.read_bytes(), mime)))

    with httpx.Client(timeout=120) as client:
        resp = client.post(f"{zipline_url}/api/upload", headers=headers, files=files)
        resp.raise_for_status()

    data = resp.json()
    for f in data["files"]:
        print(f["url"])


if __name__ == "__main__":
    main()
