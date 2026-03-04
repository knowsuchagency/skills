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

Hetzner provisions servers with root-only access. Create a user on the remote machine that matches the local username (`$USER`) so Fulcrum runs as you with your own home directory:

```bash
ssh fulcrum-server "useradd -m -s /bin/bash $USER \
  && usermod -aG sudo $USER \
  && echo '$USER ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/$USER \
  && mkdir -p /home/$USER/.ssh \
  && cp /root/.ssh/authorized_keys /home/$USER/.ssh/ \
  && chown -R $USER:$USER /home/$USER/.ssh \
  && chmod 700 /home/$USER/.ssh \
  && chmod 600 /home/$USER/.ssh/authorized_keys"
```

Now update `~/.ssh/config` on the local machine to use the new user:

```
Host fulcrum-server
    HostName <server-ip>
    User <local-username>
```

(Replace `<local-username>` with the user's actual local username — the value of `$USER`.)

Verify you can connect as the new user:

```bash
ssh fulcrum-server whoami
# Should print your local username
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

### mise (tool version manager)

```bash
curl https://mise.run | sh
```

Follow any shell activation instructions printed by the installer, then restart your shell.

### bun (JavaScript runtime)

```bash
mise use -g bun
```

### Node.js

```bash
mise use -g node
```

### dtach (terminal session persistence — essential for remote)

- **Ubuntu/Debian**: `sudo apt install -y dtach`
- **macOS**: `brew install dtach`

### uv (Python package manager)

```bash
mise use -g uv
```

### age (encryption — required by fnox)

```bash
mise use -g age
```

### fnox (secrets management — required)

```bash
mise use -g fnox
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
    User <local-username>
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

## Step 11 (Optional): Cloudflare Integration (Host Services on Custom Domains)

Ask the user if they want to connect Cloudflare so Fulcrum can deploy and host web apps on their own domain. If yes:

Fulcrum supports two ways to expose deployed apps:

- **DNS-based**: Creates A records pointing to your server IP, with automatic Cloudflare Origin CA certificates for HTTPS
- **Tunnel-based**: Creates a Cloudflare Tunnel via `cloudflared` — no public IP exposure, traffic routes through Cloudflare's edge network (more secure, works behind NAT)

Both methods require a Cloudflare API token. Tunnels additionally require your Account ID.

**Prerequisite**: A domain with its nameservers pointing to Cloudflare (managed in the Cloudflare dashboard).

### 11a. Create a Cloudflare API token

1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Click **Create Token**
3. Choose **Create Custom Token**
4. Add these permissions:
   - **Zone → DNS → Edit** (required — for creating DNS records)
   - **Zone → SSL and Certificates → Edit** (required — for generating Origin CA certificates)
   - **Account → Cloudflare Tunnel → Edit** (optional — only needed if you want tunnel-based exposure)
5. Zone Resources: **Include → All Zones** (or select a specific zone)
6. Click **Continue to summary → Create Token**
7. Copy the token (it's only shown once)

### 11b. Find your Account ID (needed for tunnels)

Your Account ID is visible in:
- The Cloudflare dashboard URL: `https://dash.cloudflare.com/<account_id>/...`
- Or on any domain's **Overview** page in the right sidebar under **API**

### 11c. Configure in Fulcrum

1. Open Fulcrum at `http://localhost:7777`
2. Go to **Settings → General → Integrations**
3. Paste the **Cloudflare API Token**
4. Paste the **Account ID** (if you want tunnel support)
5. Click **Save**

When deploying apps through Fulcrum, you can now choose DNS or Tunnel exposure and assign custom subdomains on your Cloudflare-managed domain.

## Step 12 (Optional): Agent-Browser (Web Automation for Agents)

Ask the user if they want agents to be able to browse and interact with websites (navigating pages, filling forms, clicking buttons, taking screenshots, extracting data). If yes:

### 12a. Install agent-browser

```bash
bun install -g agent-browser
```

### 12b. Download Chromium

- **Linux**: `agent-browser install --with-deps` (also installs required system libraries)
- **macOS**: `agent-browser install`

Once installed, agents can use the `agent-browser` CLI for web automation tasks.

## Step 13 (Optional): Backup Configuration

Ask the user if they want to set up automated backups. Explain the two approaches and recommend both for VPS users:

- **Hetzner Cloud Snapshots** — whole-server point-in-time images, quick disaster recovery (VPS only, same provider)
- **Restic + Backblaze B2** — encrypted, deduplicated off-site backups with file-level restore (works for any setup)

### 13a. Hetzner Cloud Snapshots (VPS only)

Only applicable if the user is on Hetzner (hcloud is already configured from Step 2).

Create a test snapshot:

```bash
hcloud server create-image fulcrum --type snapshot --description "fulcrum-backup-$(date +%Y-%m-%d)"
```

Verify it was created:

```bash
hcloud image list --type snapshot
```

Set up a daily snapshot via a systemd timer on the **VPS**:

Create `/etc/systemd/system/hcloud-snapshot.service`:

```ini
[Unit]
Description=Hetzner Cloud Server Snapshot

[Service]
Type=oneshot
ExecStart=/bin/bash -c 'hcloud server create-image fulcrum --type snapshot --description "fulcrum-backup-$(date +%%Y-%%m-%%d)"'
```

Create `/etc/systemd/system/hcloud-snapshot.timer`:

```ini
[Unit]
Description=Daily Hetzner Cloud Snapshot

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now hcloud-snapshot.timer
```

Set up weekly cleanup to delete snapshots older than 30 days. Create `/usr/local/bin/hcloud-snapshot-cleanup.sh`:

```bash
#!/bin/bash
CUTOFF=$(date -d "30 days ago" +%s 2>/dev/null || date -v-30d +%s)
hcloud image list --type snapshot -o json | jq -r '.[] | "\(.id) \(.description) \(.created)"' | while read -r id desc created; do
  created_ts=$(date -d "$created" +%s 2>/dev/null || date -jf "%Y-%m-%dT%H:%M:%S" "$created" +%s)
  if [ "$created_ts" -lt "$CUTOFF" ]; then
    echo "Deleting snapshot $id ($desc)"
    hcloud image delete "$id"
  fi
done
```

```bash
sudo chmod +x /usr/local/bin/hcloud-snapshot-cleanup.sh
```

Create `/etc/systemd/system/hcloud-snapshot-cleanup.service`:

```ini
[Unit]
Description=Clean up old Hetzner Cloud snapshots

[Service]
Type=oneshot
ExecStart=/usr/local/bin/hcloud-snapshot-cleanup.sh
```

Create `/etc/systemd/system/hcloud-snapshot-cleanup.timer`:

```ini
[Unit]
Description=Weekly Hetzner snapshot cleanup

[Timer]
OnCalendar=Mon *-*-* 04:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now hcloud-snapshot-cleanup.timer
```

Pricing: ~€0.012/GB/month stored. An 80 GB server snapshot costs ~€0.96/month.

### 13b. Restic + Backblaze B2 (off-site backups)

This works for both local and remote installations.

#### Install restic

- **Ubuntu/Debian**: `sudo apt install -y restic`
- **macOS**: `brew install restic`

#### Create a Backblaze B2 bucket

Tell the user to:

1. Create a Backblaze account at https://www.backblaze.com/sign-up (if they don't have one)
2. In the B2 Cloud Storage console, create a **private** bucket (e.g. `fulcrum-backups`)
3. Go to **Account → Application Keys** and create a key scoped to that bucket
4. Copy the **Application Key ID** and **Application Key** (shown only once)

#### Store credentials with fnox

```bash
fnox set B2_ACCOUNT_ID "<app-key-id>" -g
fnox set B2_ACCOUNT_KEY "<app-key-secret>" -g
fnox set RESTIC_PASSWORD "<strong-backup-password>" -g
fnox set RESTIC_REPOSITORY "b2:<bucket-name>:/fulcrum" -g
```

Remind the user to save the `RESTIC_PASSWORD` somewhere safe — without it the backups cannot be decrypted.

#### Initialize the repository

```bash
fnox exec -- restic init
```

#### Run a test backup

Back up the entire disk, excluding virtual filesystems and ephemeral directories:

```bash
fnox exec -- restic backup / \
  --exclude /proc \
  --exclude /sys \
  --exclude /dev \
  --exclude /tmp \
  --exclude /run \
  --exclude /mnt \
  --exclude /media \
  --exclude /swapfile \
  --exclude node_modules
```

Verify the snapshot:

```bash
fnox exec -- restic snapshots
```

#### Set up automated hourly backups

Restic only stores diffs (deduplicated), so hourly backups are lightweight after the initial run.

**Linux (systemd timer):**

Create `/etc/systemd/system/restic-backup.service`:

```ini
[Unit]
Description=Restic backup to Backblaze B2
After=network-online.target

[Service]
Type=oneshot
ExecStart=/bin/bash -c 'fnox exec -- restic backup / --exclude /proc --exclude /sys --exclude /dev --exclude /tmp --exclude /run --exclude /mnt --exclude /media --exclude /swapfile --exclude node_modules'
```

Create `/etc/systemd/system/restic-backup.timer`:

```ini
[Unit]
Description=Hourly Restic backup

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now restic-backup.timer
```

**macOS (launchctl):**

Create `~/Library/LaunchAgents/com.restic.backup.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.restic.backup</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>fnox exec -- restic backup / --exclude /proc --exclude /sys --exclude /dev --exclude /tmp --exclude /run --exclude /mnt --exclude /media --exclude /swapfile --exclude node_modules</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.restic.backup.plist
```

#### Set up weekly pruning

**Linux (systemd timer):**

Create `/etc/systemd/system/restic-prune.service`:

```ini
[Unit]
Description=Restic prune old snapshots
After=network-online.target

[Service]
Type=oneshot
ExecStart=/bin/bash -c 'fnox exec -- restic forget --keep-hourly 24 --keep-daily 30 --keep-weekly 12 --keep-monthly 24 --prune'
```

Create `/etc/systemd/system/restic-prune.timer`:

```ini
[Unit]
Description=Weekly Restic prune

[Timer]
OnCalendar=Sun *-*-* 04:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now restic-prune.timer
```

**macOS (launchctl):**

Create `~/Library/LaunchAgents/com.restic.prune.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.restic.prune</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>fnox exec -- restic forget --keep-hourly 24 --keep-daily 30 --keep-weekly 12 --keep-monthly 24 --prune</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>0</integer>
        <key>Hour</key>
        <integer>4</integer>
    </dict>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.restic.prune.plist
```

## Step 14: Verification

Confirm everything is working:

- [ ] Fulcrum UI accessible at `http://localhost:7777`
- [ ] MCP tools available in Claude Desktop (try asking Claude to list your tasks)
- [ ] If Google connected: account visible in Settings → Integrations
- [ ] If Cloudflare connected: token and account ID saved in Settings → Integrations
- [ ] For remote: tunnel persists after disconnecting/reconnecting
- [ ] If agent-browser installed: `agent-browser --version` returns a version
- [ ] If backups configured: test snapshot or `restic snapshots` shows a successful backup

Installation complete! Fulcrum is ready to use.
