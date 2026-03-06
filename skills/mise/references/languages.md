# mise Language-Specific Guides

## Table of Contents
1. [Node.js](#nodejs)
2. [Python](#python)
3. [Ruby](#ruby)
4. [Go](#go)
5. [Java](#java)
6. [Rust](#rust)
7. [Bun](#bun)
8. [Deno](#deno)
9. [Elixir/Erlang](#elixirerlang)
10. [.NET](#net)

## Node.js

```sh
mise use node@22          # Install and activate
mise use -g node@lts      # Global LTS
```

### Version Files
Priority: `mise.toml` > `.tool-versions` > `.nvmrc` > `.node-version`

### Default Packages
`~/.default-npm-packages` (one per line):
```
typescript@latest
@types/node@^20
lodash
```

### Corepack
```sh
mise settings node.corepack=true
# Or per-project:
[tools]
node = { version = "22", postinstall = "corepack enable" }
```

### Compilation from Source
```sh
mise settings node.compile=true
```

### Unofficial Builds (musl, etc.)
```sh
mise settings node.mirror_url=https://unofficial-builds.nodejs.org/download/release/
mise settings node.flavor=musl
```

### Key Settings

| Setting | Env Var | Default |
|---------|---------|---------|
| `node.compile` | `MISE_NODE_COMPILE` | auto |
| `node.corepack` | `MISE_NODE_COREPACK` | false |
| `node.default_packages_file` | `MISE_NODE_DEFAULT_PACKAGES_FILE` | ~/.default-npm-packages |
| `node.flavor` | `MISE_NODE_FLAVOR` | None |
| `node.mirror_url` | `MISE_NODE_MIRROR_URL` | None |
| `node.verify` | `MISE_NODE_VERIFY` | true |

---

## Python

```sh
mise use python@3.12      # Install and activate
mise use -g python@3.11 python@3.12  # Multiple versions
```

### Virtual Environment (recommended)
```toml
[tools]
python = "3.12"

[env]
_.python.venv = { path = ".venv", create = true }
```

Advanced venv options:
```toml
_.python.venv = { path = ".venv", create = true, python = "3.10" }
_.python.venv = { path = ".venv", create = true, uv_create_args = ["--seed"] }  # Include pip
_.python.venv = { path = ".venv", create = true, python_create_args = ["--without-pip"] }
```

### uv Integration
- If `uv` is installed, mise uses it for venv creation automatically
- `uv` excludes pip by default; add `--seed` to include it
- Bind uv to mise-managed Python:
```toml
[env]
UV_PYTHON = { value = "{{ tools.python.path }}", tools = true }
```

### uv_venv_auto Setting
```sh
mise settings python.uv_venv_auto=false          # Disable (default)
mise settings python.uv_venv_auto=source          # Source existing .venv
mise settings "python.uv_venv_auto=create|source" # Create + source
```

### Precompiled Binaries
Downloaded from python-build-standalone by default. To compile from source:
```sh
mise settings python.compile=true
```

### Default Packages
`~/.default-python-packages`:
```
pipenv
ansible
```

### Free-Threaded Python
```sh
MISE_PYTHON_COMPILE=0 MISE_PYTHON_PRECOMPILED_FLAVOR=freethreaded+pgo-full mise install python
```

### Key Settings

| Setting | Env Var | Default |
|---------|---------|---------|
| `python.compile` | `MISE_PYTHON_COMPILE` | auto |
| `python.default_packages_file` | `MISE_PYTHON_DEFAULT_PACKAGES_FILE` | None |
| `python.precompiled_arch` | `MISE_PYTHON_PRECOMPILED_ARCH` | auto |
| `python.precompiled_flavor` | `MISE_PYTHON_PRECOMPILED_FLAVOR` | install_only_stripped |
| `python.pyenv_repo` | `MISE_PYENV_REPO` | pyenv/pyenv |
| `python.uv_venv_auto` | `MISE_PYTHON_UV_VENV_AUTO` | false |
| `python.venv_stdlib` | `MISE_VENV_STDLIB` | false |

---

## Ruby

```sh
mise use ruby@3.3         # Install and activate
mise use ruby@truffleruby # Alternative implementation
```

### Installation Methods
- **Precompiled** (becoming default): `mise settings ruby.compile=false`
- **Source compilation** (current default): Uses ruby-build

### Default Gems
`~/.default-gems`:
```
pry
rubocop
bcat ~> 0.6.0
```

### Version Files
`.ruby-version`, `Gemfile` (with ruby directive)

### Custom Precompiled URL
```toml
[settings.ruby]
precompiled_url = "yourorg/ruby"
# Or full URL template:
precompiled_url = "https://my-mirror.example.com/ruby-{version}.{platform}.tar.gz"
```

### Key Settings

| Setting | Env Var | Default |
|---------|---------|---------|
| `ruby.compile` | `MISE_RUBY_COMPILE` | auto |
| `ruby.default_packages_file` | `MISE_RUBY_DEFAULT_PACKAGES_FILE` | ~/.default-gems |
| `ruby.precompiled_url` | `MISE_RUBY_PRECOMPILED_URL` | jdx/ruby |
| `ruby.ruby_build_repo` | `MISE_RUBY_BUILD_REPO` | rbenv/ruby-build |
| `ruby.ruby_install` | `MISE_RUBY_INSTALL` | false |

---

## Go

```sh
mise use go@1.22          # Install and activate
mise use -g go@prefix:1.20  # Older versions (<=1.20)
```

### Default Packages
`~/.default-go-packages`:
```
github.com/daixiang0/gci
github.com/jesseduffield/lazygit
```

### Key Settings

| Setting | Env Var | Default |
|---------|---------|---------|
| `go_download_mirror` | `MISE_GO_DOWNLOAD_MIRROR` | dl.google.com/go |
| `go_set_goroot` | `MISE_GO_SET_GOROOT` | true |
| `go_set_gobin` | `MISE_GO_SET_GOBIN` | None |
| `go_default_packages_file` | `MISE_GO_DEFAULT_PACKAGES_FILE` | ~/.default-go-packages |

---

## Java

```sh
mise use java@openjdk-21       # OpenJDK
mise use java@temurin-21       # Eclipse Temurin
mise use java@zulu-21          # Azul Zulu
mise use java@corretto-21      # Amazon Corretto
mise ls-remote java            # List all available versions
```

### Shorthand Versions
`java@21` uses the vendor from `java.shorthand_vendor` setting (default: `openjdk`).

### Version Files
`.java-version`, `.sdkmanrc` (with vendor mapping)

### Tool Options
```toml
[tools]
java = { version = "openjdk-21", release_type = "ea" }  # Early Access
```

### macOS java_home Integration
```sh
sudo mkdir /Library/Java/JavaVirtualMachines/openjdk-21.jdk
sudo ln -s ~/.local/share/mise/installs/java/openjdk-21/Contents \
  /Library/Java/JavaVirtualMachines/openjdk-21.jdk/Contents
```

### Gradle Toolchain
```sh
mkdir -p ~/.asdf/installs/ && ln -s ~/.local/share/mise/installs/java ~/.asdf/installs/
```

---

## Rust

```sh
mise use rust                  # Latest stable
mise use rust@beta             # Beta channel
mise use rust@1.82             # Specific version
```

Uses `rustup` under the hood. Installations live in `~/.rustup/`, not `~/.local/share/mise/installs/`.

### Tool Options
```toml
[tools]
rust = { version = "1.83.0", components = "rust-src,llvm-tools" }
rust = { version = "1.83.0", profile = "minimal" }
rust = { version = "1.83.0", targets = "wasm32-unknown-unknown" }
```

Profiles: `minimal` (rustc, std, cargo), `default` (+ docs, fmt, clippy), `complete` (all)

### Key Settings

| Setting | Env Var | Default |
|---------|---------|---------|
| `rust.cargo_home` | `MISE_CARGO_HOME` | ~/.cargo |
| `rust.rustup_home` | `MISE_RUSTUP_HOME` | ~/.rustup |
| `rust.default_host` | `MISE_RUST_DEFAULT_HOST` | None |

---

## Bun

```sh
mise use bun@latest
mise use bun@1.0
```

Do NOT use `bun upgrade` -- mise won't be aware of the change.

---

## Deno

```sh
mise use deno@latest
mise use deno@1
```

Do NOT use `deno upgrade` -- mise won't be aware of the change.

---

## Elixir/Erlang

Erlang must be installed before Elixir:
```sh
mise use -g erlang elixir      # Install both together
```

---

## .NET

```sh
mise use dotnet@8               # .NET SDK 8
mise use dotnet@8 dotnet@9      # Multi-targeting
```

### Isolated Mode
```sh
mise settings dotnet.isolated=true   # Separate DOTNET_ROOT per version
```

### Version File: global.json
```sh
mise settings set idiomatic_version_file_enable_tools dotnet
```

### Key Settings

| Setting | Env Var | Default |
|---------|---------|---------|
| `dotnet.isolated` | `MISE_DOTNET_ISOLATED` | false |
| `dotnet.dotnet_root` | `MISE_DOTNET_ROOT` | ~/.local/share/mise/dotnet-root |
| `dotnet.package_flags` | `MISE_DOTNET_PACKAGE_FLAGS` | None |
| `dotnet.registry_url` | `MISE_DOTNET_REGISTRY_URL` | nuget.org |
