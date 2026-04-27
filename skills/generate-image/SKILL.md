---
name: generate-image
description: Generate images using fal.ai (GPT-Image 2 by default, GPT-Image 1.5 for transparent backgrounds). Use when the user asks to generate, create, or make an image, picture, illustration, or graphic.
allowed-tools: Bash(uv run *)
---

# Image Generation — fal.ai (GPT-Image 2)

Generate images by running the bundled Python script via `uv run`. The script loads the `FAL_KEY` from fnox internally.

## Usage

```bash
uv run ./scripts/generate.py --prompt "PROMPT" [OPTIONS]
```

## Options

| Flag | Default | Choices |
|------|---------|---------|
| `--prompt` | *(required)* | Free text, 2-32k chars |
| `--model` | `gpt-2` | `gpt-2`, `gpt` |
| `--size` | `1024x1024` | `1024x1024`, `1536x1024`, `1024x1536`, `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `21:9` |
| `--quality` | `medium` | `low`, `medium`, `high` |
| `--num-images` | `1` | `1`–`4` |
| `--format` | `png` | `jpeg`, `png`, `webp` |
| `--background` | `auto` | `auto`, `transparent`, `opaque` (`--model gpt` only) |
| `--filename` | *(none)* | Output base name without extension (uses `--output-dir`) |
| `--output` | *(none)* | Output path stem without extension (overrides `--output-dir`) |
| `--output-dir` | OS temp dir | Any directory path |

## Model Selection

| Model | Endpoint | Best for |
|-------|----------|----------|
| `gpt-2` | `openai/gpt-image-2` | Default — current OpenAI image model |
| `gpt` | `fal-ai/gpt-image-1.5` | **Transparent backgrounds** (gpt-image-2 cannot produce true alpha PNGs) |

**Auto-select `gpt`** only when the user requests a transparent or non-opaque background. Otherwise stick with the default `gpt-2`.

## Workflow

1. Parse the user's request into a prompt and optional parameters.
2. Use `gpt-2` by default. Switch to `gpt` only if transparency is needed.
3. Run the script — it prints the saved file path(s) to stdout, one per line.
4. Display each saved image to the user using the Read tool.
5. Tell the user where the file(s) were saved.
