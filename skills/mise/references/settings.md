# mise Settings Reference

Settings are configured via `mise settings key=value`, `~/.config/mise/config.toml`, or environment variables.

## Core Settings

| Setting | Type | Env Var | Default | Description |
|---------|------|---------|---------|-------------|
| `activate_aggressive` | bool | `MISE_ACTIVATE_AGGRESSIVE` | false | Prioritize tool bin-paths at front of PATH |
| `all_compile` | bool | `MISE_ALL_COMPILE` | false | Disable precompiled binaries for all languages |
| `auto_install` | bool | `MISE_AUTO_INSTALL` | true | Auto-install missing tools |
| `auto_install_disable_tools` | string[] | `MISE_AUTO_INSTALL_DISABLE_TOOLS` | [] | Tools to exclude from auto-install |
| `cache_prune_age` | string | `MISE_CACHE_PRUNE_AGE` | 30d | Cache staleness threshold |
| `color` | bool | `MISE_COLOR` | true | Colored output |
| `color_theme` | string | `MISE_COLOR_THEME` | default | Theme: default, charm, base16, catppuccin, dracula |
| `default_config_filename` | string | `MISE_DEFAULT_CONFIG_FILENAME` | mise.toml | Config filename (env-only) |
| `disable_backends` | string[] | `MISE_DISABLE_BACKENDS` | [] | Backends to deactivate |
| `disable_tools` | string[] | `MISE_DISABLE_TOOLS` | [] | Tools to ignore |
| `enable_tools` | string[] | `MISE_ENABLE_TOOLS` | [] | Restrict to only these tools |
| `env` | string[] | `MISE_ENV` | [] | Active profiles (early-init) |
| `env_cache` | bool | `MISE_ENV_CACHE` | false | Cache computed env to disk |
| `env_cache_ttl` | string | `MISE_ENV_CACHE_TTL` | 1h | Cache validity duration |
| `experimental` | bool | `MISE_EXPERIMENTAL` | false | Enable experimental features |
| `jobs` | int | `MISE_JOBS` | 8 | Concurrent installation jobs |
| `locked` | bool | `MISE_LOCKED` | false | Require lockfile entries |
| `lockfile` | bool | `MISE_LOCKFILE` | None | Read/write lockfiles |
| `offline` | bool | `MISE_OFFLINE` | false | Block all HTTP requests |
| `paranoid` | bool | `MISE_PARANOID` | false | Extra security checks |
| `pin` | bool | `MISE_PIN` | false | Default to pinned versions |
| `quiet` | bool | `MISE_QUIET` | false | Suppress non-error output |
| `raw` | bool | `MISE_RAW` | false | Direct I/O passthrough |
| `verbose` | bool | `MISE_VERBOSE` | false | Detailed logs |
| `yes` | bool | `MISE_YES` | false | Auto-answer prompts |

## HTTP Settings

| Setting | Env Var | Default | Description |
|---------|---------|---------|-------------|
| `http_timeout` | `MISE_HTTP_TIMEOUT` | 30s | HTTP request timeout |
| `http_retries` | `MISE_HTTP_RETRIES` | 0 | Retry count (exponential backoff) |
| `netrc` | `MISE_NETRC` | true | Read netrc credentials |
| `prefer_offline` | `MISE_PREFER_OFFLINE` | false | Use cached data when possible |
| `use_versions_host` | `MISE_USE_VERSIONS_HOST` | true | Query mise-versions.jdx.dev |

## Security Settings

| Setting | Env Var | Default | Description |
|---------|---------|---------|-------------|
| `github_attestations` | `MISE_GITHUB_ATTESTATIONS` | true | Verify GitHub artifact attestations |
| `gpg_verify` | `MISE_GPG_VERIFY` | None | Global GPG verification |
| `slsa` | `MISE_SLSA` | true | SLSA provenance verification |
| `trusted_config_paths` | `MISE_TRUSTED_CONFIG_PATHS` | [] | Auto-trusted paths |

## Path Settings (Early-Init)

These must be set via env vars or `.miserc.toml`, not `mise.toml`:

| Setting | Env Var | Default |
|---------|---------|---------|
| `ceiling_paths` | `MISE_CEILING_PATHS` | [] |
| `ignored_config_paths` | `MISE_IGNORED_CONFIG_PATHS` | [] |
| `override_config_filenames` | `MISE_OVERRIDE_CONFIG_FILENAMES` | [] |
| `global_config_file` | `MISE_GLOBAL_CONFIG_FILE` | ~/.config/mise/config.toml |

## Status Messages

| Setting | Env Var | Default |
|---------|---------|---------|
| `status.missing_tools` | `MISE_STATUS_MESSAGE_MISSING_TOOLS` | if_other_versions_installed |
| `status.show_env` | `MISE_STATUS_MESSAGE_SHOW_ENV` | false |
| `status.show_tools` | `MISE_STATUS_MESSAGE_SHOW_TOOLS` | false |

## Hook-env Settings

| Setting | Env Var | Default |
|---------|---------|---------|
| `hook_env.cache_ttl` | `MISE_HOOK_ENV_CACHE_TTL` | 0s |
| `hook_env.chpwd_only` | `MISE_HOOK_ENV_CHPWD_ONLY` | false |

## Task Settings

| Setting | Env Var | Default |
|---------|---------|---------|
| `task.output` | `MISE_TASK_OUTPUT` | None |
| `task.timeout` | `MISE_TASK_TIMEOUT` | None |
| `task.timings` | `MISE_TASK_TIMINGS` | None |
| `task.skip` | `MISE_TASK_SKIP` | [] |
| `task.skip_depends` | `MISE_TASK_SKIP_DEPENDS` | false |
| `task.monorepo_depth` | `MISE_TASK_MONOREPO_DEPTH` | 5 |
| `task.show_full_cmd` | `MISE_TASK_SHOW_CMD_NO_TRUNC` | false |

## Directories

| Directory | Env Var | Default |
|-----------|---------|---------|
| Config | `MISE_CONFIG_DIR` | `~/.config/mise` |
| Data | `MISE_DATA_DIR` | `~/.local/share/mise` |
| Cache | `MISE_CACHE_DIR` | `~/.cache/mise` (Linux), `~/Library/Caches/mise` (macOS) |
| State | `MISE_STATE_DIR` | `~/.local/state/mise` |
| Installs | `MISE_INSTALLS_DIR` | `~/.local/share/mise/installs` |
| Shims | - | `~/.local/share/mise/shims` |
| Downloads | - | `~/.local/share/mise/downloads` |
| Plugins | - | `~/.local/share/mise/plugins` |
