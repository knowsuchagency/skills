---
name: gemini-cli
description: Use the Gemini coding agent via CLI in non-interactive mode. Only use this skill when the user explicitly mentions "Gemini", "Gemini CLI", or specifically requests to use the Gemini agent for a task. Do not use this skill for general coding requests unless the user explicitly asks for Gemini.
---

# Gemini CLI - Non-Interactive Mode

This skill provides guidance for using the Gemini coding agent via command-line interface in non-interactive mode.

## Overview

Gemini CLI is a command-line coding agent that can execute development tasks, generate code, edit files, and perform various coding operations. In non-interactive mode, Gemini executes a single task and returns results without entering an interactive session.

## When to Use This Skill

Use the Gemini CLI skill when:
- User requests code generation or modification tasks
- File operations need to be performed programmatically
- Development workflows should be automated
- One-shot coding tasks need execution without interactive sessions
- The task requires agentic coding capabilities beyond simple script execution

## Basic Command Structure

The primary pattern for non-interactive usage:

```bash
gemini [query...]
```

For positional prompts (recommended):
```bash
gemini "your task description here"
```

Legacy format (deprecated but still functional):
```bash
gemini -p "your task description here"
```

## Key Options

### Model Selection
```bash
gemini -m <model-name> "task description"
gemini -m gemini-2.5-pro "task description"
gemini -m gemini-2.5-flash "task description"
```
Specify which model to use for the task.

**Available models:**
- `gemini-2.5-pro`: More capable model with enhanced reasoning and performance for complex tasks
- `gemini-2.5-flash`: Faster, more efficient model optimized for speed and cost-effectiveness

### YOLO Mode (Auto-approve All Actions)
```bash
gemini -y "task description"
```
```bash
gemini --yolo "task description"
```
Automatically accepts all actions without prompting. Use with caution.

### Approval Modes
```bash
gemini --approval-mode default "task"      # Prompt for approval (default)
gemini --approval-mode auto_edit "task"    # Auto-approve edit tools only
gemini --approval-mode yolo "task"         # Auto-approve all tools
```

### Output Format
```bash
gemini -o text "task"    # Human-readable text output (default)
gemini -o json "task"    # JSON-formatted output for parsing
```

### Sandbox Execution
```bash
gemini -s "task description"              # Enable sandbox mode
gemini -s --sandbox-image <uri> "task"    # Specify custom sandbox image
```
Run tasks in an isolated sandbox environment for security.

### Extensions
```bash
gemini -e extension1 -e extension2 "task"    # Use specific extensions
gemini -l                                     # List available extensions
```

### Debug Mode
```bash
gemini -d "task description"
gemini --debug "task description"
```
Run with additional debugging information.

## Common Usage Patterns

### Code Generation
```bash
gemini "create a Python script that processes CSV files and generates a summary report"
```

### File Editing
```bash
gemini "refactor the authentication logic in src/auth.py to use JWT tokens"
```

### Auto-approve File Edits
```bash
gemini --approval-mode auto_edit "fix all linting errors in the current directory"
```

### Project Setup
```bash
gemini "set up a new React TypeScript project with Tailwind CSS"
```

### Bug Fixing
```bash
gemini "debug and fix the memory leak in server.js"
```

### Documentation
```bash
gemini "add JSDoc comments to all functions in utils.js"
```

### Testing
```bash
gemini "write unit tests for the UserService class using Jest"
```

### JSON Output for Automation
```bash
gemini -o json "analyze the codebase and list all TODO comments" | jq '.results'
```

### Real-World Examples (Tested)
```bash
# Add docstring with auto-approval (safe for documentation tasks)
gemini --model gemini-2.5-flash --approval-mode auto_edit "add a detailed docstring to the serve() function explaining what it does"

# Quick information query with JSON output
gemini --model gemini-2.5-flash -o json "what is the GPU type used in this configuration?" | jq -r '.response'

# Simple code annotation with YOLO mode
gemini --model gemini-2.5-flash --yolo "add a type hint comment to the MINUTES constant explaining it represents seconds per minute"

# Analysis task with clean output parsing
gemini --model gemini-2.5-flash "count the number of import statements" 2>/dev/null | jq -r '.response'

# Debug mode to understand execution flow
gemini --model gemini-2.5-flash --debug "analyze function structure" 2>&1 | head -50
```

## Working with Specific Directories

### Include Additional Directories
```bash
gemini --include-directories /path/to/dir1,/path/to/dir2 "task"
gemini --include-directories /path/to/dir1 --include-directories /path/to/dir2 "task"
```
Add directories to the workspace context beyond the current directory.

## Advanced Options

### Checkpointing (File Edit Safety)
```bash
gemini -c "make extensive refactoring changes"
gemini --checkpointing "make extensive refactoring changes"
```
Enable checkpointing to track file edit history.

### Screen Reader Mode
```bash
gemini --screen-reader "task description"
```
Enable accessibility mode for screen readers.

### Allowed Tools
```bash
gemini --allowed-tools tool1 --allowed-tools tool2 "task"
```
Specify which tools can run without confirmation.

## Best Practices

### Task Descriptions
- Be specific and clear about the desired outcome
- Include relevant context about the codebase or project
- Specify file paths when working with specific files
- Mention any constraints or requirements

**Good examples:**
```bash
gemini "add error handling to the API endpoints in src/api/users.js, wrapping all async operations in try-catch blocks"
```

```bash
gemini "create a responsive navbar component in React with mobile menu support, using Tailwind CSS classes"
```

**Avoid vague prompts:**
```bash
gemini "fix the code"  # Too vague
gemini "make it better"  # Unclear objective
```

