---
name: codex-cli
description: Use the OpenAI Codex coding agent via CLI in non-interactive mode. Only use this skill when the user explicitly mentions "Codex", "Codex CLI", or specifically requests to use the Codex agent for a task. Do not use this skill for general coding requests unless the user explicitly asks for Codex.
---

# Codex CLI - Non-Interactive Mode

This skill provides guidance for using the OpenAI Codex coding agent via command-line interface in non-interactive mode.

## Overview

Codex CLI is a command-line coding agent that can execute development tasks, generate code, edit files, and perform various coding operations. In non-interactive mode, Codex executes a single task and returns results without entering an interactive session.

## When to Use This Skill

Use the Codex CLI skill when:
- User requests code generation or modification tasks
- File operations need to be performed programmatically
- Development workflows should be automated via Codex
- One-shot coding tasks need execution without interactive sessions
- The task requires agentic coding capabilities with configurable safety controls

## Command Structure

### Non-Interactive Execution (Primary Pattern)

```bash
codex exec [OPTIONS] <PROMPT>
codex e [OPTIONS] <PROMPT>    # Short alias
```

The `exec` command runs Codex non-interactively with a single prompt.

### Interactive Mode (Default)

```bash
codex [OPTIONS] [PROMPT]
```

When no subcommand is specified, Codex enters interactive mode. Options are forwarded to the interactive CLI.

## Core Options

### Model Selection

```bash
codex exec -m <MODEL> "task description"
codex exec --model gpt-5-codex "task description"
```

Specify which model to use for the task.

**Available models:**
- `gpt-5-codex`: Optimized for coding tasks with many tools. Best choice for development work, file operations, and tasks requiring tool usage.
- `gpt-5`: Broad world knowledge with strong general reasoning. Better for tasks requiring deep understanding or complex reasoning beyond coding.

#### Open Source Models

```bash
codex exec --oss "task description"
```

Convenience flag to use local open source models via Ollama. Verifies that a local Ollama server is running.

### Working Directory

```bash
codex exec -C /path/to/project "task description"
codex exec --cd /path/to/project "task description"
```

Specify the working directory for the agent.

### Skip Git Repository Check

```bash
codex exec --skip-git-repo-check "task description"
```

Skip the git repository trust verification. Required when running Codex outside of git repositories or in untrusted directories.

**When to use:**
- Running Codex from your home directory or other non-git locations
- Quick one-off queries that don't require a git repository
- Working in directories that aren't marked as trusted

### Image Attachments

```bash
codex exec -i screenshot.png "analyze this UI mockup"
codex exec -i img1.png -i img2.png "compare these designs"
```

Attach one or more images to the initial prompt for visual analysis.

## Sandbox and Approval Configuration

### Sandbox Policies

Control the file system access level for command execution:

```bash
codex exec -s read-only "analyze codebase"
codex exec -s workspace-write "refactor authentication"
codex exec -s danger-full-access "system-wide configuration"
```

**Sandbox modes:**
- `read-only`: Commands can only read files, no write access
- `workspace-write`: Commands can write within the workspace directory
- `danger-full-access`: Full system access (use with extreme caution)

### Approval Policies

Configure when the agent requires human approval:

```bash
codex exec -a untrusted "task"      # Ask for untrusted commands
codex exec -a on-failure "task"     # Ask only if execution fails
codex exec -a on-request "task"     # Model decides when to ask
codex exec -a never "task"          # Never ask for approval
```

**Approval policies:**
- `untrusted`: Only run trusted commands (ls, cat, sed) without approval. Escalates for untrusted commands.
- `on-failure`: Run all commands without approval. Only asks if execution fails.
- `on-request`: The model decides when to ask for approval.
- `never`: Never ask for approval. Execution failures are returned to the model immediately.

### Convenience Flags

#### Full Auto Mode

```bash
codex exec --full-auto "task description"
```

Equivalent to `-a on-failure --sandbox workspace-write`. Enables low-friction sandboxed automatic execution.

#### Bypass All Safety (DANGEROUS)

```bash
codex exec --dangerously-bypass-approvals-and-sandbox "task"
```

⚠️ **EXTREMELY DANGEROUS**: Skips all confirmation prompts and executes commands without sandboxing. Intended solely for environments that are externally sandboxed (e.g., containers, VMs).

