---
name: linctl
description: Comprehensive Linear CLI tool for managing issues, projects, teams, users, and comments. This skill should be used when interacting with Linear's project management platform through command-line operations.
---

# linctl - Linear CLI Tool

## Overview

`linctl` is a comprehensive command-line interface for Linear's API designed for both agents and humans. Use this skill when users need to interact with Linear - a project management and issue tracking platform - including managing issues, projects, teams, users, and comments.

## When to Use This Skill

Use `linctl` when users ask to:
- **Issues**: Create, list, search, view, update, assign, or manage Linear issues
- **Projects**: List, view, or get details about Linear projects
- **Teams**: List teams, view team details, or see team members
- **Users**: List users, get user details, or check current user info
- **Comments**: List or create comments on issues
- **Workflows**: Automate Linear tasks or queries as part of larger workflows

## Key Concepts

### Important Default Behaviors

**Critical**: By default, `issue list` and `project list` only show items created in the **last 6 months**. This is for performance optimization.

- To see older items: Use `--newer-than 1_year_ago` or `--newer-than all_time`
- `issue list` also filters out completed/canceled items by default
- To see all statuses: Add `--include-completed` flag

**Note**: There is no separate `issue search` command. Use `issue list` with filters for searching.

### Output Formats

**Always use `--json` flag for programmatic access** to ensure reliable parsing:
- `--json, -j`: JSON output (best for Claude to parse)
- `--plaintext, -p`: Plain text output (for human readability)
- Default: Table format (interactive use only)

### Authentication

Users must authenticate before using linctl:
```bash
linctl auth              # Interactive authentication
linctl auth status       # Check if authenticated
linctl whoami            # Show current user
```

## Command Categories

### 1. Issue Management

**List Issues**
```bash
# Basic list (last 6 months, no completed)
linctl issue list --json

# With filters
linctl issue list --assignee me --json
linctl issue list --state "In Progress" --team ENG --json
linctl issue list --priority 1 --include-completed --json

# Time-based filtering
linctl issue list --newer-than 1_week_ago --json
linctl issue list --newer-than all_time --json

# Sorting
linctl issue list --sort updated --json  # Most recently updated first
linctl issue list --sort created --json  # Newest first
```

**Get Issue Details** (includes parent/children, branches, cycle, project, attachments, comments)
```bash
linctl issue get LIN-123 --json
```

**Create Issue**
```bash
linctl issue create --title "Bug fix" --team ENG --json
linctl issue create --title "New feature" --team ENG --description "Description here" --assign-me --priority 2 --json
```

**Update Issue**
```bash
linctl issue update LIN-123 --title "New title" --json
linctl issue update LIN-123 --assignee me --json
linctl issue update LIN-123 --assignee john.doe@company.com --json
linctl issue update LIN-123 --assignee unassigned --json  # Remove assignee
linctl issue update LIN-123 --state "In Progress" --json
linctl issue update LIN-123 --priority 1 --json  # 0=None, 1=Urgent, 2=High, 3=Normal, 4=Low
linctl issue update LIN-123 --due-date "2024-12-31" --json
linctl issue update LIN-123 --due-date "" --json  # Remove due date

# Multiple fields at once
linctl issue update LIN-123 --title "Critical" --assignee me --priority 1 --json
```

**Assign Issue**
```bash
linctl issue assign LIN-123 --json  # Assign to yourself
```

### 2. Project Management

**List Projects**
```bash
linctl project list --json
linctl project list --team ENG --json
linctl project list --state started --json
linctl project list --newer-than 1_month_ago --json
linctl project list --newer-than all_time --include-completed --json
```

**Get Project Details** (includes progress, team, members, initiatives, recent issues)
```bash
linctl project get <project-id> --json
```

### 3. Team Management

**List Teams**
```bash
linctl team list --json
```

**Get Team Details**
```bash
linctl team get ENG --json
linctl team show DESIGN --json
```

**List Team Members**
```bash
linctl team members ENG --json
```

### 4. User Management

**List Users**
```bash
linctl user list --json
linctl user list --active --json  # Only active users
```

**Get User Details**
```bash
linctl user get john@example.com --json
linctl user me --json  # Current user
```

### 5. Comments

**List Comments**
```bash
linctl comment list LIN-123 --json
linctl comment list LIN-123 --limit 10 --json
```

**Create Comment**
```bash
linctl comment create LIN-123 --body "Fixed in commit abc123" --json
linctl comment create LIN-123 --body "@john please review" --json
```

### 6. GitHub Integration

**Linking Pull Requests to Issues**

Linear automatically links GitHub PRs to issues when:
1. **Branch name contains issue ID**: `git checkout -b feature/dat-123-description`
2. **PR description contains keywords**: Use "Closes", "Fixes", or "Resolves" followed by issue ID

```markdown
## PR Description Example

Closes DAT-123
Fixes DAT-456

This PR implements the feature described in DAT-123...
```

When Linear's GitHub integration detects these keywords:
- Creates an attachment on the Linear issue linking to the PR
- Shows PR status (draft/open/merged/closed)
- Automatically closes the issue when PR is merged (if using "Closes")

