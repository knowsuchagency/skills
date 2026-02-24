---
name: generate-image
description: Generate images using fal.ai (Gemini or GPT-Image). Use when the user asks to generate, create, or make an image, picture, illustration, or graphic.
allowed-tools: Bash(uv run *)
---

# Image Generation — fal.ai (Gemini / GPT-Image)

Generate images by running the bundled Python script via `uv run`. The script loads the `FAL_KEY` from fnox internally.

## Usage

```bash
uv run ./scripts/generate.py --prompt "PROMPT" [OPTIONS]
```

## Options

| Flag | Default | Choices |
|------|---------|---------|
| `--prompt` | *(required)* | Free text, 2-32k chars |
| `--model` | `gemini-flash` | `gemini-flash`, `gemini-pro`, `gpt` |
| `--size` | `1024x1024` | `1024x1024`, `1536x1024`, `1024x1536`, `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `21:9` |
| `--quality` | `high` | `low`, `medium`, `high` |
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
| `gpt` | varies | **Transparent backgrounds**, or when user asks for GPT/DALL-E |

**Auto-select `gpt`** when the user requests a transparent or non-opaque background. Gemini models do not support transparency.

## Workflow

1. Parse the user's request into a prompt and optional parameters.
2. Choose the model — use `gemini-flash` by default, `gpt` if transparency is needed.
3. Run the script — it prints the saved file path(s) to stdout, one per line.
4. Display each saved image to the user using the Read tool.
5. Tell the user where the file(s) were saved.