## Configuration Management

### Override Configuration Values

```bash
codex exec -c model="o3" "task"
codex exec -c 'sandbox_permissions=["disk-full-read-access"]' "task"
codex exec -c shell_environment_policy.inherit=all "task"
```

Override configuration values from `~/.codex/config.toml`:
- Use dotted paths for nested values (`foo.bar.baz`)
- Values are parsed as JSON; if parsing fails, treated as literal strings
- Can specify multiple `-c` flags

### Configuration Profiles

```bash
codex exec -p production "task"
codex exec --profile development "task"
```

Load a configuration profile from `config.toml` to specify default options.

## Web Search

```bash
codex exec --search "research best practices for React state management"
```

Enable web search (off by default). When enabled, the native `web_search` tool is available to the model without per-call approval.

## Common Usage Patterns

### Safe Code Analysis (Read-Only)

```bash
codex exec -s read-only "analyze the code quality in src/ and suggest improvements"
```

### Automated Refactoring (Workspace Write)

```bash
codex exec -s workspace-write -a on-failure "refactor all API endpoints to use async/await"
```

### Quick Fix with Auto-Approval

```bash
codex exec --full-auto "fix ESLint errors in components/"
```

### Code Generation with Specific Model

```bash
codex exec -m gpt-5-codex "create a REST API with authentication using Express.js"
```

### Multi-Image Analysis

```bash
codex exec -i wireframe.png -i screenshot.png "compare this wireframe with the current implementation"
```

### Project-Specific Task

```bash
codex exec -C ~/projects/myapp "add unit tests for the UserService class"
```

### Research-Driven Development

```bash
codex exec --search "implement OAuth2 authentication following current best practices"
```

### Local Open Source Model

```bash
codex exec --oss "document all functions in utils.py"
```

### Custom Configuration

```bash
codex exec -c model="o3" -c 'sandbox_permissions=["disk-full-read-access"]' "task"
```

### Quick Query Outside Git Repository

```bash
codex exec --skip-git-repo-check -s read-only "explain how to configure VS Code keybindings"
```

## Other Commands

### Apply Diffs

```bash
codex apply
codex a    # Short alias
```

Apply the latest diff produced by Codex agent as a `git apply` to your local working tree.

### Resume Sessions

```bash
codex resume              # Picker to select session
codex resume --last       # Continue most recent session
```

Resume a previous interactive session.

### Authentication

```bash
codex login    # Manage login credentials
codex logout   # Remove stored authentication
```

### MCP Server (Experimental)

```bash
codex mcp
```

Run Codex as an MCP server and manage MCP servers.

### Protocol Stream

```bash
codex proto    # Run protocol stream via stdin/stdout
codex p        # Short alias
```

### Shell Completion

```bash
codex completion
```

Generate shell completion scripts.

### Debug Commands

```bash
codex debug
```

Internal debugging commands.

## Best Practices

### Task Descriptions

- Be specific and actionable with clear objectives
- Include context about the codebase or project
- Specify file paths for targeted operations
- Mention constraints, requirements, or preferred approaches

**Good examples:**
```bash
codex exec --full-auto "add error handling to all database queries in src/models/, wrapping them in try-catch blocks with proper logging"
```

```bash
codex exec -s workspace-write "create a responsive navigation component using TypeScript and Tailwind CSS, with mobile hamburger menu"
```

**Avoid vague prompts:**
```bash
codex exec "fix bugs"              # Too vague
codex exec "improve performance"   # Unclear objective
```

### Security and Safety

**Choose appropriate sandbox levels:**
- Use `read-only` for analysis, auditing, or when testing unfamiliar code
- Use `workspace-write` for most development tasks within a project
- Use `danger-full-access` only when system-wide changes are required
- Never use `--dangerously-bypass-approvals-and-sandbox` except in externally sandboxed environments

**Choose appropriate approval policies:**
- Use `untrusted` (default) for maximum safety
- Use `on-failure` with `--full-auto` for efficient development workflows
- Use `on-request` to let the model handle approval decisions
- Use `never` only in controlled, automated environments

**Recommended safe automation:**
```bash
codex exec --full-auto "task"    # Balanced: workspace-write + on-failure
```

