---
name: wmill-cli
description: Use the Windmill CLI to manage workspaces, sync resources, and execute scripts/flows. Use this skill when the user asks about "Windmill", "wmill", "wmill cli" or deploying/running Windmill scripts and flows.
---

# Windmill CLI (wmill)

This skill provides guidance for using the Windmill CLI (`wmill`) to interact with Windmill instances.

## Overview

The Windmill CLI allows you to sync your local filesystem with a remote Windmill workspace, run scripts and flows, and manage your configuration. It is the primary tool for developing Windmill resources locally.

## When to Use This Skill

Use the Windmill CLI skill when:
- Syncing local code with a remote Windmill workspace (push/pull)
- Running Windmill scripts or flows from the command line
- Bootstrapping new scripts, flows, or apps
- Managing workspace configurations
- Managing instance-level settings
- Launching a local development server with HMR

## Command Structure

```bash
wmill [COMMAND] [SUBCOMMAND] [OPTIONS]
```

## Global Options

These flags work with most commands:

| Option | Description |
|--------|-------------|
| `--workspace <ws>` | Target a specific workspace (overrides current selection) |
| `--token <token>` | Explicitly provide an auth token |
| `--base-url <url>` | Specify the base URL (requires --token and --workspace) |
| `--debug`, `--verbose` | Enable verbose logging for debugging |
| `--show-diffs` | Show diff information when syncing (may show sensitive info) |
| `--config-dir <dir>` | Custom configuration directory |

Environment variable: `HEADERS='h1: v1, h2: v2'` to add headers to all requests.

---

## Project Initialization

```bash
wmill init                         # Bootstrap project with wmill.yaml
wmill init --use-default           # Use default settings without checking backend
wmill init --use-backend           # Use backend git-sync settings if available
wmill init --repository <repo>     # Specify repository path with --use-backend
wmill init --bind-profile          # Auto-bind workspace profile to current Git branch
```

---

## Workspaces & Configuration

Manage connection to Windmill workspaces.

```bash
wmill workspace add [name] [id] [remote]   # Add a workspace (interactive wizard if no args)
wmill workspace add --create               # Create workspace if it doesn't exist
wmill workspace switch <name>              # Switch to a different configured workspace
wmill workspace remove <name>              # Remove a configured workspace
wmill workspace whoami                     # Show current user, workspace, and base URL

# Git branch binding
wmill workspace bind                       # Bind current Git branch to active workspace
wmill workspace bind --branch <branch>     # Bind specific branch
wmill workspace unbind                     # Remove workspace binding from current branch

# Forking (for development environments)
wmill workspace fork [name] [id]           # Create a forked workspace
wmill workspace delete-fork <fork_name>    # Delete a forked workspace and its git branch
```

---

## Syncing

Sync local files with remote workspace. Main workflow for deploying changes.

### Pull

```bash
wmill sync pull                    # Pull remote resources to local filesystem
wmill sync pull --yes              # Pull without confirmation
wmill sync pull --dry-run          # Show changes without applying
wmill sync pull --show-diffs       # Show diff details
wmill sync pull --plain-secrets    # Pull secrets as plain text
wmill sync pull --json             # Use JSON instead of YAML
```

**Skip options** (exclude from pull):
- `--skip-variables` - Skip variables (including secrets)
- `--skip-secrets` - Skip only secret variables
- `--skip-resources` - Skip resources
- `--skip-resource-types` - Skip resource types
- `--skip-scripts` - Skip scripts
- `--skip-flows` - Skip flows
- `--skip-apps` - Skip apps
- `--skip-folders` - Skip folders
- `--skip-workspace-dependencies` - Skip workspace dependencies

**Include options** (opt-in, not synced by default):
- `--include-schedules` - Include schedules
- `--include-triggers` - Include triggers
- `--include-users` - Include users
- `--include-groups` - Include groups
- `--include-settings` - Include workspace settings
- `--include-key` - Include workspace encryption key

**Filter options**:
- `-i, --includes <patterns>` - Comma-separated glob patterns to include
- `-e, --excludes <patterns>` - Comma-separated glob patterns to exclude
- `--extra-includes <patterns>` - Additional include patterns (adds to wmill.yaml)
- `--repository <repo>` - Specify repository path when multiple exist
- `--promotion <branch>` - Use promotionOverrides from specified branch

### Push

