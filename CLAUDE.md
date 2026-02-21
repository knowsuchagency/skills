# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Claude Code plugin (`knowsuchagency` v2.0.0) providing 8 skills — markdown-based knowledge modules that Claude Code loads on demand. There is no build system, compilation, or test suite; all content is static Markdown.

## Architecture

```
.claude-plugin/
  plugin.json          # Plugin manifest (name, version, author)
  marketplace.json     # Marketplace registry entry
skills/
  <skill-name>/
    SKILL.md           # Skill definition with YAML frontmatter
    references/        # Optional subdirectory for large reference content
```

Each skill is defined by a single `SKILL.md` with YAML frontmatter:
- `name` — unique skill identifier
- `description` — natural language triggers for skill discovery
- `allowed-tools` — optional restricted Bash commands the skill may use

## Skills

Two categories:
- **Executable skills** (generate-image, edit-image) — contain Python scripts run via `uv run`, use `fnox` for secrets
- **Reference skills** (fnox, codex-cli, gemini-cli, linear-cli, typst, wmill-cli) — pure documentation/CLI guides

The typst skill splits content across `references/` subdirectory files (core-syntax.md, programming.md, visualization.md).

## Installation

```
/plugin marketplace add knowsuchagency/claude
/plugin install knowsuchagency
```
