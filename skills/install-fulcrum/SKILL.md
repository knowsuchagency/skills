---
name: install-fulcrum
description: Guide users through installing Fulcrum step-by-step. Use when the user asks to install, set up, or deploy Fulcrum on their local machine or a remote VPS/server.
---

# Fulcrum Installation Guide

You are guiding the user through installing Fulcrum step-by-step. Follow this workflow in order, adapting based on the user's answers. Ask questions before proceeding at each decision point.

## Step 1: Local or Remote?

Ask the user:

> Where do you want to install Fulcrum?
> 1. **Local machine** — run Fulcrum on this computer
> 2. **Remote VPS** — run Fulcrum on a server (recommended for always-on operation; agents keep working when you close your laptop)

If remote, ask whether they already have a VPS or need to create one. If they need one, recommend **Hetzner Cloud** for its affordability, good performance, and EU/US datacenter options — but let them choose any provider they prefer.

## Step 2 (Remote + Hetzner): Provision a VPS with hcloud CLI

Skip this step if the user chose local installation or already has a VPS.

### 2a. Install hcloud CLI

- **macOS**: `brew install hcloud`
- **Linux**: Download from https://github.com/hetznercloud/cli/releases or use your package manager

### 2b. Create Hetzner account and API token

Tell the user to:

