# mise Tasks Reference

## Table of Contents
1. [TOML Tasks](#toml-tasks)
2. [File Tasks](#file-tasks)
3. [Task Arguments (usage spec)](#task-arguments)
4. [Running Tasks](#running-tasks)
5. [Task Configuration Options](#task-configuration-options)
6. [Templates in Tasks](#templates-in-tasks)
7. [Monorepo Support](#monorepo-support)

## TOML Tasks

Define tasks inline in `mise.toml`:

```toml
[tasks]
# Simple command
build = "npm run build"

# Multi-line script
deploy = """
npm run build
aws s3 sync dist/ s3://my-bucket
"""

# Full configuration
[tasks.test]
run = "npm test"
description = "Run test suite"
depends = ["build"]
env = { NODE_ENV = "test" }
dir = "{{config_root}}"
sources = ["src/**/*", "tests/**/*"]
outputs = ["coverage/**/*"]
```

### Task Properties

| Property | Description |
|----------|-------------|
| `run` | Command(s) to execute (string or array of strings) |
| `description` | Human-readable description |
| `depends` | Tasks to run first |
| `depends_post` | Tasks to run after |
| `wait_for` | Tasks that must complete first (but don't trigger) |
| `env` | Environment variables for this task |
| `dir` | Working directory (supports templates) |
| `sources` | Source file globs for change detection |
| `outputs` | Output file globs for change detection |
| `shell` | Override shell for this task |
| `quiet` | Suppress output |
| `silent` | Suppress all output including errors |
| `raw` | Direct I/O passthrough |
| `hide` | Hide from task list |
| `alias` | Alternative task name(s) |
| `file` | External script file to run |

### Multiple Commands
```toml
[tasks.setup]
run = [
  "npm install",
  "npm run build",
  "npm run migrate"
]
```

### Parallel Execution Within a Task
```toml
[tasks.ci]
run = [
  ["npm run lint", "npm run typecheck"],   # These run in parallel
  "npm test"                                # This runs after both complete
]
```

### Conditional Dependencies
```toml
[tasks.deploy]
depends = ["build"]
[tasks.deploy.depends_post]
run = "notify-slack"
```

---

## File Tasks

Standalone scripts in `mise-tasks/` or `.mise/tasks/` directories.

### Basic File Task
```bash
#!/usr/bin/env bash
# mise-tasks/build
set -euo pipefail
npm run build
```

### File Task with Metadata
```bash
#!/usr/bin/env bash
# mise-tasks/deploy
#MISE description="Deploy to production"
#MISE depends=["build", "test"]
#MISE sources=["src/**/*"]
#MISE outputs=["dist/**/*"]
#MISE env={NODE_ENV="production"}
#MISE dir="{{config_root}}"
#MISE hide=false
#MISE raw=false
#MISE quiet=false

set -euo pipefail
echo "Deploying..."
```

### Any Language
```python
#!/usr/bin/env python3
# mise-tasks/analyze
#MISE description="Analyze codebase"
import os
print(f"Analyzing {os.getcwd()}")
```

### Task Directory Structure
```
project/
├── mise.toml              # Can define TOML tasks
├── mise-tasks/            # File tasks directory
│   ├── build              # ./mise-tasks/build
│   ├── test               # ./mise-tasks/test
│   └── deploy/
│       ├── staging        # Task name: deploy:staging
│       └── production     # Task name: deploy:production
└── .mise/
    └── tasks/             # Alternative file tasks directory
        └── lint
```

Subdirectories create namespaced tasks (e.g., `deploy/staging` becomes `mise run deploy:staging`).

### Remote Tasks
```toml
[tasks]
build = { file = "https://example.com/scripts/build.sh" }
lint = { file = "git::https://github.com/org/tasks.git//lint.sh" }
```

---

## Task Arguments

mise integrates with the `usage` spec for CLI-style arguments in file tasks.

### Usage Spec in File Tasks
```bash
#!/usr/bin/env bash
# mise-tasks/greet
#MISE description="Greet a user"
#USAGE flag "-g --greeting <greeting>" help="Greeting word" {
#USAGE   choices "hi" "hello" "hey"
#USAGE }
#USAGE flag "-u --user <user>" help="User to greet"
#USAGE arg "<message>" help="Greeting message"

set -euo pipefail
echo "${usage_greeting}, ${usage_user}! ${usage_message}"
```

Usage:
```sh
mise run greet --user jdx -g hey "How are you?"
mise run greet --help    # Shows auto-generated help
```

### Arguments are Environment Variables
All arguments/flags become env vars prefixed with `usage_`:
- `--greeting hey` → `$usage_greeting = "hey"`
- `--user jdx` → `$usage_user = "jdx"`
- positional `"message"` → `$usage_message = "message"`

### TOML Task Arguments
```toml
[tasks.greet]
run = "echo Hello, $usage_name!"
[tasks.greet.usage]
args = [
  { name = "name", help = "Name to greet" }
]
flags = [
  { name = "loud", short = "l", help = "Use uppercase", type = "bool" }
]
```

### Custom Completions
```bash
#USAGE flag "--dir <dir>" help="Target directory"
#USAGE complete "dir" run="find . -maxdepth 1 -type d"
```

---

## Running Tasks

### Basic Execution
```sh
mise run build                    # Run a task
mise run build test               # Run multiple tasks sequentially
mise run build -- --verbose       # Pass args after --
mise build                        # Shorthand (skip "run" if no command conflict)
```

### Parallel Execution
```sh
mise run lint ::: test            # Run lint and test in parallel
mise run lint ::: test ::: build  # Three tasks in parallel
```

### Watch Mode
```sh
mise watch build                  # Rerun on file changes
mise watch build --glob "src/**/*.rs"  # Watch specific patterns
mise watch build --exts rs,toml   # Filter by extension
mise watch build --clear          # Clear screen before each run
```
Requires `watchexec`: `mise use -g watchexec`

### Dry Run
```sh
mise run build --dry-run          # Show what would run without executing
```

### Task Output Modes
```sh
mise run build --output prefix     # Prefix output with task name
mise run build --output interleave # Interleave output (default)
mise run build --output keep-order # Buffer and show in order
mise run build --output quiet      # Suppress stdout
mise run build --output silent     # Suppress all output
```

Or set globally:
```sh
mise settings task.output=prefix
```

### Task Information
```sh
mise tasks ls                     # List all tasks
mise tasks info build             # Show task details
mise tasks deps                   # Show dependency tree
```

### Source/Output Change Detection
When `sources` and `outputs` are specified, mise skips the task if outputs are newer than sources:

```toml
[tasks.build]
run = "npm run build"
sources = ["src/**/*.ts", "package.json"]
outputs = ["dist/**/*"]
```

Force re-run: `mise run build --force`

---

## Task Configuration Options

### All Task Properties
```toml
[tasks.example]
run = "echo hello"                          # Command(s) to run
description = "Example task"                # Description for task list
alias = "ex"                                # Short alias
depends = ["other-task"]                    # Pre-dependencies
depends_post = ["cleanup"]                  # Post-dependencies
wait_for = ["slow-task"]                    # Wait without triggering
env = { KEY = "value" }                     # Task-specific env vars
dir = "{{config_root}}/subdir"              # Working directory
sources = ["src/**/*"]                      # Source files for caching
outputs = ["dist/**/*"]                     # Output files for caching
shell = "bash -c"                           # Custom shell
quiet = false                               # Suppress stdout
silent = false                              # Suppress all output
raw = false                                 # Direct I/O passthrough
hide = false                                # Hide from `mise tasks ls`
file = "scripts/build.sh"                   # External script file
```

### Task Settings (global)

| Setting | Env Var | Default | Description |
|---------|---------|---------|-------------|
| `task.output` | `MISE_TASK_OUTPUT` | None | Output style |
| `task.timeout` | `MISE_TASK_TIMEOUT` | None | Default timeout |
| `task.timings` | `MISE_TASK_TIMINGS` | None | Show elapsed time |
| `task.skip` | `MISE_TASK_SKIP` | [] | Tasks to skip |
| `task.skip_depends` | `MISE_TASK_SKIP_DEPENDS` | false | Skip dependencies |
| `task.monorepo_depth` | `MISE_TASK_MONOREPO_DEPTH` | 5 | Monorepo search depth |

---

## Templates in Tasks

Tasks support Tera templates (same as mise.toml env vars).

### Available Template Variables
```toml
[tasks.info]
run = """
echo "Config root: {{config_root}}"
echo "CWD: {{cwd}}"
echo "Mise bin: {{mise_bin}}"
echo "Mise data: {{mise_data_dir}}"
echo "Mise config: {{mise_config_dir}}"
"""
```

### Template Functions
- `{{env.VAR_NAME}}` — Environment variable
- `{{config_root}}` — Directory containing the config file
- `{{cwd}}` — Current working directory
- `{{exec(command="cmd")}}` — Execute command and use output
- `{{arch()}}` — System architecture
- `{{os()}}` — Operating system
- `{{os_family()}}` — OS family

---

## Monorepo Support

mise discovers tasks from parent directories and subdirectories automatically.

### Configuration
```toml
# Root mise.toml
[settings]
task.monorepo_depth = 5                      # Search depth
task.monorepo_exclude_dirs = ["vendor"]       # Exclude directories
task.monorepo_respect_gitignore = true        # Honor .gitignore
```

### Namespacing
Tasks from subdirectories are namespaced:
```
project/
├── mise.toml          # tasks: build, test
└── packages/
    ├── api/
    │   └── mise.toml  # tasks: api:build, api:test
    └── web/
        └── mise.toml  # tasks: web:build, web:test
```

```sh
mise run api:build
mise run web:test
```
