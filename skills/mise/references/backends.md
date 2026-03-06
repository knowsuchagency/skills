# mise Backends Reference

## Table of Contents
1. [Aqua](#aqua)
2. [GitHub](#github)
3. [Cargo](#cargo)
4. [npm](#npm)
5. [pipx](#pipx)
6. [Go](#go)
7. [HTTP](#http)
8. [asdf (Legacy)](#asdf-legacy)
9. [Other Backends](#other-backends)

## Aqua

The aqua registry is compiled into the mise binary. No separate install needed. Native Windows support with built-in checksum/signature verification.

```sh
mise use -g aqua:BurntSushi/ripgrep
```

```toml
[tools]
"aqua:BurntSushi/ripgrep" = "latest"
```

### Aqua Tool Options
```toml
[tools]
aws-cli = { version = "latest", symlink_bins = true }  # Filter exposed binaries
```

### Aqua Settings

| Setting | Env Var | Default | Description |
|---------|---------|---------|-------------|
| `aqua.baked_registry` | `MISE_AQUA_BAKED_REGISTRY` | true | Use built-in registry |
| `aqua.cosign` | `MISE_AQUA_COSIGN` | true | Cosign signature verification |
| `aqua.github_attestations` | `MISE_AQUA_GITHUB_ATTESTATIONS` | true | GitHub attestation verification |
| `aqua.minisign` | `MISE_AQUA_MINISIGN` | true | Minisign verification |
| `aqua.slsa` | `MISE_AQUA_SLSA` | true | SLSA provenance verification |
| `aqua.registry_url` | `MISE_AQUA_REGISTRY_URL` | None | Custom registry URL |

### Troubleshooting Aqua
- Missing environments: Edit `supported_envs` in `registry.yaml`
- Version format issues: Use `version_prefix` instead of `version_filter`
- Disable: `MISE_DISABLE_BACKENDS=aqua`

---

## GitHub

Downloads release assets from GitHub repositories. Auto-detects the correct binary based on OS/arch/libc.

```sh
mise use -g github:BurntSushi/ripgrep
mise use -g github:cli/cli@2.40.1     # Specific version
```

```toml
[tools]
"github:BurntSushi/ripgrep" = "latest"
```

### GitHub Tool Options

```toml
# Asset pattern matching
"github:cli/cli" = { version = "latest", asset_pattern = "gh_*_linux_x64.tar.gz" }

# Version prefix (filters tags and strips prefix)
"github:user/repo" = { version = "latest", version_prefix = "release-" }

# Platform-specific patterns
[tools."github:cli/cli"]
version = "latest"
[tools."github:cli/cli".platforms]
linux-x64 = { asset_pattern = "gh_*_linux_x64.tar.gz" }
macos-arm64 = { asset_pattern = "gh_*_macOS_arm64.tar.gz" }

# Checksum verification
[tools."github:owner/repo"]
version = "1.0.0"
checksum = "sha256:a1b2c3d4..."

# Size verification
"github:cli/cli" = { version = "latest", size = "12345678" }

# Strip directory components during extraction
"github:cli/cli" = { version = "latest", strip_components = 1 }

# Binary renaming (single-file downloads)
[tools."github:docker/compose"]
version = "2.29.1"
bin = "docker-compose"

# Rename executables from archives
[tools."github:yt-dlp/yt-dlp"]
version = "latest"
asset_pattern = "yt-dlp_linux.zip"
rename_exe = "yt-dlp"

# Skip macOS .app bundles
[tools."github:nicklockwood/SwiftFormat"]
version = "latest"
rename_exe = "swiftformat"
no_app = true

# Binary path with Tera templating
[tools."github:cli/cli"]
version = "latest"
bin_path = "cli-{{ version }}/bin"

# Filter exposed binaries
"github:jgm/pandoc" = { version = "latest", filter_bins = "pandoc" }

# GitHub Enterprise API URL
"github:myorg/mytool" = { version = "latest", api_url = "https://github.mycompany.com/api/v3" }
```

Binary path lookup order: specified path -> bin/ directory -> install root -> subdirectories.

### GitHub Settings

| Setting | Env Var | Default |
|---------|---------|---------|
| `github.github_attestations` | `MISE_GITHUB_GITHUB_ATTESTATIONS` | true |
| `github.slsa` | `MISE_GITHUB_SLSA` | true |

Auth for private repos: `export MISE_GITHUB_ENTERPRISE_TOKEN="your-token"`

---

## Cargo

Install Rust crates via cargo. Uses `cargo-binstall` for precompiled binaries when available.

```sh
mise use -g cargo:eza
mise use -g cargo-binstall        # Install binstall for faster installs
```

### Cargo Tool Options
```toml
# Features
"cargo:cargo-edit" = { version = "latest", features = "add" }

# Disable default features
"cargo:cargo-edit" = { version = "latest", default-features = false }

# Git-based installation
"cargo:https://github.com/user/repo" = { version = "tag:v1.0.0", bin = "demo" }

# Locked dependencies (enabled by default)
"cargo:some-tool" = { version = "latest", locked = false }
```

### Git References
```sh
mise use cargo:https://github.com/user/repo@tag:v1.0
mise use cargo:https://github.com/user/repo@branch:main
mise use cargo:https://github.com/user/repo@rev:abc123
```

### Cargo Settings

| Setting | Env Var | Default |
|---------|---------|---------|
| `cargo.binstall` | `MISE_CARGO_BINSTALL` | true |
| `cargo.binstall_only` | `MISE_CARGO_BINSTALL_ONLY` | false |
| `cargo.registry_name` | `MISE_CARGO_REGISTRY_NAME` | None |

---

## npm

Install Node.js packages globally via npm/bun/pnpm.

```sh
mise use -g npm:prettier
mise use -g npm:typescript
```

```toml
[tools]
"npm:prettier" = "latest"
"npm:eslint" = "9"
```

### npm Settings

| Setting | Env Var | Default |
|---------|---------|---------|
| `npm.package_manager` | `MISE_NPM_PACKAGE_MANAGER` | npm |

Valid values: `npm`, `bun`, `pnpm`. Configure: `mise settings set npm.package_manager bun`

---

## pipx

Install Python CLI tools in isolated virtual environments. Prefers `uvx` (uv's equivalent) when uv is installed.

```sh
mise use -g pipx:black
mise use -g pipx:psf/black          # GitHub source
mise use -g pipx:black@24.3.0       # Specific version
```

### pipx Supported Syntax

| Format | Example |
|--------|---------|
| PyPI latest | `pipx:black` |
| PyPI versioned | `pipx:black@24.3.0` |
| GitHub latest | `pipx:psf/black` |
| GitHub versioned | `pipx:psf/black@24.3.0` |
| Git branch | `pipx:git+https://github.com/psf/black.git@main` |
| HTTPS zip | `pipx:https://github.com/psf/black/archive/18.9b0.zip` |

### pipx Tool Options
```toml
# Extras
"pipx:harlequin" = { version = "latest", extras = "postgres,s3" }

# Additional pipx args
"pipx:black" = { version = "latest", pipx_args = "--preinstall" }

# Disable uv for specific tools
"pipx:ansible" = { version = "latest", uvx = "false", pipx_args = "--include-deps" }

# uvx-specific args
"pipx:ansible-core" = { version = "latest", uvx_args = "--with ansible" }
```

### pipx Settings

| Setting | Env Var | Default |
|---------|---------|---------|
| `pipx.registry_url` | `MISE_PIPX_REGISTRY_URL` | `https://pypi.org/pypi/{}/json` |
| `pipx.uvx` | `MISE_PIPX_UVX` | true |

### Reinstall After Python Version Change
```sh
mise install -f pipx:psf/black      # Single tool
mise install -f "pipx:*"            # All pipx tools
```

---

## Go

Install Go packages via `go install`.

```sh
mise use -g go:github.com/DarthSim/hivemind
```

### Go Tool Options
```toml
# Build tags
[tools]
"go:github.com/golang-migrate/migrate/v4/cmd/migrate" = { version = "latest", tags = "postgres" }
```

Prerequisite: Go must be installed (`mise use -g go`).

---

## HTTP

Install tools from direct HTTP/HTTPS URLs.

```toml
[tools."http:my-tool"]
version = "1.0.0"
url = "https://example.com/releases/my-tool-v{{version}}-{{os()}}-{{arch()}}.tar.gz"
```

### HTTP Key Options

| Option | Description |
|--------|-------------|
| `url` (required) | Download URL. Templates: `{{version}}`, `{{os()}}`, `{{arch()}}` |
| `checksum` | SHA256 verification |
| `size` | File size verification |
| `strip_components` | Remove directory levels during extraction |
| `bin` | Rename single-file downloads |
| `rename_exe` | Rename executables in archives |
| `format` | Archive type (tar.gz, tar.xz, zip, etc.) |
| `bin_path` | Binary directory within archives |

### Version Listing for HTTP
```toml
[tools."http:my-tool"]
version = "1.0.0"
url = "https://example.com/my-tool-{{version}}.tar.gz"
version_list_url = "https://api.github.com/repos/org/tool/tags"
version_json_path = "$[*].name"
```

### Platform-Specific URLs
```toml
[tools."http:my-tool"]
version = "1.0.0"
[tools."http:my-tool".platforms]
macos-x64 = { url = "https://example.com/my-tool-macos-x64.tar.gz" }
linux-arm64 = { url = "https://example.com/my-tool-linux-arm64.tar.gz" }
```

### Caching
Downloads cache in `$MISE_CACHE_DIR/http-tarballs/`. Autopruner removes unused entries after 30 days.

---

## asdf (Legacy)

asdf plugins are considered legacy. Prefer aqua or github backends.

```toml
[tools]
"asdf:mise-plugins/asdf-php" = "latest"
```

Limitations:
- Shell-based (bash dependency) — no Windows support
- Higher security risks (arbitrary shell code execution)
- Slower than native backends
- No built-in checksum/signature verification

Migration: Tools are being moved from asdf to aqua and github backends.

---

## Other Backends

| Backend | Status | Example |
|---------|--------|---------|
| GitLab | Stable | `gitlab:owner/repo` |
| Forgejo | Stable | `forgejo:owner/repo` |
| Conda | Experimental | `conda:package` |
| .NET | Experimental | `dotnet:package` |
| gem | Stable | `gem:package` |
| S3 | Experimental | `s3:bucket/path` |
| SPM | Experimental | `spm:package` |
| vfox | Stable | `vfox:plugin` |
| ubi | **Deprecated** | Use `github:` instead |

### Disabling Backends
```sh
mise settings disable_backends=asdf,ubi
```