1. Create a Hetzner Cloud account at https://console.hetzner.cloud (if they don't have one)
2. Create a project (e.g. "Fulcrum")
3. Go to **Security → API Tokens** and generate a new token with **read & write** permissions
4. Copy the token (it's only shown once)

### 2c. Configure hcloud

```bash
hcloud context create fulcrum
# Paste the API token when prompted
```

### 2d. Upload SSH key

```bash
hcloud ssh-key create --name fulcrum --public-key-from-file ~/.ssh/id_ed25519.pub
```

If the user doesn't have an SSH key, help them generate one first with `ssh-keygen -t ed25519`.

### 2e. Create the server

```bash
hcloud server create --name fulcrum --type cax21 --image ubuntu-24.04 --ssh-key fulcrum --location fsn1
```

- **cax21** (default): 4 ARM vCPU, 8GB RAM, 80GB disk (~€6.49/mo) — best value; ARM-only locations below
- **cpx31** (alternative): 4 AMD vCPU, 8GB RAM, 80GB disk (~€12/mo) — use if you need a US or Singapore location
- Let the user pick a location:
  - `fsn1` — Germany (Falkenstein) — ARM & x86
  - `nbg1` — Germany (Nuremberg) — ARM & x86
  - `hel1` — Finland (Helsinki) — ARM & x86
  - `ash` — US East (Ashburn, VA) — x86 only
  - `hil` — US West (Hillsboro, OR) — x86 only
  - `sin` — Singapore — x86 only

Note the server's IPv4 address from the output.

### 2f. Configure SSH access (initial)

Add to `~/.ssh/config` on the local machine (we'll update the user in the next step):

```
Host fulcrum-server
    HostName <server-ip>
    User root
```

Verify connectivity:

```bash
ssh fulcrum-server
```

### 2g. Create non-root user

Hetzner provisions servers with root-only access. Create a dedicated `fulcrum` user with sudo privileges so the service doesn't run as root:

```bash
ssh fulcrum-server "useradd -m -s /bin/bash fulcrum \
  && usermod -aG sudo fulcrum \
  && echo 'fulcrum ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/fulcrum \
  && mkdir -p /home/fulcrum/.ssh \
  && cp /root/.ssh/authorized_keys /home/fulcrum/.ssh/ \
  && chown -R fulcrum:fulcrum /home/fulcrum/.ssh \
  && chmod 700 /home/fulcrum/.ssh \
  && chmod 600 /home/fulcrum/.ssh/authorized_keys"
```

Now update `~/.ssh/config` on the local machine to use the new user:

```
Host fulcrum-server
    HostName <server-ip>
    User fulcrum
```

Verify you can connect as the new user:

```bash
ssh fulcrum-server whoami
# Should print: fulcrum
```

## Step 3: Check Prerequisites

On the target machine (local or remote via SSH), verify:

```bash
git --version
curl --version
```

Both should be available. On Ubuntu they are pre-installed; on macOS git comes with Xcode Command Line Tools.

## Step 4: Install Core Dependencies

Run these on the target machine:

### bun (JavaScript runtime)

```bash
curl -fsSL https://bun.sh/install | bash
source ~/.bashrc  # or restart shell
```

### Node.js

- **Ubuntu/Debian**: `curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && sudo apt-get install -y nodejs`
- **macOS**: `brew install node`

### dtach (terminal session persistence — essential for remote)

- **Ubuntu/Debian**: `sudo apt install -y dtach`
- **macOS**: `brew install dtach`

### uv (Python package manager)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### age (encryption — required by fnox)

- **Ubuntu/Debian**: `sudo apt install -y age`
- **macOS**: `brew install age`

### fnox (secrets management — required)

- **macOS**: `brew install jdx/tap/fnox`
- **Linux / fallback**: Download the latest release binary from the GitHub API:

```bash
# Detect platform and install the latest fnox release
FNOX_URL=$(curl -s https://api.github.com/repos/jdx/fnox/releases/latest \
  | grep "browser_download_url" \
  | grep "$(uname -s | tr '[:upper:]' '[:lower:]')-$(uname -m)" \
  | head -1 | cut -d '"' -f 4)
curl -fsSL "$FNOX_URL" | sudo tar xz -C /usr/local/bin fnox
```

### Claude Code (AI coding agent CLI)

Check if already installed:

```bash
claude --version
```

If not installed:

- **macOS / Linux**: `curl -fsSL https://claude.ai/install.sh | bash`
- **macOS (Homebrew)**: `brew install --cask claude-code`

The native install (curl) is recommended as it auto-updates in the background.

If this is a fresh install, the user needs to connect Claude Code to their Claude subscription. Tell them to either SSH into the machine or — once Fulcrum is installed and running — open a terminal session from the Fulcrum UI, then run:

```bash
claude auth login
```

This prints an OAuth URL. They copy it into a browser on their local machine, authenticate with their Claude Pro/Max/Teams subscription, and the token is stored on the remote machine automatically.

## Step 5: Install Fulcrum CLI

```bash
bun install -g @knowsuchagency/fulcrum@latest
```

## Step 6: Start Fulcrum Server

```bash
fulcrum up
```

Verify it's running — the web UI should be accessible at `http://localhost:7777` on the machine where Fulcrum is running.

## Step 7 (Remote only): Configure Persistent SSH Port Forwarding

This makes the remote Fulcrum instance accessible at `http://localhost:7777` on the user's local machine. Port 3000 is also forwarded for web apps and dev servers that agents may spin up on the remote machine.

### Option A: SSH config (simplest)

Update `~/.ssh/config` on the local machine:

```
Host fulcrum-server
    HostName <server-ip>
    User fulcrum
    LocalForward 7777 localhost:7777
    LocalForward 3000 localhost:3000
```

Then connect with `ssh fulcrum-server` — the tunnel is active as long as the SSH session is open.

### Option B: autossh (auto-reconnecting)

Install autossh (`brew install autossh` or `apt install autossh`) and run:

```bash
autossh -M 0 -f -N -o "ServerAliveInterval=30" -o "ServerAliveCountMax=3" -L 7777:localhost:7777 -L 3000:localhost:3000 fulcrum-server
```

### Option C: systemd user service (persistent across reboots)

Create `~/.config/systemd/user/fulcrum-tunnel.service`:

```ini
[Unit]
Description=SSH tunnel to Fulcrum server
After=network-online.target

[Service]
ExecStart=/usr/bin/ssh -N -o ServerAliveInterval=30 -o ServerAliveCountMax=3 -o ExitOnForwardFailure=yes -L 7777:localhost:7777 -L 3000:localhost:3000 fulcrum-server
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

Enable it:

```bash
systemctl --user daemon-reload
systemctl --user enable --now fulcrum-tunnel
```

After configuring the tunnel, verify `http://localhost:7777` is accessible from the local machine's browser.

## Step 8: Configure Claude Desktop (MCP over stdio)

This lets Claude Desktop interact with Fulcrum via the Model Context Protocol.

### 8a. Install fulcrum CLI on the local machine

If Fulcrum is running remotely, the CLI must also be installed **locally** so Claude Desktop can invoke it:

```bash
bun install -g @knowsuchagency/fulcrum@latest
```

### 8b. Add MCP server config

Edit the Claude Desktop config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

Add (or merge into existing config):

```json
{
  "mcpServers": {
    "fulcrum": {
      "command": "fulcrum",
      "args": ["mcp"]
    }
  }
}
```

If Fulcrum is running remotely (accessed via port forwarding), the default `http://localhost:7777` will work as-is since the tunnel forwards the port locally.

### 8c. Restart Claude Desktop

Quit and reopen Claude Desktop for the MCP config to take effect.

## Step 9 (Optional): Install Claude Code Plugin

If the user also uses Claude Code (the CLI), install the Fulcrum plugin:

```bash
claude plugin marketplace add knowsuchagency/fulcrum
claude plugin install fulcrum@fulcrum --scope user
```

## Step 10 (Optional): Google Integration (Gmail + Calendar)

Ask the user if they want to connect Google for Gmail monitoring and Google Calendar sync. If yes:

### 10a. Create a Google Cloud project

1. Go to https://console.cloud.google.com/
2. Create a new project (e.g. "Fulcrum")
3. Select the project

### 10b. Enable APIs

In the project, go to **APIs & Services → Library** and enable:

- **Google Calendar API**
- **Gmail API**

### 10c. Configure OAuth consent screen

Go to **APIs & Services → OAuth consent screen**:

1. User type: **External** (or Internal if you have Google Workspace)
2. App name: "Fulcrum" (or anything you like)
3. User support email: your email
4. Add scopes: `calendar`, `gmail.modify`, `userinfo.email`
5. Add your own email as a **test user** (required while the app is in "Testing" status)
6. Save

### 10d. Create OAuth credentials

Go to **APIs & Services → Credentials**:

1. Click **Create Credentials → OAuth 2.0 Client ID**
2. Application type: **Web application**
3. Name: "Fulcrum"
4. Authorized redirect URI: `http://localhost:7777/api/google/oauth/callback`
5. Click Create
6. Copy the **Client ID** and **Client Secret**

### 10e. Configure in Fulcrum

1. Open Fulcrum at `http://localhost:7777`
2. Go to **Settings → General → Integrations**
3. Paste the Google OAuth Client ID and Client Secret
4. Click Save
5. Click **Add Account** — this opens the Google consent screen
6. Authorize access with your Google account
7. Back in Settings, toggle **Calendar** and/or **Gmail** features as desired

## Step 11: Verification

Confirm everything is working:

- [ ] Fulcrum UI accessible at `http://localhost:7777`
- [ ] MCP tools available in Claude Desktop (try asking Claude to list your tasks)
- [ ] If Google connected: account visible in Settings → Integrations
- [ ] For remote: tunnel persists after disconnecting/reconnecting

Installation complete! Fulcrum is ready to use.
