---
name: share
description: Share/upload files to Zipline. Use when the user asks to share, upload, publish, or host a file.
allowed-tools: Bash(uv run *)
---

# Share — Zipline File Upload

Upload files to Zipline and return public URLs. The script loads `ZIPLINE_TOKEN` and `ZIPLINE_URL` from env vars or fnox.

## Usage

```bash
uv run ./scripts/share.py FILE [FILE...] [OPTIONS]
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `FILE` (positional) | *(required)* | One or more file paths to upload |
| `--expires` | *(none)* | Auto-delete after duration (e.g. `1d`, `7d`) |
| `--password` | *(none)* | Password-protect the file |
| `--max-views` | *(none)* | Delete after N views |
| `--format` | *(none)* | Filename style: `random`, `date`, `uuid`, `name`, `gfycat`, `random-words` |
| `--original-name` | off | Preserve original filename in download |
| `--url` | *(env/fnox `ZIPLINE_URL` or built-in)* | Zipline server URL |
| `--folder` | *(none)* | Folder ID to organize into |

## Workflow

1. Identify the file(s) the user wants to share.
2. Run the script — it prints one URL per uploaded file to stdout.
3. Report the URL(s) to the user.
