# mise CLI Command Reference

## Tool Management

### `mise use [FLAGS] <TOOL@VERSION>...` (alias: `u`)
Install tool, activate it, and update config file.
```sh
mise use node@22                  # Add to project mise.toml
mise use -g python@3.12           # Add to global config
mise use --pin node@22.1.0        # Pin exact version
mise use --fuzzy node@22          # Allow fuzzy matching
mise use --remove node            # Remove from config
mise use --path ./mise.toml node@22  # Specify config file
```
Flags: `-g/--global`, `-p/--pin`, `--fuzzy`, `--remove`, `--path`, `-j/--jobs`, `--raw`

### `mise install [FLAGS] [TOOL@VERSION]...` (alias: `i`)
Install tools without updating config.
```sh
mise install                      # Install all from config
mise install node@22              # Install specific version
mise install -f node              # Force reinstall
```
Flags: `-f/--force`, `-j/--jobs`, `--raw`, `-v/--verbose`

### `mise uninstall <INSTALLED_TOOL@VERSION>...` (alias: `rm`)
Remove installed tool versions.
```sh
mise uninstall node@20            # Remove specific version
mise uninstall --all node         # Remove all versions
```

### `mise ls [FLAGS] [INSTALLED_TOOL]...`
List installed and active tools.
```sh
mise ls                           # All tools
mise ls node                      # Node versions only
mise ls --current                 # Currently active tools
mise ls --json                    # JSON output
mise ls --missing                 # Missing tools
mise ls --prunable                # Tools safe to prune
```
Flags: `-c/--current`, `-J/--json`, `-m/--missing`, `--prunable`, `--no-header`, `--prefix`

### `mise outdated [FLAGS] [TOOL@VERSION]...`
Show available updates.
```sh
mise outdated                     # All tools
mise outdated --json              # JSON output
mise outdated --bump              # Compare against latest (not just range)
mise outdated --local             # Local config only
```

### `mise upgrade [FLAGS] [INSTALLED_TOOL@VERSION]...` (alias: `up`)
Upgrade tools to newer versions.
```sh
mise upgrade                      # All tools
mise upgrade node                 # Single tool
mise upgrade --bump               # Upgrade + update mise.toml
mise upgrade --dry-run            # Preview changes
mise upgrade --interactive        # Menu selection
mise upgrade --exclude go         # Skip specific tools
```

### `mise prune [FLAGS] [INSTALLED_TOOL]...`
Delete unused tool versions.
```sh
mise prune                        # Remove all unused
mise prune --dry-run              # Preview
mise prune node                   # Only node versions
```

## Execution

### `mise exec [FLAGS] [TOOL@VERSION]... -- <COMMAND>...` (alias: `x`)
Execute a command with mise tool versions.
```sh
mise x node@20 -- node app.js
mise x python@3.12 -- python script.py
mise x -- npm test                # Use configured versions
```

### `mise run [FLAGS] <TASK> [ARGS]...` (alias: `r`)
Run a defined task.
```sh
mise run build
mise run test -- --coverage
mise run lint ::: test            # Parallel execution
mise run build --dry-run
mise run build --force            # Ignore source/output caching
mise run build --output prefix    # Prefix output with task name
```
Flags: `-j/--jobs`, `-n/--dry-run`, `-f/--force`, `-o/--output`, `--raw`, `-q/--quiet`, `-t/--timings`

### `mise watch [FLAGS] <TASK> [ARGS]...` (alias: `w`)
Watch files and rerun task on changes.
```sh
mise watch build
mise watch build --glob "src/**/*"
mise watch build --exts rs,toml
mise watch serve --restart        # Restart on changes
```
Requires `watchexec`.

## Environment

### `mise env [FLAGS] [TOOL@VERSION]...`
Print environment variables.
```sh
mise env                          # Current env
mise env --json                   # JSON output
mise env -s bash                  # Shell format
```

### `mise set [FLAGS] [ENV_VARS]...`
Set environment variables in mise.toml.
```sh
mise set NODE_ENV=production
mise set DATABASE_URL=postgres://localhost/mydb
mise set --file .env              # Set from .env file
```

### `mise unset <KEYS>...`
Remove environment variables.
```sh
mise unset NODE_ENV
```

### `mise shell [FLAGS] <TOOL@VERSION>...` (alias: `sh`)
Set tool version for current shell session.
```sh
mise shell node@20
mise shell --unset node           # Remove session override
```

### `mise en`
Enter a subshell with the mise environment active.

## Information

### `mise which [FLAGS] <BIN_NAME>`
Show path to a tool's binary.
```sh
mise which node                   # Full path
mise which node --plugin          # Plugin name
mise which node --version         # Version number
```

### `mise where <TOOL@VERSION>`
Show installation directory.
```sh
mise where node@20
```

### `mise doctor` (alias: `dr`)
Diagnose issues.
```sh
mise doctor                       # Full diagnostics
mise doctor --json                # JSON output
mise doctor path                  # PATH diagnostics
```

### `mise ls-remote [TOOL] [PREFIX]`
List available remote versions.
```sh
mise ls-remote node               # All node versions
mise ls-remote node 22            # Versions starting with 22
```

## Configuration

### `mise trust [FLAGS] [CONFIG_FILE]`
Mark a config file as trusted.
```sh
mise trust                        # Trust in current directory
mise trust --all                  # Trust all in tree
mise trust --show                 # Show trust status
mise trust --untrust              # Remove trust
mise trust --ignore               # Ignore config
```

### `mise config` (alias: `cfg`)
Manage config files.
```sh
mise cfg ls                       # List loaded configs
mise cfg get tools.node           # Get a value
mise cfg set tools.node 22        # Set a value
```

### `mise settings [FLAGS]`
Manage settings.
```sh
mise settings                     # Show all settings
mise settings get jobs            # Get single setting
mise settings set jobs 4          # Set a setting
mise settings ls                  # List settings
mise settings unset jobs          # Remove setting
```

## Maintenance

### `mise self-update [FLAGS] [VERSION]`
Update mise itself.
```sh
mise self-update                  # Latest version
mise self-update --force          # Force update
mise self-update --no-plugins     # Skip plugin updates
```
Not available when installed via package manager.

### `mise cache clear`
Clear internal cache.

### `mise reshim`
Rebuild shims directory.

### `mise implode`
Remove everything (nuclear option — keeps config).

## Other Commands

| Command | Description |
|---------|-------------|
| `mise activate` | Output shell activation code |
| `mise deactivate` | Deactivate mise |
| `mise completion <SHELL>` | Generate shell completions |
| `mise bin-paths` | List bin paths for installed tools |
| `mise latest <TOOL>` | Show latest available version |
| `mise link <TOOL@VERSION> <PATH>` | Symlink external installation |
| `mise search <QUERY>` | Search registry for tools |
| `mise tool <TOOL>` | Show tool info (backend, versions) |
| `mise fmt` | Format mise.toml files |
| `mise generate bootstrap` | Generate bootstrap installer script |
| `mise generate github-action` | Generate GitHub Action workflow |
| `mise generate git-pre-commit` | Generate pre-commit hook |
| `mise generate task-docs` | Generate task documentation |
| `mise tasks ls` | List available tasks |
| `mise tasks info <TASK>` | Show task details |
| `mise tasks deps` | Show task dependency tree |
| `mise plugins ls` | List installed plugins |
| `mise plugins install` | Install a plugin |
| `mise registry` | Show tool registry |
| `mise sync python --uv` | Sync Python versions with uv |
