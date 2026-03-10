---
name: dokploy
description: Manage Dokploy self-hosted PaaS deployments via CLI. Use when the user asks to deploy, manage, inspect, or configure applications, databases, Docker containers, domains, backups, or any infrastructure on Dokploy. Triggers include "dokploy", "deploy to dokploy", "list projects", "check containers", "manage domains", or any Dokploy administration task.
allowed-tools: Bash(uvx mcp2cli *), Bash(fnox *)
---

# Dokploy CLI

Interact with your Dokploy instance via `mcp2cli`, which dynamically generates a CLI from the Dokploy OpenAPI spec.

## Usage

```bash
fnox exec -- uvx mcp2cli \
  --spec "$DOKPLOY_URL/settings.getOpenApiDocument" \
  --base-url "$DOKPLOY_URL" \
  --auth-header "x-api-key:env:DOKPLOY_DEFAULT" \
  [OPTIONS] COMMAND [ARGS...]
```

Or with env vars already exported:

```bash
uvx mcp2cli \
  --spec "$DOKPLOY_URL/settings.getOpenApiDocument" \
  --base-url "$DOKPLOY_URL" \
  --auth-header "x-api-key:env:DOKPLOY_DEFAULT" \
  [OPTIONS] COMMAND [ARGS...]
```

## Global Options

| Flag | Description |
|------|-------------|
| `--list` | List all available commands grouped by resource |
| `--pretty` | Pretty-print JSON output |
| `--cache-ttl SECONDS` | Cache the spec for N seconds (default: 3600) |
| `--refresh` | Force-refresh the cached spec |

## Setup

### Base URL

Store your Dokploy instance URL in fnox:

```bash
fnox set DOKPLOY_URL https://dokploy.example.com/api -g
```

### Authentication

Store the API token in fnox:

```bash
fnox set DOKPLOY_DEFAULT <your-api-token> -g
```

The `--auth-header "x-api-key:env:DOKPLOY_DEFAULT"` flag tells mcp2cli to read the token from the `DOKPLOY_DEFAULT` environment variable at runtime. Use `fnox exec --` to inject it.

## Examples

Commands use **kebab-case** (e.g., `project-all`, `application-one`, `docker-get-containers`). Use `--list` to discover all available commands.

```bash
# List all available commands
fnox exec -- uvx mcp2cli \
  --spec "$DOKPLOY_URL/settings.getOpenApiDocument" \
  --base-url "$DOKPLOY_URL" \
  --auth-header "x-api-key:env:DOKPLOY_DEFAULT" \
  --list

# List all projects
fnox exec -- uvx mcp2cli \
  --spec "$DOKPLOY_URL/settings.getOpenApiDocument" \
  --base-url "$DOKPLOY_URL" \
  --auth-header "x-api-key:env:DOKPLOY_DEFAULT" \
  --pretty project-all

# Get a specific application
fnox exec -- uvx mcp2cli \
  --spec "$DOKPLOY_URL/settings.getOpenApiDocument" \
  --base-url "$DOKPLOY_URL" \
  --auth-header "x-api-key:env:DOKPLOY_DEFAULT" \
  --pretty application-one --applicationId <appId>

# Create a project
fnox exec -- uvx mcp2cli \
  --spec "$DOKPLOY_URL/settings.getOpenApiDocument" \
  --base-url "$DOKPLOY_URL" \
  --auth-header "x-api-key:env:DOKPLOY_DEFAULT" \
  project-create --name "my-project"

# Deploy an application
fnox exec -- uvx mcp2cli \
  --spec "$DOKPLOY_URL/settings.getOpenApiDocument" \
  --base-url "$DOKPLOY_URL" \
  --auth-header "x-api-key:env:DOKPLOY_DEFAULT" \
  application-deploy --applicationId <appId>

# List Docker containers
fnox exec -- uvx mcp2cli \
  --spec "$DOKPLOY_URL/settings.getOpenApiDocument" \
  --base-url "$DOKPLOY_URL" \
  --auth-header "x-api-key:env:DOKPLOY_DEFAULT" \
  --pretty docker-get-containers
```