**Supported Keywords:**
- `Closes DAT-XXX` - Will close issue when PR merges
- `Fixes DAT-XXX` - Will close issue when PR merges
- `Resolves DAT-XXX` - Will close issue when PR merges

**View Linked PRs:**
```bash
linctl issue get DAT-123 --json | jq '.attachments.nodes[] | select(.url | contains("github.com")) | {title, url, status: .metadata.status}'
```

## Time-based Filtering Reference

| Expression | Description | Example |
|-----------|-------------|---------|
| *(no flag)* | Last 6 months (default) | `--newer-than 6_months_ago` |
| `1_day_ago` | Last 24 hours | `--newer-than 1_day_ago` |
| `1_week_ago` | Last 7 days | `--newer-than 1_week_ago` |
| `2_weeks_ago` | Last 14 days | `--newer-than 2_weeks_ago` |
| `1_month_ago` | Last month | `--newer-than 1_month_ago` |
| `3_months_ago` | Last quarter | `--newer-than 3_months_ago` |
| `1_year_ago` | Last year | `--newer-than 1_year_ago` |
| `all_time` | No date filter | `--newer-than all_time` |
| ISO date | Since specific date | `--newer-than 2025-07-01` |

## Priority Values

- `0` = None
- `1` = Urgent
- `2` = High
- `3` = Normal (default)
- `4` = Low

## Practical Examples

### Daily Standup
```bash
# My issues from last week
linctl issue list --assignee me --newer-than 1_week_ago --sort updated --json

# Recent comments on my issues
linctl issue list --assignee me --json | jq -r '.[].identifier' | xargs -I {} linctl comment list {} --limit 3 --json
```

### Sprint Planning
```bash
# Current month's issues in Todo state
linctl issue list --newer-than 1_month_ago --state "Todo" --json

# Team's in-progress work
linctl issue list --team ENG --state "In Progress" --json
```

### Project Tracking
```bash
# Projects nearing completion
linctl project list --json | jq '.[] | select(.progress > 0.8) | {name, progress}'

# Get project details with timeline
linctl project get <project-id> --json | jq '{name, startDate, targetDate, progress}'
```

### Issue Triage
```bash
# Urgent unassigned issues
linctl issue list --priority 1 --json | jq '.[] | select(.assignee == null)'

# Recently updated issues for review
linctl issue list --newer-than 2_days_ago --sort updated --json
```

### Team Analysis
```bash
# Find team by member
linctl team list --json | jq -r '.[].key' | xargs -I {} sh -c 'echo "Team: {}"; linctl team members {} --json | jq ".[] | select(.email == \"john@example.com\")"'

# Team workload
linctl team list --json | jq '.[] | {team: .key, name: .name, issues: .issueCount}'
```

## Error Handling

Common issues and solutions:

**"Not authenticated"**
```bash
linctl auth  # Run authentication first
```

**Missing old issues**
- Remember the 6-month default filter
- Use `--newer-than all_time` to see all issues

**Invalid team key**
- Use team key (e.g., "ENG") not display name
- List teams first: `linctl team list --json`

**Invalid priority**
- Use numbers 0-4 only
- 0=None, 1=Urgent, 2=High, 3=Normal, 4=Low

**Performance issues**
- Avoid `all_time` on large workspaces
- Use specific time ranges: `--newer-than 1_year_ago`
- Combine filters to narrow results

## Best Practices

1. **Always use `--json` flag** when calling linctl from Claude for reliable parsing
2. **Check authentication first** with `linctl auth status` if commands fail
3. **Use time filters wisely** - start with recent data (`1_week_ago`, `1_month_ago`) before using `all_time`
4. **Combine filters** to narrow results and improve performance
5. **Parse JSON with jq** for complex data extraction and manipulation
6. **Include `--include-completed`** when historical data is needed
7. **Use `issue list` with filters** for finding issues - there is no separate search command
8. **Get full issue context** with `issue get` before updating to avoid overwriting data
9. **Link PRs to issues** by including "Closes DAT-XXX" in PR descriptions for automatic tracking

## Integration Patterns

### With bash workflows
```bash
#!/bin/bash
# Create issue and assign to self
issue_id=$(linctl issue create --title "Investigate bug" --team ENG --assign-me --json | jq -r '.identifier')
echo "Created issue: $issue_id"

# Add follow-up comment
linctl comment create "$issue_id" --body "Starting investigation" --json
```

### With data analysis
```bash
# Export issues for analysis
linctl issue list --newer-than all_time --json > all_issues.json

# Analyze with jq
cat all_issues.json | jq '[.[] | {
  team: .team,
  priority: .priority,
  state: .state
}] | group_by(.team) | map({team: .[0].team, count: length})'
```

## Additional Resources

- Installation: `brew install dorkitude/linctl/linctl` (macOS/Linux)
- Full documentation: `linctl docs`
- GitHub: https://github.com/dorkitude/linctl
- Linear API: https://developers.linear.app/

## Notes

- linctl is optimized for both human and agent use
- All read operations are safe and don't modify data
- Write operations (create, update, assign) require explicit commands
- Authentication credentials stored in `~/.linctl-auth.json`
- Configuration in `~/.linctl.yaml`