### Working Directory Management

Always specify `-C/--cd` when working on a specific project:
```bash
codex exec -C ~/work/project "task"
```

This ensures the agent operates in the correct context.

### Model Selection Strategy

- Use `gpt-5-codex` (default) for coding, development, and tool-heavy tasks
- Use `gpt-5` for tasks requiring deep reasoning, complex problem-solving, or broad world knowledge
- Use `--oss` for privacy-sensitive work or offline development with local Ollama models
- The model choice depends on whether the task is primarily coding-focused or reasoning-focused

### Configuration Management

Store frequently used settings in `~/.codex/config.toml`:
- Create profiles for different workflows (development, production, research)
- Use `-p/--profile` to switch between configurations
- Use `-c/--config` for one-off overrides

### Image Usage

Attach images when visual context is helpful:
- UI mockups and designs for implementation
- Screenshots of errors or bugs
- Diagrams or architecture drawings
- Multiple images for comparison or context

## Integration Examples

### CI/CD Pipeline

```bash
#!/bin/bash
# Automated code formatting in CI
codex exec --full-auto -C "$CI_PROJECT_DIR" "format all TypeScript files according to Prettier standards"
```

### Pre-Commit Hook

```bash
#!/bin/bash
# Check for common issues before commit
codex exec -s read-only "analyze staged files for potential bugs or security issues"
```

### Build Script Integration

```bash
#!/bin/bash
# Generate documentation
codex exec -s workspace-write -C ./src "generate API documentation for all exported functions"
```

### Automated Testing

```bash
# Generate tests for new features
codex exec --full-auto "write unit tests for all functions added in the last commit"
```

## Troubleshooting

### Approval Prompts Blocking Automation

**Issue:** Task requires approval in automated scripts
**Solution:** Use appropriate approval policy
```bash
codex exec -a on-failure "task"    # Only ask on failures
codex exec -a never "task"         # Never ask (use with caution)
```

### Sandbox Restrictions

**Issue:** Command fails due to insufficient permissions
**Solution:** Adjust sandbox policy
```bash
codex exec -s workspace-write "task"      # Allow workspace writes
codex exec -s danger-full-access "task"   # Allow full access (careful!)
```

### Model Access Issues

**Issue:** Specific model not available
**Solution:** Check available models and use `--oss` for local models
```bash
codex exec --oss "task"    # Use local Ollama models
```

### Working Directory Confusion

**Issue:** Agent operates in wrong directory
**Solution:** Always specify working directory explicitly
```bash
codex exec -C /path/to/project "task"
```

### Configuration Conflicts

**Issue:** Settings conflict between command-line and config file
**Solution:** Use `-c` to override specific values
```bash
codex exec -c model="gpt-4" -p production "task"
```

### Git Repository Trust Error

**Issue:** Error message "Not inside a trusted directory and --skip-git-repo-check was not specified"
**Solution:** Use `--skip-git-repo-check` flag when running outside git repositories
```bash
codex exec --skip-git-repo-check "task"
```

This error occurs when:
- Running Codex from home directory or non-git locations
- The current directory is not a git repository
- The directory hasn't been marked as trusted

## Version and Help

```bash
codex --version    # Check installed version
codex -V          # Short form

codex --help      # Show full help
codex -h          # Show help summary

codex exec --help # Help for exec command
```

## Configuration File Location

Codex configuration is stored in:
```
~/.codex/config.toml
```

Create profiles, set defaults, and configure preferences in this file to avoid repetitive command-line flags.

## Safety Reminders

⚠️ **Critical Safety Notes:**
- Review generated code before deploying to production
- Use appropriate sandbox and approval settings for the task
- Never use `--dangerously-bypass-approvals-and-sandbox` in development environments
- Test with `read-only` sandbox first when working with unfamiliar codebases
- Keep credentials and sensitive data out of prompts
- Use `--full-auto` as the default for efficient, safe automation

## Comparison with Interactive Mode

**Use `codex exec` when:**
- Automating tasks in scripts or CI/CD
- Running one-off commands
- Integrating with other tools
- Need predictable, non-interactive behavior

**Use interactive mode when:**
- Exploring solutions iteratively
- Need back-and-forth conversation
- Complex tasks requiring clarification
- Learning or experimentation
