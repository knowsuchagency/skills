---
name: mise
description: >
  Comprehensive guide for mise (mise-en-place), a polyglot dev tool manager, environment variable manager, and task runner.
  Use this skill whenever the user mentions mise, .tool-versions, mise.toml, tool version management, or needs help with:
  managing development tool versions (node, python, ruby, go, java, rust, etc.), setting up project environments,
  configuring mise tasks, writing mise.toml configuration, using mise backends (aqua, cargo, github, npm, pipx, go, http),
  setting up CI/CD with mise, Docker integration, shims vs PATH activation, environment variables with mise,
  secrets management with sops/age, or migrating from asdf/nvm/pyenv/rbenv. Also use when the user asks about
  tool version managers, polyglot version management, or replacing Makefiles/npm scripts with a task runner.
---

# mise (mise-en-place)

mise is a polyglot tool version manager (replacing asdf, nvm, pyenv, rbenv), environment variable manager (replacing direnv), and task runner (replacing make, npm scripts). It's written in Rust for speed and works across macOS, Linux, and Windows.

## Quick Reference

### Installation
```sh
curl https://mise.run | sh                    # Universal
brew install mise                              # macOS
apt install mise                               # Ubuntu/Debian
mise activate zsh >> ~/.zshrc                  # Shell activation (zsh)
eval "$(mise activate bash)" >> ~/.bashrc      # Shell activation (bash)
mise activate fish | source >> ~/.config/fish/config.fish  # Fish
```

### Essential Commands
```sh
mise use node@22                  # Install + activate + update mise.toml (project)
mise use -g python@3.12           # Install globally
mise install                      # Install all tools from config
mise ls                           # List installed tools
mise x node@20 -- node app.js    # One-off execution
mise run build                    # Run a task
mise watch build                  # Watch + run task on changes
mise outdated                     # Check for updates
mise upgrade                      # Upgrade tools
mise doctor                       # Diagnose issues
mise trust                        # Trust a config file
mise self-update                  # Update mise itself
```

## Configuration Files

mise reads config files hierarchically (most specific wins):

```
~/.config/mise/config.toml        # Global config
~/work/mise.toml                  # Workspace
~/work/project/mise.toml          # Project (highest priority)
~/work/project/.tool-versions     # Legacy asdf format (also supported)
```

Also supports idiomatic files: `.node-version`, `.ruby-version`, `.python-version`, `.go-version`, `.java-version`.

### mise.toml Format

```toml
min_version = "2024.9.5"

[tools]
node = "22"                       # Fuzzy version (latest 22.x)
python = "3.12.0"                 # Exact version
ruby = "latest"                   # Latest available
go = "prefix:1.21"                # Prefix matching
"npm:prettier" = "latest"         # npm backend
"cargo:eza" = "latest"            # Cargo backend
"pipx:black" = "latest"           # pipx backend
"github:BurntSushi/ripgrep" = "latest"  # GitHub releases

[env]
NODE_ENV = "development"
DATABASE_URL = "postgres://localhost/mydb"
_.path = ["./node_modules/.bin", "./bin"]   # Prepend to PATH
_.file = ".env"                             # Load .env file
_.python.venv = { path = ".venv", create = true }  # Auto-create venv

[tasks]
build = "npm run build"
test = "npm test"
lint = { run = "eslint src/", depends = ["build"] }

[plugins]
# Custom plugin sources (rarely needed)
my-tool = "https://github.com/org/mise-my-tool"
```

### .tool-versions Format (asdf-compatible)
```
node 22.0.0
python 3.12.0
ruby 3.3.0
```

## Tool Version Management

### Version Specifiers
- `22` or `22.1` — Fuzzy match (latest matching installed; installs latest available)
- `22.1.0` — Exact version
- `latest` — Latest available version
- `prefix:1.21` — Prefix match (useful for Go <=1.20)
- `lts` — Latest LTS (Node.js)
- `system` — Use system-installed version
- `path:/custom/path` — Custom installation path

