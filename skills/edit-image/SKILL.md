---
name: edit-image
description: Edit images using fal.ai (Gemini or GPT-Image). Use when the user asks to edit, modify, alter, transform, or change an existing image.
allowed-tools: Bash(uv run *)
---

# Image Editing — fal.ai (Gemini / GPT-Image)

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
| `--model` | `gemini-flash` | `gemini-flash`, `gemini-pro`, `gpt` |
| `--mask` | *(none)* | Mask image — local path or URL (GPT only) |
| `--size` | `auto` | `auto`, `1024x1024`, `1536x1024`, `1024x1536`, `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `21:9` |
| `--quality` | `high` | `low`, `medium`, `high` |
| `--fidelity` | `high` | `low`, `high` — how closely to follow the source image (GPT only) |
| `--num-images` | `1` | `1`–`4` |
| `--format` | `png` | `jpeg`, `png`, `webp` |
| `--background` | `auto` | `auto`, `transparent`, `opaque` (GPT only) |
| `--seed` | *(none)* | Integer for reproducibility (Gemini only) |
| `--filename` | *(none)* | Output base name without extension (uses `--output-dir`) |
| `--output` | *(none)* | Output path stem without extension (overrides `--output-dir`) |
| `--output-dir` | OS temp dir | Any directory path |

## Model Selection

| Model | Cost | Best for |
|-------|------|----------|
| `gemini-flash` | $0.039/img | Default — fast, cheap, good quality |
| `gemini-pro` | $0.15/img | Highest quality, 4K resolution (`--quality high` → 4K) |
| `gpt` | varies | **Transparent backgrounds**, masks, fidelity control, or when user asks for GPT/DALL-E |

**Auto-select `gpt`** when the user needs transparent backgrounds, mask-based editing, or fidelity control. Gemini models do not support these features.

## Workflow

1. Identify the source image(s) — the user may provide paths or reference recently generated/saved images.
2. Parse the edit prompt and any optional parameters.
3. Choose the model — use `gemini-flash` by default, `gpt` if transparency/masks/fidelity are needed.
4. Run the script — it uploads local files, calls the API, and prints saved file path(s) to stdout.
5. Display each saved image to the user using the Read tool.
6. Tell the user where the file(s) were saved.
