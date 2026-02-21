---
name: fnox
description: Manage secrets with the fnox CLI - a secrets management tool that bridges encrypted secrets in git with remote cloud providers. Use this skill when the user asks about "fnox", "secrets management", or needs to set, get, list, import, export, or manage encrypted secrets and secret providers.
---

# fnox CLI — Secrets Management

fnox manages secrets as environment variables, supporting both encrypted secrets in git (`fnox.toml`) and remote cloud providers.

## Global Options

`-c <CONFIG>` config file | `-P <PROFILE>` profile | `-v` verbose | `--if-missing error|warn|ignore` | `--no-defaults`

## Commands

### Secrets CRUD

```bash
fnox set <KEY> [VALUE]                    # Set secret (prompts if no value)
fnox set KEY val -p age                   # With specific provider
fnox set KEY val -g                       # In global config
fnox set KEY val -P staging               # In specific profile
fnox set KEY val -d "description"         # With description
fnox set KEY val -k "provider-key-name"   # Different key name in provider
fnox set KEY --default "fallback"         # Set default fallback

fnox get <KEY>                            # Get secret value
fnox get KEY -P production                # From specific profile

fnox list                                 # List secrets (names only)
fnox list -V                              # Show values
fnox list -f                              # Full provider keys
fnox list -s                              # Show source files

fnox remove <KEY>                         # Remove secret
fnox remove KEY -g                        # From global config
```

### Execute with Secrets

```bash
fnox exec -- <COMMAND>                    # Run with secrets as env vars
fnox exec -P production -- ./deploy.sh    # With profile
fnox exec --if-missing error -- ./app     # Fail on missing
```

### Import / Export

```bash
fnox export                               # stdout as KEY=value
fnox export -f json|yaml|toml             # Other formats
fnox export -o .env                       # To file

fnox import -p <PROVIDER> [FORMAT]        # Import (default: env format from stdin)
fnox import -p age -i .env                # From .env file
fnox import -p age -i data.json json      # From JSON
fnox import -p age --filter "^DB_"        # Regex filter
fnox import -p age --prefix "APP_"        # Add prefix
fnox import -p age -f                     # Skip confirmation
```

### Check & Scan

```bash
fnox check                                # Validate all required secrets
fnox check -a                             # Include warn/ignore secrets
fnox scan                                 # Scan repo for leaked secrets
fnox scan -d /path -q                     # Specific dir, quiet mode
fnox scan -i "*.test.*"                   # Ignore pattern
```

### Init & Diagnostics

```bash
fnox init                                 # Interactive wizard
fnox init --skip-wizard                   # Minimal config
fnox init -g                              # Global config
fnox doctor                               # Diagnostic info
fnox config-files                         # List loaded config files
fnox profiles                             # List profiles
```

## Providers

**Encryption (in git):** `age`, `aws-kms`, `azure-kms`, `gcp-kms`
**Cloud:** `aws` (Secrets Manager), `aws-ps` (Parameter Store), `azure-sm`, `gcp`, `vault`, `infisical`
**Password managers:** `1password`, `bitwarden`, `passwordstate`
**Local:** `keychain` (OS), `keepass`, `password-store` (pass/GPG), `plain`

```bash
fnox provider list                        # List configured
fnox provider add <NAME> <TYPE>           # Add (e.g. fnox provider add my-age age)
fnox provider add <NAME> <TYPE> -g        # Add globally
fnox provider remove <NAME>               # Remove
fnox provider test [NAME]                 # Test connection (-a for all)
```

### Provider Configuration Examples

```toml
# password-store (GPG-encrypted, uses `pass`)
[providers.pass]
type = "password-store"
prefix = "fnox/"              # optional path prefix
store_dir = "/custom/path"    # optional (default: ~/.password-store)

# Age encryption (secrets stored as ciphertext in git)
[providers.age]
type = "age"
recipients = [
  "age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2el...",
  "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI...",  # also accepts SSH keys
]

# 1Password
[providers.onepass]
type = "1password"
vault = "Development"         # required
account = "my.1password.com"  # optional

# HashiCorp Vault
[providers.vault]
type = "vault"
address = "https://vault.example.com:8200"
path = "secret/myapp"         # base secret path
# token via VAULT_TOKEN env var or `token` key

# AWS Secrets Manager
[providers.aws]
type = "aws"
region = "us-east-1"
prefix = "myapp/"             # optional

# AWS Parameter Store
[providers.aws-ps]
type = "aws-ps"
region = "us-east-1"

# GCP Secret Manager
[providers.gcp]
type = "gcp-sm"
project = "my-project"

# Azure Key Vault Secrets
[providers.azure]
type = "azure-sm"
vault_url = "https://myvault.vault.azure.net"

# Infisical
[providers.infisical]
type = "infisical"
project_id = "your-project-id"  # optional, uses default if omitted
environment = "dev"              # optional (dev/staging/prod)
path = "/"                       # optional secret path
# auth via INFISICAL_TOKEN env var

# Plain text (non-sensitive defaults only)
[providers.plain]
type = "plain"
```

## Configuration

### File Priority (low to high)

1. `~/.config/fnox/config.toml` — Global
2. Parent `fnox.toml` files — Hierarchical
3. `./fnox.toml` — Current dir
4. `fnox.$FNOX_PROFILE.toml` — Profile-specific
5. `fnox.local.toml` — Local overrides (gitignore this)

### fnox.toml Structure

```toml
if_missing = "warn"

[providers.age]
type = "age"
recipients = ["age1abc..."]

[secrets]
DATABASE_URL = { provider = "age", value = "ENC[...]" }
API_KEY = { provider = "aws", key_name = "prod/api-key" }
DEBUG = { default = "false" }

[profiles.production]
if_missing = "error"

[profiles.production.secrets]
DATABASE_URL = { provider = "aws", key_name = "prod/db-url" }
```

### Secret Resolution Order

Encrypted values → Provider references → Environment variables → Default fallback

## Environment Variables

`FNOX_PROFILE` — active profile | `FNOX_AGE_KEY` / `FNOX_AGE_KEY_FILE` — age key | `FNOX_IF_MISSING` — runtime override | `FNOX_CONFIG_DIR` — config dir

Provider-specific: `AWS_*`, `AZURE_*`, `GOOGLE_APPLICATION_CREDENTIALS`, `OP_SERVICE_ACCOUNT_TOKEN`, `BW_SESSION`, `VAULT_ADDR`, `VAULT_TOKEN`

## Common Patterns

### Multi-Environment Setup

```bash
fnox set API_URL "http://localhost:3000"                        # default
fnox set API_URL "https://staging.example.com" -P staging       # staging
fnox set API_URL "https://api.example.com" -P production        # production
fnox exec -P production -- ./deploy.sh
```

### Diagnostics

```bash
fnox doctor                    # Show diagnostic info about fnox state
fnox config-files              # List all config files that would be loaded
fnox profiles                  # List available profiles
fnox check                     # Validate all required secrets are defined
fnox provider test -a          # Test all provider connections
```

## Shell Integration

```bash
eval "$(fnox activate bash)"   # or zsh/fish — auto-loads secrets on cd
fnox deactivate                # disable
```
