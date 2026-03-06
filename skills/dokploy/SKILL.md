---
name: dokploy
description: Manage Dokploy self-hosted PaaS deployments via CLI. Use when the user asks to deploy, manage, inspect, or configure applications, databases, Docker containers, domains, backups, or any infrastructure on Dokploy. Triggers include "dokploy", "deploy to dokploy", "list projects", "check containers", "manage domains", or any Dokploy administration task.
allowed-tools: Bash(uv run *)
---

# Dokploy CLI

A dynamic CLI generated from the Dokploy OpenAPI spec. Every API endpoint becomes a subcommand with typed flags.

## Usage

```bash
uv run SKILL_DIR/scripts/dokploy.py [OPTIONS] COMMAND [ARGS...]
```

## Global Options

| Flag | Default | Description |
|------|---------|-------------|
| `--org` | `DEFAULT` | fnox key suffix — loads `DOKPLOY_<ORG>` token |
| `--url` | from `DOKPLOY_URL` env/fnox | Override base URL |
| `--list` | | List all available commands grouped by resource |
| `--refresh-cache` | | Force-refresh the cached OpenAPI spec |
| `--pretty` | | Pretty-print JSON output |

## Setup

### Base URL

The script needs to know your Dokploy instance URL. Configure it one of these ways (checked in order):

1. `--url` flag: `uv run dokploy.py --url https://dokploy.example.com/api ...`
2. `DOKPLOY_URL` environment variable
3. fnox: `fnox set DOKPLOY_URL https://dokploy.example.com/api -g`

### Authentication

API tokens are stored in fnox (or env vars) with the naming convention `DOKPLOY_<ORG>`:
- `DOKPLOY_DEFAULT` — default org token (used when no `--org` is specified)
- `DOKPLOY_<NAME>` — additional org tokens as needed

Store a token: `fnox set DOKPLOY_DEFAULT <your-api-token> -g`

Select a non-default org with `--org <NAME>`. The token is loaded via `fnox get DOKPLOY_<NAME>`.

## Examples

```bash
# List all available commands
uv run dokploy.py --list

# List all projects
uv run dokploy.py --pretty project.all

# Get a specific application
uv run dokploy.py --pretty application.one --applicationId <appId>

# Create a project
uv run dokploy.py project.create --name "my-project"

# Deploy an application
uv run dokploy.py application.deploy --applicationId <appId>

# List Docker containers
uv run dokploy.py --pretty docker.getContainers

# Use a different org
uv run dokploy.py --org <ORG_NAME> project.all

# Complex body via stdin
echo '{"name":"app","projectId":"xyz"}' | uv run dokploy.py application.create --stdin

# Get help for any command
uv run dokploy.py application.deploy --help
```

## Deploying a Local Repo (Git Provider)

Dokploy can clone directly from the host machine via SSH — no GitHub/GitLab needed. This is the preferred approach for repos that already live on the server.

### Prerequisites

An SSH key must exist in Dokploy and its public key must be in `~/.ssh/authorized_keys` on the host.

To create and register a new key:
```bash
# Generate a key in Dokploy
uv run dokploy.py sshKey.generate --type ed25519
# Save it (use the output privateKey/publicKey)
uv run dokploy.py sshKey.create \
  --name "host-key" --description "SSH key for host access" \
  --privateKey "$PRIVATE_KEY" --publicKey "$PUBLIC_KEY"
# Add the public key to the host
echo "$PUBLIC_KEY" >> ~/.ssh/authorized_keys
```

### Deployment Workflow

```bash
# 1. Create a project
uv run dokploy.py project.create --name "MyApp"
# Returns: projectId, environmentId

# 2. Create a compose service
uv run dokploy.py compose.create \
  --name "myapp" \
  --environmentId "<envId>" \
  --composeType "docker-compose"
# Returns: composeId

# 3. Configure Git provider (clone from host via Docker bridge gateway)
uv run dokploy.py compose.update \
  --composeId "<composeId>" \
  --sourceType "git" \
  --customGitUrl "ssh://<user>@<docker-bridge-ip>/absolute/path/to/repo" \
  --customGitBranch "main" \
  --customGitSSHKeyId "<sshKeyId>"

# 4. Set environment variables (if needed)
uv run dokploy.py compose.update \
  --composeId "<composeId>" \
  --env "KEY=value"

# 5. Create domain with HTTPS
uv run dokploy.py domain.create \
  --host "app.example.com" \
  --port 8080 \
  --https \
  --composeId "<composeId>" \
  --serviceName "service-name-from-compose" \
  --domainType "compose" \
  --certificateType "letsencrypt"

# 6. Deploy
uv run dokploy.py compose.deploy --composeId "<composeId>"

# 7. Check deployment status
uv run dokploy.py --pretty deployment.allByCompose --composeId "<composeId>"
```

### Important Notes

- **Docker bridge gateway IP**: Find it with `docker network inspect bridge | jq '.[0].IPAM.Config[0].Gateway'`. Use this IP in Git URLs so Dokploy containers can reach the host via SSH (e.g., `ssh://user@172.17.0.1/path/to/repo`).
- **Host port conflicts**: If the compose file binds host ports (e.g., `ports: "8090:8090"`), set a non-conflicting port via env vars. Traefik handles external routing, so host port bindings are only needed for inter-service access.
- **Domain port**: The `--port` in `domain.create` refers to the container's internal port, not the host-mapped port.
- **Service name**: The `--serviceName` must match the service key in the docker-compose.yml (e.g., `pocketbase`, not the container name).

## Spec Caching

The OpenAPI spec is cached at `~/.cache/dokploy/<org>_openapi.json` for 1 hour. Use `--refresh-cache` to force a fresh fetch.
