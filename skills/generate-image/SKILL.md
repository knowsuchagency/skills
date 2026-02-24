---
name: generate-image
description: Generate images using fal.ai GPT-Image 1.5. Use when the user asks to generate, create, or make an image, picture, illustration, or graphic.
allowed-tools: Bash(uv run *)
---

# Image Generation — fal.ai GPT-Image 1.5

Generate images by running the bundled Python script via `uv run`. The script loads the `FAL_KEY` from fnox internally.

## Usage

```bash
uv run ./scripts/generate.py --prompt "PROMPT" [OPTIONS]
```

## Options

| Flag | Default | Choices |
|------|---------|---------|
| `--prompt` | *(required)* | Free text, 2-32k chars |
| `--size` | `1024x1024` | `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait) |
| `--quality` | `high` | `low`, `medium`, `high` |
| `--num-images` | `1` | `1`–`4` |
| `--format` | `png` | `jpeg`, `png`, `webp` |
| `--background` | `auto` | `auto`, `transparent`, `opaque` |
| `--output-dir` | OS temp dir | Any directory path |

## Workflow

1. Parse the user's request into a prompt and optional parameters (size, quality, count, format, background).
2. Run the script — it prints the saved file path(s) to stdout, one per line.
3. Display each saved image to the user using the Read tool.
4. Tell the user where the file(s) were saved.
