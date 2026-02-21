# knowsuchagency — Claude Code Plugin

A collection of skills for [Claude Code](https://claude.com/claude-code).

## Installation

```
/plugin marketplace add knowsuchagency/claude
/plugin install knowsuchagency
```

## Skills

| Skill | Description |
|-------|-------------|
| `generate-image` | Generate images using fal.ai GPT-Image 1.5 |
| `edit-image` | Edit images using fal.ai GPT-Image 1.5 |
| `install-fulcrum` | Guided step-by-step installation of [Fulcrum](https://github.com/knowsuchagency/fulcrum) (local or remote VPS) |
| `fnox` | Manage secrets with the fnox CLI |
| `codex-cli` | Use the OpenAI Codex coding agent via CLI |
| `gemini-cli` | Use the Google Gemini coding agent via CLI |
| `linear-cli` | Manage Linear issues, projects, and teams |
| `typst` | Expert reference for the Typst typesetting system |
| `wmill-cli` | Manage Windmill workspaces and scripts |

## Prerequisites

- [uv](https://docs.astral.sh/uv/) — required by image generation/editing skills
- [fnox](https://github.com/fnox-rs/fnox) — secrets management (used by image skills to load API keys)
- A [fal.ai](https://fal.ai) account and `FAL_KEY` — for image generation/editing
