# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Claude Code plugin — markdown-based skills that Claude Code loads on demand. No build system, compilation, or test suite; all content is static Markdown.

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

## Versioning

When bumping the version, update **both** files:
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

## Skills

Two categories:
- **Executable skills** — contain Python scripts run via `uv run`, use `fnox` for secrets
- **Reference skills** — pure documentation, CLI guides, or interactive installation workflows
