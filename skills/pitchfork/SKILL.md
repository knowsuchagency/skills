---
name: pitchfork
description: >
  Guide for pitchfork, a daemon/process manager for developers (by jdx, author of mise).
  Use this skill whenever the user mentions pitchfork, pitchfork.toml, or needs help managing
  background processes and long-running dev services: starting/stopping/restarting daemons,
  running a command in the background, viewing daemon logs, defining services in pitchfork.toml,
  auto start/stop on entering/leaving a project directory, ready checks (delay, output, HTTP, TCP),
  file-watch restarts, cron-scheduled tasks, dependency chains between services, auto-restart on
  failure, the pitchfork TUI/web dashboard, boot/supervisor management, or its MCP server. Also
  use when the user wants a lighter alternative to pm2/foreman/overmind/systemd for local dev,
  or wants to prevent duplicate background processes.
---

# Pitchfork

Pitchfork is a "devilishly good" daemon/process manager for developers, written in Rust by
[jdx](https://github.com/jdx) (author of mise). It starts background services only if they're
not already running (no duplicates), auto-restarts on failure with backoff, resolves dependency
chains, and can auto start/stop daemons as you `cd` in and out of a project. Monitor via a
terminal TUI or web dashboard, and integrate with AI assistants through a built-in MCP server.

Docs: https://pitchfork.en.dev — Repo: https://github.com/jdx/pitchfork

## Installation

```sh
mise use -g pitchfork            # Recommended (jdx's own tool)
cargo install pitchfork-cli      # From crates.io
# or download a binary from https://github.com/jdx/pitchfork/releases
pitchfork --version              # Verify
```

### Shell activation (enables auto start/stop + supervisor)

```sh
echo 'eval "$(pitchfork activate bash)"' >> ~/.bashrc                       # Bash
echo 'eval "$(pitchfork activate zsh)"' >> ~/.zshrc                         # Zsh
echo 'pitchfork activate fish | source' >> ~/.config/fish/config.fish       # Fish
```

Optionally start daemons at boot:

```sh
pitchfork boot enable      # Run the supervisor (and boot-marked daemons) at login/startup
pitchfork boot status
pitchfork boot disable
```

## Core commands

```sh
pitchfork run NAME -- CMD...   # Run an ad-hoc command in the background under NAME
pitchfork start [ID...]        # Start configured daemon(s); --all for everything
pitchfork start --all
pitchfork stop [ID...]         # Stop running daemon(s)
pitchfork restart [ID...]      # Restart daemon(s)
pitchfork status ID            # Detailed status of one daemon
pitchfork list                 # List all daemons + state (--hide-header to omit header)
pitchfork logs [ID]            # Tail logs; -n N for lines, -f to follow, omit ID for all
pitchfork wait ID              # Block until the daemon's ready check passes
pitchfork enable ID            # Mark a daemon active (eligible for auto/start --all)
pitchfork disable ID           # Mark a daemon inactive
```

Examples:

```sh
pitchfork run web -- npm run dev          # Background a dev server
pitchfork run api -- ./server --port 8080
pitchfork logs web -f                     # Follow logs
pitchfork wait api && curl localhost:8080 # Wait for ready, then hit it
```

Logs are stored under `~/.local/state/pitchfork/logs`.

## Configuration: `pitchfork.toml`

Define daemons in a `pitchfork.toml` at your project root. Each `[daemons.<id>]` block describes
one service.

```toml
[daemons.postgres]
run = "postgres -D ./data"
auto = ["start", "stop"]        # auto-start on cd-in, auto-stop on cd-out
ready_port = 5432               # ready when this TCP port accepts connections

[daemons.redis]
run = "redis-server"
auto = ["start", "stop"]
ready_output = "Ready to accept connections"   # ready when this string appears in output

[daemons.api]
run = "npm run dev:api"
depends = ["postgres", "redis"] # started after deps are ready (topological order)
ready_http = "http://localhost:8080/health"    # ready when this URL returns success
restart = "on-failure"          # auto-restart with exponential backoff
watch = ["src/**/*.ts"]         # restart when matching files change

[daemons.worker]
run = "npm run worker"
depends = ["redis"]
ready_delay = 2                 # simply wait N seconds, then consider ready

[daemons.cleanup]
run = "./scripts/cleanup.sh"
cron = "0 */5 * * * *"          # run on a cron schedule (sec min hour dom mon dow)
```

### Common daemon keys

| Key            | Purpose                                                              |
|----------------|---------------------------------------------------------------------|
| `run`          | The command to execute.                                             |
| `auto`         | List of lifecycle hooks: `"start"` (on cd-in), `"stop"` (on cd-out). |
| `depends`      | Daemons that must be ready first; resolved topologically, run in parallel. |
| `ready_delay`  | Seconds to wait before marking ready.                              |
| `ready_output` | Output substring/pattern that signals readiness.                  |
| `ready_http`   | HTTP endpoint that must return success.                           |
| `ready_port`   | TCP port that must accept connections.                            |
| `watch`        | Glob patterns; matching file changes trigger a restart.           |
| `cron`         | Cron expression for scheduled runs.                               |
| `restart`      | Restart policy (e.g. `on-failure`) with retry limits + backoff.   |

Manage config entries from the CLI too:

```sh
pitchfork config add ID -- CMD...   # Add a daemon to pitchfork.toml
pitchfork config remove ID          # Remove a daemon from config
```

## Auto start/stop

With shell activation in place, mark daemons `auto = ["start", "stop"]`. Entering the project
directory starts them; leaving stops them — so services come up exactly when you're working and
clean up when you move on. This is the primary day-to-day workflow.

## Monitoring

```sh
pitchfork tui        # Terminal dashboard (Vim keybindings)
```

There is also a web dashboard for browser-based monitoring. Use `pitchfork list` for a quick
text overview and `pitchfork logs -f` to follow output.

## Supervisor & proxy

A background supervisor process tracks daemons and performs restarts/scheduling.

```sh
pitchfork supervisor start
pitchfork supervisor status
pitchfork supervisor stop
```

Port/proxy management (route to daemons, trust local certs):

```sh
pitchfork proxy status
pitchfork proxy add ...
pitchfork proxy remove ...
pitchfork proxy trust
```

## MCP server (AI assistants)

Pitchfork ships an MCP server so assistants like Claude and Cursor can manage daemons:

```sh
pitchfork mcp        # Start the MCP server (wire into your assistant's MCP config)
```

## Tips

- Pitchfork won't start a daemon that's already running — safe to re-run `start`.
- Use `pitchfork wait ID` in scripts/CI to block until a service is actually ready instead of
  sleeping a fixed amount.
- Prefer `depends` + `ready_*` over manual ordering; pitchfork parallelizes independent daemons.
- Run `pitchfork <command> --help` for exact flags on any subcommand.