### Multiple Versions
```toml
[tools]
python = ["3.11", "3.12"]   # First is default; both available as python3.11, python3.12
```

### OS-Specific Tools
```toml
[tools]
ripgrep = { version = "latest", os = ["linux", "macos"] }
```

### Postinstall Commands
```toml
[tools]
node = { version = "22", postinstall = "corepack enable" }
```

## Backends

mise supports multiple backends for installing tools. For details on specific backends, read `references/backends.md`.

| Backend | Syntax | Example |
|---------|--------|---------|
| Core/Registry | `tool` | `node`, `python`, `ruby` |
| aqua | `aqua:owner/repo` | `aqua:BurntSushi/ripgrep` |
| GitHub | `github:owner/repo` | `github:cli/cli` |
| Cargo | `cargo:crate` | `cargo:eza` |
| npm | `npm:package` | `npm:prettier` |
| pipx | `pipx:package` | `pipx:black` |
| Go | `go:module` | `go:github.com/DarthSim/hivemind` |
| HTTP | `http:name` | `http:my-tool` (requires url option) |

Short names (e.g., `node`, `ripgrep`, `terraform`) are resolved via the mise registry, which maps them to the best backend automatically.

## Environment Variables

```toml
[env]
# Static values
API_KEY = "abc123"

# Load from file
_.file = ".env"
_.file = [".env", ".env.local"]

# PATH manipulation
_.path = ["./bin", "./node_modules/.bin"]

# Python virtualenv
_.python.venv = { path = ".venv", create = true }

# Templates
PROJECT = "{{ config_root | basename }}"
HOME_DIR = "{{ env.HOME }}"
```

### Environment Profiles
```sh
# Activate a profile
MISE_ENV=staging mise install

# Or in settings
mise settings env=staging
```
This loads `mise.staging.toml` or `.mise.staging.toml` in addition to the base config.

## Tasks

mise provides a task runner that replaces make/npm scripts. For comprehensive task documentation, read `references/tasks.md`.

### TOML Tasks (inline in mise.toml)
```toml
[tasks]
build = "npm run build"
test = { run = "npm test", depends = ["build"] }
dev = { run = "npm run dev", sources = ["src/**/*"], outputs = ["dist/**/*"] }

[tasks.deploy]
run = """
npm run build
aws s3 sync dist/ s3://my-bucket
"""
depends = ["test"]
env = { NODE_ENV = "production" }
```

### File Tasks (standalone scripts in mise-tasks/ or .mise/tasks/)
```bash
#!/usr/bin/env bash
#MISE description="Run database migrations"
#MISE depends=["build"]
#USAGE flag "-e --env <env>" help="Target environment" default="dev"

set -euo pipefail
echo "Running migrations for ${usage_env}..."
```

### Running Tasks
```sh
mise run build                    # Run single task
mise run build test               # Run multiple tasks
mise run build -- --verbose       # Pass args to task
mise watch build                  # Watch mode (requires watchexec)
mise run lint ::: test            # Run lint and test in parallel
```

## Activation Methods

### 1. Shell Activation (recommended for interactive use)
```sh
eval "$(mise activate bash)"     # In ~/.bashrc
eval "$(mise activate zsh)"      # In ~/.zshrc
mise activate fish | source      # In config.fish
```
Updates PATH on each prompt. Full feature support including hooks.

### 2. Shims (recommended for IDEs and non-interactive)
```sh
eval "$(mise activate --shims)"  # Add to shell profile
# Or manually:
export PATH="$HOME/.local/share/mise/shims:$PATH"
```
Shims are symlinks that resolve the correct tool version on each invocation. Limitation: env vars from mise.toml are only available to tools, not the shell itself.

### 3. Explicit Execution
```sh
mise exec -- node app.js         # Run with mise environment
mise run my-task                  # Run a task
mise en                           # Enter mise environment subshell
```

## Language-Specific Guides

For detailed language configuration (Node.js, Python, Ruby, Go, Java, Rust, etc.), read `references/languages.md`.