```bash
wmill sync push                    # Push local resources to remote workspace
wmill sync push --yes              # Push without confirmation
wmill sync push --dry-run          # Show changes without applying
wmill sync push --show-diffs       # Show diff details
wmill sync push --message <msg>    # Add message to all updated scripts/flows/apps
wmill sync push --parallel <n>     # Process N changes in parallel
```

Push accepts the same `--skip-*`, `--include-*`, `-i`, `-e`, `--extra-includes`, and `--repository` options as pull.

---

## Scripts

Manage and run scripts.

```bash
# Run a script on remote (use Windmill path, no extension)
wmill script run <path>                    # e.g., wmill script run u/myuser/my_script
wmill script run <path> -d '{"arg": 1}'    # With JSON input data
wmill script run <path> -d @input.json     # With input from file
wmill script run <path> -d @-              # With input from stdin
wmill script run <path> --silent           # Only output final result

# Show script details
wmill script show <path>                   # Display script metadata and code

# Create a new script
wmill script bootstrap <path> <language>
# Languages: python3, deno, bun, go, bash, powershell, nativets, php, rust, ansible, csharp
# Example: wmill script bootstrap f/utils/clean_data.py python3
wmill script bootstrap <path> <lang> --summary "My script"
wmill script bootstrap <path> <lang> --description "Detailed description"

# Push a single script (use local file path with extension)
wmill script push <local_file_path>        # e.g., wmill script push u/myuser/my_script.py

# Re-generate metadata (lock file and schema)
wmill script generate-metadata             # All scripts
wmill script generate-metadata <script>    # Specific script
wmill script generate-metadata --lock-only
wmill script generate-metadata --schema-only
wmill script generate-metadata --dry-run
wmill script generate-metadata -i "f/**"   # Only matching patterns

# Options
wmill script --show-archived               # Include archived scripts in output
```

---

## Flows

Manage and run flows.

```bash
# Run a flow
wmill flow run <path>                      # Run a flow by path
wmill flow run <path> -d '{"arg": 1}'      # With JSON input
wmill flow run <path> --silent             # Only output final result

# Create a new flow
wmill flow bootstrap <flow_path>           # Create empty flow template

# Push a flow (requires both file path and remote path)
wmill flow push <file_path> <remote_path>

# Re-generate lock files for inline scripts
wmill flow generate-locks                  # All flows
wmill flow generate-locks <flow>           # Specific flow
wmill flow generate-locks --yes            # Skip confirmation
wmill flow generate-locks -i "f/**"        # Only matching patterns
```

---

## Apps

Manage Windmill apps.

```bash
# Push an app
wmill app push <file_path> <remote_path>

# Create a new raw app from template
wmill app new

# Start development server for building apps
wmill app dev
wmill app dev --port <port>                # Specify port
wmill app dev --host <host>                # Specify host (default: localhost)
wmill app dev --entry <file>               # Entry point (default: index.ts or index.tsx)
wmill app dev --no-open                    # Don't auto-open browser

# Lint an app folder
wmill app lint                             # Lint current directory
wmill app lint <app_folder>                # Lint specific folder

# Generate documentation files from remote
wmill app generate-agents                  # Regenerate AGENTS.md and DATATABLES.md
wmill app generate-agents <app_folder>

# Re-generate lock files for app runnables
wmill app generate-locks
wmill app generate-locks <app_folder>
```

---

## Resources

Manage Windmill resources (API keys, configurations, etc.)

```bash
# Push a resource file to Windmill
wmill resource push <file_path> <remote_path>
```

To access resources in scripts, use the Windmill SDK:
```python
# Python
resource = wmill.get_resource("u/myuser/my_resource")
```

---

## Resource Types

Manage resource type definitions.

```bash
wmill resource-type list                   # List all resource types
wmill resource-type push <file> <name>     # Push a resource type definition
wmill resource-type generate-namespace     # Generate TypeScript RT namespace from resource types
```

---

## Variables

Manage Windmill variables.

```bash
# Push a variable from file
wmill variable push <file_path> <remote_path>
wmill variable push <file> <path> --plain-secrets    # Push secrets as plain text

# Create/update a variable directly
wmill variable add <value> <remote_path>
wmill variable add <value> <path> --plain-secrets
```

---

## Schedules & Triggers

```bash
wmill schedule push <file_path> <remote_path>    # Push a schedule
wmill trigger push <file_path> <remote_path>     # Push a trigger
```