## Deploying a Local Repo (Git Provider)

Dokploy can clone directly from the host machine via SSH -- no GitHub/GitLab needed. This is the preferred approach for repos that already live on the server.

### Prerequisites

An SSH key must exist in Dokploy and its public key must be in `~/.ssh/authorized_keys` on the host.

To create and register a new key:
```bash
# Generate a key in Dokploy
fnox exec -- uvx mcp2cli \
  --spec "$DOKPLOY_URL/settings.getOpenApiDocument" \
  --base-url "$DOKPLOY_URL" \
  --auth-header "x-api-key:env:DOKPLOY_DEFAULT" \
  ssh-key-generate --type ed25519

# Save it (use the output privateKey/publicKey)
fnox exec -- uvx mcp2cli \
  --spec "$DOKPLOY_URL/settings.getOpenApiDocument" \
  --base-url "$DOKPLOY_URL" \
  --auth-header "x-api-key:env:DOKPLOY_DEFAULT" \
  ssh-key-create --name "host-key" --description "SSH key for host access" \
  --privateKey "$PRIVATE_KEY" --publicKey "$PUBLIC_KEY"

# Add the public key to the host
echo "$PUBLIC_KEY" >> ~/.ssh/authorized_keys
```

### Deployment Workflow

```bash
# For brevity, define a helper alias (or use fnox exec inline each time):
alias dk='fnox exec -- uvx mcp2cli \
  --spec "$DOKPLOY_URL/settings.getOpenApiDocument" \
  --base-url "$DOKPLOY_URL" \
  --auth-header "x-api-key:env:DOKPLOY_DEFAULT"'

# 1. Create a project
dk project-create --name "MyApp"
# Returns: projectId, environmentId

# 2. Create a compose service
dk compose-create \
  --name "myapp" \
  --environmentId "<envId>" \
  --composeType "docker-compose"
# Returns: composeId

# 3. Configure Git provider (clone from host via Docker bridge gateway)
dk compose-update \
  --composeId "<composeId>" \
  --sourceType "git" \
  --customGitUrl "ssh://<user>@<docker-bridge-ip>/absolute/path/to/repo" \
  --customGitBranch "main" \
  --customGitSSHKeyId "<sshKeyId>"

# 4. Set environment variables (if needed)
dk compose-update \
  --composeId "<composeId>" \
  --env "KEY=value"

# 5. Create domain with HTTPS
dk domain-create \
  --host "app.example.com" \
  --port 8080 \
  --https \
  --composeId "<composeId>" \
  --serviceName "service-name-from-compose" \
  --domainType "compose" \
  --certificateType "letsencrypt"

# 6. Deploy
dk compose-deploy --composeId "<composeId>"

# 7. Check deployment status
dk --pretty deployment-all-by-compose --composeId "<composeId>"
```

### Important Notes

- **Docker bridge gateway IP**: Find it with `docker network inspect bridge | jq '.[0].IPAM.Config[0].Gateway'`. Use this IP in Git URLs so Dokploy containers can reach the host via SSH (e.g., `ssh://user@172.17.0.1/path/to/repo`).
- **Host port conflicts**: If the compose file binds host ports (e.g., `ports: "8090:8090"`), set a non-conflicting port via env vars. Traefik handles external routing, so host port bindings are only needed for inter-service access.
- **Domain port**: The `--port` in `domain-create` refers to the container's internal port, not the host-mapped port.
- **Service name**: The `--serviceName` must match the service key in the docker-compose.yml (e.g., `pocketbase`, not the container name).

## Spec Caching

mcp2cli caches the OpenAPI spec automatically (default: 1 hour). Use `--refresh` to force a fresh fetch, or `--cache-ttl <seconds>` to customize the TTL.
