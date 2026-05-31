# knowsuchagency — Skills

A collection of skills for [Claude Code](https://claude.com/claude-code).

## Installation

Install with the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
# Install all skills
npx skills add knowsuchagency/skills

# List skills before installing
npx skills add knowsuchagency/skills --list

# Install specific skills
npx skills add knowsuchagency/skills --skill generate-image --skill fnox

# Install globally (~/.claude/skills) for Claude Code
npx skills add knowsuchagency/skills -g -a claude-code
```

## Skills

| Skill | Description |
|-------|-------------|
| `generate-image` | Generate images using fal.ai GPT-Image 1.5 |
| `edit-image` | Edit images using fal.ai GPT-Image 1.5 |
| `fnox` | Manage secrets with the fnox CLI |
| `codex-cli` | Use the OpenAI Codex coding agent via CLI |
| `gemini-cli` | Use the Google Gemini coding agent via CLI |
| `typst` | Expert reference for the Typst typesetting system |
| `mise` | Comprehensive guide for mise — polyglot tool version manager, environment manager, and task runner |

## Prerequisites

- [uv](https://docs.astral.sh/uv/) — required by image generation/editing skills
- [fnox](https://github.com/fnox-rs/fnox) — secrets management (used by image skills to load API keys)
- A [fal.ai](https://fal.ai) account and `FAL_KEY` — for image generation/editing