Key patterns:
- **Node.js**: `mise use node@22`, supports `.nvmrc`/`.node-version`, corepack, default packages
- **Python**: `mise use python@3.12`, virtualenv support (`_.python.venv`), uv integration, precompiled binaries
- **Ruby**: `mise use ruby@3.3`, precompiled binaries, default gems, ruby-build/ruby-install
- **Go**: `mise use go@1.22`, default packages, GOROOT/GOBIN management
- **Java**: `mise use java@temurin-21`, vendor prefixes, `.sdkmanrc` support
- **Rust**: `mise use rust@1.82`, uses rustup, components/targets/profiles

## Settings

Configure via `mise settings key=value`, `~/.config/mise/config.toml`, or env vars (`MISE_*`).

Key settings:
```sh
mise settings auto_install=true           # Auto-install missing tools
mise settings jobs=8                       # Parallel install jobs
mise settings experimental=true            # Enable experimental features
mise settings pin=true                     # Pin versions in mise.toml
mise settings trusted_config_paths=~/work  # Auto-trust configs
mise settings python.compile=true          # Compile Python from source
mise settings node.corepack=true           # Enable corepack for Node
```

For the full settings reference, read `references/settings.md`.

## CI/CD Integration

### GitHub Actions
```yaml
steps:
  - uses: actions/checkout@v6
  - uses: jdx/mise-action@v3
  - run: mise run test
```

### Generic CI
```sh
curl https://mise.run | sh
export PATH="$HOME/.local/bin:$PATH"
mise install
mise exec -- npm test
```

### Docker
```dockerfile
FROM debian:12-slim
RUN apt-get update && apt-get -y install curl git ca-certificates && rm -rf /var/lib/apt/lists/*
ENV MISE_DATA_DIR="/mise" MISE_INSTALL_PATH="/usr/local/bin/mise" PATH="/mise/shims:$PATH"
RUN curl https://mise.run | sh
COPY mise.toml .
RUN mise install
```

## Hooks

```toml
[hooks]
enter = "echo 'Entered {{config_root}}'"      # On directory entry
cd = "echo 'Changed to {{cwd}}'"              # On cd
leave = "echo 'Left project'"                  # On directory exit
preinstall = "echo 'About to install'"         # Before tool install
postinstall = "echo 'Installed'"               # After tool install
```

## Lockfiles

Create a lockfile for reproducible builds:
```sh
touch mise.lock
mise install     # Populates mise.lock with exact versions + checksums
```
Commit `mise.lock` to version control. Use `mise settings locked=true` to require lockfile entries.

## Security & Trust

mise requires explicit trust for config files that use potentially dangerous features:
```sh
mise trust                        # Trust mise.toml in current directory
mise trust --all                  # Trust all configs in directory tree
mise trust ~/project/mise.toml    # Trust specific file
```

Settings for security:
- `paranoid` — Extra security checks
- `github_attestations` — Verify GitHub artifact attestations
- `aqua.cosign` — Cosign signature verification
- `aqua.slsa` — SLSA provenance verification

## Troubleshooting

```sh
mise doctor                       # Comprehensive diagnostics
MISE_DEBUG=1 mise install         # Debug output
MISE_TRACE=1 mise install         # Trace-level output
mise cache clear                  # Clear cached data
mise self-update                  # Update mise
mise implode                      # Remove everything (nuclear option)
```

Common issues:
- **Wrong version**: Check `mise ls`, `which -a node`, ensure mise is last in shell rc
- **Rate limiting**: Set `MISE_GITHUB_TOKEN` or `GITHUB_TOKEN`
- **Activation issues**: `mise activate` must be in rc files (interactive shells), not profile files
- **Auto-install not working**: At least one version of the tool must be installed first

## Reference Files

For deeper information on specific topics, read these reference files:
- `references/backends.md` — Detailed backend configuration (aqua, github, cargo, npm, pipx, go, http)
- `references/tasks.md` — Complete task system documentation (TOML tasks, file tasks, arguments, templates)
- `references/languages.md` — Language-specific configuration guides
- `references/settings.md` — Full settings reference
- `references/cli.md` — Complete CLI command reference