---

## Folders

```bash
wmill folder push <file_path> <remote_path>      # Push a folder configuration
```

---

## Development Server

```bash
wmill dev                          # Start dev server with HMR
wmill dev --includes <pattern>     # Filter paths with glob pattern
```

---

## Instance Management

Manage Windmill instances (for multi-instance setups).

```bash
wmill instance add [name] [remote] [token]   # Add a new instance
wmill instance remove <instance>             # Remove an instance
wmill instance switch <instance>             # Switch current instance
wmill instance whoami                        # Show current instance info

# Sync instance-level settings
wmill instance pull                          # Pull settings, users, configs, groups
wmill instance push                          # Push settings, users, configs, groups
```

---

## Git-Sync Settings

Manage git-sync settings between local wmill.yaml and backend.

```bash
wmill gitsync-settings pull                  # Pull settings from backend to wmill.yaml
wmill gitsync-settings push                  # Push settings from wmill.yaml to backend
```

---

## Workers & Queues

Monitor and manage workers.

```bash
wmill workers                                # List all workers by worker group
wmill workers --instance <name>              # For specific instance

wmill worker-groups pull                     # Pull worker group configs
wmill worker-groups push                     # Push worker group configs

wmill queues                                 # List all queues with metrics
wmill queues <workspace>                     # Filter by workspace
```

---

## Dependencies

Manage workspace dependencies.

```bash
wmill dependencies push <file_path>          # Push workspace dependencies from file
wmill deps push <file_path>                  # Alias
```

---

## Jobs

Import and export jobs.

```bash
wmill jobs pull                              # Pull completed and queued jobs
wmill jobs pull <workspace>                  # From specific workspace
wmill jobs push                              # Push jobs to workspace
wmill jobs push <workspace>
```

---

## User Management

```bash
wmill user add <email> [password]            # Create a user
wmill user remove <email>                    # Delete a user
wmill user create-token                      # Create an API token
wmill user create-token --email <e> --password <p>
```

---

## Hub (Experimental)

```bash
wmill hub pull                               # Pull definitions from hub (experimental, internal)
```

---

## Version & Upgrade

```bash
wmill version                                # Show version information
wmill --version                              # Same as above

wmill upgrade                                # Upgrade to latest version
wmill upgrade --version <ver>                # Upgrade to specific version
wmill upgrade --list-versions                # Show available versions
wmill upgrade --force                        # Replace even if up-to-date
```

---

## Shell Completions

```bash
wmill completions bash                       # Generate bash completions
wmill completions zsh                        # Generate zsh completions
wmill completions fish                       # Generate fish completions

# Enable completions (add to ~/.bashrc or equivalent):
source <(wmill completions bash)
```

---

## Common Usage Patterns

### Initial Setup

```bash
# 1. Connect to your instance
wmill workspace add

# 2. Initialize project
wmill init

# 3. Download existing scripts and resources
wmill sync pull
```

### Creating and Deploying a Script

```bash
# 1. Create file
wmill script bootstrap u/myuser/hello.py python3

# 2. Edit the file locally...

# 3. Generate metadata (lock file)
wmill script generate-metadata u/myuser/hello.py

# 4. Test run on remote
wmill script run u/myuser/hello

# 5. Deploy
wmill script push u/myuser/hello.py
# OR
wmill sync push
```

### Safe Deployment Workflow

```bash
# Preview changes
wmill sync push --dry-run --show-diffs

# Deploy with confirmation
wmill sync push

# Deploy without confirmation (CI/CD)
wmill sync push --yes
```

---

## Troubleshooting

### Authentication Issues
If commands fail with auth errors:
1. Check current status: `wmill workspace whoami`
2. Refresh credentials: `wmill workspace add` (can overwrite existing)

### Sync Conflicts
If unsure about changes:
- Use `--dry-run` to preview changes
- Use `--show-diffs` to see detailed diffs

### Path Arguments
- **For `run` and `show` commands**: Use the Windmill path WITHOUT file extension
  - Example: `wmill script run u/myuser/my_script`
- **For `push` commands**: Use the local file path WITH extension
  - Example: `wmill script push u/myuser/my_script.py`
- **For `flow push` and `resource push`**: Both file path AND remote path required
  - Example: `wmill flow push ./my_flow.yaml f/folder/my_flow`