### Approval Modes
- Use `default` mode (prompt for approval) when making significant changes
- Use `auto_edit` mode for safe operations like formatting, linting, or documentation
- Use `yolo` mode only for trusted, low-risk tasks or in automated pipelines
- Always review changes after execution, especially in `auto_edit` or `yolo` modes
- **Note**: `--approval-mode auto_edit` works excellently for docstrings, comments, and formatting tasks

### Model Selection
- Use `gemini-2.5-pro` for complex tasks requiring enhanced reasoning and performance
- Use `gemini-2.5-flash` for faster execution and routine tasks where speed is preferred
- Consider cost and latency trade-offs when choosing between models
- **Always specify model explicitly** with `--model` or `-m` flag to ensure consistency

### Output Handling
- Use `-o json` when integrating with scripts or pipelines
- Parse JSON output with tools like `jq` for automation (e.g., `jq -r '.response'`)
- Use text output (default) for human review and interaction
- **JSON output includes valuable stats**: token usage, tool calls, file edits, latency metrics
- Filter stderr with `2>&1` or `2>/dev/null` when parsing JSON to avoid debug messages mixing in

### Execution Flow
- **Positional arguments are preferred** over `-p` flag (which is deprecated)
- Use quotes around task descriptions to avoid shell parsing issues
- Gemini CLI automatically discovers and reads GEMINI.md files (global and project-specific)
- Debug mode (`--debug` or `-d`) reveals memory discovery, IDE connections, and experiment IDs
- The CLI may attempt IDE connection - harmless error if `/tmp/gemini/ide` doesn't exist

### Security Considerations
- Use sandbox mode (`-s`) for untrusted code execution
- Be cautious with `--yolo` mode in production environments
- Review file changes before committing them
- Use checkpointing (`-c`) for complex refactoring tasks

### Performance Tips
- For automation: use `--yolo` or `--approval-mode auto_edit` to avoid interactive prompts
- Combine flags efficiently: `gemini --model gemini-2.5-flash -o json --yolo "task"`
- Add delays between API calls to respect rate limits (2-4 seconds recommended)
- JSON output is more parseable and consistent for scripting than text output

## Integration Examples

### Shell Script Integration
```bash
#!/bin/bash
result=$(gemini -o json "analyze code quality in src/" | jq -r '.summary')
echo "Code Quality: $result"
```

### CI/CD Pipeline
```bash
# Auto-format code in CI
gemini --yolo "format all JavaScript files using Prettier standards"
```

### Pre-commit Hook
```bash
# Validate changes before commit
gemini "check if the changes in staged files maintain backward compatibility"
```

## Troubleshooting

### Task Not Executing
- Verify the task description is clear and actionable
- Check if required files or directories exist
- Ensure proper permissions for file operations
- Use debug mode (`-d`) to see detailed execution logs

### Permission Issues
- Tasks may require confirmation depending on approval mode
- Use `--allowed-tools` to pre-approve specific tools
- Consider using appropriate approval mode for the task

### Output Parsing
- Ensure `-o json` is used when expecting JSON output
- Handle potential errors in JSON parsing
- Check for error messages in the output before processing

### Rate Limiting
- **CRITICAL**: Gemini CLI may hit rate limits, especially with gemini-2.5-flash
- When rate limited, you'll see: `You have exhausted your capacity on this model. Your quota will reset after Xs.`
- The CLI automatically retries with exponential backoff (e.g., 1s, 2s, 3s delays)
- These retries are handled internally - no action needed on your part
- To avoid rate limits: add delays between consecutive calls (e.g., `sleep 2-4` seconds)
- Rate limits are per-model, so switching models won't help immediately

## Common Pitfalls & Quirks

### Output Handling Gotchas
- **Stderr mixing with stdout**: Gemini outputs status messages ("Loaded cached credentials", retry messages) to stdout, not stderr
- When parsing JSON: use `2>/dev/null` to filter actual stderr, but be aware status messages will still appear
- Solution: Either parse around status messages or extract JSON specifically with `jq`

### Rate Limit Behavior
- Rate limit errors appear BEFORE actual output, making them look more severe than they are
- The tool completes successfully after retries - don't treat rate limit messages as failures
- In automation: increase timeouts to account for retry delays (use 120000ms+)

### Approval Modes
- `--approval-mode auto_edit` specifically auto-approves edit operations but may still prompt for other tools
- `--yolo` mode prints "YOLO mode is enabled" but still shows retry messages
- Both modes work as expected - the status messages are informational only

### JSON Output Structure
- Response is in `.response` field (not `.result` or `.output`)
- Stats are comprehensive: includes token counts (with cache hits!), tool call metrics, file edit stats
- The response field may contain multi-line formatted text, including markdown

### Model Flag
- Short form: `-m` or long form: `--model` (both work identically)
- Model name must be exact: `gemini-2.5-flash` or `gemini-2.5-pro`
- No default model is shown in help - always specify explicitly for consistency

## Version Information

To check the Gemini CLI version:
```bash
gemini -v
gemini --version
```

To see all available options:
```bash
gemini -h
gemini --help
```

## Notes on Deprecated Flags

Several flags are deprecated in favor of settings.json configuration:
- `--telemetry*` flags (use settings.json `telemetry.*` settings)
- `--proxy` (use settings.json `proxy` setting)
- `-p/--prompt` (use positional arguments instead)
- `-a/--all-files` (use @ includes in the application)
- `--show-memory-usage` (use settings.json `ui.showMemoryUsage`)
- `-c/--checkpointing` (use settings.json `general.checkpointing.enabled`)
- `--sandbox-image` (use settings.json `tools.sandbox`)

While these flags still work, they will be removed in future versions. Update to use positional arguments and settings.json configuration instead.
