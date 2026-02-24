---
name: edit-image
description: Edit images using fal.ai GPT-Image 1.5. Use when the user asks to edit, modify, alter, transform, or change an existing image.
allowed-tools: Bash(uv run *)
---

# Image Editing — fal.ai GPT-Image 1.5

Edit images by running the bundled Python script via `uv run`. The script loads the `FAL_KEY` from fnox internally and uploads local files to fal CDN automatically.

## Usage

```bash
uv run ./scripts/edit.py --prompt "PROMPT" --image <path-or-url> [OPTIONS]
```

## Options

| Flag | Default | Choices |
|------|---------|---------|
| `--prompt` | *(required)* | Edit instruction, 2-32k chars |
| `--image` | *(required, repeatable)* | Local file path or URL |
| `--mask` | *(none)* | Mask image — local path or URL |
| `--size` | `auto` | `auto`, `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait) |
| `--quality` | `high` | `low`, `medium`, `high` |
| `--fidelity` | `high` | `low`, `high` — how closely to follow the source image |
| `--num-images` | `1` | `1`–`4` |
| `--format` | `png` | `jpeg`, `png`, `webp` |
| `--background` | `auto` | `auto`, `transparent`, `opaque` |
| `--output-dir` | OS temp dir | Any directory path |

## Workflow

1. Identify the source image(s) — the user may provide paths or reference recently generated/saved images.
2. Parse the edit prompt and any optional parameters.
3. Run the script — it uploads local files, calls the API, and prints saved file path(s) to stdout.
4. Display each saved image to the user using the Read tool.
5. Tell the user where the file(s) were saved.
