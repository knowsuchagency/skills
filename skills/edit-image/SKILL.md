---
name: edit-image
description: Edit images using fal.ai (GPT-Image 2 by default, GPT-Image 1.5 for transparency/masks/fidelity). Use when the user asks to edit, modify, alter, transform, or change an existing image.
allowed-tools: Bash(uv run *)
---

# Image Editing — fal.ai (GPT-Image 2)

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
| `--model` | `gpt-2` | `gpt-2`, `gpt` |
| `--mask` | *(none)* | Mask image — local path or URL (`--model gpt` only) |
| `--size` | `auto` | `auto`, `1024x1024`, `1536x1024`, `1024x1536`, `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `21:9` |
| `--quality` | `medium` | `low`, `medium`, `high` |
| `--fidelity` | `high` | `low`, `high` — how closely to follow the source image (`--model gpt` only) |
| `--num-images` | `1` | `1`–`4` |
| `--format` | `png` | `jpeg`, `png`, `webp` |
| `--background` | `auto` | `auto`, `transparent`, `opaque` (`--model gpt` only) |
| `--filename` | *(none)* | Output base name without extension (uses `--output-dir`) |
| `--output` | *(none)* | Output path stem without extension (overrides `--output-dir`) |
| `--output-dir` | OS temp dir | Any directory path |

## Model Selection

| Model | Endpoint | Best for |
|-------|----------|----------|
| `gpt-2` | `openai/gpt-image-2/edit` | Default — current OpenAI image model |
| `gpt` | `fal-ai/gpt-image-1.5/edit` | **Transparent backgrounds**, mask-based editing, or fidelity control |

**Auto-select `gpt`** only when the user needs transparent backgrounds, masks, or fidelity control. Otherwise stick with the default `gpt-2`.

## Workflow

1. Identify the source image(s) — the user may provide paths or reference recently generated/saved images.
2. Parse the edit prompt and any optional parameters.
3. Use `gpt-2` by default. Switch to `gpt` only if transparency, masks, or fidelity control is needed.
4. Run the script — it uploads local files, calls the API, and prints saved file path(s) to stdout.
5. Display each saved image to the user using the Read tool.
6. Tell the user where the file(s) were saved.
